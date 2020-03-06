from __future__ import print_function
from searcher import searcher_data
from searcher import util

from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, SearchField, FTSModel
# from playhouse.apsw_ext import APSWDatabase
import inspect
import threading
import time
import hou
import hdefereval as hd
import os
import sys

# info
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"


current_file_path = os.path.abspath(
    inspect.getsourcefile(lambda: 0)
)

scriptpath = os.path.dirname(current_file_path)
dbpath = os.path.join(scriptpath, "python/searcher/db/searcher.db")

# db = SqliteExtDatabase(':memory:')
db = SqliteExtDatabase(dbpath)
dbc = None
settingdata = {}
isloading = True
tempkey = ""


class settings(Model):
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


class hcontext(Model):
    id = AutoField()
    context = CharField(unique=True)
    title = TextField()
    description = TextField()

    class Meta:
        table_name = 'hcontext'
        database = db


class hotkeys(Model):
    hotkey_symbol = CharField(unique=True)
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


def create_tables():
    with db:
        db.create_tables([settings, hcontext, hotkeys])


def worker():
    hd.executeInMainThreadWithResult(updatecontext)


def py_unique(data):
    return list(set(data))


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


# region --------------------------------------------------- Initial Setup


def initialsetup(cur):
    currentidx = hou.hotkeys.changeIndex()
    chindex = getchangeindex(cur)

    if len(chindex) == 0:
        chindex = int(currentidx)
        updatechangeindex(chindex, True)
        updatedataasync()
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                "Searcher database created", severity=hou.severityType.Message)
        else:
            print("Searcher database created")
    else:
        chindex = int(chindex[0][0])

    if int(currentidx) != chindex:
        getlastusedhk(cur)
        updatedataasync()
        updatechangeindex(int(currentidx))
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                "Searcher database created and populated", severity=hou.severityType.Message)


def dbupdate(cur):
    currentidx = hou.hotkeys.changeIndex()
    chindex = getchangeindex(cur)

    if int(currentidx) != chindex:
        getlastusedhk(cur)
        updatedataasync()
        updatechangeindex(int(currentidx))
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                "Searcher database updated", severity=hou.severityType.Message)


def updatedataasync():
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()

# endregionc

# region --------------------------------------------------- Retrieve


def getchangeindex(cur):
    try:
        cur.execute("SELECT indexvalue FROM settings")
        result = cur.fetchall()
        return result
    except(AttributeError, TypeError) as e:
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                ("Could not get Searcher changeindex: " + str(e)), severity=hou.severityType.Warning)
        else:
            print("Could not get Searcher changeindex: " + str(e))


def getlastusedhk(cur):
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
                    settings.update(lastused="").where(
                        settings.id == 1).execute()
                    currentidx = hou.hotkeys.changeIndex()
                    updatechangeindex(int(currentidx))
                else:
                    hou.hotkeys.clearAssignments(str(lasthk[0]))
                    hou.hotkeys.saveOverrides()
                    hkcheck = hou.hotkeys.assignments(str(lasthk[0]))
                    if len(hkcheck) is 0:
                        settings.update(lastused="").where(
                            settings.id == 1).execute()
                        currentidx = hou.hotkeys.changeIndex()
                        updatechangeindex(int(currentidx))
                    else:
                        if hou.isUIAvailable():
                            hou.ui.setStatusMessage(
                                ("Could not clear last assigned temp hotkey on last attempt:"), severity=hou.severityType.Warning)
                        else:
                            print(
                                "Could not clear last assigned temp hotkey on last attempt:")
            else:
                if hou.isUIAvailable():
                    hou.ui.setStatusMessage(
                        ("Could not clear last assigned temp hotkey:"), severity=hou.severityType.Warning)
                else:
                    print("Could not clear last assigned temp hotkey:")

    except(AttributeError, TypeError) as e:
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                ("Could not query last assigned temp hotkey:" + str(e)), severity=hou.severityType.Warning)
        else:
            print("Could not query last assigned temp hotkey: " + str(e))

# region --------------------------------------------------- Updates


def updatechangeindex(indexval, new=False):
    try:
        if new is True:
            defaultkey = ""
            for i in range(len(util.HOTKEYLIST)):
                result = hou.hotkeys.findConflicts("h", util.HOTKEYLIST[i])
                if not result:
                    defaultkey = util.HOTKEYLIST[i]

            settings.insert(indexvalue=indexval,
                            defaulthotkey=defaultkey, searchdescription=0, searchprefix=0, searchcurrentcontext=0, lastused="", id=1).execute()
        else:
            settings.update(indexvalue=indexval).where(
                settings.id == 1).execute()
    except(AttributeError, TypeError) as e:
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                ("Could not update Searcher context database: " + str(e)),
                severity=hou.severityType.Warning
            )
        else:
            print("Could not update Searcher context database: " + str(e))


def updatecontext(debug=False):
    try:
        time1 = time.time()
        cleardatabase()
        ctxdata, hkeydata = getdata()
        with db.atomic():
            for data_dict in ctxdata:
                hcontext.replace_many(data_dict).execute()
        with db.atomic():
            for idx in hkeydata:
                hotkeys.replace_many(idx).execute()
        time2 = time.time()
        if debug:
            if hou.isUIAvailable():
                hou.ui.setStatusMessage(
                    ('DB update took %0.3f ms' %
                        ((time2 - time1) * 1000.0)), severity=hou.severityType.Message)
            else:
                print('DB update took %0.3f ms' %
                      ((time2 - time1) * 1000.0))  # TODO Remove this timer
    except(AttributeError, TypeError) as e:
        hou.ui.setStatusMessage(
            ("Could not update Searcher context database: " + str(e)), severity=hou.severityType.Warning)
# endregion


def cleardatabase():
    try:
        delhk = "DELETE FROM hotkeys"
        delctx = "DELETE FROM hcontext"
        db.cursor().execute(delhk)
        db.cursor().execute(delctx)
        result = db.cursor().fetchall()

        return result
    except(AttributeError, TypeError) as e:
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                ("Could not clear db for refresh: " + str(e)), severity=hou.severityType.Warning)
        else:
            print("Could not clear db for refresh: " + str(e))


def deferaction(action, val):
    hd.executeDeferred(action, val)
    # hd.execute_deferred_after_waiting(action, 25)


def checklasthk(cur):
    getlastusedhk(cur)


def main():
    if os.path.isfile(searcher_data.searcher_settings):
        settingdata = searcher_data.loadsettings()
    else:
        searcher_data.createdefaults()
        settingdata = searcher_data.loadsettings()

    if not os.path.isfile(dbpath):
        create_tables()
        cur = db.cursor()
        deferaction(initialsetup, cur)
    else:
        cur = db.cursor()
        deferaction(dbupdate, cur)


if __name__ == '__main__':
    main()