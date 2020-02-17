from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from builtins import range
from past.utils import old_div
import platform
import os

import sys

from hutil import py23
import hutil.Qt
from hutil.Qt import QtWidgets
from hutil.Qt import QtCore
from hutil.Qt import QtGui
from hutil.Qt import QtUiTools

import hou
import hdefereval
from inspect import currentframe
from .widgets import *

import hou
import os
# from .datahandler import datahandler
# from . import gofunctions
from .cwidgets import InputLineEdit

the_scaled_icon_size = hou.ui.scaledSize(16)
the_icon_size = 16

num = 0
# info
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"

scriptpath = os.path.dirname(os.path.realpath(__file__))


class SearcherSettings(QtWidgets.QFrame):
    closeParent = QtCore.Signal(int)
    cancel = QtCore.Signal()

    @QtCore.Slot(str)
    def setText(self, text):
        self.capturekey.setText(text)

    def text(self):
        return self.capturekey.text()

    def __init__(self, handler, tmphotkey, parent=None):
        super(SearcherSettings, self).__init__(parent=parent)

        self._keysToIgnore = [QtCore.Qt.Key.Key_Enter, QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Escape,
                              QtCore.Qt.Key.Key_Tab]
        self.context_dict = {}
        self.command_dict = {}
        self.contexts = None
        self.commands = None
        self.addKeyWidget = None
        self.context_data = None
        self.command_data = None
        self.keys_changed = False
        self.keystring = ""
        self.keyindex = 0
        self.canedit = False
        self.KeySequence = None
        self.hkholder = ""

        self.datahandler = handler
        self.tmphotkey = tmphotkey

        self.setObjectName('searcher-settings')
        # ------------------------------------------------- Build UI
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # Load UI File
        loader = QtUiTools.QUiLoader()
        loader.registerCustomWidget(InputLineEdit.InputLineEdit)
        self.ui = loader.load(scriptpath + '/searchersettings.ui')

        # Get UI Elements
        self.hkinput = self.ui.findChild(QtWidgets.QLineEdit, "hkinput_txt")
        self.addhkeys = self.ui.findChild(
            QtWidgets.QPushButton, "addhotkeys_btn")
        self.updatehkeys = self.ui.findChild(
            QtWidgets.QPushButton, "updatehotkeys_btn")
        self.testcontext = self.ui.findChild(
            QtWidgets.QPushButton, "test_context_btn")
        self.cleardata = self.ui.findChild(
            QtWidgets.QPushButton, "cleardata_btn")
        self.savedata = self.ui.findChild(QtWidgets.QPushButton, "save_btn")
        self.discarddata = self.ui.findChild(
            QtWidgets.QPushButton, "discard_btn")

        # Create Connections
        self.hkinput.setText(self.tmphotkey)
        self.addhkeys.clicked.connect(self.addhotkeys_cb)
        self.updatehkeys.clicked.connect(self.updatehotkeys_cb)
        self.testcontext.clicked.connect(self.testcontext_cb)
        self.cleardata.clicked.connect(self.cleardata_cb)
        self.savedata.clicked.connect(self.save_cb)
        self.discarddata.clicked.connect(self.discard_cb)

        # Layout
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addWidget(self.ui)
        self.setLayout(mainlayout)
        self.hkinput.installEventFilter(self)

    # ------------------------------------------------------------------------------------------------------------------ Callbacks
    def defaulthk_cb(self):
        return

    def addhotkeys_cb(self):
        self.gofunc.callgofunction("ahk", self.gocommandtext.text().strip())

    def updatehotkeys_cb(self):
        self.gofunc.callgofunction("uhk", self.gocommandtext.text().strip())

    def cleardata_cb(self):
        self.gofunc.callgofunction("c", self.gocommandtext.text().strip())

    def save_cb(self):
        if self.hkinput.text() == "":
            buttonindex = hou.ui.displayMessage("Please enter a hotkey")
            self.activateWindow()
            self.hkinput.setFocus()
            self.canedit = True
        else:
            self.tmphotkey = self.hkinput.text()
            self.datahandler.updatetmphotkey(self.tmphotkey)
            self.close()

    def discard_cb(self):
        self.hkinput.setText(self.tmphotkey)
        self.close()

    def testcontext_cb(self):
        self.symbol = self.gocommandtext.text()
        hk = hou.hotkeys.assignments(self.symbol)
        print("Hotkey Value before revert: ", hk)

        hou.hotkeys._restoreBackupTables()
        hou.hotkeys.saveOverrides()
        hk = hou.hotkeys.assignments(self.symbol)
        print("Hotkey Value after restore: ", hk)

        hou.hotkeys.revertToDefaults(self.symbol, True)
        hou.hotkeys.saveOverrides()
        hk = hou.hotkeys.assignments(self.symbol)
        print("Hotkey Value after revert: ", hk)

    def cleardata_cb(self):
        self.gofunc.callgofunction("c", self.gocommandtext.text().strip())

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.hkholder = self.hkinput.text()
            self.hkinput.setText("")
            self.hkinput.setPlaceholderText("Input key sequence")
            self.canedit = True

        if event.type() == QtCore.QEvent.KeyPress:
            self.keyindex += 1
            self.keystring = hou.qt.qtKeyToString(
                event.key(), int(event.modifiers()), event.text())
            # print("Line ", get_linenumber(), "-", self.keystring, "-", event.text())
            if self.canedit:
                if self.keystring not in ["Esc", "Backspace"]:
                    if self.hkinput.hasFocus():
                        self.KeySequence = QtGui.QKeySequence(
                            self.keystring).toString()
                        self.hkinput.setText(self.KeySequence)
                if self.keystring in ["Esc", "Backspace"]:
                    self.hkinput.setText(self.hkholder)

        if event.type() == QtCore.QEvent.KeyRelease:
            self.keyindex -= 1
            if self.keyindex == 0:
                if self.hkinput.text() == "":
                    self.hkinput.setText(self.hkholder)
                if self.hkinput.text() != "":
                    self.canedit = False
        return False


# for debugging:
def get_linenumber():
    cf = currentframe()
    return "{}-{}".format(cf.f_back.f_code.co_name, cf.f_back.f_lineno)


def fromKeyDisplayString(keystr):
    if platform.system() != "Darwin":
        return keystr
    outkeystr = py23.unicodeType(keystr).replace(u"\u2318", "Cmd+", 1)
    outkeystr = outkeystr.replace(u"\u2325", "Alt+", 1)
    outkeystr = outkeystr.replace(u"\u21e7", "Shift+", 1)
    outkeystr = outkeystr.replace(u"\u2303", "Ctrl+", 1)
    return outkeystr
