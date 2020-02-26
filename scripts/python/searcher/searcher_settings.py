from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import weakref

from builtins import range
from past.utils import old_div
import platform
import os

import sys
import hou
import hdefereval
from hutil import py23
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

from inspect import currentframe
from .widgets import *
from searcher import util
from searcher import searcher_data

the_scaled_icon_size = hou.ui.scaledSize(16)
the_icon_size = 16

num = 0
# info
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"

scriptpath = os.path.dirname(os.path.realpath(__file__))


def bc(v):
    return str(v).lower() in ("yes", "true", "t", "1")


class SearcherSettings(QtWidgets.QWidget):
    """ Searcher Settings and Debug Menu"""

    def __init__(self, handler, tmphotkey, parent=None):
        super(SearcherSettings, self).__init__(parent=parent)

        # ------------------------------------------------- Component variables
        self.settings = {}
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
        self.hkinput = tmphotkey
        self.datahandler = handler
        self.tmphotkey = tmphotkey

        self.setObjectName('searcher-settings')
        # ------------------------------------------------- Build UI
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.settings = searcher_data.loadsettings()
        self.isdebug = bc(self.settings[util.SETTINGS_KEYS[4]])
        
        # Load UI File
        loader = None
        if int(hver) >= 391:
            loader = _QtUiTools.QUiLoader()
        else:
            loader = QtUiTools.QUiLoader()
        self.ui = loader.load(scriptpath + '/searchersettings.ui')

        # Get UI Elements

        tooltip = hou.qt.ToolTip()
        tooltip.setTitle("Tooltip Example - SOP Torus Help")
        tooltip.setText("This tooltip links to the SOP Torus help page.")
        tooltip.setHelpUrl("/nodes/sop/torus")

        self.hotkey_icon = self.ui.findChild(
            QtWidgets.QToolButton,
            "hotkey_icon"
        )
        self.debugflag = self.ui.findChild(
            QtWidgets.QCheckBox,
            "debugflag_chk"
        )
        self.in_memory_db = self.ui.findChild(
            QtWidgets.QCheckBox,
            "inmemory_chk"
        )
        self.savewindowsize = self.ui.findChild(
            QtWidgets.QCheckBox,
            "windowsize_chk"
        )
        self.hkinput = self.ui.findChild(
            QtWidgets.QLineEdit,
            "hkinput_txt"
        )
        self.database_path = self.ui.findChild(
            QtWidgets.QLineEdit,
            "databasepath_txt"
        )
        self.test1 = self.ui.findChild(
            QtWidgets.QPushButton,
            "test1_btn"
        )
        self.testcontext = self.ui.findChild(
            QtWidgets.QPushButton,
            "test_context_btn"
        )
        self.cleardata = self.ui.findChild(
            QtWidgets.QPushButton,
            "cleardata_btn"
        )
        self.savedata = self.ui.findChild(
            QtWidgets.QPushButton,
            "save_btn"
        )
        self.discarddata = self.ui.findChild(
            QtWidgets.QPushButton,
            "discard_btn"
        )

        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addWidget(self.ui)
        mainlayout.addWidget(hou.qt.createHelpButton("/ref/panes/lightmixer"))

        # ------------------------------------------------- Create Connections
        # self.in_memory_db.stateChanged.connect(self.toggledebug)
        self.hotkey_icon.clicked.connect(self.hotkeyicon_cb)
        self.hotkey_icon.setIcon(util.INFO_ICON)
        info_button_size = hou.ui.scaledSize(16)
        self.hotkey_icon.setProperty("flat", True)
        self.hotkey_icon.setIcon(util.INFO_ICON)
        self.hotkey_icon.setIconSize(QtCore.QSize(
            info_button_size,
            info_button_size
        ))

        tooltip.setTargetWidget(self.hotkey_icon)

        self.hkinput.setText(self.tmphotkey)
        self.hkinput.setStatusTip("Status Tip?")
        self.hkinput.setWhatsThis("Whats this?")
        # self.hkinput.setToolTip(
        #     "If left to the default value of (Ctrl+Alt+Shift+F7), in the event that Searcher detects a conflict it will automatically attempt to try different key combinations.")
        self.hkinput.setStyleSheet(util.TOOLTIP)
        self.database_path.setText(str(self.settings['database_path']))
        self.test1.clicked.connect(self.test1_cb)
        self.testcontext.clicked.connect(self.testcontext_cb)
        self.cleardata.clicked.connect(self.cleardata_cb)
        self.savedata.clicked.connect(self.save_cb)
        self.discarddata.clicked.connect(self.discard_cb)

        # ------------------------------------------------- Apply Layout
        self.setLayout(mainlayout)
        self.installEventFilter(self)

        self.debugflag.setChecked(bc(self.settings[util.SETTINGS_KEYS[4]]))
        self.debugflag.setVisible(bc(self.settings[util.SETTINGS_KEYS[4]]))
        self.in_memory_db.setChecked(bc(self.settings[util.SETTINGS_KEYS[0]]))
        self.savewindowsize.setChecked(
            bc(self.settings[util.SETTINGS_KEYS[2]]))

        # ------------------------------------------------- Add EventFilters
        self.hkinput.installEventFilter(self)
        self.debugflag.installEventFilter(self)
    # ----------------------------------------------------------------------------------- Callbacks

    def hotkeyicon_cb(self):
        self.settings['in_memory_db'] = self.in_memory_db.isChecked()
        print(self.settings['in_memory_db'])

    def toggledebug(self):
        self.settings['in_memory_db'] = self.in_memory_db.isChecked()
        print(self.settings['in_memory_db'])

    def defaulthk_cb(self):
        return

    def test1_cb(self):
        hkeys = []
        for i in range(len(util.HOTKEYLIST)):
            result = hou.hotkeys.findConflicts("h", util.HOTKEYLIST[i])
            hkeys.append(result)
        print (hkeys)

    def cleardata_cb(self):
        self.datahandler.cleardb()

    def save_cb(self):
        if self.hkinput.text() == "":
            buttonindex = hou.ui.displayMessage("Please enter a hotkey")
            self.activateWindow()
            self.hkinput.setFocus()
            self.canedit = True
        else:
            if self.hkinput.text() != self.tmphotkey:
                self.tmphotkey = self.hkinput.text()
                self.datahandler.updatetmphotkey(self.tmphotkey)

            for i in range(len(util.SETTINGS_KEYS)):
                if util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "bool":
                    self.settings[util.SETTINGS_KEYS[i]] = getattr(
                        self, util.SETTINGS_KEYS[i]).isChecked()
                elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "text":
                    self.settings[util.SETTINGS_KEYS[i]] = getattr(
                        self, util.SETTINGS_KEYS[i]).text()

            if self.isdebug:
                print(self.settings)

            searcher_data.savesettings(self.settings)
            self.close()

    def discard_cb(self):
        self.hkinput.setText(self.tmphotkey)
        self.hkholder = ""
        self.close()

    def testcontext_cb(self):
        return

    # ----------------------------------------------------------------------------------- Actions
    def savecheck(self):
        buttonindex = hou.ui.displayMessage(
            "Save changes?", buttons=('Save', 'Discard'), default_choice=0, title="Unsaved Changes:",)
        if buttonindex == 0:
            self.tmphotkey = self.hkinput.text()
            self.datahandler.updatetmphotkey(self.tmphotkey)
            self.hkholder = ""
        elif buttonindex == 1:
            self.hkinput.setText(self.hkholder)
            self.hkholder = ""

    # ----------------------------------------------------------------------------------- Events
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.hkholder = self.hkinput.text()
            self.hkinput.setText("")
            self.hkinput.setPlaceholderText("Input key sequence")
            self.canedit = True
        if event.type() == QtCore.QEvent.Close:
            if self.canedit is False and self.hkholder is not "":
                self.savecheck()
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_D:
                if not self.debugflag.isVisible():
                    self.debugflag.setVisible(True)

            if event.key() == QtCore.Qt.Key_Escape:
                if self.canedit is False:
                    self.close()
            else:
                self.keyindex += 1
                self.keystring = hou.qt.qtKeyToString(
                    event.key(),
                    int(event.modifiers()),
                    event.text()
                )
                if self.canedit:
                    if self.keystring not in ["Esc", "Backspace"]:
                        if self.hkinput.hasFocus():
                            self.KeySequence = QtGui.QKeySequence(
                                self.keystring).toString()
                            self.hkinput.setText(self.KeySequence)
                    if self.keystring in ["Esc", "Backspace"]:
                        self.hkinput.setText(self.hkholder)

        if event.type() == QtCore.QEvent.KeyRelease:
            if event.key() == QtCore.Qt.Key_Escape:
                return QtCore.QObject.eventFilter(self, obj, event)
            else:
                self.keyindex -= 1
                if self.keyindex == 0:
                    if self.hkinput.text() == "":
                        self.hkinput.setText(self.hkholder)
                    if self.hkinput.text() != "":
                        self.canedit = False
        return False
