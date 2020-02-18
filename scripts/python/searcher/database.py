import hou
import os
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, SearchField, FTSModel
import time

scriptpath = os.path.dirname(os.path.realpath(__file__))
db = SqliteExtDatabase(scriptpath + "/db/searcher.db")
db.connect()
cur = db.cursor()


class settings(Model):
    id = IntegerField()
    indexvalue = IntegerField()
    defaulthotkey = TextField()
    searchdescription = IntegerField()
    searchprefix = IntegerField()
    searchcurrentcontext = IntegerField()

    class Meta:
        table_name = 'settings'
        database = db


class hcontext(Model):
    id = AutoField()
    context = CharField()
    title = TextField()
    description = TextField()

    class Meta:
        table_name = 'hcontext'
        database = db


class hotkeys(Model):
    hotkey_symbol = TextField()
    label = TextField()
    description = TextField()
    assignments = TextField()
    context = TextField()

    class Meta:
        table_name = 'hotkeys'
        database = db


class hotkeyindex(FTSModel):
    description = SearchField()
    label = SearchField()

    class Meta:
        table_name = 'hotkeyindex'
        database = db
        options = {'tokenize': 'porter',
                   'description': hotkeys.description}


db.create_tables([settings, hcontext, hotkeys])


def getdata():
    rval = []
    contextdata = []
    hotkeydata = []

    def getcontexts(r, context_symbol, root):
        keys = None
        branches = hou.hotkeys.contextsInContext(context_symbol)
        for branch in branches:
            branch_path = "%s/%s" % (r, branch['label'])
            contextdata.append(
                {'context': branch['symbol'], 'title': branch['label'], 'description': branch['help']})
            commands = hou.hotkeys.commandsInContext(branch['symbol'])
            for command in commands:
                keys = hou.hotkeys.assignments(command['symbol'])
                ctx = command['symbol'].rsplit('.', 1)
                hotkeydata.append(
                    {'hotkey_symbol': command['symbol'], 'label': command['label'], 'description': command['help'],
                     'assignments': " ".join(keys), 'context': ctx[0]})
            getcontexts(branch_path, branch['symbol'], root)

    getcontexts("", "", rval)
    return contextdata, hotkeydata


class Databases(object):
    def __init__(self):
        self.a = 1

    # --------------------------------------------------- Retrieve
    def getchangeindex(self):
        try:
            cur.execute("SELECT indexvalue FROM settings")
            result = cur.fetchall()
            return result
        finally:
            db.close()

    def getdefhotkey(self):
        try:
            cur.execute("SELECT defaulthotkey FROM settings")
            result = cur.fetchall()
            return result
        finally:
            db.close()

    def gethcontexts(self):
        try:
            cur.execute("SELECT * FROM hcontext")
            result = cur.fetchall()
            return result
        finally:
            db.close()

    def gethcontextod(self, inputlist):
        try:
            result = []
            query = (hcontext
                     .select()
                     .where(hcontext.context.in_(inputlist)))
            for hctx in query:
                result.append((hctx.title, hctx.description, hctx.context))
            return result
        finally:
            db.close()

    def ctxfilterresults(self, inputTerm):
        try:
            result = []
            query = (hotkeys
                     .select()
                     .where(hotkeys.context.in_(inputTerm))).execute()
            for hctx in query:
                result.append((hctx.label, hctx.description,
                               hctx.assignments, hctx.hotkey_symbol, hctx.context))
            query.close()
            return result
        finally:
            db.close()

    def searchresults(self, inputTerm):
        try:
            cur.execute(
                "SELECT label, description, assignments, hotkey_symbol, context FROM hotkeys WHERE label LIKE '%"
                + str(inputTerm)
                + "%' OR description LIKE '%"
                + str(inputTerm)
                + "%'"
            )
            result = cur.fetchall()
            return result
        finally:
            db.close()

    # --------------------------------------------------- Updates
    def updatechangeindex(self, indexval, new=False):
        try:
            if new is True:
                defaultkey = (u"Ctrl+Alt+Shift+F7")
                settings.insert(indexvalue=indexval,
                                defaulthotkey=defaultkey, searchdescription=0, searchprefix=0, searchcurrentcontext=0, id=1).execute()
            else:
                settings.update(indexvalue=indexval).where(
                    settings.id == 1).execute()
            return
        finally:
            db.close()

    def updatetmphk(self, tmpkey):
        try:
            print tmpkey
            result = settings.update(
                defaulthotkey=tmpkey).where(id == 1).execute()
            print result
            return
        finally:
            db.close()

    def updatecontext(self):
        try:
            ctxdata, hkeydata = getdata()

            # with db.atomic():
            #     for idx in range(0, len(ctxdata), 100):
            #         hcontext.replace_many(ctxdata[idx:idx+100]).execute()
            # with db.atomic():
            #     for idx in range(0, len(hkeydata), 100):
            #         hotkeys.replace_many(hkeydata[idx:idx+100]).execute()

            time1 = time.time()
            with db.atomic():
                for data_dict in ctxdata:
                    hcontext.replace_many(data_dict).execute()
            with db.atomic():
                for idx in hkeydata:
                    hotkeys.replace_many(idx).execute()
            time2 = time.time()
            print('DB update took %0.3f ms' % ((time2 - time1) * 1000.0))
        finally:
            db.close()
