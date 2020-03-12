# region Imports
from __future__ import print_function
from __future__ import absolute_import
import weakref

from searcher import util
from searcher import ptime
from searcher import animator
from searcher import database
from searcher import HelpButton
from searcher import datahandler
from searcher import searcher_data
from searcher import searcher_settings
from searcher import language_en as la

import hou
import platform
import os
import sys
import re
from string import ascii_letters
import hdefereval as hd
hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    hver = int(ver[ver.rindex('.')+1:])
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets

reload(searcher_settings)
reload(searcher_data)
reload(datahandler)
reload(HelpButton)
reload(animator)
reload(database)
reload(ptime)
reload(util)
reload(la)
# endregion

# --------------------------------------------------------------------  App Info
__package__ = "Searcher"
__version__ = "0.1b"
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"
# endregion

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
searcher_window = QtWidgets.QMainWindow()
# endregion

# --------------------------------------------------------------------  Class Functions


def keyconversion(key):
    for i in range(len(key)):
        if key[i] in util.KEYCONVERSIONS:
            key[i] = util.KEYCONVERSIONS[key[i]]
    return key
# endregion

# --------------------------------------------------------------------  Searcher Class


class Searcher(QtWidgets.QWidget):
    """instance.id Searcher for Houdini"""
    # SECTION Class init

    def __init__(self, kwargs, settings, windowsettings):
        super(Searcher, self).__init__(hou.qt.mainWindow())
        self._drag_active = False
        self.animationDuration = 200
        self.uiwidth = int(520)
        self.uiheight = int(300)

        # Setting vars
        kwargs = kwargs
        self.settingdata = settings
        self.windowsettings = windowsettings
        self.isdebug = util.Dbug(
            util.bc(self.settingdata[util.SETTINGS_KEYS[4]]), 
            str(self.settingdata[util.SETTINGS_KEYS[10]])
        )
        self.menuopened = False
        self.windowispin = util.bc(self.settingdata[util.SETTINGS_KEYS[5]])
        self.showctx = util.bc(self.settingdata[util.SETTINGS_KEYS[7]])
        self.originalsize = self.settingdata[util.SETTINGS_KEYS[3]]
        self.animatedsettings = util.bc(
            self.settingdata[util.SETTINGS_KEYS[8]])
        self.mainlayout = QtWidgets.QVBoxLayout()
        self.settingslayout = QtWidgets.QVBoxLayout()
        self.app = QtWidgets.QApplication.instance()

        # UI Vars
        self.handler, self.tmpkey = self.initialsetup()
        self.ui = searcher_settings.SearcherSettings(
            self.handler, 
            self.tmpkey, 
            self
        )
        if self.animatedsettings:
            self.anim = animator.Animator(self.ui, self.anim_complete)

        # Functional Vars
        self.endtime = 0
        self.lastused = {}
        self.starttime = 0
        self.treecatnum = 0
        self.hotkeystime = 0
        self.hcontexttime = 0
        self.treeitemsnum = 0
        self.tmpsymbol = None
        self.searching = False
        self.ctxsearch = False
        self.showglobal = True
        self.previous_pos = None
        self.searchprefix = False
        self.keys_changed = False
        self.searchdescription = False
        self.searchcurrentcontext = False

        # Functionals
        hou.hotkeys._createBackupTables()
        self.uisetup()

        # Event System Initialization
        self.installEventFilter(self)
        self.searchbox.installEventFilter(self)
        self.pinwindow.installEventFilter(self)
        self.helpButton.installEventFilter(self)
        self.searchfilter.installEventFilter(self)
        self.contexttoggle.installEventFilter(self)
        self.opensettingstool.installEventFilter(self)
        self.searchresultstree.installEventFilter(self)

        # ---------------------------------- Build Settings
        # NOTE Build Settings -----------------------------
        self.buildsettingsmenu()

    # !SECTION

    # ------------------------------------------------------ Settings Menu
    # SECTION Settings Menu ----------------------------------------------
    # ----------------------------------- buildsettingsmenu
    # NOTE buildsettingsmenu ------------------------------
    def buildsettingsmenu(self):
        self.ui.setWindowFlags(
            QtCore.Qt.Tool |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.ui.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.ui.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.ui.setStyleSheet("QWidget { background: rgb(58, 58, 58); }"
                              "QWidget#SearcherSettings { border: 2px solid rgb(35, 35, 35); } ")

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


    # !SECTION

    # ----------------------------------------------------------------- UI
    # SECTION UI ---------------------------------------------------------
    # ------------------------------------- setupresulttree
    # NOTE setupresulttree --------------------------------
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
        self.searchresultstree.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.searchresultstree.header().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.searchresultstree.header().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.searchresultstree.header().setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)
        self.searchresultstree.header().setSectionResizeMode(
            4, QtWidgets.QHeaderView.ResizeToContents)
        self.searchresultstree.setStyleSheet("""QHeaderView::section{
                                             color: rgb(200, 200, 200);
                                             resize:both;
                                             overflow:auto;
                                             padding: 4px;
                                             height:20px;
                                             border: 0px solid rgb(150, 150, 150);
                                             border-bottom: 1px solid rgb(150, 150, 150);
                                             border-left:0px solid rgb(50, 50, 50);
                                             border-right:1px solid rgb(60, 60, 60);
                                             background: rgb(36, 36, 36);
                                             }""")

    # -------------------------------------- Build Settings
    # NOTE Build Settings ---------------------------------
    def uisetup(self):
        names = ["open", "save", "hotkey", "perference"]
        self.completer = QtWidgets.QCompleter(names)

        # Layout
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)

        self.titlerow = QtWidgets.QHBoxLayout()
        self.titlerow.setSpacing(5)

        self.titlespacer1 = QtWidgets.QSpacerItem(
            8, 0,
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Minimum
        )

        self.searcherlbl = QtWidgets.QLabel("Searcher")
        font = QtGui.QFont()
        font.setPointSize(15)
        self.searcherlbl.setFont(font)
        self.searcherlbl.setAlignment(QtCore.Qt.AlignCenter)

        self.titlespacer2 = QtWidgets.QSpacerItem(
            40, 0,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )

        self.contexttoggle = QtWidgets.QPushButton()
        self.helpButton = HelpButton.HelpButton("main", la.ln_helppanel, 16)
        self.pinwindow_btn = QtWidgets.QToolButton()
        self.opensettings_btn = QtWidgets.QToolButton()

        self.titlespacer3 = QtWidgets.QSpacerItem(
            8, 0,
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Minimum
        )

        # ----------------------------------- Search Filter
        # NOTE Search Filter ------------------------------
        self.searchrow = QtWidgets.QHBoxLayout()
        self.searchrow.setSpacing(0)
        self.frame = QtWidgets.QFrame()
        searchframe_details = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred
        )
        searchframe_details.setHorizontalStretch(2)
        searchframe_details.setVerticalStretch(0)
        searchframe_details.setHeightForWidth(
            self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(searchframe_details)
        self.frame.setMinimumSize(QtCore.QSize(0, 20))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.searchfilter_btn = QtWidgets.QToolButton(self.frame)
        self.searchfilter_btn.setGeometry(QtCore.QRect(0, 0, 26, 20))
        self.searchfilter_btn.setBaseSize(QtCore.QSize(16, 16))
        self.searchfilter_btn.setStyleSheet(
            u"background-color: rgb(19, 19, 19);")
        self.searchfilter_btn.setArrowType(QtCore.Qt.NoArrow)

        # -------------------------------------- Search Box
        # NOTE Search Box ---------------------------------
        self.searchbox_txt = QtWidgets.QLineEdit()
        searchbox_details = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        searchbox_details.setHorizontalStretch(99)
        searchbox_details.setVerticalStretch(0)
        searchbox_details.setHeightForWidth(
            self.searchbox_txt.sizePolicy().hasHeightForWidth())
        self.searchbox_txt.setSizePolicy(searchbox_details)
        self.searchbox_txt.setMinimumSize(QtCore.QSize(50, 0))
        self.searchbox_txt.setMouseTracking(False)
        self.searchbox_txt.setStyleSheet(u"background-color: rgb(19, 19, 19);")
        self.searchbox_txt.setFrame(False)

        # ------------------------------------ Results Tree
        # NOTE Results Tree -------------------------------
        self.searchresults_tree = QtWidgets.QTreeWidget()
        __qtreewidgetitem = QtWidgets.QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1")
        resultstree_header = QtGui.QFont()
        resultstree_header.setPointSize(9)
        __qtreewidgetitem.setFont(0, resultstree_header)
        self.searchresults_tree.setHeaderItem(__qtreewidgetitem)
        resultstree_details = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding
        )
        resultstree_details.setHorizontalStretch(0)
        resultstree_details.setVerticalStretch(0)
        # resultstree_details.setHeightForWidth(
        #     self.searchresults_tree.sizePolicy().hasHeightForWidth())
        self.searchresults_tree.setSizePolicy(resultstree_details)
        resultstree_font = QtGui.QFont()
        resultstree_font.setPointSize(9)
        self.searchresults_tree.setFont(resultstree_font)
        self.searchresults_tree.setMouseTracking(False)
        self.searchresults_tree.setFocusPolicy(QtCore.Qt.NoFocus)
        self.searchresults_tree.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.searchresults_tree.setLineWidth(0)
        self.searchresults_tree.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.searchresults_tree.setAlternatingRowColors(True)
        self.searchresults_tree.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.searchresults_tree.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)

        # -------------------------------------- Info Panel
        # NOTE Info Panel ---------------------------------
        self.infobar = QtWidgets.QHBoxLayout()
        self.infobar.setObjectName("infobar")
        self.infobargrid = QtWidgets.QGridLayout()
        self.infobargrid.setObjectName("infobargrid")
        self.info_lbl = QtWidgets.QLabel()
        self.infolbl_font = QtGui.QFont()
        self.infolbl_font.setPointSize(8)
        self.infolbl_font.setBold(False)
        self.infolbl_font.setWeight(50)
        self.info_lbl.setFont(self.infolbl_font)
        self.info_lbl.setStyleSheet(u"background-color: rgb(26, 26, 26);")
        self.info_lbl.setMargin(2)
        self.info_lbl.setIndent(5)
        self.overlay = overlayLabel(self.info_lbl)
        self.overlay.setFont(self.infolbl_font)
        self.overlay.setStyleSheet(u"background-color: rgb(26, 26, 26);")
        self.overlay.setMargin(2)
        self.overlay.setIndent(5)
        self.treetotal_lbl = QtWidgets.QLabel()
        treetotal_size = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        treetotal_size.setHorizontalStretch(0)
        treetotal_size.setVerticalStretch(0)
        treetotal_size.setHeightForWidth(self.treetotal_lbl.sizePolicy().hasHeightForWidth())
        self.treetotal_lbl.setSizePolicy(treetotal_size)
        self.treetotal_lbl.setMinimumSize(QtCore.QSize(150, 0))
        self.treetotal_lbl.setMaximumSize(QtCore.QSize(150, 16777215))
        self.treetotal_lbl.setObjectName("treetotal_lbl")
        self.treetotal_lbl.setStyleSheet(u"background-color: rgb(26, 26, 26);")
        self.treetotal_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        
        # --------------------------- Layout Implementation
        # NOTE Layout Implementation ----------------------
        self.titlerow.addItem(self.titlespacer1)
        self.titlerow.addWidget(self.searcherlbl)
        self.titlerow.addItem(self.titlespacer2)
        self.titlerow.addWidget(self.contexttoggle)
        self.titlerow.addWidget(self.helpButton)
        self.titlerow.addWidget(self.pinwindow_btn)
        self.titlerow.addWidget(self.opensettings_btn)
        self.titlerow.addItem(self.titlespacer3)
        self.verticalLayout.addLayout(self.titlerow)
        self.searchrow.addWidget(self.frame)
        self.searchrow.addWidget(self.searchbox_txt)
        self.verticalLayout.addLayout(self.searchrow)
        self.verticalLayout.addWidget(self.searchresults_tree)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        
        self.infobargrid.addWidget(self.overlay, 1, 0, 1, 1)
        self.infobargrid.addWidget(self.info_lbl, 1, 0, 1, 1)
        self.infobargrid.addWidget(self.treetotal_lbl, 1, 1, 1, 1)

        self.infobar.addLayout(self.infobargrid)
        self.gridLayout.addLayout(self.infobar, 3, 0, 1, 1)

        # NOTE Layout to functionality connection ---------
        self.searchfilter = self.searchfilter_btn
        self.pinwindow = self.pinwindow_btn
        self.opensettingstool = self.opensettings_btn
        self.searchresultstree = self.searchresults_tree
        self.searchbox = self.searchbox_txt
        self.infolbl = self.info_lbl

        # ---------------------------- Settings and details
        # NOTE Settings and details -----------------------
        self.searchbox.setPlaceholderText(" Begin typing to search..")
        self.searchbox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.searchbox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.searchbox.setClearButtonEnabled(True)

        self.searchfilter.clicked.connect(self.searchfilter_cb)
        searchfilter_button_size = hou.ui.scaledSize(12)
        self.searchfilter.setProperty("flat", True)
        self.searchfilter.setIcon(util.SEARCH_ICON)
        self.searchfilter.setIconSize(QtCore.QSize(
            searchfilter_button_size,
            searchfilter_button_size
        ))

        self.setctxicon()
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
        self.contexttoggle.clicked[bool].connect(self.showctx_cb)
        self.contexttoggle.setStyleSheet("QPushButton { width: 8px; border: none; }"
                                         "QPushButton:checked { width: 8px; border: none;}")

        self.pinwindow.clicked.connect(self.pinwindow_cb)
        self.setpinicon()
        pinwindow_button_size = hou.ui.scaledSize(16)
        self.pinwindow.setProperty("flat", True)
        self.pinwindow.setIconSize(QtCore.QSize(
            pinwindow_button_size,
            pinwindow_button_size
        ))

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

        self.searchbox.textChanged.connect(self.textchange_cb)
        self.searchbox.customContextMenuRequested.connect(self.openmenu)
        self.searchresultstree.itemActivated.connect(self.searchclick_cb)

        self.mainlayout.setAlignment(QtCore.Qt.AlignBottom)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.mainlayout.setGeometry(QtCore.QRect(0, 0, 1400, 1200))

        self.mainlayout.addLayout(self.gridLayout)
        self.setLayout(self.mainlayout)

        self.searchbox.setToolTip(la.ln_searchbox)
        self.contexttoggle.setToolTip(la.ln_contexttoggle)
        self.pinwindow.setToolTip(la.ln_pinwindow)
        self.searchfilter.setToolTip(la.ln_searchfilter)
        self.opensettingstool.setToolTip(la.ln_opensettingstool)
        self.searchresultstree.setToolTip(la.ln_searchresultstree)

        self.setupresulttree()
        self.searchbox.setFocus()
        self.searchbox.grabKeyboard()

        # !SECTION

    # ---------------------------------------------------------- Functions
    # SECTION Functions --------------------------------------------------
    # ----------------------------------- count_chars Setup
    # NOTE count_chars ------------------------------------
    def count_chars(self, txt):
        result = 0
        for char in txt:
            result += 1     # same as result = result + 1
        return result

    # --------------------------------------- Initial Setup
    # NOTE Initial Setup ----------------------------------
    def initialsetup(self):
        self.handler = datahandler.DataHandler(self.isdebug)
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

        tmpkey = self.handler.getdefaulthotkey()
        self.tmpkey = tmpkey[0][0]
        return self.handler, self.tmpkey

    # ------------------------------------------- Panel/Node
    # NOTE Panel/Node -------------------------------------
    def getnode(self):
        nodeSelect = hou.selectedNodes()
        for node in nodeSelect:
            getName = node.name()
            print(getName)

    def getpane(self):
        try:
            return hou.ui.paneTabUnderCursor().type()
        except (AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(
                ("No context options to display" + str(e)),
                severity=hou.severityType.Message
            )
    # !SECTION

    # ---------------------------------------------------------- Callbacks
    # SECTION Callbacks --------------------------------------------------
    # ------------------------------------- searchfilter_cb
    # NOTE searchfilter_cb --------------------------------
    def searchfilter_cb(self):
        self.openmenu()

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
        searcher_data.savesettings(self.settingdata)
        self.setctxicon()

    # ---------------------------------------- pinwindow_cb
    # NOTE pinwindow_cb -----------------------------------
    def pinwindow_cb(self):
        self.windowispin = not self.windowispin
        self.settingdata[util.SETTINGS_KEYS[5]] = self.windowispin
        searcher_data.savesettings(self.settingdata)
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
                QtCore.QPoint(-self.ui.width() + 31, 26))
            self.ui.setGeometry(
                pos.x(),
                pos.y(),
                self.ui.width(),
                self.ui.height()
            )
            self.ui.show()
            self.ui.activateWindow()
            self.ui.setFocus()
            if self.animatedsettings:
                self.anim.start_animation(True)
        else:
            if self.animatedsettings:
                _ = self.anim.start_animation(False)
            else:
                self.ui.isopened = True
                self.ui.close()

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

    # ----------------------------------------- ctxsearcher
    # NOTE ctxsearcher ------------------------------------
    def ctxsearcher(self, ctx=None):
        results = None
        ctxresult = []

        if ctx is None:
            self.ctxsearch = True
            if self.isdebug:
                print(self.getpane())
            ctxresult = util.PANETYPES[self.getpane()]
            results = self.handler.searchctx(ctxresult)

        elif ctx == ":v":
            self.ctxsearch = True
            ctxresult.append("h.pane")
            results = self.handler.searchctx(ctxresult)

        elif ctx == ":c":
            self.ctxsearch = True
            ctxresult = util.PANETYPES[self.getpane()]
            if self.isdebug:
                print(self.getpane())
            results = self.handler.searchctx(ctxresult)

        elif ctx == ":g":
            self.ctxsearch = True
            ctxresult.append("h")
            results = self.handler.searchctx(ctxresult)

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
        self.starttime = ptime.time()
        if len(text) > 0:
            self.infolbl.setText(self.searchresultstree.toolTip())
        if text in util.CTXSHOTCUTS:
            self.ctxsearcher(text)
        elif len(text) > 1 and text not in util.CTXSHOTCUTS:
            self.searching = True
            allowed = re.compile(r'[^a-zA-Z ]+')
            text = re.sub(allowed, '', text)
            str = text.split()
            searchstring = ['%s*' % (x,) for x in str]
            txt, timer = self.handler.searchtext(
                ' '.join(searchstring), 
                self.isdebug, 
                self.settingdata[util.SETTINGS_KEYS[9]]
            )
            self.hotkeystime = timer
            self.searchtablepopulate(txt)
        else:
            self.searching = False
            self.treetotal_lbl.setText("")
            self.searchresultstree.clear()
            self.infolbl.setText(
                "Begin typing to search or click magnifying glass icon to display options")
    
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
    # !SECTION

    # ------------------------------------------------------------- Search
    # SECTION Search -----------------------------------------------------
    # -------------------------------------------- openmenu
    # NOTE openmenu ---------------------------------------
    def openmenu(self):
        self.menuopened = True
        self.searchmenu = QtWidgets.QMenu()
        self.searchmenu.setProperty('flat', True)
        self.searchmenu.setStyleSheet(util.MENUSTYLE)
        self.searchmenu.setWindowFlags(
            self.searchmenu.windowFlags() |
            QtCore.Qt.NoDropShadowWindowHint
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
            self.searchbox.mapToGlobal(QtCore.QPoint(0, 20)))
        if self.action == self.globalprefix:
            self.searchbox.setText(":g")
        if self.action == self.contextprefix:
            self.searchbox.setText(":c")
        if self.action == self.viewprefix:
            self.searchbox.setText(":v")

        self.searchmenu.installEventFilter(self)

    def handlemenuhovered(self, action):
        self.infolbl.setText(action.toolTip())

    def getContext(self, ctx):
        """Return Houdini context string."""
        try:
            hou_context = ctx.pwd().childTypeCategory().name()
        except:
            return None

        print ("Hou Context: ", hou_context)
        return util.CONTEXTTYPE[hou_context]

    # endregion

    # --------------------------------- searchtablepopulate
    # NOTE searchtablepopulate ----------------------------
    def searchtablepopulate(self, data):
        if len(data) > 0:
            goalnum = 15
            self.treecatnum = 0
            self.treeitemsnum = 0
            self.searchresultstree.clear()
            hotkeys = []
            context_list = []
            hcontext_tli = {}

            for i in range(len(data)):
                if data[i][4] not in context_list:
                    if self.ctxsearch:
                        context_list.append(data[i][4])
                    else:
                        context_list.append(data[i][4])

            result, hctimer = self.handler.gethcontextod(context_list)
            self.hcontexttime = hctimer

            treebuildtimer = ptime.time()
            for hc in range(len(result)):
                hcontext_tli[result[hc][2]] = (QtWidgets.QTreeWidgetItem(
                    self.searchresultstree, [
                        result[hc][0],
                        result[hc][1]
                    ]
                ))
                self.searchresultstree.expandItem(hcontext_tli[result[hc][2]])
                self.treecatnum += 1

            base_keys = hcontext_tli.keys()
            for i in range(len(data)):
                for j in range(len(base_keys)):
                    if base_keys[j] in data[i][4]:
                        if self.isdebug and self.isdebug.level in {"ALL"}:
                            hotkeys.append(QtWidgets.QTreeWidgetItem(
                                hcontext_tli[base_keys[j]], [
                                    data[i][0],
                                    data[i][1],
                                    data[i][2],
                                    data[i][3],
                                    data[i][4]
                                ]
                            ))
                            self.treeitemsnum += 1
                        else:
                            hotkeys.append(QtWidgets.QTreeWidgetItem(
                                hcontext_tli[base_keys[j]], [
                                    data[i][0],
                                    data[i][1],
                                    data[i][2],
                                    data[i][3]
                                ]
                            ))
                            self.treeitemsnum += 1
            treebuildtimerend = ptime.time()
            treebuildtotal = ((treebuildtimerend - treebuildtimer) * 1000.0)
            
            # Display the number of added results by iteration
            catval = ("%d : Contexts | " % self.treecatnum)
            itmval = ("%d : Results " % self.treeitemsnum)
            catval = catval.rjust(goalnum - self.count_chars(str(self.treecatnum)), " ")
            itmval = itmval.rjust((goalnum + 2) - self.count_chars(str(self.treeitemsnum)), " ")
            self.treetotal_lbl.setText((catval + itmval))

            # Performance monitors to check how long different aspects take to run ----------
            self.endtime = ptime.time()
            totaltime = ((self.endtime - self.starttime) * 1000.0)
            if self.isdebug and self.isdebug.level in {"TIMER", "ALL"}:
                if hou.isUIAvailable():
                    hou.ui.setStatusMessage(
                        (('Context Search %0.4f ms | ' % self.hcontexttime) 
                        + ('Hotkey Search %0.4f ms | ' % self.hotkeystime) 
                        + ('Tree build %0.4f ms | ' % treebuildtotal) 
                        + ('Total : %0.4f ms' % (totaltime))) , severity=hou.severityType.Message)
                else:
                    print('Search took %0.4f ms' % self.hotkeystime)

    # !SECTION

    # -------------------------------------------------- Hotkey Processing
    # SECTION Hotkey Processing ------------------------------------------
    # -------------------------------------- processkey
    # NOTE processkey ---------------------------------
    def processkey(self, key, tmphk=False):
        hk = key
        if tmphk:
            lastkey = (str(self.tmpsymbol) + " " + str(hk[0]))
            self.handler.updatelasthk(lastkey)

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
        hou.hotkeys._createBackupTables()
        result = hou.hotkeys.addAssignment(symbol, self.tmpkey)
        self.keys_changed = True
        self.setKeysChanged(False)
        return result

    # -------------------------------- removetemphotkey
    # NOTE removetemphotkey ---------------------------
    def removetemphotkey(self, symbol, tmpkey):
        hou.hotkeys._restoreBackupTables()
        hou.hotkeys.revertToDefaults(symbol, True)
        self.keys_changed = True
        self.setKeysChanged(False)

    # !SECTION

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
    # SECTION Events -----------------------------------------------------
    def checktooltip(self, obj, hasleft=False):
        if hasleft:
            # self.fade_out(self.infolbl, 200)
            if self.searching and self.infolbl.text() != self.searchresultstree.toolTip():
                self.infolbl.setText(self.searchresultstree.toolTip())
                self.fade_in(self.infolbl, 200)
            elif not self.searching and self.infolbl.text() != self.searchbox.toolTip():
                self.infolbl.setText(self.searchbox.toolTip())
                self.fade_in(self.infolbl, 200)
        else:
            if obj == self.searchresultstree or obj == self.searchbox:
                if self.searching and self.infolbl.text() != self.searchresultstree.toolTip():
                    self.infolbl.setText(self.searchresultstree.toolTip())
                    self.fade_in(self.infolbl, 200)
                elif not self.searching and self.infolbl.text() != self.searchbox.toolTip():
                    self.infolbl.setText(self.searchbox.toolTip())
                    self.fade_in(self.infolbl, 200)
            elif self.infolbl.text() != obj.toolTip():
                self.infolbl.setText(obj.toolTip())
                self.fade_in(self.infolbl, 200)

    def eventFilter(self, obj, event):
        # ------------------------------------------- Mouse
        # NOTE Mouse --------------------------------------
        if event.type() == QtCore.QEvent.Enter:
            self.checktooltip(obj)
        if event.type() == QtCore.QEvent.Leave:
            self.checktooltip(obj, True)
        if event.type() == QtCore.QEvent.ToolTip:
            return True

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if obj == self.searchbox:
                return QtCore.QObject.eventFilter(self, obj, event)
            else:
                self.previous_pos = event.globalPos()
                return QtCore.QObject.eventFilter(self, obj, event)

        if event.type() == QtCore.QEvent.MouseMove:
            if obj == self:
                delta = event.globalPos() - self.previous_pos
                self.move(self.x() + delta.x(), self.y() + delta.y())
                if self.ui.isVisible():
                    self.ui.move(self.ui.x() + delta.x(),
                                 self.ui.y() + delta.y())
                self.previous_pos = event.globalPos()
                self._drag_active = True
            else:
                return QtCore.QObject.eventFilter(self, obj, event)

        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if self._drag_active:
                self._drag_active = False

        # ---------------------------------------- Keypress
        # NOTE Keypress -----------------------------------
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Tab:
                if self.searching:
                    self.searchbox.releaseKeyboard()
                    self.searchbox.clearFocus()
                    self.searchresultstree.setFocus()
                    self.searchresultstree.setCurrentItem(
                        self.searchresultstree.topLevelItem(0).child(0))
                    return True
                else:
                    # self.searchbox.releaseKeyboard()
                    # self.searchbox.clearFocus()
                    if self.menuopened:
                        self.searchmenu.setFocus()
                    else:
                        self.searchbox.setText(":c")
                        self.ctxsearcher()
                        self.searchresultstree.setFocus()
                        self.searchresultstree.setCurrentItem(
                            self.searchresultstree.topLevelItem(0).child(0))
                    return True
            if event.key() == QtCore.Qt.Key_Escape:
                if self.ui.isVisible():
                    pass
                else:
                    if self.menuopened:
                        if self.searchmenu.isVisible():
                            self.searchmenu.setVisible(False)
                            return QtCore.QObject.eventFilter(self, obj, event)
                        else:
                            self.menuopened = False
                    else:
                        self.close()
            if event.key() == QtCore.Qt.Key_Colon:
                if self.searchbox.text() == "":
                    self.searchbox.releaseKeyboard()
                    self.searchbox.clearFocus()
                    self.openmenu()
                    return True

        # ------------------------------------------ Window
        # NOTE Window -------------------------------------
        if event.type() == QtCore.QEvent.WindowActivate:
            self.searchbox.grabKeyboard()
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            if self.ui.isVisible():
                self.searchbox.releaseKeyboard()
                return QtCore.QObject.eventFilter(self, obj, event)
            if self.windowispin:
                return QtCore.QObject.eventFilter(self, obj, event)
            else:
                self.close()
        elif event.type() == QtCore.QEvent.FocusIn:
            if obj == self.window:
                self.searchbox.grabKeyboard()
        elif event.type() == QtCore.QEvent.FocusOut:
            pass

        # ------------------------------------------- Close
        # NOTE Close --------------------------------------
        if event.type() == QtCore.QEvent.Close:
            try:
                if util.bc(self.settingdata[util.SETTINGS_KEYS[2]]):
                    self.windowsettings.setValue("geometry", self.saveGeometry())
            except (AttributeError, TypeError) as e:
                if hou.isUIAvailable():
                    hou.ui.setStatusMessage(
                        ("Could not save window dimensions: " + str(e)), severity=hou.severityType.Warning)
                else:
                    print("Could not save window dimensions: " + str(e))

            if self.menuopened:
                self.searchmenu.setVisible(False)

            if self.tmpsymbol is not None:
                hd.executeDeferred(
                    self.removetemphotkey,
                    self.tmpsymbol,
                    self.tmpkey
                )
            self.searchbox.releaseKeyboard()
            try:
                self.parent().setFocus()
                self.setParent(None)
                self.deleteLater()
            except:
                self.setParent(None)
                self.deleteLater()
        return QtCore.QObject.eventFilter(self, obj, event)
    # !SECTION
    # endregion
# endregion


class overlayLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(overlayLabel, self).__init__(parent)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

# ------------------------------------------------------------------------ Setup Functions


def center():
    return parent_widget.mapToGlobal(
        QtCore.QPoint(
            parent_widget.rect().center().x(),
            parent_widget.rect().center().y()
        )
    )


def CreateSearcherPanel(kwargs, searcher_window=None):
    kwargs = kwargs
    try:
        searcher_window.close()
        searcher_window.deleteLater()
    except:
        pass

    settings = searcher_data.loadsettings()
    windowsettings = QtCore.QSettings("instance.id", "Searcher")

    searcher_window = Searcher(kwargs, settings, windowsettings)
    searcher_window.setWindowFlags(
        QtCore.Qt.Tool |
        QtCore.Qt.CustomizeWindowHint |
        QtCore.Qt.WindowStaysOnTopHint
    )

    # util.SETTINGS_KEYS[2] = savewindowsize
    # util.SETTINGS_KEYS[3] = windowsize
    if util.bc(settings[util.SETTINGS_KEYS[2]]) and windowsettings.value("geometry") is not None:
        searcher_window.restoreGeometry(windowsettings.value("geometry"))
    else:
        searcher_window.resize(
            int(settings[util.SETTINGS_KEYS[3]][0]),
            int(settings[util.SETTINGS_KEYS[3]][1])
        )
        pos = center()
        searcher_window.setGeometry(
            pos.x() - (searcher_window.width() / 2),
            pos.y() - (searcher_window.height() / 2),
            searcher_window.width(),
            searcher_window.height()
        )
    searcher_window.searchbox.setFocus()
    searcher_window.setWindowTitle('Searcher')
    searcher_window.show()
    searcher_window.activateWindow()
# endregion
