from __future__ import print_function
import weakref

from . import searcher_settings
from . import gofunctions
from . import database
from . import data
from . import cwidgets
from datahandler import datahandler

from pyautogui import press, typewrite, hotkey
# noinspection PyUnresolvedReferences
import hou
from husdui.common import error_print, debug_print
import toolutils
import drivertoolutils
import platform
import objecttoolutils
import os
import sys
import hdefereval as hd
if os.environ["HFS"] != "":
    # noinspection PyUnresolvedReferences
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets
    from hutil.Qt import QtUiTools
else:
    os.environ['QT_API'] = 'pyside2'
    from PySide import QtUiTools
    # noinspection PyUnresolvedReferences
    from qtpy import QtGui
    # noinspection PyUnresolvedReferences
    from qtpy import QtCore
    # noinspection PyUnresolvedReferences
    from qtpy import QtWidgets

# info
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"

reload(datahandler)
reload(database)
reload(gofunctions)
reload(searcher_settings)
reload(data)
reload(cwidgets)

mousePos = None
cur_screen = QtWidgets.QDesktopWidget().screenNumber(
    QtWidgets.QDesktopWidget().cursor().pos())
screensize = QtWidgets.QDesktopWidget().screenGeometry(cur_screen)
centerPoint = QtWidgets.QDesktopWidget().availableGeometry(cur_screen).center()

sys.path.append(os.path.join(os.path.dirname(__file__)))
script_path = os.path.dirname(os.path.realpath(__file__))
# gofuncs = gofunctions.GoFunctions()
name = "Searcher"

parent_widget = hou.qt.mainWindow()


def keyconversion(key):
    for i in range(len(key)):
        if key[i] in data.keyconversions:
            key[i] = data.keyconversions[key[i]]
    return key


class Searcher(QtWidgets.QWidget):
    """instance.id Searcher for Houdini"""
    hotkeyInvoked = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(Searcher, self).__init__(parent)
        self.installEventFilter(self)
        self.window = QtWidgets.QMainWindow()
        self.handler, self.tmpkey = self.initialsetup()
        self.ui = searcher_settings.SearcherSettings(self.handler, self.tmpkey)

        self.hktest = True

        self.keys_changed = False
        self.tmpsymbol = None
        self.searching = True

        hou.hotkeys._createBackupTables()

        self.main_widget = QtWidgets.QWidget(self)

        # Load UI File
        loader = QtUiTools.QUiLoader()
        mainui = loader.load(script_path + "/searcher.ui")

        # Get UI Elements
        self.opensettings = mainui.findChild(
            QtWidgets.QPushButton, "opensettings_btn")
        self.searchresultstree = mainui.findChild(
            QtWidgets.QTreeWidget, "searchresults_tree")

        self.searchbox = mainui.findChild(
            QtWidgets.QLineEdit, "searchbox_txt")
        self.searchbox.setPlaceholderText("Search..")
        self.searchbox.setFocusPolicy(QtCore.Qt.StrongFocus)

        # Create Connections
        self.opensettings.clicked.connect(self.opensettings_cb)
        self.searchbox.textChanged.connect(self.textchange_cb)
        self.searchresultstree.itemDoubleClicked.connect(self.searchclick_cb)
        self.searchresultstree.itemActivated.connect(self.searchclick_cb)

        # Layout
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.setAlignment(QtCore.Qt.AlignTop)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        mainlayout.setGeometry(QtCore.QRect(0, 0, 1400, 1200))
        mainlayout.addWidget(mainui)
        self.setLayout(mainlayout)

        self.setupContext()
        self.activateWindow()
        self.searchbox.setFocus()
        self.searchbox.grabKeyboard()

    # ------------------------------------------------------------------------------------------------------------------ Callbacks
    def _emitHotkey(self, symbol):
        print (symbol)
        self.hotkeyInvoked.emit(symbol)

    def opensettings_cb(self):
        self.open_settings()

    def textchange_cb(self, text):
        if len(text) > 1:
            txt = self.handler.searchtext(text)
            self.searchtablepopulate(txt)
        else:
            self.searchresultstree.clear()

    def searchclick_cb(self, item, column):
        hk = item.text(2)
        self.tmpsymbol = item.text(3)

        if self.hktest == True:
            if hk == "":
                self.chindex = hou.hotkeys.changeIndex()
                result = self.createtemphotkey(self.tmpsymbol)
                if result is True:
                    self.chindex = hou.hotkeys.changeIndex()
                    hk = hou.hotkeys.assignments(self.tmpsymbol)
                    self.processmenukey(item.text(0), self.tmpsymbol, hk)
            else:
                hk = hou.hotkeys.assignments(self.tmpsymbol)
                self.processmenukey(item.text(0), self.tmpsymbol, hk)
                self.tmpsymbol = None
            return

        if hk == "":
            self.chindex = hou.hotkeys.changeIndex()
            result = self.createtemphotkey(self.tmpsymbol)
            if result is True:
                self.chindex = hou.hotkeys.changeIndex()
                hk = hou.hotkeys.assignments(self.tmpsymbol)
                self.processkey(hk)
        else:
            hk = hou.hotkeys.assignments(self.tmpsymbol)
            self.processkey(hk)
            self.tmpsymbol = None

    # ------------------------------------------------------------------------------------------------------------------ Actions
    # ---------------------------------------------- Navigation
    def open_settings(self):
        self.ui.show()

    # ---------------------------------------------- UI
    def setupContext(self):
        cols = 4
        self.searchresultstree.setColumnCount(cols)
        self.searchresultstree.setColumnWidth(0, 250)
        self.searchresultstree.setColumnWidth(1, 450)
        self.searchresultstree.setColumnWidth(2, 100)
        self.searchresultstree.setColumnWidth(3, 150)
        self.searchresultstree.setHeaderLabels(
            ["Label", "Description", "Assignments", "Symbol"])

    # ---------------------------------------------- Search Functionality
    def searchtablepopulate(self, data):
        rows = len(data)

        if rows > 0:
            self.searchresultstree.clear()
            hcontext_tli = {}
            hotkeys = []
            context_list = []

            for i in range(rows):
                if data[i][4] not in context_list:
                    context_list.append(data[i][4])

            result = self.handler.gethcontextod(context_list)

            for hc in range(len(result)):
                hcontext_tli[result[hc][2]] = (QtWidgets.QTreeWidgetItem(
                    self.searchresultstree, [result[hc][0], result[hc][1]]))
                self.searchresultstree.expandItem(hcontext_tli[result[hc][2]])

            base_keys = hcontext_tli.keys()
            for i in range(rows):
                for j in range(len(base_keys)):
                    if base_keys[j] in data[i][4]:
                        hotkeys.append(QtWidgets.QTreeWidgetItem(
                            hcontext_tli[base_keys[j]], [
                                data[i][0], data[i][1], data[i][2], data[i][3]]
                        ))

    # ---------------------------------------------- Initial Setup
    def initialsetup(self):
        self.handler = datahandler.DataHandler()
        currentidx = hou.hotkeys.changeIndex()

        # print("Current Index:", currentidx)

        chindex = self.handler.getchangeindex()
        # print("Current db Index:", chindex)
        # print("DB Index len=", len(chindex))
        if len(chindex) == 0:
            chindex = int(currentidx)
            self.handler.updatechangeindex(chindex, True)
            self.handler.updatedata()
        else:
            chindex = int(chindex[0][0])

        if int(currentidx) != chindex:
            self.handler.updatedata()
            self.handler.updatechangeindex(int(currentidx))

        tmpkey = self.handler.getdefaulthotkey()
        self.tmpkey = tmpkey[0][0]
        return self.handler, self.tmpkey

    # ---------------------------------------------- Hotkey Processing
    def _hotkeyMenuAction(self, symbol, owner):
        owner._emitHotkey(symbol)

    def processmenukey(self, label, symbol, key):
        hk = key
        if self.tmpsymbol is None:
            key = key.split(' ')
            key = key[0].split('+')
        else:
            key = key[0].split('+')

        key = keyconversion(key)
        modifiers = data.MODIFIERS
        mods = []
        ikey = None
        skey = None
        for i in range(len(key)):
            if str(key[i]) in modifiers:
                mods.append(data.MODIFIERS[str(key[i])])
            else:
                ikey = data.KEY_DICT[str(key[i])]
                skey = key[i]

        keypress = QtGui.QKeyEvent(
            QtGui.QKeyEvent.KeyPress, ikey, QtCore.Qt.NoModifier, skey)

        QtGui.QGuiApplication.sendEvent(self.parent(), keypress)

        # if len(key) == 2:
        #     print("Initiating len(2) Hotkey")
        #     keypress = QtGui.QKeyEvent(
        #         QtGui.QKeyEvent.KeyPress, ikey, mods[0], skey)
        # if len(key) == 3:
        #     hotkey(str(key[0]), str(key[1]), str(key[2]))
        # if len(key) == 4:
        #     keypress = QtGui.QShortcutEvent(keysequence, True)
        #     # QtGui.QKeyEvent.KeyPress, ikey, (mods[0] & mods[1] & mods[2]), str(skey))
        # if len(key) == 5:
        #     hotkey(str(key[0]), str(key[1]), str(
        #         key[2]), str(key[3]), str(key[4]))
        # else:

        # keypress = QtGui.QKeyEvent(
        #     QtGui.QKeyEvent.KeyPress, QtGui.QKeySequence(key), QtCore.Qt.NoModifier, str(key))

        # QtGui.QGuiApplication.sendEvent(perfMonWidget, keypress)
        # self.hotkeyInvoked.emit(self.tmpsymbol)

    def processkey(self, key):
        if self.tmpsymbol is None:
            key = key.split(' ')
            key = key[0].split('+')
        else:
            key = key[0].split('+')

        key = keyconversion(key)
        self.searchbox.releaseKeyboard()
        self.searchbox.clearFocus()

        parent_widget.activateWindow()
        parent_widget.setFocus()
        parent_widget.focusWidget()

        if len(key) == 2:
            hotkey(str(key[0]), str(key[1]))
        if len(key) == 3:
            hotkey(str(key[0]), str(key[1]), str(key[2]))
        if len(key) == 4:
            hotkey(str(key[0]), str(key[1]), str(key[2]), str(key[3]))
        if len(key) == 5:
            hotkey(str(key[0]), str(key[1]), str(
                key[2]), str(key[3]), str(key[4]))
        else:
            hotkey(str(key))

    def setKeysChanged(self, changed):
        if self.keys_changed and not changed:
            if not hou.hotkeys.saveOverrides():
                print("ERROR: Couldn't save hotkey override file.")
        self.keys_changed = changed
        self.chindex = hou.hotkeys.changeIndex()
        self.handler.updatechangeindex(self.chindex)

    def createtemphotkey(self, symbol):
        hou.hotkeys._createBackupTables()
        result = hou.hotkeys.addAssignment(symbol, self.tmpkey)
        self.keys_changed = True
        self.setKeysChanged(False)
        return result

    def removetemphotkey(self, symbol, tmpkey):
        hou.hotkeys._restoreBackupTables()
        hou.hotkeys.revertToDefaults(symbol, True)
        self.keys_changed = True
        self.setKeysChanged(False)

    # ------------------------------------------------------------------------------------------------------------------ Events
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            self.searchbox.grabKeyboard()
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            if self.ui.isVisible():
                self.searchbox.releaseKeyboard()
            else:
                self.close()
        elif event.type() == QtCore.QEvent.FocusIn:
            pass
        elif event.type() == QtCore.QEvent.FocusOut:
            pass
        return False

    def closeEvent(self, event):
        if self.tmpsymbol is not None:
            hd.execute_deferred_after_waiting(
                self.removetemphotkey, 5, self.tmpsymbol, self.tmpkey)
        self.searchbox.releaseKeyboard()
        self.parent().setFocus()
        self.setParent(None)
        self.deleteLater()

    def keyPressEvent(self, event):

        if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            pass
        if event.key() == QtCore.Qt.Key_Tab:
            self.searching = False
            self.searchbox.releaseKeyboard()
            self.searchresultstree.setFocus()
            self.searchresultstree.setCurrentItem(
                self.searchresultstree.topLevelItem(0).child(0))

        if event.key() == QtCore.Qt.Key_Escape:
            if self.ui.isVisible():
                pass
            else:
                self.close()

    # ------------------------------------------------------------------------------------------------------------------ Event Callbacks
    def kill_pane_tab(self):
        self.searchbox.releaseKeyboard()
        self.parent().setFocus()
        self.setParent(None)
        self.close()


def center():
    return parent_widget.mapToGlobal(
        QtCore.QPoint(
            parent_widget.rect().center().x(),
            parent_widget.rect().center().y()
        )
    )


def hideEvent(self, event):
    self.releaseKeyboard()
    self.parent().setFocus()
    self.setParent(None)


def closeEvent(self, event):
    self.releaseKeyboard()
    self.parent().setFocus()
    self.setParent(None)


def CreateSearcherPanel(kwargs, searcher_window=None):
    kwargs = kwargs
    try:
        searcher_window.close()
        searcher_window.deleteLater()

    except:
        pass

    searcher_window = Searcher()
    searcher_window.setWindowFlags(
        QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
    searcher_window.resize(1000, 600)
    searcher_window.setParent(parent_widget, QtCore.Qt.Window)

    pos = center()
    searcher_window.setGeometry(pos.x() - (searcher_window.width() / 2), pos.y() - (
        searcher_window.height() / 2), searcher_window.width(), searcher_window.height())

    searcher_window.searchbox.setFocus()
    searcher_window.show()
