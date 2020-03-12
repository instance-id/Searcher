from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from searcher import about
from searcher import bugreport
from searcher import bugreport_ui
from searcher import about_ui
from searcher import searcher_data
from searcher import util
from searcher import language_en as la
from searcher import searchersettings_ui

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
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets
    if hver >= 395:
        from hutil.Qt import QtUiTools
    elif hver <= 394 and hver >= 391:
        from hutil.Qt import _QtUiTools
    elif hver < 391 and hver >= 348:
        from hutil.Qt import QtUiTools

reload(about)
reload(about_ui)
reload(bugreport)
reload(bugreport_ui)
reload(searchersettings_ui)

# --------------------------------------------------------------------  App Info
__package__ = "Searcher"
__version__ = "0.1b"
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"

the_scaled_icon_size = hou.ui.scaledSize(16)
the_icon_size = 16

scriptpath = os.path.dirname(os.path.realpath(__file__))

def bc(v):
    return str(v).lower() in ("yes", "true", "t", "1")

class SearcherSettings(QtWidgets.QWidget):
    """ Searcher Settings and Debug Menu"""

    def __init__(self, handler, tmphotkey, parent=None):
        super(SearcherSettings, self).__init__(parent=parent)
        # -------------------------------------------- settings
        # NOTE settings ---------------------------------------
        self.parentwindow = parent
        self.settings = {}
        self.context_dict = {}
        self.command_dict = {}
        self.currentsettings = {}
        self.performcheck = True
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
        self.defaulthotkey = tmphotkey
        self.datahandler = handler
        self.tmphotkey = tmphotkey
        self.isopened = False

        self.setObjectName('searcher-settings')
        # --------------------------------------------- beginui
        # NOTE beginui ----------------------------------------
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.settings = searcher_data.loadsettings()
        self.isdebug = util.Dbug(util.bc(self.settings[util.SETTINGS_KEYS[4]]), str(self.settings[util.SETTINGS_KEYS[10]]))

        self.la = la.TT_SETTINGS
        # Load UI File
        self.ui = searchersettings_ui.Ui_SearcherSettings()
        self.ui.setupUi(self, self.width, self.height, bc(self.settings[util.SETTINGS_KEYS[8]]))
        self.ui.retranslateUi(self)

        self.bugreport = bugreport.BugReport(self.parentwindow)
        self.bugreport.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.bugreport.setWindowFlags(
            QtCore.Qt.Tool |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.NoDropShadowWindowHint
        )
        self.bugreport.setParent(self.parentwindow)
        self.bugreport.resize(520, 250)

        self.settingslayout = QtWidgets.QVBoxLayout()

        # Get UI Elements
        self.hotkey_icon = self.ui.hotkey_icon

        # headerrow
        self.in_memory_db = self.ui.inmemory_chk
        self.in_memory_db.setToolTip(la.TT_SETTINGS[self.in_memory_db.objectName()])
        self.savewindowsize = self.ui.windowsize_chk
        self.savewindowsize.setToolTip(la.TT_SETTINGS[self.savewindowsize.objectName()])

        # secondrow
        self.maxresults = self.ui.maxresults_txt
        self.maxresults.setToolTip(la.TT_SETTINGS[self.maxresults.objectName()])
        self.animatedsettings = self.ui.animatedsettings_chk
        self.animatedsettings.setToolTip(la.TT_SETTINGS[self.animatedsettings.objectName()])
        # thirdrow
        self.defaulthotkey = self.ui.defaulthotkey_txt
        self.defaulthotkey.setToolTip(la.TT_SETTINGS[self.defaulthotkey.objectName()])
        self.database_path = self.ui.databasepath_txt
        self.database_path.setToolTip(la.TT_SETTINGS[self.database_path.objectName()])

        # fourthrow
        self.test1 = self.ui.test1_btn
        self.cleardata = self.ui.cleardata_btn
        self.cleardata.setToolTip(la.TT_SETTINGS[self.cleardata.objectName()])

        # fifthrow
        self.about = self.ui.about_btn
        self.about.setToolTip(la.TT_SETTINGS[self.about.objectName()])
        about_button_size = hou.ui.scaledSize(32)
        self.about.setProperty("flat", True)
        self.about.setIcon(util.ABOUT_ICON1)
        self.about.setIconSize(QtCore.QSize(
            about_button_size,
            about_button_size
        ))

        self.bugreportbtn = self.ui.bug_btn
        self.bugreportbtn.setCheckable(True)
        self.bugreportbtn.setChecked(False)
        bugreport_button_size = hou.ui.scaledSize(21)
        self.bugreportbtn.setProperty("flat", True)
        self.bugreportbtn.setIcon(util.BUG_ICON)
        self.bugreportbtn.setIconSize(QtCore.QSize(
            bugreport_button_size,
            bugreport_button_size
        ))

        self.debuglevel = self.ui.debuglevel_cbx
        for lvl in util.DEBUG_LEVEL:
            self.debuglevel.addItem(str(lvl))
        self.debuglevel.setToolTip(la.TT_SETTINGS[self.debuglevel.objectName()])
        self.debugflag = self.ui.debugflag_chk
        self.debugflag.setToolTip(la.TT_SETTINGS[self.debugflag.objectName()])
        self.debuglevel.setVisible(bc(self.settings[util.SETTINGS_KEYS[4]]))
        self.debugflag.setVisible(bc(self.settings[util.SETTINGS_KEYS[4]]))

        self.savedata = self.ui.save_btn
        self.savedata.setToolTip(la.TT_SETTINGS[self.savedata.objectName()])
        
        self.discarddata = self.ui.discard_btn
        self.discarddata.setToolTip(la.TT_SETTINGS[self.discarddata.objectName()])

        # -------------------------------------------- sixthrow
        # NOTE sixthrow ---------------------------------------
        # self.in_memory_db.stateChanged.connect(self.toggledebug)
        self.hotkey_icon.clicked.connect(self.hotkeyicon_cb)
        info_button_size = hou.ui.scaledSize(16)
        self.hotkey_icon.setProperty("flat", True)
        self.hotkey_icon.setIcon(util.INFO_ICON)
        self.hotkey_icon.setIconSize(QtCore.QSize(
            info_button_size,
            info_button_size
        ))

        self.defaulthotkey.setToolTip(la.TT_SETTINGS[self.discarddata.objectName()])
        self.defaulthotkey.setStyleSheet(util.TOOLTIP)
        
        # --------------------------------------------- connect
        # NOTE connect ----------------------------------------
        self.test1.clicked.connect(self.test1_cb)
        self.cleardata.clicked.connect(self.cleardata_cb)
        self.about.clicked.connect(self.about_cb)
        self.bugreportbtn.clicked.connect(self.bug_cb)
        self.savedata.clicked.connect(self.save_cb)
        self.discarddata.clicked.connect(self.discard_cb)

        # -------------------------------------------- about_cb
        # NOTE about_cb ---------------------------------------
        self.settingslayout = self.ui.verticallayout
        self.setLayout(self.ui.gridLayout)
        
        # ---------------------------------------- eventfilters
        # NOTE eventfilters -----------------------------------
        self.installEventFilter(self)
        self.about.installEventFilter(self)
        self.cleardata.installEventFilter(self)
        self.savedata.installEventFilter(self)
        self.discarddata.installEventFilter(self)
        self.updatecurrentvalues()
        self.fieldsetup()

    # --------------------------------------------------------------- Callbacks
    # SECTION Callbacks -------------------------------------------------------

    def bug_cb(self, toggled):
        pos = self.bugreportbtn.mapToGlobal(
                QtCore.QPoint( -43, 35))
        self.bugreport.setGeometry(
                pos.x(),
                pos.y(),
                self.bugreport.width(),
                self.bugreport.height()
            )

        if toggled == True:
            self.bugreport.show()
        else:
            self.bugreport.close()
            self.bugreport.setParent(None)
    # -------------------------------------------- about_cb
    # NOTE about_cb ---------------------------------------
    def about_cb(self):
        self.about = about.About(self.parentwindow)
        self.about.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.about.setWindowFlags(
            QtCore.Qt.Popup |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.NoDropShadowWindowHint |
            QtCore.Qt.WindowStaysOnTopHint

        )
        self.about.setParent(self.parentwindow)
        self.about.move(self.pos().x() - 175, self.pos().y())
        self.about.show()
        
    # NOTE hotkeyicon_cb ----------------------------------
    def hotkeyicon_cb(self):
        self.settings['in_memory_db'] = self.in_memory_db.isChecked()
        print(self.settings['in_memory_db'])

    # ----------------------------------------- toggledebug
    # NOTE toggledebug ------------------------------------
    def toggledebug(self):
        self.settings['in_memory_db'] = self.in_memory_db.isChecked()
        print(self.settings['in_memory_db'])

    # ---------------------------------------- defaulthk_cb
    # NOTE defaulthk_cb -----------------------------------
    def defaulthk_cb(self):
        return

    # -------------------------------------------- test1_cb
    # NOTE test1_cb ---------------------------------------
    def test1_cb(self):
        hkeys = []
        for i in range(len(util.HOTKEYLIST)):
            result = hou.hotkeys.findConflicts("h", util.HOTKEYLIST[i])
            if result:
                print ("Confliction found: {}".format(result))
            else:
                print("No Confliction: {}".format(result))
            hkeys.append(result)
        print (hkeys)

    # --------------------------------------- cleardata_cb
    # NOTE cleardata_cb ----------------------------------
    def cleardata_cb(self):
        self.datahandler.cleardb()

    # --------------------------------------------- save_cb
    # NOTE save_cb ----------------------------------------
    def save_cb(self):
        if self.defaulthotkey.text() == "":
            _ = hou.ui.displayMessage("Please enter a hotkey")
            self.activateWindow()
            self.defaulthotkey.setFocus()
            self.canedit = True
        else:
            if self.defaulthotkey.text() != self.tmphotkey:
                self.tmphotkey = self.defaulthotkey.text()
                self.datahandler.updatetmphotkey(self.tmphotkey)

            for i in range(len(util.SETTINGS_KEYS)):
                if util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "bool":
                    self.settings[util.SETTINGS_KEYS[i]] = getattr(self, util.SETTINGS_KEYS[i]).isChecked()
                elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "text":
                    self.settings[util.SETTINGS_KEYS[i]] = getattr(self, util.SETTINGS_KEYS[i]).text()
                elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "intval":
                    self.settings[util.SETTINGS_KEYS[i]] = getattr(self, util.SETTINGS_KEYS[i]).value()
                elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "cbx":
                    self.settings[util.SETTINGS_KEYS[i]] = getattr(self, util.SETTINGS_KEYS[i]).currentText()

            if self.isdebug and self.isdebug.level in {"ALL"}:
                print(self.settings)

            searcher_data.savesettings(self.settings)
            self.performcheck = False
            if self.animatedsettings:
                self.parentwindow.anim.start_animation(False)
                self.isopened = True
            else:
                self.close()
    # ------------------------------------------ discard_cb
    # NOTE discard_cb -------------------------------------
    def discard_cb(self):
        if self.animatedsettings:
            self.parentwindow.anim.start_animation(False)
            self.isopened = True
            self.performcheck=True
        else:
            self.close()

    # !SECTION

    # ----------------------------------------------------------------- Actions
    # SECTION Actions ---------------------------------------------------------
    # --------------------------------- updatecurrentvalues
    # NOTE updatecurrentvalues ----------------------------
    def updatecurrentvalues(self):
        for i in range(len(util.SETTINGS_KEYS)):
            self.currentsettings[util.SETTINGS_KEYS[i]] = self.settings[util.SETTINGS_KEYS[i]]
            if util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "bool":
                getattr(self, util.SETTINGS_KEYS[i]).setChecked(bc(self.currentsettings[util.SETTINGS_KEYS[i]]))
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "text":
                getattr(self, util.SETTINGS_KEYS[i]).setText(self.currentsettings[util.SETTINGS_KEYS[i]])
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "intval":
                getattr(self, util.SETTINGS_KEYS[i]).setValue(int(self.currentsettings[util.SETTINGS_KEYS[i]]))
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "cbx":
                getattr(self, util.SETTINGS_KEYS[i]).setCurrentText(str(self.currentsettings[util.SETTINGS_KEYS[i]]))
    
    # ------------------------------------------ fieldsetup
    # NOTE fieldsetup -------------------------------------
    def fieldsetup(self):
        for i in range(len(util.SETTINGS_KEYS)):
            if util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "bool":
                getattr(self, util.SETTINGS_KEYS[i]).setChecked(bc(self.currentsettings[util.SETTINGS_KEYS[i]]))
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "text":
                getattr(self, util.SETTINGS_KEYS[i]).setText(self.currentsettings[util.SETTINGS_KEYS[i]])
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "intval":
                getattr(self, util.SETTINGS_KEYS[i]).setValue(int(self.currentsettings[util.SETTINGS_KEYS[i]]))
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "cbx":
                getattr(self, util.SETTINGS_KEYS[i]).setCurrentText(str(self.currentsettings[util.SETTINGS_KEYS[i]]))
            try:
                getattr(self, util.SETTINGS_KEYS[i]).installEventFilter(self)
            except (AttributeError, TypeError):
                pass

        if self.isdebug and self.isdebug.level in {"ALL"}:
            print(self.currentsettings)

    # ------------------------------------- checkforchanges
    # NOTE checkforchanges --------------------------------
    def checkforchanges(self):
        for i in range(len(util.SETTINGS_KEYS)):
            if util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "bool":
                if getattr(self, util.SETTINGS_KEYS[i]).isChecked() != bc(self.currentsettings[util.SETTINGS_KEYS[i]]):
                    return True
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "text":
                if getattr(self, util.SETTINGS_KEYS[i]).text() != self.currentsettings[util.SETTINGS_KEYS[i]]:
                    return True
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "intval":
               if getattr(self, util.SETTINGS_KEYS[i]).value() != self.currentsettings[util.SETTINGS_KEYS[i]]:
                    return True
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "cbx":
                if getattr(self, util.SETTINGS_KEYS[i]).currentText() != self.currentsettings[util.SETTINGS_KEYS[i]]:
                    return True
        return False
    # ------------------------------------------- savecheck
    # NOTE savecheck --------------------------------------
    def savecheck(self):
        buttonindex = hou.ui.displayMessage(
            "Save changes?",
            buttons=('Save', 'Discard'),
            default_choice=0,
            title="Unsaved Changes:"
        )
        if buttonindex == 0:
            self.save_cb()
            self.hkholder = ""
        elif buttonindex == 1:
            self.defaulthotkey.setText(self.hkholder)
            self.hkholder = ""
    # !SECTION

    # ------------------------------------------------------------------ Events
    # SECTION Events ----------------------------------------------------------
    def eventFilter(self, obj, event):
        # ------------------------------------------ Window
        # NOTE Window -------------------------------------
        if event.type() == QtCore.QEvent.WindowActivate:
            self.ui.isopened = True
            self.performcheck = True
            self.updatecurrentvalues()
            return True

        # ------------------------------------------- Mouse
        # NOTE Mouse --------------------------------------
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if obj == self.defaulthotkey:
                self.hkholder = self.defaulthotkey.text()
                self.defaulthotkey.setText("")
                self.defaulthotkey.setPlaceholderText("Input key sequence")
                self.canedit = True
        if event.type() == QtCore.QEvent.Enter:
            self.parentwindow.checktooltip(obj)
        if event.type() == QtCore.QEvent.Leave:
            self.parentwindow.checktooltip(obj, True)
        if event.type() == QtCore.QEvent.ToolTip:
            return True

        # ---------------------------------------- Keypress
        # NOTE Keypress -----------------------------------
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_D:
                if obj != self.defaulthotkey:
                    if not self.debugflag.isVisible():
                        self.debugflag.setVisible(True)

            if event.key() == QtCore.Qt.Key_Escape:
                if self.performcheck:
                    if self.checkforchanges():
                        self.savecheck()
                if self.animatedsettings:
                    self.parentwindow.anim.start_animation(False)
                    self.isopened = True
                    self.performcheck=True
                else:
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
                        if self.defaulthotkey.hasFocus():
                            self.KeySequence = QtGui.QKeySequence(self.keystring).toString()
                            self.defaulthotkey.setText(self.KeySequence)
                    if self.keystring in ["Esc", "Backspace"]:
                        self.defaulthotkey.setText(self.hkholder)

        # -------------------------------------- Keyrelease
        # NOTE Keyrelease ---------------------------------
        if event.type() == QtCore.QEvent.KeyRelease:
            if event.key() == QtCore.Qt.Key_Escape:
                return QtCore.QObject.eventFilter(self, obj, event)
            else:
                self.keyindex -= 1
                if self.keyindex == 0:
                    if self.defaulthotkey.text() == "":
                        self.defaulthotkey.setText(self.hkholder)
                    if self.defaulthotkey.text() != "":
                        self.canedit = False

        # ------------------------------------------- Close
        # NOTE Close --------------------------------------
        if event.type() == QtCore.QEvent.Close:
            self.ui.isopened = False
            self.parentwindow.opensettingstool.setChecked(False)
            self.performcheck=True

        return QtCore.QObject.eventFilter(self, obj, event)


class LinkLabel(QtWidgets.QLabel):
    def __init__(self, parent, text):
        super(LinkLabel, self).__init__(parent)

        self.setText(text)
        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)