from __future__ import print_function
from __future__ import absolute_import
import weakref

import hou
import os

from searcher import util
from searcher import searcher_data
from searcher import ptime as ptime



from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, RowIDField, FTS5Model, SearchField
import time

def get_db():
    return getattr(hou.session, "DATABASE", None)

scriptpath = os.path.dirname(os.path.realpath(__file__))
hou.session.DATABASE = DatabaseProxy()
db = get_db()

# -------------------------------------- DatabaseModels
# SECTION DatabaseModels ------------------------------
class Settings(Model):
    id = IntegerField(unique=True)
    indexvalue = IntegerField()
    defaulthotkey = TextField()
    searchdescription = IntegerField()
    searchprefix = IntegerField()
    searchcurrentcontext = IntegerField()
    lastused = TextField()

    class Meta:
        table_name = 'settings'
        database = db


class HContext(Model):
    id = AutoField()
    context = TextField(unique=True)
    title = TextField()
    description = TextField()

    class Meta:
        table_name = 'hcontext'
        database = db

class HContextIndex(FTS5Model):
    # rowid = RowIDField()
    context = SearchField()
    title = SearchField()
    description = SearchField()

    class Meta:
        database = db
        options = {'prefix': [2, 3], 'tokenize': 'porter'}

class Hotkeys(Model):
    hotkey_symbol = CharField(unique=True)
    label = CharField()
    description = TextField()
    assignments = TextField()
    context = TextField()

    class Meta:
        table_name = 'hotkeys'
        database = db


class HotkeysIndex(FTS5Model):
    # rowid = RowIDField()
    hotkey_symbol = SearchField(unindexed=True)
    label = SearchField()
    description = SearchField()
    assignments = SearchField(unindexed=True)
    context = SearchField(unindexed=True)

    def clear_index(self):
        HotkeysIndex.delete().where(HotkeysIndex.rowid == self.id).execute()

    class Meta:
        # table_name = 'hotkeysindex'
        database = db
        options = {'prefix': [2, 3], 'tokenize': 'porter'}
#!SECTION

# --------------------------------------------------------- DatabaseModels
# SECTION DatabaseModels -------------------------------------------------
# ----------------------------------------------- py_unique
# NOTE py_unique ------------------------------------------
def py_unique(data):
    return list(set(data))

# ------------------------------------------------- getdata
# NOTE getdata --------------------------------------------
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
                {'context': branch['symbol'],
                 'title': branch['label'],
                 'description': branch['help']}
            )
            commands = hou.hotkeys.commandsInContext(branch['symbol'])
            for command in commands:
                keys = hou.hotkeys.assignments(command['symbol'])
                ctx = command['symbol'].rsplit('.', 1)
                hotkeydata.append(
                    {'hotkey_symbol': command['symbol'], 
                    'label': command['label'], 
                    'description': command['help'],
                    'assignments': " ".join(keys), 
                    'context': ctx[0]}
                )
            getcontexts(branch_path, branch['symbol'], root)

    getcontexts("", "", rval)
    return contextdata, hotkeydata
# !SECTION

class Databases(object):
    def __init__(self):
        self.settings = searcher_data.loadsettings()
        self.isdebug = util.bc(self.settings[util.SETTINGS_KEYS[4]])
        inmemory = util.bc(self.settings[util.SETTINGS_KEYS[0]])
        if inmemory:
            val = ':memory:'
        else:
            val = (scriptpath + "/db/searcher.db")

        db.initialize(
            SqliteExtDatabase(
                val,
                pragmas=(
                    ("cache_size", -1024 * 64), 
                    ("journal_mode", "wal"), 
                    ("synchronous", 0)
                )))

        self.cur = db.cursor()
        if inmemory:
            db.create_tables([
                Settings, 
                HContext, 
                HContextIndex, 
                Hotkeys, 
                HotkeysIndex]
            )
            self.initialsetup(self.cur)

        self.a = 1
        self.isdebug = None
        self.contexttime = 0
        self.hotkeystime = 0

    # ----------------------------------------------------------- Retrieve
    # SECTION Retrieve ---------------------------------------------------
    # -------------------------------------- getchangeindex
    # NOTE getchangeindex ---------------------------------    
    def getchangeindex(self):
        try:
            self.cur.execute("SELECT indexvalue FROM settings")
            result = self.cur.fetchall()
            return result
        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(("Could not get Searcher changeindex: " + str(e)), severity=hou.severityType.Error)

    # ------------------------------------------- getlastusedhk
    # NOTE getlastusedhk --------------------------------------
    def getlastusedhk(self, cur):
        try:
            cur.execute("SELECT lastused FROM settings")
            result = cur.fetchall()
            if str(result[0][0]) != "":
                lasthk = str(result[0][0]).split(' ')
                rmresult = hou.hotkeys.removeAssignment(
                    str(lasthk[0]).strip(), str(lasthk[1]).strip())
                if rmresult:
                    hkcheck = hou.hotkeys.assignments(str(lasthk[0]))
                    hou.hotkeys.saveOverrides()
                    if len(hkcheck) is 0:
                        Settings.update(lastused="").where(Settings.id == 1).execute()
                        currentidx = hou.hotkeys.changeIndex()
                        updatechangeindex(int(currentidx))
                    else:
                        hou.hotkeys.clearAssignments(str(lasthk[0]))
                        hou.hotkeys.saveOverrides()
                        hkcheck = hou.hotkeys.assignments(str(lasthk[0]))
                        if len(hkcheck) is 0:
                            Settings.update(lastused="").where(Settings.id == 1).execute()
                            currentidx = hou.hotkeys.changeIndex()
                            updatechangeindex(int(currentidx))
                        else:
                            if hou.isUIAvailable():
                                hou.ui.setStatusMessage(("Could not clear last assigned temp hotkey on last attempt:"), severity=hou.severityType.Warning)
                            else:
                                print("Could not clear last assigned temp hotkey on last attempt:")
                else:
                    if hou.isUIAvailable():
                        hou.ui.setStatusMessage(("Could not clear last assigned temp hotkey:"), severity=hou.severityType.Warning)
                    else:
                        print("Could not clear last assigned temp hotkey:")

        except(AttributeError, TypeError) as e:
            if hou.isUIAvailable():
                hou.ui.setStatusMessage(("Could not query last assigned temp hotkey:" + str(e)), severity=hou.severityType.Warning)
            else:
                print("Could not query last assigned temp hotkey: " + str(e))

    def getdefhotkey(self):
        try:
            self.cur.execute("SELECT defaulthotkey FROM settings")
            result = self.cur.fetchall()
            return result
        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(("Could not get Searcher default hotkey: " + str(e)), severity=hou.severityType.Error)

    def gethcontexts(self):
        try:
            self.cur.execute("SELECT * FROM hcontext")
            result = self.cur.fetchall()
            return result
        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(("Could not get Searcher hcontext: " + str(e)), severity=hou.severityType.Error)

    def gethcontextod(self, inputlist):
        try:
            time1 = ptime.time()
            result = []
            # query = (HContextIndex
            #          .select(HContextIndex)
            #          .where(HContextIndex.match(inputlist)))
            query = (HContext
                     .select()
                     .where(HContext.context.in_(inputlist))).execute()
            for hctx in query:
                result.append((hctx.title, hctx.description, hctx.context))
            uniqueresult = py_unique(result)
            time2 = ptime.time()
            self.contexttime = ((time2 - time1) * 1000.0)
            return uniqueresult, self.contexttime
        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(("Could not update Searcher context database: " + str(e)), severity=hou.severityType.Error)

    # def gethcontextod(self, inputlist):
    #     try:
    #         result = []
    #         query = (HContext
    #                  .select()
    #                  .where(HContext.context.in_(inputlist))).execute()
    #         for hctx in query:
    #             result.append((hctx.title, hctx.description, hctx.context))
    #         uniqueresult = py_unique(result)
    #         return uniqueresult
    #     except(AttributeError, TypeError) as e:
    #         hou.ui.setStatusMessage(("Could not update Searcher context database: " + str(e)), severity=hou.severityType.Error)

    def ctxfilterresults(self, inputTerm):
        try:
            result = []
            query = (Hotkeys
                     .select()
                     .where(Hotkeys.context.in_(inputTerm))).execute()
            for hctx in query:
                result.append((hctx.label, hctx.description, hctx.assignments, hctx.hotkey_symbol, hctx.context))
            uniqueresult = py_unique(result)
            return uniqueresult
        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(("Could not get Searcher context results: " + str(e)), severity=hou.severityType.Error)
    
    
    def searchresults(self, inputTerm, debug, limit=0):
        self.isdebug = debug
        try:
            time1 = ptime.time()
            self.cur.execute(
                "SELECT label, description, assignments, hotkey_symbol, context FROM hotkeysindex WHERE hotkeysindex MATCH '"
                + str(inputTerm)
                + "' ORDER BY rank" 
                + " LIMIT " 
                + str(limit)
            )
            result = self.cur.fetchall()
            uniqueresult = py_unique(result)
            
            time2 = ptime.time()
            self.hotkeystime = ((time2 - time1) * 1000.0)

            return uniqueresult, self.hotkeystime
        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(("Could not get Searcher results: " + str(e)), severity=hou.severityType.Error)

    # ---------------------------------------------------------- Updates
    def updatechangeindex(self, indexval, new=False):
        try:
            if new is True:
                defaultkey = ""
                for i in range(len(util.HOTKEYLIST)):
                    result = hou.hotkeys.findConflicts("h", util.HOTKEYLIST[i])
                    if not result:
                        defaultkey = util.HOTKEYLIST[i]

                Settings.insert(indexvalue=indexval,
                                defaulthotkey=defaultkey, searchdescription=0, searchprefix=0, searchcurrentcontext=0, lastused="", id=1).execute()
            else:
                Settings.update(indexvalue=indexval).where(
                    Settings.id == 1).execute()
        except(AttributeError, TypeError) as e:
            if hou.isUIAvailable():
                hou.ui.setStatusMessage(
                    ("Could not update Searcher context database: " + str(e)),
                    severity=hou.severityType.Warning
                )
            else:
                print("Could not update Searcher context database: " + str(e))

    def updatetmphk(self, tmpkey):
        try:
            _ = Settings.update(
                defaulthotkey=tmpkey).where(id == 1).execute()
            return
        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(("Could not update Searcher temp hotkey: " + str(e)), severity=hou.severityType.Error)

    def updatelastkey(self, lastkey):
        try:
            _ = Settings.update(lastused=lastkey).where(id == 1).execute()
            return
        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(("Could not update Searcher temp hotkey: " + str(e)), severity=hou.severityType.Error)

    def updatecontext(self, debug):
        self.isdebug = debug
        try:
            time1 = ptime.time()
            self.cleardatabase()
            ctxdata, hkeydata = getdata()
            with db.atomic():
                for data_dict in ctxdata:
                    HContext.replace_many(data_dict).execute()
            with db.atomic():
                for idx in hkeydata:
                    Hotkeys.replace_many(idx).execute()
                    HotkeysIndex.replace_many(idx).execute()
            time2 = ptime.time()
            if self.isdebug and self.isdebug.level in {"TIMER", "ALL"}:
                res = ((time2 - time1) * 1000.0)
                if hou.isUIAvailable():
                    hou.ui.setStatusMessage(
                        ('DB update took %0.4f ms' % res), severity=hou.severityType.Message)
                else:
                    print('DB update took %0.4f ms' % res)  # TODO Remove this timer
                return res

        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(("Could not update Searcher context database: " + str(e)), severity=hou.severityType.Error)

    def cleardatabase(self):
        try:
            delhk = "DELETE FROM hotkeys"
            delctx = "DELETE FROM hcontext"
            delhkindex = "DELETE FROM hotkeysindex"
            delhcindex = "DELETE FROM hcontextindex"
            self.cur.execute(delhk)
            self.cur.execute(delctx)
            result = self.cur.fetchall()

            return result
        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(("Could not update Searcher temp hotkey: " + str(e)),severity=hou.severityType.Error)

    def initialsetup(self, cur):
        currentidx = hou.hotkeys.changeIndex()
        chindex = self.getchangeindex()

        if len(chindex) == 0:
            chindex = int(currentidx)
            self.updatechangeindex(chindex, True)
            self.updatecontext(self.isdebug)
            if hou.isUIAvailable():
                hou.ui.setStatusMessage(
                    "Searcher database created", severity=hou.severityType.Message)
            else:
                print("Searcher database created")
        else:
            chindex = int(chindex[0][0])

        if int(currentidx) != chindex:
            self.getlastusedhk(cur)
            self.updatecontext()
            self.updatechangeindex(int(currentidx))

            if hou.isUIAvailable():
                hou.ui.setStatusMessage(
                    "Searcher database created and populated", severity=hou.severityType.Message)

   