# region Imports
from __future__ import print_function

import json
import os
import hou

if os.environ["HFS"] != "":
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets
    from hutil.Qt import QtUiTools
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
    "in_memory_db": "False",
    "database_path": defaultdbpath,
    "savewindowsize": "False",
    "windowsize": [1000, 600],
    "debug": "False",
}

SETTINGS_KEYS = [
    'in_memory_db',
    'database_path',
    'savewindowsize',
    'windowsize',
    'debug'
]


def createdefaults():
    settingsdata.beginGroup('Searcher')
    for i in range(len(SETTINGS_KEYS)):
        settingsdata.setValue(
            SETTINGS_KEYS[i], DEFAULT_SETTINGS[SETTINGS_KEYS[i]])
    settingsdata.endGroup()


def savesettings(settingdict):
    settingsdata.beginGroup('Searcher')
    keys = settingdict.keys()
    for i in range(len(keys)):
        settingsdata.setValue(keys[i], settingdict[keys[i]])

    settingsdata.endGroup()


def loadsettings():
    results = {}
    settingsdata.beginGroup('Searcher')
    for i in range(len(SETTINGS_KEYS)):
        results.update(
            {SETTINGS_KEYS[i]: settingsdata.value(SETTINGS_KEYS[i])})

    settingsdata.endGroup()
    return results


def databasepath():
    settings = settingsdata
    settings.beginGroup('Searcher')
    database_path = settings.value('database_path')
    return database_path
