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
from searcher import searcher_data
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
    if hver >= 395:
        from hutil.Qt import QtUiTools
    elif hver <= 394 and hver >= 391:
        from hutil.Qt import _QtUiTools
    elif hver < 391 and hver >= 348:
        from hutil.Qt import QtUiTools

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

        self.bugreport = bugreport.BugReport(self)
        self.bugreport.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.bugreport.setWindowFlags(
            QtCore.Qt.Tool |
            # QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.NoDropShadowWindowHint
        )
        self.bugreport.resize(width, height - 60)

        self.theme = theme.Theme(self)
        self.theme.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.theme.setWindowFlags(
            QtCore.Qt.Tool |
            # QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.NoDropShadowWindowHint
        )
        self.theme.resize(width, height - 190)

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
        theme_button_size = hou.ui.scaledSize(21)
        self.themebtn.setProperty("flat", True)
        self.themebtn.setIcon(util.BUG_ICON)
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
        self.about.clicked.connect(self.about_cb)
        self.bugreportbtn.clicked.connect(self.bug_cb)
        self.themebtn.clicked.connect(self.theme_cb)
        self.savedata.clicked.connect(self.save_cb)
        self.discarddata.clicked.connect(self.discard_cb)

        # -------------------------------------------- about_cb
        # NOTE about_cb ---------------------------------------
        self.settingslayout = self.ui.verticallayout
        self.setLayout(self.ui.gridLayout)
        
        # ---------------------------------------- eventfilters
        # NOTE eventfilters -----------------------------------
        self.installEventFilter(self)
        self.ui.maxresults_lbl.installEventFilter(self)
        self.ui.defaulthotkey_lbl.installEventFilter(self)
        self.ui.dbpath_lbl.installEventFilter(self)
        self.bugreportbtn.installEventFilter(self)
        self.about.installEventFilter(self)
        self.cleardata.installEventFilter(self)
        self.savedata.installEventFilter(self)
        self.discarddata.installEventFilter(self)
        self.updatecurrentvalues()
        self.fieldsetup()

    # --------------------------------------------------------------- Callbacks
    # SECTION Callbacks -------------------------------------------------------
    # ---------------------------------------------- bug_cb
    # NOTE bug_cb -----------------------------------------
    def bug_cb(self, toggled):
        if toggled == True and not self.bugreport.isVisible():
            if self.animatedsettings.isChecked():
                pos = self.bugreportbtn.mapToGlobal(
                    QtCore.QPoint( -43, 34))
            else:
                pos = self.bugreportbtn.mapToGlobal(
                    QtCore.QPoint( -45, 35))
            self.bugreport.setGeometry(
                    pos.x(),
                    pos.y(),
                    self.bugreport.width(),
                    self.bugreport.height()
                )
            self.bugreport.show()
        else:
            self.bugreport.close()

    # -------------------------------------------- theme_cb
    # NOTE theme_cb ---------------------------------------
    def theme_cb(self, toggled):
        if toggled == True and not self.theme.isVisible():
            if self.animatedsettings.isChecked():
                pos = self.themebtn.mapToGlobal(
                    QtCore.QPoint( -77, 34))
            else:
                pos = self.themebtn.mapToGlobal(
                    QtCore.QPoint( -79, 35))
            self.theme.setGeometry(
                    pos.x(),
                    pos.y(),
                    self.theme.width(),
                    self.theme.height()
                )
            self.theme.show()
        else:
            self.theme.close()

    # -------------------------------------------- about_cb
    # NOTE about_cb ---------------------------------------
    def about_cb(self):
        self.aboutui = about.About(self.parentwindow)
        self.aboutui.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.aboutui.setWindowFlags(
            QtCore.Qt.Popup |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.NoDropShadowWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.aboutui.setParent(self.parentwindow)
        self.aboutui.move(self.pos().x() - 175, self.pos().y())
        self.aboutui.show()
        
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

            searcher_data.savesettings(self.settings)
            if self.resetdb:
                hou.session.DBCONNECTION = None
                hou.session.DATABASE = None
                self.resetdb = False
            if self.modifylayout:
                self.parentwindow.sui.metricpos.setVisible(
                    self.settings[util.SETTINGS_KEYS[12]])
            self.performcheck = False
            if self.bugreport.isVisible():
                self.bugreport.close()
                self.bugreportbtn.setChecked(False)
            if self.theme.isVisible():
                self.theme.close()
                self.themebtn.setChecked(False)
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
        if self.bugreport.isVisible():
            self.bugreport.close()
            self.bugreportbtn.setChecked(False)
        if self.theme.isVisible():
            self.theme.close()
            self.themebtn.setChecked(False)
        if self.settings[util.SETTINGS_KEYS[8]]:
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
    # !SECTION

    # ------------------------------------------------------------- Events
    # SECTION Events -----------------------------------------------------
    def eventFilter(self, obj, event):
        # ------------------------------------------ Window
        # NOTE Window -------------------------------------
        if event.type() == QtCore.QEvent.WindowActivate:
            self.ui.isopened = True
            self.performcheck = True
            # self.updatecurrentvalues()
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
                if obj == self:
                    if self.performcheck:
                        if self.checkforchanges():
                            self.savecheck()
                    if self.animatedsettings.isChecked() and not self.waitforclose:
                        if self.bugreport.isVisible():
                            self.bugreport.close()
                            self.bugreportbtn.setChecked(False)
                        if self.theme.isVisible():
                            self.theme.close()
                            self.themebtn.setChecked(False)
                        self.parentwindow.anim.start_animation(False)
                        self.isopened = True
                        return True
                    elif self.waitforclose:
                        if self.bugreport.isVisible():
                            self.bugreport.close()
                        if self.theme.isVisible():
                            self.theme.close()
                            self.themebtn.setChecked(False)
                        self.close()
                        self.parentwindow.close()
                        return True
                    else:
                        if self.bugreport.isVisible():
                            self.bugreport.close()
                        if self.theme.isVisible():
                            self.theme.close()
                            self.themebtn.setChecked(False)
                        self.close()
                        return True
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
            self.resetdb = False
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