# region Imports
from __future__ import print_function
from __future__ import absolute_import
import weakref

from searcher import util
from searcher import database
from searcher import datahandler
from searcher import searcher_ui
from searcher import searcher_data
from searcher import searcher_settings

from pyautogui import press, typewrite, hotkey
import hou
from husdui.common import error_print, debug_print
import toolutils
import drivertoolutils
import platform
import objecttoolutils
import os
import sys
import hdefereval as hd
import stateutils
hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    hver = int(ver[ver.rindex('.')+1:])
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets
    if int(hver) >= 391:
        from hutil.Qt import _QtUiTools
    elif int(hver) < 391:
        from hutil.Qt import QtUiTools

reload(searcher_settings)
reload(searcher_data)
reload(searcher_ui)
reload(datahandler)
reload(database)
reload(util)
# endregion

# region -------------------------------------------------------------  App Info
__package__ = "Searcher"
__version__ = "0.1b"
__author__ = "instance.id"
__copyright__ = "2020 All rights reserved. See LICENSE for more details."
__status__ = "Prototype"
# endregion

# region -------------------------------------------------------------  Variables / Constants
kwargs = {}
settings = {}
hasran = False
isdebug = False
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

# region -------------------------------------------------------------  Class Functions


def keyconversion(key):
    for i in range(len(key)):
        if key[i] in util.KEYCONVERSIONS:
            key[i] = util.KEYCONVERSIONS[key[i]]
    return key
# endregion

# region -------------------------------------------------------------  Searcher Class


class Searcher(QtWidgets.QWidget):
    """instance.id Searcher for Houdini"""

    def __init__(self, kwargs, settings, windowsettings):
        super(Searcher, self).__init__(hou.qt.mainWindow())
        mainui = searcher_ui.Ui_Searcher()
        mainui.setupUi(self)
        mainui.retranslateUi(self)

        self._drag_active = False

        # Setting vars
        kwargs = kwargs
        self.settingdata = settings
        self.windowsettings = windowsettings
        self.isdebug = util.bc(self.settingdata[util.SETTINGS_KEYS[4]])
        self.menuopened = False
        self.windowispin = util.bc(self.settingdata[util.SETTINGS_KEYS[5]])
        self.originalsize = self.settingdata[util.SETTINGS_KEYS[3]]

        # if hver >= 391:
        self.app = QtWidgets.QApplication.instance()

        # UI Vars
        self.handler, self.tmpkey = self.initialsetup()
        self.ui = searcher_settings.SearcherSettings(self.handler, self.tmpkey)

        # Functional Vars
        self.lastused = {}
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
        self.uisetup(mainui)

        # Event System Initialization
        self.installEventFilter(self)
        self.searchbox.installEventFilter(self)
        self.pinwindow.installEventFilter(self)
        self.searchfilter.installEventFilter(self)
        self.opensettingstool.installEventFilter(self)
        self.searchresultstree.installEventFilter(self)

    # region ------------------------------------------------------------- Settings
    def open_settings(self):
        self.ui.setWindowTitle('Searcher - Settings')
        self.ui.show()
        self.ui.setFocus()
    # endregion

    # region ------------------------------------------------------------- UI
    def setupContext(self):
        cols = 4
        self.searchresultstree.setColumnCount(cols)
        self.searchresultstree.setColumnWidth(0, 250)
        if self.isdebug:
            self.searchresultstree.setColumnWidth(1, 350)
        else:
            self.searchresultstree.setColumnWidth(1, 450)
        self.searchresultstree.setColumnWidth(2, 100)
        self.searchresultstree.setColumnWidth(3, 150)
        if self.isdebug:
            self.searchresultstree.setColumnWidth(4, 150)
            self.searchresultstree.setHeaderLabels([
                "Label",
                "Description",
                "Assignments",
                "Symbol",
                "Context"
            ])
        else:
            self.searchresultstree.setHeaderLabels([
                "Label",
                "Description",
                "Assignments",
                "Symbol"
            ])

    def uisetup(self, mainui):
        self.main_widget = QtWidgets.QWidget(self)

        # Load UI File
        loader = None
        if int(hver) >= 391:
            loader = _QtUiTools.QUiLoader()
        else:
            loader = QtUiTools.QUiLoader()

        # mainui = loader.load(script_path + "/searcher_ui.py")
        # mainui = loader.load(script_path + "/searcher_ui.py")

        names = ["open", "save", "hotkey", "perference"]
        self.completer = QtWidgets.QCompleter(names)

        # Get UI Elements
        # self.searchfilter = mainui.findChild(
        #     QtWidgets.QToolButton,
        #     "searchfilter_btn"
        # )

        # self.searchfilter = mainui(
        #     QtWidgets.QToolButton,
        #     "searchfilter_btn"
        # )

        # self.pinwindow = mainui.findChild(
        #     QtWidgets.QToolButton,
        #     "pinwindow_btn"
        # )
        # self.opensettingstool = mainui.findChild(
        #     QtWidgets.QToolButton,
        #     "opensettings_btn"
        # )
        # self.searchresultstree = mainui.findChild(
        #     QtWidgets.QTreeWidget,
        #     "searchresults_tree"
        # )
        # self.searchbox = mainui.findChild(
        #     QtWidgets.QLineEdit,
        #     "searchbox_txt"
        # )
        # self.infolbl = mainui.findChild(
        #     QtWidgets.QLabel,
        #     "info_lbl"
        # )
        #

        self.searchfilter = mainui.searchfilter_btn
        self.pinwindow = mainui.pinwindow_btn
        self.opensettingstool = mainui.opensettings_btn
        self.searchresultstree = mainui.searchresults_tree
        self.searchbox = mainui.searchbox_txt
        self.infolbl = mainui.info_lbl

        self.searchbox.setPlaceholderText(" Search..")
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

        self.pinwindow.clicked.connect(self.pinwindow_cb)
        self.setpinicon()
        pinwindow_button_size = hou.ui.scaledSize(16)
        self.pinwindow.setProperty("flat", True)
        self.pinwindow.setIconSize(QtCore.QSize(
            pinwindow_button_size,
            pinwindow_button_size
        ))

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

        # Layout
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.setAlignment(QtCore.Qt.AlignBottom)
        mainlayout.setContentsMargins(0, 0, 0, 0)
        mainlayout.setGeometry(QtCore.QRect(0, 0, 1400, 1200))

        mainlayout.addWidget(HelpButton("main"))
        mainlayout.addWidget(self.searchfilter)
        mainlayout.addWidget(self.pinwindow)
        mainlayout.addWidget(self.opensettingstool)
        mainlayout.addWidget(self.searchresultstree)
        mainlayout.addWidget(self.searchbox)
        mainlayout.addWidget(self.infolbl)
        self.setLayout(mainlayout)

        self.searchbox.setToolTip(
            'Begin typing to search or click magnifying glass icon to display options')
        self.pinwindow.setToolTip(
            'Pin the search window to keep it from closing automatically when losing focus')
        self.searchfilter.setToolTip(
            'Select a predefined filter')
        self.opensettingstool.setToolTip(
            'General application settings')
        self.searchresultstree.setToolTip(
            'Double click an action to attempt to perform it. Some actions only work in specific contexts')

        self.setupContext()
        self.searchbox.setFocus()
        self.searchbox.grabKeyboard()

        # endregion

    # region ------------------------------------------------------------- Initial Setup

    def initialsetup(self):
        self.handler = datahandler.DataHandler(self.isdebug)
        currentidx = hou.hotkeys.changeIndex()
        chindex = self.handler.getchangeindex()

        if len(chindex) == 0:
            chindex = int(currentidx)
            self.handler.updatechangeindex(chindex, True)
            self.handler.updatedataasync()
            hou.ui.setStatusMessage(
                "Searcher database created",
                severity=hou.severityType.Message
            )
        else:
            chindex = int(chindex[0][0])

        if int(currentidx) != chindex:
            self.handler.updatedataasync()
            self.handler.updatechangeindex(int(currentidx))

        tmpkey = self.handler.getdefaulthotkey()
        self.tmpkey = tmpkey[0][0]
        return self.handler, self.tmpkey

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

    # endregion
    # region ------------------------------------------------------------- Callbacks
    def searchfilter_cb(self):
        self.openmenu()

    def pinwindow_cb(self):
        self.windowispin = not self.windowispin
        self.settingdata[util.SETTINGS_KEYS[5]] = self.windowispin
        searcher_data.savesettings(self.settingdata)
        self.setpinicon()

    def setpinicon(self):
        if self.windowispin:
            self.pinwindow.setIcon(util.PIN_IN_ICON)
        else:
            self.pinwindow.setIcon(util.PIN_OUT_ICON)

    def opensettings_cb(self):
        self.open_settings()

    def globalkeysearch(self):
        self.ctxsearch = True
        ctx = []
        ctx.append("h")
        results = self.handler.searchctx(ctx)
        self.searchtablepopulate(results)
        self.ctxsearch = False

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

    def textchange_cb(self, text):
        if len(text) > 0:
            self.infolbl.setText(self.searchresultstree.toolTip())
        if text in util.CTXSHOTCUTS:
            self.ctxsearcher(text)
        elif len(text) > 1 and text not in util.CTXSHOTCUTS:
            self.searching = True
            txt = self.handler.searchtext(text)
            self.searchtablepopulate(txt)
        else:
            self.searching = False
            self.searchresultstree.clear()
            self.infolbl.setText(
                "Begin typing to search or click magnifying glass icon to display options")

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
    # endregion

    # region ------------------------------------------------------------- Searchbar Menu
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

    # region ------------------------------------------------------------- Search Functionality
    def searchtablepopulate(self, data):
        if len(data) > 0:
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

            result = self.handler.gethcontextod(context_list)

            for hc in range(len(result)):
                hcontext_tli[result[hc][2]] = (QtWidgets.QTreeWidgetItem(
                    self.searchresultstree, [
                        result[hc][0],
                        result[hc][1]
                    ]
                ))
                self.searchresultstree.expandItem(hcontext_tli[result[hc][2]])

            base_keys = hcontext_tli.keys()
            for i in range(len(data)):
                for j in range(len(base_keys)):
                    if base_keys[j] in data[i][4]:
                        if self.isdebug:
                            hotkeys.append(QtWidgets.QTreeWidgetItem(
                                hcontext_tli[base_keys[j]], [
                                    data[i][0],
                                    data[i][1],
                                    data[i][2],
                                    data[i][3],
                                    data[i][4]
                                ]
                            ))
                        else:
                            hotkeys.append(QtWidgets.QTreeWidgetItem(
                                hcontext_tli[base_keys[j]], [
                                    data[i][0],
                                    data[i][1],
                                    data[i][2],
                                    data[i][3]
                                ]
                            ))
    # endregion

    # region ------------------------------------------------------------- Hotkey Processing

    def processkey(self, key, tmphk=False):
        hk = key
        if tmphk:
            lastkey = (str(self.tmpsymbol) + " " + str(hk[0]))
            self.handler.updatelasthk(lastkey)

        key = key[0].split('+')

        mods = []
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
            hd.executeDeferred(self.app.sendEvent,
                               hou.ui.mainQtWindow(), keypress)
            self.close()

        except(AttributeError, TypeError) as e:
            hou.ui.setStatusMessage(
                ("Could not trigger hotkey event: " + str(e)),
                severity=hou.severityType.Warning
            )

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
    # endregion

    # region ------------------------------------------------------------- Events
    def checktooltip(self, obj):
        if obj == self.searchresultstree:
            if self.searching:
                self.infolbl.setText(obj.toolTip())
            else:
                self.infolbl.setText(self.searchbox.toolTip())
        else:
            self.infolbl.setText(obj.toolTip())

    def eventFilter(self, obj, event):
        # ---------------------------------------------------- Mouse
        if event.type() == QtCore.QEvent.Enter:
            self.checktooltip(obj)
        elif event.type() == QtCore.QEvent.Leave:
            self.infolbl.setText("")
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
                self.move(self.x() + delta.x(), self.y()+delta.y())
                self.previous_pos = event.globalPos()
                self._drag_active = True
            else:
                return QtCore.QObject.eventFilter(self, obj, event)

        if event.type() == QtCore.QEvent.MouseButtonRelease:
            if self._drag_active:
                self._drag_active = False

        # ------------------------------------------------- Keypress
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

        # ------------------------------------------------- Window
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

        # ------------------------------------------------- Close
        if event.type() == QtCore.QEvent.Close:
            try:
                if util.bc(self.settingdata[util.SETTINGS_KEYS[2]]):
                    self.windowsettings.setValue(
                        "geometry",
                        self.saveGeometry()
                    )
            except (AttributeError, TypeError) as e:
                if hou.isUIAvailable():
                    hou.ui.setStatusMessage(
                        ("Could not save window dimensions: " + str(e)),
                        severity=hou.severityType.Warning
                    )
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

        # endregion
# endregion


# region ----------------------------------------------------------------- Help
class HelpButton(QtWidgets.QPushButton):
    """Generic Help button."""

    def __init__(self, name, parent=None):
        super(HelpButton, self).__init__(
            hou.qt.createIcon("BUTTONS_help"), "", parent=parent
        )

        self._name = name

        self.setToolTip("Show Help.")
        self.setIconSize(QtCore.QSize(14, 14))
        self.setMaximumSize(QtCore.QSize(14, 14))
        self.setFlat(True)

        self.clicked.connect(self.display_help)

    # -------------------------------------------------------------------------
    # METHODS
    # -------------------------------------------------------------------------

    def display_help(self):
        """Display help page."""
        # Look for an existing, float help browser.
        for pane_tab in hou.ui.paneTabs():
            if isinstance(pane_tab, hou.HelpBrowser):
                if pane_tab.isFloating():
                    browser = pane_tab
                    break

        # Didn't find one, so create a new floating browser.
        else:
            desktop = hou.ui.curDesktop()
            browser = desktop.createFloatingPaneTab(
                hou.paneTabType.HelpBrowser)

        browser.displayHelpPath("/searcher/{}".format(self._name))
# endregion


# region ----------------------------------------------------------------- Setup Functions


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
        # searcher_window.windowFlags() |
        QtCore.Qt.Tool |
        # QtCore.Qt.WindowSystemMenuHint |
        # QtCore.Qt.WindowTitleHint |
        QtCore.Qt.CustomizeWindowHint |
        # QtCore.Qt.FramelessWindowHint
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
