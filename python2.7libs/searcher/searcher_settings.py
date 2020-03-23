from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from searcher import util
from searcher import about
from searcher import theme
from searcher import about_ui
from searcher import theme_ui
from searcher import bugreport
from searcher import bugreport_ui
from searcher import settings_data
from searcher import language_en as la
from searcher import searcher_settings_ui

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
else:
    from PyQt5 import QtGui
    from PyQt5 import QtCore
    from PyQt5 import QtWidgets

reload(about)
reload(theme)
reload(about_ui)
reload(theme_ui)
reload(bugreport)
reload(bugreport_ui)
reload(searcher_settings_ui)

# --------------------------------------------------------------------  App Info
__package__ = "Searcher"
__version__ = "0.1b"
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"

# --------------------------------------------- hou.session
# NOTE hou.session ----------------------------------------
def get_settings():
    return getattr(hou.session, "SETTINGS", None)

the_scaled_icon_size = hou.ui.scaledSize(16)
the_icon_size = 16

scriptpath = os.path.dirname(os.path.realpath(__file__))

def bc(v):
    return str(v).lower() in ("yes", "true", "t", "1")

class SearcherSettings(QtWidgets.QWidget):
    """ Searcher Settings and Debug Menu"""

    def __init__(self, handler, width, height, parent=None):
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
        self.datahandler = handler
        self.isopened = False
        self.resetdb = False
        self.waitforclose = False
        self.modifylayout = False
        self.uiwidth = width
        self.uiheight = height
        self.windowlist = ["about", "bugreport", "theme"]
        self.parentwindow.oldPos = self.parentwindow.pos()

        # --------------------------------------------- beginui
        # NOTE beginui ----------------------------------------
        self.setObjectName('searcher-settings')
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.settings = get_settings()
        self.isdebug = util.Dbug(
            self.settings[util.SETTINGS_KEYS[4]], 
            str(self.settings[util.SETTINGS_KEYS[10]]),
            self.settings[util.SETTINGS_KEYS[12]],
            self.settings[util.SETTINGS_KEYS[13]],
        )

        self.la = la.TT_SETTINGS
        # Load UI File
        self.ui = searcher_settings_ui.Ui_SearcherSettings()
        self.ui.setupUi(self, self.uiwidth, self.uiheight, bc(self.settings[util.SETTINGS_KEYS[8]]))
        self.ui.retranslateUi(self)

        self.about = about.About(self)
        self.about.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.about.setWindowFlags(
            QtCore.Qt.Tool 
            | QtCore.Qt.FramelessWindowHint 
            | QtCore.Qt.CustomizeWindowHint
            #| QtCore.Qt.NoDropShadowWindowHint 
            # | QtCore.Qt.X11BypassWindowManagerHint
        )
        self.about.resize(width, height - 180)

        self.bugreport = bugreport.BugReport(self)
        self.bugreport.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.bugreport.setWindowFlags(
            QtCore.Qt.Tool 
            | QtCore.Qt.FramelessWindowHint 
            | QtCore.Qt.CustomizeWindowHint
            #| QtCore.Qt.NoDropShadowWindowHint
            # | QtCore.Qt.X11BypassWindowManagerHint
        )
        self.bugreport.resize(width, height - 180)

        self.theme = theme.Theme(self)
        self.theme.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.theme.setWindowFlags(
            QtCore.Qt.Tool
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.NoDropShadowWindowHint
            # | QtCore.Qt.X11BypassWindowManagerHint
        )
        self.theme.resize(width, height - 90)

        self.settingslayout = QtWidgets.QVBoxLayout()

        # Get UI Elements
        self.hotkey_icon = self.ui.hotkey_icon

        # headerrow
        self.in_memory_db = self.ui.inmemory_chk
        self.in_memory_db.setToolTip(la.TT_SETTINGS[self.in_memory_db.objectName()])
        self.savewindowsize = self.ui.windowsize_chk
        self.savewindowsize.setToolTip(la.TT_SETTINGS[self.savewindowsize.objectName()])

        # secondrow
        self.ui.maxresults_lbl.setToolTip(la.TT_SETTINGS[self.ui.maxresults_lbl.objectName()])
        self.maxresults = self.ui.maxresults_txt
        self.maxresults.setToolTip(la.TT_SETTINGS[self.maxresults.objectName()])
        self.animatedsettings = self.ui.animatedsettings_chk
        self.animatedsettings.setToolTip(la.TT_SETTINGS[self.animatedsettings.objectName()])
        
        # thirdrow
        self.ui.defaulthotkey_lbl.setToolTip(la.TT_SETTINGS[self.ui.defaulthotkey_lbl.objectName()])
        self.defaulthotkey = self.ui.defaulthotkey_txt
        self.defaulthotkey.setToolTip(la.TT_SETTINGS[self.defaulthotkey.objectName()])
        
        # fourthrow
        self.ui.dbpath_lbl.setToolTip(la.TT_SETTINGS[self.ui.dbpath_lbl.objectName()])
        self.database_path = self.ui.databasepath_txt
        self.database_path.setToolTip(la.TT_SETTINGS[self.database_path.objectName()])
        self.dbpath_btn = self.ui.dbpath_icon 
        dbpath_button_size = hou.ui.scaledSize(16)
        self.dbpath_btn.setProperty("flat", True)
        self.dbpath_btn.setIcon(util.FILE_ICON)
        self.dbpath_btn.setIconSize(QtCore.QSize(
            dbpath_button_size,
            dbpath_button_size
        ))

        # fifthrow
        self.metrics = self.ui.metrics_chk
        self.metrics.setToolTip(la.TT_SETTINGS[self.metrics.objectName()])
        self.cleardata = self.ui.cleardata_btn
        self.cleardata.setToolTip(la.TT_SETTINGS[self.cleardata.objectName()])

        # sixthrow
        self.aboutbtn = self.ui.about_btn
        self.aboutbtn.setToolTip(la.TT_SETTINGS[self.aboutbtn.objectName()])
        self.aboutbtn.setCheckable(True)
        self.aboutbtn.setChecked(False)
        about_button_size = hou.ui.scaledSize(32)
        self.aboutbtn.setProperty("flat", True)
        self.aboutbtn.setIcon(util.ABOUT_ICON1)
        self.aboutbtn.setIconSize(QtCore.QSize(
            about_button_size,
            about_button_size
        ))

        self.bugreportbtn = self.ui.bug_btn
        self.bugreportbtn.setToolTip(la.TT_SETTINGS[self.bugreportbtn.objectName()])
        self.bugreportbtn.setCheckable(True)
        self.bugreportbtn.setChecked(False)
        bugreport_button_size = hou.ui.scaledSize(21)
        self.bugreportbtn.setProperty("flat", True)
        self.bugreportbtn.setIcon(util.BUG_ICON)
        self.bugreportbtn.setIconSize(QtCore.QSize(
            bugreport_button_size,
            bugreport_button_size
        ))

        self.themebtn = self.ui.theme_btn
        self.themebtn.setToolTip(la.TT_SETTINGS[self.themebtn.objectName()])
        self.themebtn.setCheckable(True)
        self.themebtn.setChecked(False)
        theme_button_size = hou.ui.scaledSize(27)
        self.themebtn.setProperty("flat", True)
        self.themebtn.setIcon(util.COLOR_ICON)
        self.themebtn.setIconSize(QtCore.QSize(
            theme_button_size,
            theme_button_size
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
        info_button_size = hou.ui.scaledSize(16)
        self.hotkey_icon.setProperty("flat", True)
        self.hotkey_icon.setIcon(util.INFO_ICON)
        self.hotkey_icon.setIconSize(QtCore.QSize(
            info_button_size,
            info_button_size
        ))

        # --------------------------------------------- connect
        # NOTE connect ----------------------------------------
        self.hotkey_icon.clicked.connect(self.hotkeyicon_cb)
        self.dbpath_btn.clicked.connect(self.dbpath_cb)
        self.cleardata.clicked.connect(self.cleardata_cb)
        self.aboutbtn.clicked.connect(self.window_cb)
        self.bugreportbtn.clicked.connect(self.window_cb)
        self.themebtn.clicked.connect(self.window_cb)
        self.savedata.clicked.connect(self.save_cb)
        self.discarddata.clicked.connect(self.discard_cb)

        # -------------------------------------------- about_cb
        # NOTE about_cb ---------------------------------------
        self.settingslayout = self.ui.verticallayout
        self.setLayout(self.ui.gridLayout)
        
        # ----------------------------------- Startup Functions
        # NOTE Startup Functions ------------------------------
        self.updatecurrentvalues()
        self.fieldsetup()

    # --------------------------------------------------------------- Functions
    # SECTION Functions -------------------------------------------------------
    def closewindows(self):
        for i in range(len(self.windowlist)):
            if getattr(self, self.windowlist[i]).isVisible():
                getattr(self, self.windowlist[i]).close()
                getattr(self, self.windowlist[i] + "btn").setChecked(False)

    # ----------------------------------------- mapposition
    # NOTE mapposition ------------------------------------
    def mapposition(self, w, h, s):
        parent =  s.parent()
        pos = parent.mapToGlobal(QtCore.QPoint(w ,h))
        getattr(self, s.objectName()).setGeometry(
            pos.x(),
            pos.y() + parent.height(),
            getattr(self, s.objectName()).width(),
            getattr(self, s.objectName()).height()) 
        getattr(self, s.objectName()).show()
    # !SECTION Functions
        
    # --------------------------------------------------------------- Callbacks
    # SECTION Callbacks -------------------------------------------------------
    # ------------------------------------------- window_cb
    # The sender is the actual button, but the button is 
    # the same as the window instance so that both can be 
    # sent and accessed in methods via one variable.
    # NOTE window_cb --------------------------------------
    def window_cb(self, toggled):
        self.closewindows()
        s = self.sender()

        if toggled == True and not getattr(self, s.objectName()).isVisible():
            if s.objectName() == "about":
                self.mapposition(0, 0, s) if self.animatedsettings.isChecked() else self.mapposition(0, 0, s)
            elif s.objectName() == "bugreport":
                self.mapposition(0, 0, s) if self.animatedsettings.isChecked() else self.mapposition(0, 0, s)
            elif s.objectName() == "theme":
                self.mapposition(0, 0, s) if self.animatedsettings.isChecked() else self.mapposition(0, 0, s)
        else:
            if s.objectName() in self.windowlist:
                getattr(self, s.objectName()).close()
        
    # --------------------------------------- hotkeyicon_cb
    # NOTE hotkeyicon_cb ----------------------------------
    def hotkeyicon_cb(self):
        self.settings['in_memory_db'] = self.in_memory_db.isChecked()
        print(self.settings['in_memory_db'])

    # ------------------------------------------- dbpath_cb
    # NOTE dbpath_cb --------------------------------------
    def dbpath_cb(self):
        path = os.path.normpath(self.database_path.text()).replace("\\", "/")
        dbpath = hou.expandString(hou.ui.selectFile(
            start_directory=os.path.dirname(path),
            title="Save Database",
            pattern="searcher.db",
            file_type=hou.fileType.Clip,
            default_value="searcher.db"))
        if dbpath != "":
            if not dbpath.endswith("searcher.db"):
                dbpath = dbpath + "searcher.db"
            self.database_path.setText((os.path.normpath(dbpath)))

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
            self.checkforchanges()
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

            settings_data.savesettings(self.settings)
            
            if self.resetdb:
                hou.session.DBCONNECTION = None
                hou.session.DATABASE = None
                self.resetdb = False

            if self.modifylayout:
                self.parentwindow.sui.metricpos.setVisible(
                    self.settings[util.SETTINGS_KEYS[12]])

            self.performcheck = False
            self.closewindows()

            if self.animatedsettings.isChecked() and not self.waitforclose:
                self.parentwindow.anim.start_animation(False)
                self.isopened = True
            elif self.waitforclose:
                if self.bugreport.isVisible():
                    self.bugreport.close()
                self.close()
                self.parentwindow.close()
            else:
                self.close()

    # ------------------------------------------ discard_cb
    # NOTE discard_cb -------------------------------------
    def discard_cb(self):
        self.closewindows()

        if self.settings[util.SETTINGS_KEYS[8]]:
            self.parentwindow.anim.start_animation(False)
            self.isopened = True
            self.performcheck=True
        else:
            self.close()

    # !SECTION Callbacks

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
        if self.isdebug and self.isdebug.level in {"ALL"}:
            print(len(util.SETTINGS_KEYS))
        for i in range(len(util.SETTINGS_KEYS)):
            if self.isdebug and self.isdebug.level in {"ALL"}:
                print(i)
            if util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "bool":
                if self.isdebug and self.isdebug.level in {"ALL"}:
                    print("Name: ", getattr(self, util.SETTINGS_KEYS[i]).objectName())
                    print("Shown settings: ", getattr(self, util.SETTINGS_KEYS[i]).isChecked())
                    print("Current settings: ", bc(self.currentsettings[util.SETTINGS_KEYS[i]]))
                if getattr(self, util.SETTINGS_KEYS[i]).isChecked() != bc(self.currentsettings[util.SETTINGS_KEYS[i]]):
                    if util.SETTINGS_KEYS[i] == util.SETTINGS_KEYS[0]: 
                        self.resetdb = True
                    elif util.SETTINGS_KEYS[i] == util.SETTINGS_KEYS[8]:
                        self.waitforclose = True
                    elif util.SETTINGS_KEYS[i] == util.SETTINGS_KEYS[12]:
                        self.modifylayout = True
                    if self.isdebug and self.isdebug.level in {"ALL"}:
                        print("Offending item: ", i)
                    return True
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "text":
                if self.isdebug and self.isdebug.level in {"ALL"}:
                    print("Name: ", getattr(self, util.SETTINGS_KEYS[i]).objectName())
                    print("Shown settings: ", getattr(self, util.SETTINGS_KEYS[i]).text())
                    print("Current settings: ",self.currentsettings[util.SETTINGS_KEYS[i]])
                if getattr(self, util.SETTINGS_KEYS[i]).text() != self.currentsettings[util.SETTINGS_KEYS[i]]:
                    if self.isdebug and self.isdebug.level in {"ALL"}:
                        print("Offending item: ", i)
                    return True
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "intval":
                if self.isdebug and self.isdebug.level in {"ALL"}:
                    print("Name: ", getattr(self, util.SETTINGS_KEYS[i]).objectName())
                    print("Shown settings: ", getattr(self, util.SETTINGS_KEYS[i]).value())
                    print("Current settings: ",self.currentsettings[util.SETTINGS_KEYS[i]])
                if getattr(self, util.SETTINGS_KEYS[i]).value() != int(self.currentsettings[util.SETTINGS_KEYS[i]]):
                    if self.isdebug and self.isdebug.level in {"ALL"}:
                        print("Offending item: ", i)
                    return True
            elif util.SETTINGS_TYPES[util.SETTINGS_KEYS[i]] == "cbx":
                if self.isdebug and self.isdebug.level in {"ALL"}:
                    print("Name: ", getattr(self, util.SETTINGS_KEYS[i]).objectName())
                    print("Shown settings: ", getattr(self, util.SETTINGS_KEYS[i]).currentText())
                    print("Current settings: ", str(self.currentsettings[util.SETTINGS_KEYS[i]]))
                if getattr(self, util.SETTINGS_KEYS[i]).currentText() != str(self.currentsettings[util.SETTINGS_KEYS[i]]):
                    if self.isdebug and self.isdebug.level in {"ALL"}:
                        print("Offending item: ", i)
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
            self.hkholder = ""
    
    # ------------------------------------ closeroutine
    # NOTE closeroutine -------------------------------
    def closeroutine(self):
        if self.performcheck:
            if self.checkforchanges():
                self.savecheck()
        if self.animatedsettings.isChecked() and not self.waitforclose:
            self.closewindows()
            self.parentwindow.anim.start_animation(False)
            self.isopened = True
            return True
        elif self.waitforclose:
            self.closewindows()
            self.close()
            self.parentwindow.close()
            return True
        else:
            self.closewindows()
            self.close()

    # !SECTION Actions

    def movesubwindows(self, pos, resize=False):
        if self.about.isVisible():
            if resize: self.about.move(self.about.x() + pos.x(), self.about.y())
            else: self.about.move(self.about.x() + pos.x(), self.about.y() + pos.y())
        if self.bugreport.isVisible():
            if resize: self.bugreport.move(self.bugreport.x() + pos.x(), self.bugreport.y())
            else: self.bugreport.move(self.bugreport.x() + pos.x(), self.bugreport.y() + pos.y())
        if self.theme.isVisible():
            if resize: self.theme.move(self.theme.x() + pos.x(), self.theme.y())
            else: self.theme.move(self.theme.x() + pos.x(), self.theme.y() + pos.y())

    # ------------------------------------------------------------- Events
    # SECTION Events -----------------------------------------------------
    # ------------------------------------- addeventfilters
    # NOTE addeventfilters --------------------------------
    def addeventfilters(self):
        self.installEventFilter(self)
        self.about.installEventFilter(self)
        self.savedata.installEventFilter(self)
        self.cleardata.installEventFilter(self)
        self.discarddata.installEventFilter(self)
        self.bugreportbtn.installEventFilter(self)
        self.ui.dbpath_lbl.installEventFilter(self)
        self.ui.maxresults_lbl.installEventFilter(self)
        self.ui.defaulthotkey_lbl.installEventFilter(self)

    # ---------------------------------- removeeventfilters
    # NOTE removeeventfilters -----------------------------
    def removeeventfilters(self):
        self.removeEventFilter(self)
        self.about.removeEventFilter(self)
        self.savedata.removeEventFilter(self)
        self.cleardata.removeEventFilter(self)
        self.discarddata.removeEventFilter(self)
        self.bugreportbtn.removeEventFilter(self)
        self.ui.dbpath_lbl.removeEventFilter(self)
        self.ui.maxresults_lbl.removeEventFilter(self)
        self.ui.defaulthotkey_lbl.removeEventFilter(self)

    def eventFilter(self, obj, event):
        event_type = event.type()

        # ------------------------------------------ Window
        # NOTE Window -------------------------------------
        if event_type == QtCore.QEvent.WindowActivate:
            self.addeventfilters()
            self.ui.isopened = True
            self.performcheck = True

        # ------------------------------------------- Mouse
        # SECTION Mouse -----------------------------------
        # ----------------------- MouseButtonPress
        # NOTE MouseButtonPress ------------------
        if event_type == QtCore.QEvent.MouseButtonPress:
            if obj == self:
                self.activateWindow()

        # -------------------- MouseButtonDblClick
        # NOTE MouseButtonDblClick ---------------
        if event_type == QtCore.QEvent.MouseButtonDblClick:
            if obj == self.defaulthotkey:
                self.hkholder = self.defaulthotkey.text()
                self.defaulthotkey.setText("")
                self.defaulthotkey.setPlaceholderText("Input key sequence")
                self.canedit = True

        # ---------------------------------- Enter
        # NOTE Enter -----------------------------
        if event_type == QtCore.QEvent.Enter:
            self.parentwindow.checktooltip(obj)

        # ---------------------------------- Leave
        # NOTE Leave -----------------------------
        if event_type == QtCore.QEvent.Leave:
            self.parentwindow.checktooltip(obj, True)

        # -------------------------------- ToolTip
        # NOTE ToolTip ---------------------------
        if event_type == QtCore.QEvent.ToolTip:
            return True
        # !SECTION

        # ---------------------------------------- Keypress
        # SECTION Keypress --------------------------------
        if event_type == QtCore.QEvent.KeyPress:
        # ---------------------------------- Key_D
        # NOTE Key_D -----------------------------
            if event.key() == QtCore.Qt.Key_D:
                if obj != self.defaulthotkey:
                    if not self.debugflag.isVisible():
                        self.debugflag.setVisible(True)

        # ----------------------------- Key_Escape
        # NOTE Key_Escape ------------------------
            if event.key() == QtCore.Qt.Key_Escape:
                if obj == self:
                    self.closeroutine()
                    return True

        # ----------------------------------- else
        # NOTE else ------------------------------
            else:
                if obj == self.defaulthotkey:
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
        # !SECTION

        # -------------------------------------- Keyrelease
        # SECTION Keyrelease ------------------------------
        if event_type == QtCore.QEvent.KeyRelease:
            if event.key() == QtCore.Qt.Key_Escape:
                return QtCore.QObject.eventFilter(self, obj, event)
            else:
                self.keyindex -= 1
                if self.keyindex == 0:
                    if self.defaulthotkey.text() == "":
                        self.defaulthotkey.setText(self.hkholder)
                    if self.defaulthotkey.text() != "":
                        self.canedit = False
        # !SECTION

        # ------------------------------------------- Close
        # NOTE Close --------------------------------------
        if event_type == QtCore.QEvent.Close:
            self.ui.isopened = False
            self.resetdb = False
            self.parentwindow.opensettingstool.setChecked(False)
            self.performcheck=True
            if not self.parentwindow.isActiveWindow():
                self.parentwindow.activateWindow()
            self.removeeventfilters()
            
        return QtCore.QObject.eventFilter(self, obj, event)
    
    # !SECTION Events

class LinkLabel(QtWidgets.QLabel):
    def __init__(self, parent, text):
        super(LinkLabel, self).__init__(parent)

        self.setText(text)
        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)


