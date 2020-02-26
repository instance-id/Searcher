# region Imports
from __future__ import print_function
from __future__ import absolute_import
import weakref
from searcher import util

import json
import os
import hou

hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    hver = int(ver[ver.rindex('.')+1:])
    if int(hver) >= 391:
        from hutil.Qt import _QtUiTools
        from hutil.Qt import QtGui
        from hutil.Qt import QtCore
        from hutil.Qt import QtWidgets
    elif int(hver) < 391:
        from hutil.Qt import QtUiTools
        from hutil.Qt import QtGui
        from hutil.Qt import QtCore
        from hutil.Qt import QtWidgets
else:
    os.environ['QT_API'] = 'pyside2'
    from PySide import QtUiTools
    from qtpy import QtGui
    from qtpy import QtCore
    from qtpy import QtWidgets
# endregion

settingsfile = "searcher_settings.ini"
scriptpath = os.path.dirname(os.path.realpath(__file__))
defaultdbpath = os.path.join(scriptpath, 'db', 'searcher.db')
searcher_settings = os.path.join(
    hou.homeHoudiniDirectory(), 'Searcher', settingsfile)
settingsdata = QtCore.QSettings(searcher_settings, QtCore.QSettings.IniFormat)

DEFAULT_SETTINGS = {
    util.SETTINGS_KEYS[0]: "False",         # in_memory_db
    util.SETTINGS_KEYS[1]: defaultdbpath,   # database_path
    util.SETTINGS_KEYS[2]: "False",         # savewindowsize
    util.SETTINGS_KEYS[3]: [1000, 600],     # windowsize
    util.SETTINGS_KEYS[4]: "False",         # debugflag
}


def createdefaults():
    settingsdata.beginGroup('Searcher')
    for i in range(len(util.SETTINGS_KEYS)):
        settingsdata.setValue(
            util.SETTINGS_KEYS[i], DEFAULT_SETTINGS[util.SETTINGS_KEYS[i]])
    settingsdata.endGroup()


def savesettings(settingdict):
    try:
        settingsdata.beginGroup('Searcher')
        keys = settingdict.keys()
        for i in range(len(keys)):
            settingsdata.setValue(keys[i], settingdict[keys[i]])

        settingsdata.endGroup()
    except (AttributeError, TypeError) as e:
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                ("Could not save settings: " + str(e)), severity=hou.severityType.Warning)
        else:
            print("Could not save settings: " + str(e))


def loadsettings():
    results = {}
    try:
        settingsdata.beginGroup('Searcher')
        for i in range(len(util.SETTINGS_KEYS)):
            results.update(
                {util.SETTINGS_KEYS[i]: settingsdata.value(util.SETTINGS_KEYS[i])})

        settingsdata.endGroup()
        return results
    except (AttributeError, TypeError) as e:
        if hou.isUIAvailable():
            hou.ui.setStatusMessage(
                ("Could not load settings: " + str(e)), severity=hou.severityType.Warning)
        else:
            print("Could not load settings: " + str(e))
