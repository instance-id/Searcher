from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import weakref
import timeit

from searcher import util
from searcher import style
from searcher import ptime
from searcher import animator
from searcher import database
from searcher import HelpButton
from searcher import datahandler
from searcher import searcher_ui
from searcher import settings_data
from searcher import searcher_settings
from searcher import searcher_settings_ui
from searcher import language_en as la

import os
import re
import sys
import hou
import time
import platform
import threading
import hdefereval as hd
from canvaseventtypes import *
from string import ascii_letters
from collections import Iterable

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

reload(searcher_settings_ui)
reload(searcher_settings)
reload(settings_data)
reload(searcher_ui)
reload(datahandler)
reload(HelpButton)
reload(animator)
reload(database)
reload(style)
reload(ptime)
reload(util)
reload(la)


# --------------------------------------------------------------------  Variables / Constants
kwargs = {}
settings = {}
hasran = False
mousePos = None
cur_screen = QtWidgets.QDesktopWidget().screenNumber(
    QtWidgets.QDesktopWidget().cursor().pos()
)
screensize = QtWidgets.QDesktopWidget().screenGeometry(cur_screen)
centerPoint = QtWidgets.QDesktopWidget().availableGeometry(cur_screen).center()

sys.path.append(os.path.join(os.path.dirname(__file__)))
script_path = os.path.dirname(os.path.realpath(__file__))
name = "Searcher"

parent_widget = hou.qt.mainWindow()
# endregion

# --------------------------------------------------------------------  Class Functions

def get_settings():
    return getattr(hou.session, "SETTINGS", None)

def get_dbhandler():
    return getattr(hou.session, "DBHANDLER", None)

def keyconversion(key):
    for i in range(len(key)):
        if key[i] in util.KEYCONVERSIONS:
            key[i] = util.KEYCONVERSIONS[key[i]]
    return key
# endregion

# --------------------------------------------------------------------  Searcher Class

class Searcher(QtWidgets.QWidget):
    """instance.id Searcher for Houdini"""
    # ------------------------------------------------------------- Class init
    # SECTION Class init -----------------------------------------------------
    def __init__(self, kwargs, settings, windowsettings, searcher_window, animated):
        super(Searcher, self).__init__(hou.qt.mainWindow())
        self.parentwindow = hou.qt.mainWindow()
        self.searcher_window = self
        self._drag_active = False
        self.settingdata = settings
        self.animationDuration = 200
        self.animated = animated
        self.animated = False

        # Setting vars
        self.kwargs = kwargs
        self.windowsettings = windowsettings
        self.isdebug = util.Dbug(
            self.settingdata[util.SETTINGS_KEYS[4]],
            str(self.settingdata[util.SETTINGS_KEYS[10]]),
            self.settingdata[util.SETTINGS_KEYS[12]],
            self.settingdata[util.SETTINGS_KEYS[13]],
        )
        self.appcolors = util.AppColors(self.settingdata[util.SETTINGS_KEYS[14]])
        self.windowispin = util.bc(self.settingdata[util.SETTINGS_KEYS[5]])
        self.expanditems = self.settingdata[util.SETTINGS_KEYS[15]]
        self.showctx = util.bc(self.settingdata[util.SETTINGS_KEYS[7]])
        self.originalsize = self.settingdata[util.SETTINGS_KEYS[3]]
        self.animatedsettings = self.settingdata[util.SETTINGS_KEYS[8]]
        self.settingslayout = QtWidgets.QVBoxLayout()
        self.app = QtWidgets.QApplication.instance()

        # UI Vars
        if self.animatedsettings:
            self.uiwidth = int(520)
            self.uiheight = int(300)
        else:
            self.uiwidth = int(520)
            self.uiheight = int(242)

        self.handler = self.initialsetup()
        self.ui = searcher_settings.SearcherSettings(
            self.handler,
            self.uiwidth,
            self.uiheight,
            self
        )
        if self.animatedsettings:
            self.anim = animator.Animator(self.ui, self.anim_complete)

        # Performance timers
        # self.timerprofile = None  # ANCHOR hou perf timer ---------------------------------------- hou perf timer
        # self.searchevent = None   # ANCHOR hou perf timer ---------------------------------------- hou perf timer
        self.endtime = 0
        self.starttime = 0
        self.hotkeystime = 0
        self.regtimetotal = 0
        self.hcontexttime = 0
        self.threadtimer = None

        # Functional Vars
        self.lastused = {}
        self.treecatnum = 0
        self.treeitemsnum = 0
        self.hotkeys = []
        self.context_list = []
        self.hcontext_tli = {}
        self.tmpkey = None
        self.tiptimer = None
        self.resizing = False
        self.mouseout = False
        self.tmpsymbol = None
        self.searching = False
        self.ctxsearch = False
        self.showglobal = True
        self.menuopened = False
        self.overhandle = False
        self.previous_pos = None
        self.searchprefix = False
        self.keys_changed = False
        self.holdinfobanner = False
        self.searchdescription = False
        self.searchcurrentcontext = False

        # Functionals
        hou.hotkeys._createBackupTables()
        self.uisetup()

        # Event System Initialization
        self.addshortcuts()

        # ---------------------------------- Build Settings
        # NOTE Build Settings -----------------------------
        self.buildsettingsmenu()
        # self.demoitems()

        # hou.playbar.moveToPane(hou.ui.paneUnderCursor()) # TODO - -- Test
        # print(hou.playbar.eventCallbacks())
        # hou.PathBasedPaneTab()
        # if self.kwargs:
        #     if isinstance(self.kwargs, Iterable):
        #         for i in self.kwargs:
        #             print(i)
        #     else:
        #         print(self.kwargs)

    # !SECTION Class init

    def getwidgets(self):
        # allWidgets = QtWidgets.QApplication.allWidgets()
        # for w in allWidgets:
        #     if w.windowTitle() != "":
        #         print("Title: %s" % w.windowTitle())

        pos = QtGui.QCursor.pos()
        if self.isdebug and self.isdebug.level in {"ALL"}:
            print("Position: X:%d Y: %d" % (pos.x(), pos.y()))
            
        mainwin = QtWidgets.QApplication
        undermouse = util.widgets_at(mainwin, pos)

        for w in undermouse:
            if w.windowTitle() != "":
                print("Title: %s" % w.windowTitle())

    #     outputpath =  os.path.join(
    #         hou.homeHoudiniDirectory(), 'Searcher', "output.json"
    #     )
    #     info = hou.ui.viewerStateInfo()
    #     sample = open(outputpath, 'w') 
    #     print(info, file = sample) 
    #     sample.close() 
    #     print(info)

    # ------------------------------------------------------ Settings Menu
    # SECTION Settings Menu ----------------------------------------------
    # ----------------------------------- buildsettingsmenu
    # NOTE buildsettingsmenu ------------------------------
    def buildsettingsmenu(self):
        self.ui.setWindowFlags(
            QtCore.Qt.Tool 
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.FramelessWindowHint
        )
        self.ui.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        if self.settingdata[util.SETTINGS_KEYS[8]]:
            self.ui.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.ui.setStyleSheet(style.SETTINGSMENU)

        self.settingslayout = self.ui.settingslayout
        if self.animatedsettings:
            self.anim.setContentLayout(self.settingslayout)
            self.anim.resize(
                self.uiwidth,
                self.uiheight
            )
        self.ui.resize(
            self.uiwidth,
            self.uiheight
        )

    # !SECTION Settings Menu

    # ----------------------------------------------------------------- UI
    # SECTION UI ---------------------------------------------------------
    # -------------------------------------------- UI Setup
    # NOTE UI Setup ---------------------------------------
    def uisetup(self):
        names = ["open", "save", "hotkey", "perference"]
        # self.completer = QtWidgets.QCompleter(names)
        self.completer = QtWidgets.QCompleter(names)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setModel(QtWidgets.QDirModel(self.completer))
        self.completer.setCompletionMode(self.completer.InlineCompletion)

        self.sui = searcher_ui.Ui_Searcher()
        self.sui.setupUi(self, self.animated)
        self.sui.mainlayout.addLayout(self.sui.gridLayout)
        self.setLayout(self.sui.mainlayout)

        # ---------------------------------- UI Connections
        # NOTE UI Connections -----------------------------
        self.helpButton = self.sui.helpButton

        # ------------------------------------- Result Tree
        # NOTE Result Tree --------------------------------
        self.searchresultstree = self.sui.searchresults_tree
        self.searchresultstree.itemActivated.connect(self.searchclick_cb)

        # -------------------------------------- Search Box
        # NOTE Search Box ---------------------------------
        self.searchbox = self.sui.searchbox_txt
        self.searchbox.textChanged.connect(self.textchange_cb)
        self.searchbox.customContextMenuRequested.connect(self.openmenu)
        self.searchbox.setPlaceholderText(" Begin typing to search..")
        self.searchbox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.searchbox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.searchbox.setClearButtonEnabled(True)
        self.searchbox.setCompleter(self.completer)

        # ----------------------------------- Search Filter
        # NOTE Search Filter ------------------------------
        self.searchfilter = self.sui.searchfilter_btn
        self.searchfilter.clicked.connect(self.searchfilter_cb)
        self.searchfilter.setFixedWidth(26)
        self.searchfilter.setFixedHeight(26)
        self.searchfilter.setProperty("flat", True)
        self.searchfilter.setIcon(util.SEARCH_ICON)
        self.searchfilter.setIconSize(QtCore.QSize(
            hou.ui.scaledSize(16),
            hou.ui.scaledSize(16)
        ))

        # ----------------------------------- Item Expander
        # NOTE Item Expander ------------------------------
        self.expander = self.sui.expander
        self.setexpandericon()
        self.expander.clicked.connect(self.expander_cb)
        expander_button_size = hou.ui.scaledSize(18)
        self.expander.setProperty("flat", True)
        self.expander.setIconSize(QtCore.QSize(
            expander_button_size,
            expander_button_size
        ))

        # -------------------------------------- Metric Pos
        # NOTE Metric Pos ---------------------------------
        self.metricpos = self.sui.metricpos
        self.setmetricicon()
        self.metricpos.clicked.connect(self.metricpos_cb)
        metricpos_button_size = hou.ui.scaledSize(16)
        self.metricpos.setProperty("flat", True)
        self.metricpos.setIconSize(QtCore.QSize(
            metricpos_button_size,
            metricpos_button_size
        ))
        self.metricpos.setVisible(self.settingdata[util.SETTINGS_KEYS[12]])

        # ---------------------------------- Context Toggle
        # NOTE Context Toggle -----------------------------
        self.contexttoggle = self.sui.contexttoggle
        self.contexttoggle.clicked[bool].connect(self.showctx_cb)
        self.contexttoggle.setCheckable(True)
        self.contexttoggle.setChecked(self.showctx)
        self.contexttoggle.setFixedWidth(20)
        self.contexttoggle.setFixedHeight(20)
        contexttoggle_button_size = hou.ui.scaledSize(16)
        self.contexttoggle.setProperty("flat", True)
        self.contexttoggle.setIconSize(QtCore.QSize(
            contexttoggle_button_size,
            contexttoggle_button_size
        ))
        self.setctxicon()
        self.contexttoggle.setStyleSheet(style.CONTEXTTOGGLE)

        # -------------------------------------- Pin Window
        # NOTE Pin Window ---------------------------------
        self.pinwindow = self.sui.pinwindow_btn
        self.setpinicon()
        self.pinwindow.clicked.connect(self.pinwindow_cb)
        pinwindow_button_size = hou.ui.scaledSize(16)
        self.pinwindow.setProperty("flat", True)
        self.pinwindow.setIconSize(QtCore.QSize(
            pinwindow_button_size,
            pinwindow_button_size
        ))

        # ----------------------------------- Settings Menu
        # NOTE Settings Menu ------------------------------
        self.opensettingstool = self.sui.opensettings_btn
        self.opensettingstool.setCheckable(True)
        self.opensettingstool.setChecked(False)
        self.opensettingstool.clicked.connect(self.opensettings_cb)
        opensettingstool_button_size = hou.ui.scaledSize(16)
        self.opensettingstool.setProperty("flat", True)
        self.opensettingstool.setIcon(util.SETTINGS_ICON)
        self.opensettingstool.setIconSize(QtCore.QSize(
            opensettingstool_button_size,
            opensettingstool_button_size
        ))

        # ---------------------------------------- Info Bar
        # NOTE Info Bar -----------------------------------
        self.infolbl = self.sui.info_lbl
        self.treetotal_lbl = self.sui.treetotal_lbl

        # ---------------------------------- Resize Handles
        # NOTE Resize Handles -----------------------------
        self.leftresize = self.sui.leftresize
        self.rightresize = self.sui.rightresize

        # ---------------------------------------- Tooltips
        # NOTE Tooltips -----------------------------------
        self.searchbox.setToolTip(la.TT_MW[self.searchbox.objectName()])
        self.contexttoggle.setToolTip(la.TT_MW[self.contexttoggle.objectName()])
        self.pinwindow.setToolTip(la.TT_MW[self.pinwindow.objectName()])
        self.searchfilter.setToolTip(la.TT_MW[self.searchfilter.objectName()])
        self.opensettingstool.setToolTip(la.TT_MW[self.opensettingstool.objectName()])
        self.searchresultstree.setToolTip(la.TT_MW[self.searchresultstree.objectName()])

        self.setupresulttree()
        self.searchbox.setFocus()
        self.searchbox.grabKeyboard()

    # ----------------------------------- Setup Result Tree
    # NOTE Setup Result Tree ------------------------------
    def setupresulttree(self):
        cols = 4
        self.searchresultstree.setColumnCount(cols)
        self.searchresultstree.setColumnWidth(0, 250)
        if self.isdebug and self.isdebug.level in {"ALL"}:
            self.searchresultstree.setColumnWidth(1, 350)
        else:
            self.searchresultstree.setColumnWidth(1, 450)
        self.searchresultstree.setColumnWidth(2, 100)
        self.searchresultstree.setColumnWidth(3, 150)
        self.searchresultstree.setColumnWidth(4, 150)
        self.searchresultstree.setHeaderLabels([
            "Label",
            "Description",
            "Assignments",
            "Symbol",
            "Context"
        ])
        self.searchresultstree.setColumnHidden(3, self.showctx)
        if not self.isdebug.level in {"ALL"}:
            self.searchresultstree.hideColumn(4)

        self.searchresultstree.header().setMinimumSectionSize(85)
        self.searchresultstree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.searchresultstree.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.searchresultstree.header().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.searchresultstree.header().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.searchresultstree.header().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.searchresultstree.setStyleSheet(style.gettreeviewstyle())

        # !SECTION UI

    # ---------------------------------------------------------- Functions
    # SECTION Functions --------------------------------------------------
    # ----------------------------------------- setinfotext
    # NOTE setinfotext ------------------------------------
    def setinfotext(self, t, d):
        text = style.gettooltipstyle(d)
        self.infolbl.setStyleSheet(style.INFOLABEL)
        self.infolbl.setText(text)
        self.fade_in(self.infolbl, t)
    # ----------------------------------------- count_chars
    # NOTE count_chars ------------------------------------
    def count_chars(self, txt):
        result = 0
        for char in txt:
            result += 1     # same as result = result + 1
        return result

    # --------------------------------------- Initial Setup
    # NOTE Initial Setup ----------------------------------
    def initialsetup(self):
        self.handler = get_dbhandler()
        if not self.handler:
            hou.session.DBHANDLER = datahandler.DataHandler(self.isdebug)
            self.handler = get_dbhandler()

        currentidx = hou.hotkeys.changeIndex()
        chindex = self.handler.getchangeindex()

        if len(chindex) == 0:
            chindex = int(currentidx)
            self.handler.updatechangeindex(chindex, True)
            self.handler.updatedataasync(self.isdebug)
            hou.ui.setStatusMessage(
                "Searcher database created",
                severity=hou.severityType.Message
            )
        else:
            chindex = int(chindex[0][0])

        if int(currentidx) != chindex:
            self.handler.updatedataasync(self.isdebug)
            self.handler.updatechangeindex(int(currentidx))

        return self.handler

    # --------------------------------------------- getnode
    # NOTE getnode ----------------------------------------
    def getnode(self):
        nodeSelect = hou.selectedNodes()
        for node in nodeSelect:
            getName = node.name()
            if self.isdebug and self.isdebug.level in {"ALL"}:
                print(getName)

    # ---------------------------------------------- getpane
    # NOTE getpane -----------------------------------------
    def getpane(self):
        try:
            return hou.ui.paneTabUnderCursor().type()
        except (AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(
                ("No context options to display: " + str(e)),
                severity=hou.severityType.Message
            )

    # !SECTION Functions

    # ---------------------------------------------------------- Callbacks
    # SECTION Callbacks --------------------------------------------------
    # ------------------------------------- searchfilter_cb
    # NOTE searchfilter_cb --------------------------------
    def searchfilter_cb(self):
        self.openmenu()

    # ------------------------------------- setexpandericon
    # NOTE setexpandericon --------------------------------
    def setexpandericon(self):
        if self.expanditems:
            self.expander.setIcon(util.COLLAPSE_ALL_ICON)
            self.expander.setToolTip(la.TT_MW['collapse_all'])
        else:
            self.expander.setIcon(util.EXPAND_ALL_ICON)
            self.expander.setToolTip(la.TT_MW['expand_all'])

    # ----------------------------------------- expander_cb
    # NOTE expander_cb ------------------------------------
    def expander_cb(self):
        if self.expanditems:
            self.searchresultstree.collapseAll()
        else:
            self.searchresultstree.expandAll()

        self.expanditems = not self.expanditems
        self.setexpandericon()
        self.settingdata[util.SETTINGS_KEYS[15]] = self.expanditems
        settings_data.savesettings(self.settingdata)

    # --------------------------------------- setmetricicon
    # NOTE setmetricicon ----------------------------------
    def setmetricicon(self):
        if self.isdebug.mainwindow:
            self.metricpos.setIcon(util.UP_ICON)
            self.metricpos.setToolTip(la.TT_MW['metricposself'])

        else:
            self.metricpos.setIcon(util.DOWN_ICON)
            self.metricpos.setToolTip(la.TT_MW['metricposmain'])

    # ---------------------------------------- metricpos_cb
    # NOTE metricpos_cb -----------------------------------
    def metricpos_cb(self):
        self.isdebug.mainwindow = not self.isdebug.mainwindow
        self.settingdata[util.SETTINGS_KEYS[13]] = self.isdebug.mainwindow
        settings_data.savesettings(self.settingdata)
        self.setmetricicon()

    # ------------------------------------------ setctxicon
    # NOTE setctxicon -------------------------------------
    def setctxicon(self):
        if self.showctx:
            self.contexttoggle.setIcon(util.COLLAPSE_ICON)
        else:
            self.contexttoggle.setIcon(util.EXPAND_ICON)
        self.searchresultstree.setColumnHidden(3, self.showctx)

    # ------------------------------------------ showctx_cb
    # NOTE showctx_cb -------------------------------------
    def showctx_cb(self, pressed):
        self.showctx = True if pressed else False
        self.settingdata[util.SETTINGS_KEYS[7]] = self.showctx
        settings_data.savesettings(self.settingdata)
        self.setctxicon()

    # ---------------------------------------- pinwindow_cb
    # NOTE pinwindow_cb -----------------------------------
    def pinwindow_cb(self):
        self.windowispin = not self.windowispin
        self.settingdata[util.SETTINGS_KEYS[5]] = self.windowispin
        settings_data.savesettings(self.settingdata)
        self.setpinicon()

    # ------------------------------------------ setpinicon
    # NOTE setpinicon -------------------------------------
    def setpinicon(self):
        if self.windowispin:
            self.pinwindow.setIcon(util.PIN_IN_ICON)
        else:
            self.pinwindow.setIcon(util.PIN_OUT_ICON)

    # ------------------------------------- opensettings_cb
    # NOTE opensettings_cb --------------------------------
    def opensettings_cb(self, doopen):
        self.ui.isopened = self.ui.isVisible()

        if self.animatedsettings:
            self.open_settings(doopen)
        elif self.ui.isopened:
            self.open_settings(False)
        else:
            self.open_settings(True)

    # --------------------------------------- open_settings
    # NOTE open_settings ----------------------------------
    def open_settings(self, doopen):
        if doopen:
            pos = self.opensettingstool.mapToGlobal(
                    QtCore.QPoint(-self.ui.width() + 31, 28))
            self.ui.setGeometry(
                pos.x(),
                pos.y(),
                self.ui.width(),
                self.ui.height()
            )
            self.ui.updatecurrentvalues()
            self.ui.show()
            self.ui.activateWindow()
            self.ui.setFocus()
            if self.animatedsettings:
                self.anim.start_animation(True)
        else:
            if self.ui.performcheck:
                if self.ui.checkforchanges():
                    self.ui.savecheck()
            if self.animatedsettings and not self.ui.waitforclose:
                self.ui.closewindows()
                _ = self.anim.start_animation(False)
            else:
                self.ui.isopened = True
                self.ui.closewindows()
                self.ui.close()
                if self.ui.waitforclose:
                    self.close()

    def anim_complete(self):
        if self.ui.isopened:
            self.ui.close()
            self.ui.isopened = False
            self.opensettingstool.setChecked(False)

    # ------------------------------------- globalkeysearch
    # NOTE globalkeysearch --------------------------------
    def globalkeysearch(self):
        self.ctxsearch = True
        ctx = []
        ctx.append("h")
        results = self.handler.searchctx(ctx)
        self.searchtablepopulate(results)
        self.ctxsearch = False

    def processdesktop(self, ran, result):
        print("---- %s" % ran)
        print(result)
        print("Window Name: %s | Whats This?: %s | Type: %s" % (result.windowTitle(), result.whatsThis(), result.accessibleName()))
        if isinstance(result, Iterable):
            print("Item amount: %d" % len(result))
            try:
                for i in result:
                    print(i.windowTitle())
                    if ran == "hou.ui.paneTabs()":
                        print("Name : %s | Item: %s | Type: %s" % (i.name(), i, i.type))     
                    elif ran == "util.widgets_at(mainwin, pos)":
                        print("Window Name: %s | Item: %s | Type: %s" % (i.windowTitle(), i.type, i.type))
                    else:
                        print(i)

            except(AttributeError, TypeError) as e:
                if hou.isUIAvailable():
                    hou.ui.setStatusMessage(
                        (("Error in %s : " % ran) + str(e)), severity=hou.severityType.Warning)
                    pass
                else:
                    print(("Error in %s : " % ran) + str(e))
                    pass

    # ------------------------------------------------------ Context Terms
    # SECTION Context Terms ----------------------------------------------
    # ----------------------------------------- ctxsearcher
    # NOTE ctxsearcher ------------------------------------
    def ctxsearcher(self, ctx=None):
        self.starttime = ptime.time()
        results = None
        ctxresult = []

        # ---------------------------- None or :c
        # NOTE None or :c -----------------------
        if ctx is None or ctx == ":c":
            self.ctxsearch = True
            skipelse = False

            pos = QtGui.QCursor.pos()
            if self.isdebug and self.isdebug.level in {"ALL"}:
                print("Position: X:%d Y: %d" % (pos.x(), pos.y()))
            
            mainwin = QtWidgets.QApplication
            undermouse = util.widgets_at(mainwin, pos)

            for w in undermouse:
                if w.windowTitle() in util.PANES:
                    if self.isdebug and self.isdebug.level in {"ALL"}:
                        print(util.PANETYPES[w.windowTitle()])
                    ctxresult = util.PANETYPES[w.windowTitle()]
                    results = self.handler.searchctx(ctxresult)
                    skipelse = True
                    break
                else:
                    pass

            if not skipelse:
                try:
                    if self.isdebug and self.isdebug.level in {"ALL"}:
                        print(self.getpane())
                    ctxresult = util.PANETYPES[self.getpane()]
                    results = self.handler.searchctx(ctxresult)
                except(AttributeError, TypeError) as e:
                    if hou.isUIAvailable():
                        hou.ui.setStatusMessage(
                            (str(e)), severity=hou.severityType.Warning)
                    else:
                        print(str(e))

            try:
                selected_node = hou.selectedNodes()
                if selected_node:
                    print("---Params - Selected")
                    print(selected_node[0].parmTuples())
                    for i in selected_node[0].parmTuples():
                        print(i)
            except(AttributeError, TypeError) as e:
                if hou.isUIAvailable():
                    hou.ui.setStatusMessage(
                        (str(e)), severity=hou.severityType.Warning)
                else:
                    print(str(e))

        # ------------------------------------ :v
        # NOTE :v -------------------------------
        elif ctx == ":v":
            self.ctxsearch = True
            ctxresult.append("h.pane")
            results = self.handler.searchctx(ctxresult)

        # ------------------------------------ :g
        # NOTE :g -------------------------------
        elif ctx == ":g":
            self.ctxsearch = True
            ctxresult.append("h")
            results = self.handler.searchctx(ctxresult)
        # !SECTION Context Terms

        self.searchtablepopulate(results)
        self.ctxsearch = False
        self.searchbox.clearFocus()
        self.searchresultstree.setFocus()
        self.searchresultstree.setCurrentItem(
            self.searchresultstree.topLevelItem(0).child(0)
        )


    # --------------------------------------- textchange_cb
    # NOTE textchange_cb ----------------------------------
    def textchange_cb(self, text):
        # print(self.holdinfobanner)
        # self.timerprofile = hou.perfMon.startProfile("Search_Timer")  # ANCHOR hou perf timer ---------------- hou perf timer
        # self.searchevent = hou.perfMon.startEvent("Start _Timer")     # ANCHOR hou perf timer ---------------- hou perf timer

        self.starttime = ptime.time() # -----------------------------   # ANCHOR Search Timer Start
        if len(text) > 0 and not self.holdinfobanner:
            self.setinfotext(200, self.searchresultstree.toolTip())
        if text in util.CTXSHOTCUTS:
            self.ctxsearcher(text)
        elif len(text) > 1 and text not in util.CTXSHOTCUTS:
            self.searching = True
            allowed = re.compile(r'[^a-zA-Z ]+')
            text = re.sub(allowed, '', text)
            str = text.split()
            searchstring = ['%s*' % (x,) for x in str]
            regtime = ptime.time()    # -----------------------------   # ANCHOR Regex Timer Start
            self.regtimetotal = ((regtime - self.starttime) * 1000.0)
            if searchstring:
                if self.isdebug and self.isdebug.level in {"ALL"}:
                    print(searchstring)
                txt, timer = self.handler.searchtext(
                    ' '.join(searchstring),
                    self.isdebug,
                    self.settingdata[util.SETTINGS_KEYS[9]]
                )
                self.hotkeystime = timer
                self.searchtablepopulate(txt)
        else:
            self.holdinfobanner = False
            self.searching = False
            self.treetotal_lbl.setText("")
            self.searchresultstree.clear()
            self.setinfotext(200, self.searchbox.toolTip())

    # -------------------------------------- searchclick_cb
    # NOTE searchclick_cb ---------------------------------
    def searchclick_cb(self, item, column):
        hk = item.text(2)
        self.tmpsymbol = item.text(3)

        if hk == "":
            self.chindex = hou.hotkeys.changeIndex()
            result = self.createtemphotkey(self.tmpsymbol)
            if result is True:
                self.chindex = hou.hotkeys.changeIndex()
                hk = hou.hotkeys.assignments(self.tmpsymbol)
                self.processkey(hk, True)
        else:
            hk = hou.hotkeys.assignments(self.tmpsymbol)
            self.processkey(hk)
            self.tmpsymbol = None
        return

    # ------------------------------------------ getContext
    # NOTE getContext -------------------------------------
    def getContext(self, ctx):
        """Return Houdini context string."""
        try:
            hou_context = ctx.pwd().childTypeCategory().name()
        except:
            return None

        print("Hou Context: ", hou_context)
        return util.CONTEXTTYPE[hou_context]

    # !SECTION Callbacks

    # -------------------------------------------------- Hotkey Processing
    # SECTION Hotkey Processing ------------------------------------------
    # ------------------------------------- savelastkey
    # NOTE savelastkey --------------------------------
    def savelastkey(self, symbol, key):
        self.settingdata[util.SETTINGS_KEYS[11]] = (str(symbol) + " " + str(key[0]))
        settings_data.savesettings(self.settingdata)

    # -------------------------------------- processkey
    # NOTE processkey ---------------------------------
    def processkey(self, key, tmphk=False):
        if tmphk:
            self.savelastkey(self.tmpsymbol, key)

        key = key[0].split('+')

        skey = None
        ikey = None
        key = keyconversion(key)
        modifiers = util.MODIFIERS
        mod_flag = QtCore.Qt.KeyboardModifiers()
        for i in range(len(key)):
            if str(key[i]) in modifiers:
                mod_flag = mod_flag | util.MODIFIERS[str(key[i])]
            else:
                skey = key[i]
                ikey = util.KEY_DICT[str(key[i])]

        keypress = QtGui.QKeyEvent(
            QtGui.QKeyEvent.KeyPress,  # Keypress event identifier
            ikey,                      # Qt key identifier
            mod_flag,                  # Qt key modifier
            skey                       # String of Qt key identifier
        )

        hou.ui.mainQtWindow().setFocus()
        try:
            hd.executeDeferred(self.app.sendEvent, hou.ui.mainQtWindow(), keypress)
            self.close()

        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(
                ("Could not trigger hotkey event: " + str(e)),
                severity=hou.severityType.Warning
            )
            print("Could not trigger hotkey event: " + str(e))

    # ---------------------------------- setKeysChanged
    # NOTE setKeysChanged -----------------------------
    def setKeysChanged(self, changed):
        if self.keys_changed and not changed:
            if not hou.hotkeys.saveOverrides():
                print("ERROR: Couldn't save hotkey override file.")
        self.keys_changed = changed
        self.chindex = hou.hotkeys.changeIndex()
        self.handler.updatechangeindex(self.chindex)

    # -------------------------------- createtemphotkey
    # NOTE createtemphotkey ---------------------------
    def createtemphotkey(self, symbol):
        hkeys = util.gethotkeys()
        hou.hotkeys._createBackupTables()
        for i in range(len(hkeys)):
            result = hou.hotkeys.findConflicts(symbol, hkeys[i])
            if not result:
                assignresult = hou.hotkeys.addAssignment(symbol, hkeys[i])
                if assignresult:
                    self.tmpkey = hkeys[i]
                    break
                else:
                    pass
            else:
                pass

        self.keys_changed = True
        self.setKeysChanged(False)
        return assignresult

    # -------------------------------- removetemphotkey
    # NOTE removetemphotkey ---------------------------
    def removetemphotkey(self, symbol, tmpkey):
        hou.hotkeys._restoreBackupTables()
        hou.hotkeys.revertToDefaults(symbol, True)
        self.keys_changed = True
        self.setKeysChanged(False)
        hkcheck = hou.hotkeys.assignments(str(symbol))
        if len(hkcheck) is 0:
            self.settingdata[util.SETTINGS_KEYS[11]] = ""
            settings_data.savesettings(self.settingdata)

    # !SECTION Hotkey Processing

    # ------------------------------------------------------------- Search
    # SECTION Search -----------------------------------------------------
    # --------------------------------------------------- Search Menu
    # SECTION Search Menu -------------------------------------------
    # -------------------------------------------- openmenu
    # NOTE openmenu ---------------------------------------
    def openmenu(self):
        self.menuopened = True
        self.searchmenu = QtWidgets.QMenu()
        self.searchmenu.setProperty('flat', True)
        self.searchmenu.setStyleSheet(style.MENUSTYLE)
        self.searchmenu.setWindowFlags(
            self.searchmenu.windowFlags() |
            QtCore.Qt.NoDropShadowWindowHint | 
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.globalprefix = self.searchmenu.addAction("Global items")
        self.contextprefix = self.searchmenu.addAction("Context items")
        self.viewprefix = self.searchmenu.addAction("View items")

        self.globalprefix.setToolTip(
            "View application-wide actions")

        self.contextprefix.setToolTip(
            "Shows possible actions for the view in which the mouse was in when the window was opened")

        self.viewprefix.setToolTip(
            "Shows the available view panes (ex. Scene View, Render View, Composit View, etc")

        self.searchmenu.hovered.connect(self.handlemenuhovered)

        self.action = self.searchmenu.exec_(
            self.searchbox.mapToGlobal(QtCore.QPoint(0, 29)))
        if self.action == self.globalprefix:
            self.searchbox.setText(":g")
        if self.action == self.contextprefix:
            self.searchbox.setText(":c")
        if self.action == self.viewprefix:
            self.searchbox.setText(":v")

        self.searchmenu.installEventFilter(self)

    # ----------------------------------- handlemenuhovered
    # NOTE handlemenuhovered ------------------------------
    def handlemenuhovered(self, action):
        self.setinfotext(200, action.toolTip())

    # !SECTION Search Menu

    # ---------------------------------- createcontextitems
    # TODO createcontextitems -----------------------------
    def createcontextitems(self, result):
        result[2] = (QtWidgets.QTreeWidgetItem(self.searchresultstree, [result[hc][0], result[hc][1]]))

    # -------------------------------------------- openmenu
    # TODO openmenu ---------------------------------------
    def appendcontextlist(self, list):
        if list[4] not in self.context_list:
            return self.context_list.append(list[4])

    # --------------------------------- searchtablepopulate
    # NOTE searchtablepopulate ----------------------------
    def searchtablepopulate(self, data):
        if len(data) > 0:
            # tabletimer = hou.perfMon.startEvent("Table_Populate") ------- # ANCHOR hou perf timer
            self.goalnum = 7
            self.treecatnum = 0
            self.treeitemsnum = 0
            self.searchresultstree.clear()

            self.hotkeys[:] = []
            self.context_list[:] = []
            self.hcontext_tli.clear()

            # list(map(self.appendcontextlist, data))
            for i in range(len(data)):
                if data[i][4] not in self.context_list:
                    self.context_list.append(data[i][4])
                    # if self.ctxsearch:
                    # else:
                        # self.context_list.append(data[i][4])

            result, hctimer = self.handler.gethcontextod(self.context_list)
            self.hcontexttime = hctimer
            treebuildtimer = ptime.time() # ------------------------------ # ANCHOR Tree builder Start
            # TODO Test Map ---------
            for hc in range(len(result)):
                self.hcontext_tli[result[hc][2]] = (QtWidgets.QTreeWidgetItem(
                    self.searchresultstree, [
                        result[hc][0],
                        result[hc][1]
                    ]
                ))
                if self.expanditems:
                    self.searchresultstree.expandItem(self.hcontext_tli[result[hc][2]])
                self.treecatnum += 1

            base_keys = self.hcontext_tli.keys()
            for i in range(len(data)):
                for j in range(len(base_keys)):
                    if base_keys[j] == data[i][4]:
                        if self.isdebug and self.isdebug.level in {"ALL"}:
                            self.hotkeys.append(QtWidgets.QTreeWidgetItem(
                                self.hcontext_tli[base_keys[j]], [
                                    data[i][0],
                                    data[i][1],
                                    data[i][2],
                                    data[i][3],
                                    data[i][4]
                                ]
                            ))
                            self.treeitemsnum += 1
                        else:
                            self.hotkeys.append(QtWidgets.QTreeWidgetItem(
                                self.hcontext_tli[base_keys[j]], [
                                    data[i][0],
                                    data[i][1],
                                    data[i][2],
                                    data[i][3]
                                ]
                            ))
                            self.treeitemsnum += 1

            # tabletimer.stop() # ANCHOR hou perf timer ---------------------------------------- hou perf timer
            # self.searchevent.stop() # ANCHOR hou perf timer ---------------------------------------- hou perf timer
            # self.timerprofile.stop() # ANCHOR hou perf timer ---------------------------------------- hou perf timer

            treebuildtimerend = ptime.time() # --------------------------- # ANCHOR Tree Builder End
            treebuildtotal = ((treebuildtimerend - treebuildtimer) * 1000.0)

            if not self.holdinfobanner:
                try:
                    self.infolabeldelayasync()
                except(AttributeError, TypeError) as e:
                    if hou.isUIAvailable():
                        hou.ui.setStatusMessage(str(e), severity=hou.severityType.Message)
                    else:
                        print(e)

            self.styleresultstotalasync(self.treecatnum, self.treeitemsnum)
            self.endtime = ptime.time() # -----------------------------         # ANCHOR Search Timer End
            totaltime = ((self.endtime - self.starttime) * 1000.0)
            if self.isdebug.performance:
                outdata = [self.regtimetotal, self.hcontexttime, self.hotkeystime, treebuildtotal, totaltime]
                self.styletimersasync(outdata)

    # !SECTION Search

    # ------------------------------------------------------ Async Methods
    # SECTION Async Methods ----------------------------------------------
    # ------------------------------------------------- worker1
    # SECTION Workers : NOTE worker1 --------------------------
    def worker1(self, d1):
        hd.executeInMainThreadWithResult(self.styletimers, d1)

    # ------------------------------------------------- worker2
    # NOTE worker2 --------------------------------------------
    def worker2(self, d1, d2):
        hd.executeInMainThreadWithResult(self.styletotals, d1, d2)

    # ------------------------------------------------- worker3
    # NOTE worker3 --------------------------------------------
    def worker3(self):
        hd.executeInMainThreadWithResult(self.infolabeldelay)

    # !SECTION Workers

    # ---------------------------------------- styletimersasync
    # SECTION styletimers : NOTE styletimersasync -----------------------------------
    def styletimersasync(self, d1):
        thread = threading.Thread(target=self.worker1, args=(d1,))
        thread.daemon = True
        thread.start()

    # --------------------------------------------- styletimers
    # NOTE styletimers ----------------------------------------
    def styletimers(self, d1):
        if self.isdebug.mainwindow:
            perftime = style.returntimers(d1)
            if hou.isUIAvailable():
                hou.ui.setStatusMessage(perftime, severity=hou.severityType.Message)
            else:
                print(perftime)
        else:
            perftime = style.styletimers(d1)
            self.infolbl.setStyleSheet(style.INFOLABEL)
            self.infolbl.setText(perftime)
    # !SECTION styletimers

    # ---------------------------------- styleresultstotalasync
    # SECTION styleresultstotal : NOTE styleresultstotalasync -
    def styleresultstotalasync(self, d1, d2):
        thread = threading.Thread(target=self.worker2, args=(d1, d2))
        thread.daemon = True
        thread.start()

    # --------------------------------------------- styletotals
    # NOTE styletotals ----------------------------------------
    def styletotals(self, d1, d2):
        result = style.styleresulttotal(d1, d2)
        self.treetotal_lbl.setText(result)
    # !SECTION styleresultstotal

    # --------------------------------------infolabeldelayasync
    # SECTION  infolabeldelay : NOTE infolabeldelayasync ------
    def infolabeldelayasync(self):
        if self.threadtimer:
            self.threadtimer.cancel()
        self.holdinfobanner = True
        self.infolbl.setStyleSheet(style.INFOLABEL)
        self.threadtimer = threading.Timer(5, self.infolabeldelay)
        self.threadtimer.start()

    # ------------------------------------------ infolabeldelay
    # NOTE infolabeldelay -------------------------------------
    def infolabeldelay(self):
        try:
            self.infolbl.setText(style.gettooltipstyle(self.searchresultstree.toolTip()))
            hd.executeDeferred(self.fade_in, self.infolbl, 200)
            self.holdinfobanner = False
        except(AttributeError, TypeError) as e:
            if hou.isUIAvailable():
                hou.ui.setStatusMessage(e, severity=hou.severityType.Message)
            else:
                print(e)
        else:
            pass
        # print(self.timerprofile.stats()) # ANCHOR hou perf timer ---------------------------------------- hou perf timer
    # !SECTION infolabeldelay

    # --------------------------------------------- createtimer
    # NOTE createtimer ----------------------------------------
    def createtimer(self, time, func, p):
        if self.tiptimer:
            if self.tiptimer.isAlive():
                self.tiptimer.cancel()

        self.tiptimer = threading.Timer(time,(func(p)))
        self.tiptimer.start()

    # !SECTION Async Methods

    # --------------------------------------------------------- Animations
    # SECTION Animations -------------------------------------------------
    # ----------------------------------------- fade_in
    # NOTE fade_in ------------------------------------
    def fade_in(self, target, duration):
        self.effect = QtWidgets.QGraphicsOpacityEffect()
        self.tar = target
        self.tar.setGraphicsEffect(self.effect)
        self.an = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.an.setDuration(duration)
        self.an.setStartValue(0)
        self.an.setEndValue(1)
        self.an.start()

    # ---------------------------------------- fade_out
    # NOTE fade_out -----------------------------------
    def fade_out(self, target, duration):
        self.effect = QtWidgets.QGraphicsOpacityEffect()
        self.tar = target
        self.tar.setGraphicsEffect(self.effect)
        self.an = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.an.setDuration(duration)
        self.an.setStartValue(1)
        self.an.setEndValue(0)
        self.an.start()

    # !SECTION

    # ------------------------------------------------------------- Events
    # SECTION Events  ----------------------------------------------------
    # ------------------------------------- addeventfilters
    # NOTE addeventfilters --------------------------------
    def addeventfilters(self):
        self.installEventFilter(self)
        self.expander.installEventFilter(self)
        self.metricpos.installEventFilter(self)
        self.searchbox.installEventFilter(self)
        self.pinwindow.installEventFilter(self)
        self.helpButton.installEventFilter(self)
        self.leftresize.installEventFilter(self)
        self.rightresize.installEventFilter(self)
        self.searchfilter.installEventFilter(self)
        self.contexttoggle.installEventFilter(self)
        self.opensettingstool.installEventFilter(self)
        self.searchresultstree.installEventFilter(self)

    # ---------------------------------- removeeventfilters
    # NOTE removeeventfilters -----------------------------
    def removeeventfilters(self):
        self.removeEventFilter(self)
        self.expander.removeEventFilter(self)
        self.metricpos.removeEventFilter(self)
        self.searchbox.removeEventFilter(self)
        self.pinwindow.removeEventFilter(self)
        self.helpButton.removeEventFilter(self)
        self.leftresize.removeEventFilter(self)
        self.rightresize.removeEventFilter(self)
        self.searchfilter.removeEventFilter(self)
        self.contexttoggle.removeEventFilter(self)
        self.opensettingstool.removeEventFilter(self)
        self.searchresultstree.removeEventFilter(self)

    # --------------------------------------- cancelthreads
    # NOTE cancelthreads ----------------------------------
    def cancelthreads(self):
        if self.threadtimer:
            self.threadtimer.cancel()
        if self.tiptimer:
            self.tiptimer.cancel()

    # ------------------------------ createdelayedinfolabel
    # NOTE createdelayedinfolabel -------------------------
    def createdelayedinfolabel(self, tiptext):
        self.infolbl.setText(style.gettooltipstyle(tiptext))
        self.fade_in(self.infolbl, 200)

    # ---------------------------------------- checktooltip
    # NOTE checktooltip -----------------------------------
    def checktooltip(self, obj, hasleft=False):
        if hasleft:
            if self.searching and self.infolbl.text() != self.searchresultstree.toolTip():
                self.setinfotext(700, self.searchresultstree.toolTip())
            elif not self.searching and self.infolbl.text() != self.searchbox.toolTip():
                self.setinfotext(700, self.searchbox.toolTip())
        else:
            if obj == self.searchresultstree or obj == self.searchbox:
                if self.searching and self.infolbl.text() != self.searchresultstree.toolTip():
                    self.setinfotext(200, self.searchresultstree.toolTip())
                elif not self.searching and self.infolbl.text() != self.searchbox.toolTip():
                    self.setinfotext(200, self.searchbox.toolTip())
            elif self.infolbl.text() != obj.toolTip():
                self.setinfotext(200, obj.toolTip())


    # ---------------------------------------- addshortcuts
    # NOTE addshortcuts -----------------------------------
    def addshortcuts(self):
        toggleexpand_shct = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+W"), self)
        toggleexpand_shct.activated.connect(self.expander_cb)
        
        opensettings_shct = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
        opensettings_shct.activated.connect(self.opensettingstool.click)

        getpanes_shct = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+B"), self)
        getpanes_shct.activated.connect(self.getwidgets)
    
    # -------------------------------------------------------- Event Types
    # SECTION Event Types ------------------------------------------------
    # def createEventHandler(self, uievent, pending_actions):
    #     if isinstance(uievent, MouseEvent):
    def onFocusWindowChanged(self, focusWindow):
        print("Focus Changed!")
        if focusWindow is None:
            print("None!")

    def onMouseEvent(self, kwargs):
        ui_event = kwargs["ui_event"]
        print(ui_event)
        reason = ui_event.reason()
        device = ui_event.device()
        if device.isLeftButton():
            print("Clicked")

        if reason == hou.uiEventReason.Picked:
            print("LMB click")

        elif reason == hou.uiEventReason.Start:
            print("LMB was pressed down")

        elif reason == hou.uiEventReason.Active:
            print("Mouse dragged with LMB down")

        elif reason == hou.uiEventReason.Changed:
            print("LMB was released")



    def eventFilter(self, obj, event):
        event_type = event.type()

        # ------------------------------------------- Mouse
        # NOTE Mouse --------------------------------------
        # --------------------------------- Enter
        # NOTE Enter ----------------------------
        if event_type == QtCore.QEvent.Enter:
            if obj == self:
                self.mouseout = False
            if obj == self.leftresize or obj == self.rightresize:
                self.overhandle = True
                style.styleresizehandle(obj, True)
            self.checktooltip(obj)

        # --------------------------------- Leave
        # NOTE Leave ----------------------------
        if event_type == QtCore.QEvent.Leave:
            if obj == self:
                self.mouseout = True
            if obj == self.leftresize or obj == self.rightresize:
                self.overhandle = False
                style.styleresizehandle(obj, False)
            self.checktooltip(obj, True)

        # ------------------------------- ToolTip
        # NOTE ToolTip --------------------------
        if event_type == QtCore.QEvent.ToolTip:
            return True

        # ---------------------- MouseButtonPress
        # NOTE MouseButtonPress -----------------
        if event_type == QtCore.QEvent.MouseButtonPress:
            if obj == self.leftresize or obj == self.rightresize:
                self.resizing = True
                self.previous_pos = event.globalPos()

            if obj == self.searchbox:
                return QtCore.QObject.eventFilter(self, obj, event)
            else:
                if obj == self:
                    self.activateWindow()
                self.previous_pos = event.globalPos()
                if obj == self.parentwindow:
                    self.close()

        # -------------------- MouseButtonRelease
        # NOTE MouseButtonRelease ---------------
        if event_type == QtCore.QEvent.MouseButtonRelease:
            if obj == self.leftresize or obj == self.rightresize:
                self.resizing = False

            if self._drag_active:
                self._drag_active = False

        # ----------------------------- MouseMove
        # NOTE MouseMove ------------------------
        if event_type == QtCore.QEvent.MouseMove:
            if obj == self:
                delta = event.globalPos() - self.previous_pos
                self.move(self.x() + delta.x(), self.y() + delta.y())

                if self.ui.isVisible():
                    self.ui.move(self.ui.x() + delta.x(), self.ui.y() + delta.y())
                    self.ui.movesubwindows(delta)

                self.previous_pos = event.globalPos()
                self._drag_active = True

            if self.resizing:
                if obj == self.rightresize:
                    delta = event.globalPos() - self.previous_pos

                    if self.ui.isVisible():
                        self.ui.move(self.ui.x() + delta.x(), self.ui.y())
                        self.ui.movesubwindows(delta, True)
                        self.previous_pos = event.globalPos()
            else:
                return QtCore.QObject.eventFilter(self, obj, event)

        # ---------------------------- MouseHover
        # NOTE MouseHover -----------------------
        if event_type == QtCore.QEvent.HoverMove:
            pass

        # ---------------------------------------- Keypress
        # NOTE Keypress -----------------------------------
        if event_type == QtCore.QEvent.KeyPress:
            # ------------------------------- TAB
            # NOTE TAB --------------------------
            if event.key() == QtCore.Qt.Key_Tab:
                if self.searching:
                    self.searchbox.releaseKeyboard()
                    self.searchbox.clearFocus()
                    self.searchresultstree.setFocus()
                    self.searchresultstree.setCurrentItem(
                        self.searchresultstree.topLevelItem(0).child(0))
                    return True
                else:
                    if self.menuopened:
                        self.searchmenu.setFocus()
                    else:
                        self.searchbox.setText(":c")
                        self.ctxsearcher()
                        self.searchresultstree.setFocus()
                        self.searchresultstree.setCurrentItem(
                            self.searchresultstree.topLevelItem(0).child(0))
                    return True

            # ------------------------------- ESC
            # NOTE ESC --------------------------
            if event.key() == QtCore.Qt.Key_Escape:
                if self.ui.isVisible():
                    self.ui.closeroutine()
                    return True
                else:
                    if self.menuopened:
                        if self.searchmenu.isVisible():
                            self.searchmenu.setVisible(False)
                            return True
                        else:
                            self.menuopened = False
                    else:
                        self.close()

            # ------------------------------- ":"
            # NOTE ":" --------------------------
            if event.key() == QtCore.Qt.Key_Colon:
                if self.searchbox.text() == "":
                    self.searchbox.releaseKeyboard()
                    self.searchbox.clearFocus()
                    self.openmenu()
                    return True

        # ------------------------------------------ Window
        # NOTE Window -------------------------------------
        # ------------------------------ Activate
        # NOTE Activate -------------------------
        if event_type == QtCore.QEvent.WindowActivate:
            if obj == self:
                self.searchbox.grabKeyboard()

        # ---------------------------- Deactivate
        # NOTE Deactivate -----------------------
        if event_type == QtCore.QEvent.WindowDeactivate:
            if self.ui.isVisible():
                self.searchbox.releaseKeyboard()
                return True
            if self.windowispin:
                return QtCore.QObject.eventFilter(self, obj, event)
            if self.mouseout:
                self.close()

        # ------------------------------- FocusIn
        # NOTE FocusIn --------------------------
        if event_type == QtCore.QEvent.FocusIn:
            if obj == self:
                pass

        # ------------------------------ FocusOut
        # NOTE FocusOut -------------------------
        if event_type == QtCore.QEvent.FocusOut:
            if obj == self:
                pass

        # ------------------------------------------- Close
        # NOTE Close --------------------------------------
        if event_type == QtCore.QEvent.Close:
            self.cancelthreads()
            try:
                if util.bc(self.settingdata[util.SETTINGS_KEYS[2]]):
                    self.windowsettings.setValue("geometry", self.saveGeometry())
            except (AttributeError, TypeError) as e:
                if hou.isUIAvailable():
                    hou.ui.setStatusMessage(("Could not save window dimensions: " + str(e)), severity=hou.severityType.Warning)
                else:
                    print("Could not save window dimensions: " + str(e))

            if self.menuopened:
                self.searchmenu.setVisible(False)

            if self.tmpsymbol is not None:
                hd.executeDeferred(
                    self.removetemphotkey,
                    self.tmpsymbol,
                    self.tmpkey)

            self.searchbox.releaseKeyboard()
            try:
                self.parentwindow.activateWindow()
                self.parentwindow.setFocus()
                self.setParent(None)
                self.deleteLater()
            except:
                self.parentwindow.activateWindow()
                self.setParent(None)
                self.deleteLater()

        return QtCore.QObject.eventFilter(self, obj, event)

    # !SECTION Event Types
    # !SECTION Events

# -------------------------------------------------------------- Setup
# SECTION Setup ------------------------------------------------------
# ----------------------------------- Center Window
# NOTE Center Window ------------------------------
def center():
    return parent_widget.mapToGlobal(
        QtCore.QPoint(
            parent_widget.rect().center().x(),
            parent_widget.rect().center().y()
        )
    )

# ----------------------------------- Create Window
# NOTE Create Window ------------------------------
def CreateSearcherPanel(kwargs, searcher_window=None):
    kwargs = kwargs

    settings = get_settings()
    windowsettings = QtCore.QSettings("instance.id", "Searcher")

    animated = True
    searcher_window = Searcher(kwargs, settings, windowsettings, searcher_window, animated)
    searcher_window.addeventfilters()
    searcher_window.setStyleSheet(style.MAINWINDOW)
    searcher_window.setAttribute(QtCore.Qt.WA_StyledBackground, True)
    searcher_window.setWindowFlags(
        QtCore.Qt.Tool
        | QtCore.Qt.CustomizeWindowHint
        | QtCore.Qt.FramelessWindowHint
        | QtCore.Qt.WindowStaysOnTopHint
        # | QtCore.Qt.X11BypassWindowManagerHint
    )

    if util.bc(settings[util.SETTINGS_KEYS[2]]) and windowsettings.value("geometry") is not None:
        searcher_window.restoreGeometry(windowsettings.value("geometry"))
    else:
        searcher_window.resize(
            int(settings[util.SETTINGS_KEYS[3]][0]),
            int(settings[util.SETTINGS_KEYS[3]][1]),
        )
        spos = center()
        searcher_window.setGeometry(
            spos.x() - (searcher_window.width() / 2),
            spos.y() - (searcher_window.height() / 2),
            searcher_window.width(),
            searcher_window.height(),
        )
    searcher_window.searchbox.setFocus()
    searcher_window.setWindowTitle('Searcher')
    if not searcher_window.isVisible():
        searcher_window.show()
        searcher_window.activateWindow()

    # searcher_window.activateWindow()

# !SECTION Setup


__package__ = "searcher"
