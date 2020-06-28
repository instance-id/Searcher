# region Imports
from __future__ import print_function
from __future__ import absolute_import

from searcher import util
from searcher import language_en as la

import os
import hou

hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    # hver = int(ver[ver.rindex('.') + 1:])
    from hutil.Qt import QtCore

# ------------------------------------------------------ Setting Paths
# SECTION Setting Paths ----------------------------------------------
scriptpath = os.path.dirname(os.path.realpath(__file__))
app_name = "Searcher"
settingsfile = "searcher_settings.ini"
dbfile = "searcher.db"
searcher_path = os.path.join(
    hou.homeHoudiniDirectory(), app_name
)
searcher_settings = os.path.join(
    searcher_path, settingsfile
)
defaultdbpath = os.path.join(
    searcher_path, dbfile
)
settingsdata = QtCore.QSettings(searcher_settings, QtCore.QSettings.IniFormat)


# !SECTION Setting Paths

# -------------------------------------------------- Setting Functions
# SECTION Setting Functions ------------------------------------------
# -------------------------------------- createdefaults
# NOTE createdefaults ---------------------------------
def createdefaults(platform):
    def_set = util.DEFAULT_SETTINGS
    def_set[util.SETTINGS_KEYS[1]] = str(defaultdbpath)
    if platform == "unix":
        def_set[util.SETTINGS_KEYS[8]] = True
    settingsdata.beginGroup('Searcher')
    try:
        for i in range(len(util.SETTINGS_KEYS)):
            settingsdata.setValue(util.SETTINGS_KEYS[i], def_set[util.SETTINGS_KEYS[i]])
    except (AttributeError, TypeError) as e:
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                (la.SETTINGSMESSAGES['createdefaults'] + str(e)), severity=hou.severityType.Warning)
        else:
            print(la.SETTINGSMESSAGES['createdefaults'] + str(e))
    settingsdata.endGroup()
    settingsdata.setIniCodec('UTF-8')
    settingsdata.sync()


# ---------------------------------------- savesettings
# NOTE savesettings -----------------------------------
def savesettings(settingdict):
    try:
        settingsdata.beginGroup('Searcher')
        keys = settingdict.keys()
        for i in range(len(keys)):
            settingsdata.setValue(keys[i], settingdict[keys[i]])
        settingsdata.endGroup()
        settingsdata.sync()
    except (AttributeError, TypeError) as e:
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                (la.SETTINGSMESSAGES['savesettings'] + str(e)), severity=hou.severityType.Warning)
        else:
            print(la.SETTINGSMESSAGES['savesettings'] + str(e))


# ---------------------------------------- loadsettings
# NOTE loadsettings -----------------------------------
def loadsettings():
    results = {}
    try:
        settingsdata.beginGroup('Searcher')
        for i in range(len(util.SETTINGS_KEYS)):
            if util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] in {"bool", "flag"}:
                results.update({util.SETTINGS_KEYS[i]: util.bc(settingsdata.value(util.SETTINGS_KEYS[i]))})
            else:
                results.update({util.SETTINGS_KEYS[i]: settingsdata.value(util.SETTINGS_KEYS[i])})

        settingsdata.endGroup()
        return results
    except (AttributeError, TypeError) as e:
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                (la.SETTINGSMESSAGES['loadsettings'] + str(e)), severity=hou.severityType.Warning)
        else:
            print(la.SETTINGSMESSAGES['loadsettings'] + str(e))
# !SECTION Setting Functions
