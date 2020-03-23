from __future__ import print_function
from __future__ import absolute_import
from searcher import enum

from sys import platform
from typing import Tuple
import os
import hou
hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    hver = int(ver[ver.rindex('.')+1:])
    from hutil.Qt import QtCore
else:
    from PyQt5 import QtCore

script_path = os.path.dirname(os.path.realpath(__file__))

# ------------------------------------------------------- Helper Functions
# SECTION Helper Functions -----------------------------------------------
# --------------------------------------------- DEBUG_LEVEL
# NOTE DEBUG_LEVEL ----------------------------------------
DEBUG_LEVEL = enum.Enum('NONE', 'TIMER', 'ALL')
class Dbug(object):
    def __init__(self, enabled, level, perf, mainwindow=False):
        self.enabled = enabled
        self.level = level
        self.performance = perf
        self.mainwindow = mainwindow
    def __nonzero__(self): return bool(self.enabled)

class AppColors(object):
    def __init__(self, colors={}):
        self.text1 =    colors[COLORFIELDS[0]]
        self.text2 =    colors[COLORFIELDS[1]]
        self.stats1 =   colors[COLORFIELDS[2]]
        self.stats2 =   colors[COLORFIELDS[3]]
        self.tooltip =  colors[COLORFIELDS[4]]

# -------------------------------------------- get_platform
# NOTE get_platform ---------------------------------------
def get_platform():
    return getattr(hou.session, "PLATFORM", None)

# -------------------------------------------- get_settings
# NOTE get_settings ---------------------------------------
def get_settings():
    return getattr(hou.session, "SETTINGS", None)


    
# -------------------------------------------- get_settings
# NOTE get_settings ---------------------------------------
def get_path(folders=None):
    script_path = os.path.dirname(os.path.realpath(__file__))
    PATH = os.path.join(script_path, '/'.join(folders))
    return PATH.replace("\\", "/")

# ------------------------------------------ Bool Converter
# NOTE Bool Converter -------------------------------------
def bc(v):
    return str(v).lower() in ("yes", "true", "t", "1")

# !SECTION Helper Functions

# --------------------------------------------------------------- Settings
# SECTION Settings -------------------------------------------------------
# ------------------------------------------- SETTINGS_KEYS
# NOTE SETTINGS_KEYS --------------------------------------
SETTINGS_KEYS = [
    'in_memory_db',                          # 0
    'database_path',                         # 1
    'savewindowsize',                        # 2
    'windowsize',                            # 3
    'debugflag',                             # 4
    'pinwindow',                             # 5
    'defaulthotkey',                         # 6
    'showctx',                               # 7
    'animatedsettings',                      # 8
    'maxresults',                            # 9
    'debuglevel',                            # 10
    'lastkey',                               # 11
    'metrics',                               # 12
    'metricsmainwindow',                     # 13                    
    'appcolors',                             # 14
    'expanditems',                           # 15
]

# --------------------------------------------- COLORFIELDS
# The names of the customizable colorfields
# NOTE COLORFIELDS ----------------------------------------
COLORFIELDS = [
    'text1',                                # 0
    'text2',                                # 1
    'stats1',                               # 2
    'stats2',                               # 3
    'tooltip',                              # 4
]

# ------------------------------------------ SETTINGS_TYPES
# Include type if it is to be processed, else mark NA
# {bool, text, int, intval} get processed by settings menu
# {flag} is a bool but handled separate from settings menu
# {NA} is other, handled separaretly as well
# NOTE SETTINGS_TYPES -------------------------------------
SETTINGS_TYPES = {
    SETTINGS_KEYS[0]:  'bool',               # in_memory_db
    SETTINGS_KEYS[1]:  'text',               # database_path
    SETTINGS_KEYS[2]:  'bool',               # savewindowsize
    SETTINGS_KEYS[3]:  'int',                # windowsize
    SETTINGS_KEYS[4]:  'bool',               # debugflag
    SETTINGS_KEYS[5]:  'flag',               # pinwindow
    SETTINGS_KEYS[6]:  'text',               # defaulthotkey
    SETTINGS_KEYS[7]:  'flag',               # showctx
    SETTINGS_KEYS[8]:  'bool',               # animatedsettings
    SETTINGS_KEYS[9]:  'intval',             # maxresults
    SETTINGS_KEYS[10]: 'cbx',                # debuglevel
    SETTINGS_KEYS[11]: 'NA',                 # lastkey
    SETTINGS_KEYS[12]: 'bool',               # metrics
    SETTINGS_KEYS[13]: 'flag',               # metricsmainwindow
    SETTINGS_KEYS[14]: 'NA',                 # appcolors
    SETTINGS_KEYS[15]: 'flag',                 # expanditems
}

# ---------------------------------------- DEFAULT_SETTINGS
# Default settings automatically applied upon creations
# NOTE DEFAULT_SETTINGS -----------------------------------
DEFAULT_SETTINGS = {
    SETTINGS_KEYS[0]: "False",               # in_memory_db
    SETTINGS_KEYS[1]: "",                    # database_path
    SETTINGS_KEYS[2]: "False",               # savewindowsize
    SETTINGS_KEYS[3]: [750, 350],           # windowsize
    SETTINGS_KEYS[4]: "False",               # debugflag
    SETTINGS_KEYS[5]: "False",               # pinwindow
    SETTINGS_KEYS[6]: u"Ctrl+Alt+Shift+F7",  # defaulthotkey
    SETTINGS_KEYS[7]: "True",                # showctx
    SETTINGS_KEYS[8]: "True",                # animatedsettings
    SETTINGS_KEYS[9]: 100,                   # maxresults
    SETTINGS_KEYS[10]: "NONE",               # debuglevel
    SETTINGS_KEYS[11]: "",                   # lastkey
    SETTINGS_KEYS[12]: "False",              # metrics
    SETTINGS_KEYS[13]: "False",              # metricsmainwindow
    SETTINGS_KEYS[14]: {                     # appcolors
        COLORFIELDS[0] : "#607FAE",
        COLORFIELDS[1] : "#D2A00C",
        COLORFIELDS[2] : "#c2efe5",
        COLORFIELDS[3] : "#c2efe5",
        COLORFIELDS[4] : "#607FAE",
    },         
    SETTINGS_KEYS[15]: "True",              # expanditems
}
# !SECTION Settings

# ------------------------------------------------------- Key Translations
# SECTION Key Translations -----------------------------------------------

# --------------------------------------------- CTXSHOTCUTS
# Context shortcodes for predefined results
# NOTE CTXSHOTCUTS ----------------------------------------
CTXSHOTCUTS = [":v", ":c", ":g"]

# ------------------------------------------ KEYCONVERSIONS
# Convertions for arrow keys (Should be moved to main dict)
# NOTE KEYCONVERSIONS -------------------------------------
KEYCONVERSIONS = {
    "DownArrow":  "down",
    "UpArrow":    "up",
    "LeftArrow":  "left",
    "RightArrow": "right",
}

# ---------------------------------------------- HOTKEYLIST
# List of possible hotkeys to use a temp keys when running commands
# NOTE HOTKEYLIST -----------------------------------------
HOTKEYLIST = [
    (u"Ctrl+Alt+Shift+F7"),
    (u"Ctrl+Alt+Shift+F6"),
    (u"Ctrl+Alt+Shift+F8"),
    (u"Ctrl+Alt+Shift+F9"),
    (u"Ctrl+Alt+Shift+F10")
]

def gethotkeys():
    hkeys = []
    settings = get_settings()
    hkeys.append(settings[SETTINGS_KEYS[6]])
    for key in HOTKEYLIST:
        hkeys.append(key)
    return hkeys

# Used for bitmasking to determine modifiers
MODIFIERS = {}
# Used for constructing a bitmasked modifier
REVERSE_MODIFIERS = {}

# ------------------------------------------- MODIFIER_KEYS
# Used to detect if a keypress was just a modifier
# NOTE MODIFIER_KEYS --------------------------------------
MODIFIER_KEYS = {
    QtCore.Qt.Key_Alt:      "Alt",
    QtCore.Qt.Key_Meta:     "Meta",
    QtCore.Qt.Key_Shift:    "Shift",
    QtCore.Qt.Key_Control:  "Ctrl",
}

# NOTE MODIFIERS ------------------------------------------
MODIFIERS = {
    "Shift":        QtCore.Qt.ShiftModifier,
    "Control":      QtCore.Qt.ControlModifier,
    "Ctrl":         QtCore.Qt.ControlModifier,
    "Meta":         QtCore.Qt.MetaModifier,
    "Alt":          QtCore.Qt.AltModifier,
}

# -------------------------------------------- SPECIAL_KEYS
# Special keys
# NOTE SPECIAL_KEYS ---------------------------------------
SPECIAL_KEYS = {
    QtCore.Qt.Key_Backspace:    "BACKSPACE",
    QtCore.Qt.Key_Delete:       "DELETE",
    QtCore.Qt.Key_Escape:       "ESCAPE",
    QtCore.Qt.Key_hyphen:       "HYPHEN",
    QtCore.Qt.Key_Return:       "RETURN",
    QtCore.Qt.Key_Enter:        "RETURN",
    QtCore.Qt.Key_Space:        "SPACE",
    QtCore.Qt.Key_Tab:          "TAB",
    QtCore.Qt.Key_Left:         "Left",
    QtCore.Qt.Key_Right:        "Right",
    QtCore.Qt.Key_Up:           "Up",
    QtCore.Qt.Key_Down:         "Down",
    QtCore.Qt.Key_PageUp:       "Page_Up",
    QtCore.Qt.Key_PageDown:     "Page_Down",
    QtCore.Qt.Key_End:          "Page_End",
    QtCore.Qt.Key_Home:         "Page_Home",
}

# ------------------------------------------------ Platform
# # Platform conversions
# NOTE Platform -------------------------------------------
# if platform == "linux" or platform == "linux2":
#     tmp = {
#         QtCore.Qt.ShiftModifier:     "Shift",
#         QtCore.Qt.ControlModifier:   "Ctrl",
#         QtCore.Qt.AltModifier:       "Alt",
#         QtCore.Qt.MetaModifier:      "M"
#     }
#     MODIFIERS.update(tmp)
#     tmp = {
#         "Shift": QtCore.Qt.ShiftModifier,
#         "Ctrl":  QtCore.Qt.ControlModifier,
#         "Alt":   QtCore.Qt.AltModifier
#     }
#     REVERSE_MODIFIERS.update(tmp)
# elif platform == "darwin":
#     tmp = {
#         QtCore.Qt.ShiftModifier:     "s",
#         QtCore.Qt.ControlModifier:   "S",
#         QtCore.Qt.AltModifier:       "M",
#         QtCore.Qt.MetaModifier:      "C"
#     }
#     MODIFIERS.update(tmp)
#     tmp = {
#         "s": QtCore.Qt.ShiftModifier,
#         "S": QtCore.Qt.ControlModifier,
#         "M": QtCore.Qt.AltModifier,
#         "C": QtCore.Qt.MetaModifier
#     }
#     REVERSE_MODIFIERS.update(tmp)
# elif platform == "win32" or platform == "win64":
#     tmp = {
#         QtCore.Qt.ShiftModifier:     "Shift",
#         QtCore.Qt.ControlModifier:   "Ctrl",
#         QtCore.Qt.AltModifier:       "Alt",
#         QtCore.Qt.MetaModifier:      "M"
#     }
#     MODIFIERS.update(tmp)
#     tmp = {
#         "Shift": QtCore.Qt.ShiftModifier,
#         "Ctrl":  QtCore.Qt.ControlModifier,
#         "Alt":   QtCore.Qt.AltModifier
#     }
#     REVERSE_MODIFIERS.update(tmp)
# endregion

# ------------------------------------------------ KEY_DICT
# NOTE KEY_DICT -------------------------------------------
KEY_DICT = {
    # ------------------------------------- Grey keys
    "Escape":       QtCore.Qt.Key_Escape,
    "Tab":          QtCore.Qt.Key_Tab,
    "Backtab":      QtCore.Qt.Key_Backtab,
    "Backspace":    QtCore.Qt.Key_Backspace,
    "Return":       QtCore.Qt.Key_Return,
    "Enter":        QtCore.Qt.Key_Enter,
    "Insert":       QtCore.Qt.Key_Insert,
    "Del":          QtCore.Qt.Key_Delete,
    "Pause":        QtCore.Qt.Key_Pause,
    "Print":        QtCore.Qt.Key_Print,
    "SysReq":       QtCore.Qt.Key_SysReq,
    "Home":         QtCore.Qt.Key_Home,
    "End":          QtCore.Qt.Key_End,
    "Left":         QtCore.Qt.Key_Left,
    "Up":           QtCore.Qt.Key_Up,
    "Right":        QtCore.Qt.Key_Right,
    "Down":         QtCore.Qt.Key_Down,
    "Prior":         None,
    "Next":         None,
    "Shift":        QtCore.Qt.Key_Shift,
    "Control":      QtCore.Qt.Key_Control,
    "Ctrl":         QtCore.Qt.Key_Control,
    "Meta":         QtCore.Qt.Key_Meta,
    "Alt":          QtCore.Qt.Key_Alt,
    "CapsLock":     QtCore.Qt.Key_CapsLock,
    "NumLock":      QtCore.Qt.Key_NumLock,
    "ScrollLock":   QtCore.Qt.Key_ScrollLock,
    "F1":           QtCore.Qt.Key_F1,
    "F2":           QtCore.Qt.Key_F2,
    "F3":           QtCore.Qt.Key_F3,
    "F4":           QtCore.Qt.Key_F4,
    "F5":           QtCore.Qt.Key_F5,
    "F6":           QtCore.Qt.Key_F6,
    "F7":           QtCore.Qt.Key_F7,
    "F8":           QtCore.Qt.Key_F8,
    "F9":           QtCore.Qt.Key_F9,
    "F10":          QtCore.Qt.Key_F10,
    "F11":          QtCore.Qt.Key_F11,
    "F12":          QtCore.Qt.Key_F12,
    "F13":          QtCore.Qt.Key_F13,
    "F14":          QtCore.Qt.Key_F14,
    "F15":          QtCore.Qt.Key_F15,
    "F16":          QtCore.Qt.Key_F16,
    "F17":          QtCore.Qt.Key_F17,
    "F18":          QtCore.Qt.Key_F18,
    "F19":          QtCore.Qt.Key_F19,
    "F20":          QtCore.Qt.Key_F20,
    "F21":          QtCore.Qt.Key_F21,
    "F22":          QtCore.Qt.Key_F22,
    "F23":          QtCore.Qt.Key_F23,
    "F24":          QtCore.Qt.Key_F24,
    "F25":          QtCore.Qt.Key_F25,
    "F26":          QtCore.Qt.Key_F26,
    "F27":          QtCore.Qt.Key_F27,
    "F28":          QtCore.Qt.Key_F28,
    "F29":          QtCore.Qt.Key_F29,
    "F30":          QtCore.Qt.Key_F30,
    "F31":          QtCore.Qt.Key_F31,
    "F32":          QtCore.Qt.Key_F32,
    "F33":          QtCore.Qt.Key_F33,
    "F34":          QtCore.Qt.Key_F34,
    "F35":          QtCore.Qt.Key_F35,
    "Super_L":      QtCore.Qt.Key_Super_L,
    "Super_R":      QtCore.Qt.Key_Super_R,
    "Menu":         QtCore.Qt.Key_Menu,
    "Hyper_L":      QtCore.Qt.Key_Hyper_L,
    "Hyper_R":      QtCore.Qt.Key_Hyper_R,
    # ------------------------------------- Regular keys
    "Space":        QtCore.Qt.Key_Space,
    "Exclam":       QtCore.Qt.Key_Exclam,
    "!":            QtCore.Qt.Key_Exclam,
    "QuoteDbl":     QtCore.Qt.Key_QuoteDbl,
    "\"":           QtCore.Qt.Key_QuoteDbl,
    "NumberSign":   QtCore.Qt.Key_NumberSign,
    "#":            QtCore.Qt.Key_NumberSign,
    "Dollar":       QtCore.Qt.Key_Dollar,
    "$":            QtCore.Qt.Key_Dollar,
    "Percent":      QtCore.Qt.Key_Percent,
    "%":            QtCore.Qt.Key_Percent,
    "Ampersand":    QtCore.Qt.Key_Ampersand,
    "&":            QtCore.Qt.Key_Ampersand,
    "Apostrophe":   QtCore.Qt.Key_Apostrophe,
    "\'":           QtCore.Qt.Key_Apostrophe,
    "ParenLeft":    QtCore.Qt.Key_ParenLeft,
    "(":            QtCore.Qt.Key_ParenLeft,
    "ParenRight":   QtCore.Qt.Key_ParenRight,
    ")":            QtCore.Qt.Key_ParenRight,
    "Asterisk":     QtCore.Qt.Key_Asterisk,
    "*":            QtCore.Qt.Key_Asterisk,
    "Plus":         QtCore.Qt.Key_Plus,
    "+":            QtCore.Qt.Key_Plus,
    "Comma":        QtCore.Qt.Key_Comma,
    ",":            QtCore.Qt.Key_Comma,
    "Minus":        QtCore.Qt.Key_Minus,
    "-":            QtCore.Qt.Key_Minus,
    "Period":       QtCore.Qt.Key_Period,
    ".":            QtCore.Qt.Key_Period,
    "Slash":        QtCore.Qt.Key_Slash,
    "/":            QtCore.Qt.Key_Slash,
    "0":            QtCore.Qt.Key_0,
    "1":            QtCore.Qt.Key_1,
    "2":            QtCore.Qt.Key_2,
    "3":            QtCore.Qt.Key_3,
    "4":            QtCore.Qt.Key_4,
    "5":            QtCore.Qt.Key_5,
    "6":            QtCore.Qt.Key_6,
    "7":            QtCore.Qt.Key_7,
    "8":            QtCore.Qt.Key_8,
    "9":            QtCore.Qt.Key_9,
    "Colon":        QtCore.Qt.Key_Colon,
    ":":            QtCore.Qt.Key_Colon,
    "Semicolon":    QtCore.Qt.Key_Semicolon,
    ";":            QtCore.Qt.Key_Semicolon,
    "Less":         QtCore.Qt.Key_Less,
    "<":            QtCore.Qt.Key_Less,
    "Equal":        QtCore.Qt.Key_Equal,
    "=":            QtCore.Qt.Key_Equal,
    "Greater":      QtCore.Qt.Key_Greater,
    ">":            QtCore.Qt.Key_Greater,
    "Question":     QtCore.Qt.Key_Question,
    "?":            QtCore.Qt.Key_Question,
    "At":           QtCore.Qt.Key_At,
    "A":            QtCore.Qt.Key_A,
    "B":            QtCore.Qt.Key_B,
    "C":            QtCore.Qt.Key_C,
    "D":            QtCore.Qt.Key_D,
    "E":            QtCore.Qt.Key_E,
    "F":            QtCore.Qt.Key_F,
    "G":            QtCore.Qt.Key_G,
    "H":            QtCore.Qt.Key_H,
    "I":            QtCore.Qt.Key_I,
    "J":            QtCore.Qt.Key_J,
    "K":            QtCore.Qt.Key_K,
    "L":            QtCore.Qt.Key_L,
    "M":            QtCore.Qt.Key_M,
    "N":            QtCore.Qt.Key_N,
    "O":            QtCore.Qt.Key_O,
    "P":            QtCore.Qt.Key_P,
    "Q":            QtCore.Qt.Key_Q,
    "R":            QtCore.Qt.Key_R,
    "S":            QtCore.Qt.Key_S,
    "T":            QtCore.Qt.Key_T,
    "U":            QtCore.Qt.Key_U,
    "V":            QtCore.Qt.Key_V,
    "W":            QtCore.Qt.Key_W,
    "X":            QtCore.Qt.Key_X,
    "Y":            QtCore.Qt.Key_Y,
    "Z":            QtCore.Qt.Key_Z,
    "BracketLeft":  QtCore.Qt.Key_BracketLeft,
    "[":            QtCore.Qt.Key_BracketLeft,
    "BracketRight": QtCore.Qt.Key_BracketRight,
    "]":            QtCore.Qt.Key_BracketRight,
    "Backslash":    QtCore.Qt.Key_Backslash,
    "\\":           QtCore.Qt.Key_Backslash,
    "Underscore":   QtCore.Qt.Key_Underscore,
    "_":            QtCore.Qt.Key_Underscore,
    "QuoteLeft":    QtCore.Qt.Key_QuoteLeft,
    "BraceLeft":    QtCore.Qt.Key_BraceLeft,
    "{":            QtCore.Qt.Key_BraceLeft,
    "BraceRight":   QtCore.Qt.Key_BraceRight,
    "}":            QtCore.Qt.Key_BraceRight,
    "Bar":          QtCore.Qt.Key_Bar,
    "|":            QtCore.Qt.Key_Bar,
    "AsciiCircum":  QtCore.Qt.Key_AsciiCircum,
    "^":            QtCore.Qt.Key_AsciiCircum,
    "AsciiTilde":   QtCore.Qt.Key_AsciiTilde,
    "~":            QtCore.Qt.Key_AsciiTilde,
}
# !SECTION Key Translations

# --------------------------------------------------- Houdini Translations
# SECTION Houdini Translations -------------------------------------------
# --------------------------------------------- CONTEXTTYPE
# NOTE CONTEXTTYPE ----------------------------------------
CONTEXTTYPE = {
    "Cop2": "COP",
    "CopNet": "COPNET",
    "Chop": "CHOP",
    "ChopNet": "CHOPNET",
    "Dop": "DOP",
    "Driver": "ROP",
    "Object": "OBJ",
    "Particle": "PART",
    "Pop": "POP",
    "Sop": "SOP",
    "Shop": "SHOP",
    "Tsop": "TSOP",
    "Vop": "VOP",
    "VopNet": "VEX",
}

# --------------------------------------------------- PANES
# NOTE PANES ----------------------------------------------
PANES = [
    "playbar",
    "shelf",
]

# ----------------------------------------------- PANETYPES
# NOTE PANETYPES ------------------------------------------
PANETYPES = {
    hou.paneTabType.AssetBrowser:       ["h.pane.projectm"],
    hou.paneTabType.BundleList:         ["h.pane.bundle"],
    hou.paneTabType.ChannelEditor:      ["h.pane.chedit", "h.pane.chedit.dope", "h.pane.chedit.dope.py", "h.pane.chedit.graph", "h.pane.chedit.graph.py", "h.pane.chedit.table", "h.pane.chedit.table.py"],
    hou.paneTabType.ChannelList:        ["h.pane.chlist", "h.pane.chlist.ch", "h.pane.chlist.layers", "h.pane.chlist.parmbox"],
    hou.paneTabType.ChannelViewer:      ["h.pane.gview.selmodechview"],
    hou.paneTabType.CompositorViewer:   ["h.pane.imgui.state", "h.pane.imgui.state.cop"],
    hou.paneTabType.DetailsView:        ["h.pane.details"],
    hou.paneTabType.HandleList:         ["h.pane.manip"],
    hou.paneTabType.HelpBrowser:        [""],
    hou.paneTabType.IPRViewer:          ["h.pane.ipr"],
    hou.paneTabType.LightLinker:        ["h.pane.linkeditor", "h.pane.linkeditor.sheet", ],
    hou.paneTabType.MaterialPalette:    ["h.pane.material"],
    hou.paneTabType.NetworkEditor:      ["h.pane.wsheet"],
    hou.paneTabType.OutputViewer:       ["h.pane.outputsview"],
    hou.paneTabType.Parm:               ["h.pane.editparms", "h.pane.parms"],
    hou.paneTabType.ParmSpreadsheet:    ["h.pane.parmsheet"],
    hou.paneTabType.PerformanceMonitor: ["h.pane.perfmon"],
    hou.paneTabType.PythonPanel:        ["h.py"],
    hou.paneTabType.PythonShell:        ["h.pane.pythonshell", "h.py"],
    hou.paneTabType.SceneViewer:        ["h.pane.gview.selmode", "h.pane.gview.state.select"],
    hou.paneTabType.TakeList:           ["h.pane.take", "h.pane.take.content", "h.pane.take.list"],
    hou.paneTabType.Textport:           ["h.pane.textport"],
    hou.paneTabType.TreeView:           ["tree"],
    "playbar":                          ["h.playbar"],
    "shelf":                            ["h.shelf"],


}
# !SECTION Houdini Translations

# --------------------------------------------------------------- UI Info
# SECTION UI Info -------------------------------------------------------
# DOP_pyrosolver
# MISC_database
# MISC_python
# MISC_rename
# NETVIEW_64bit_badge # bug
# NETVIEW_comment_badge
# NETVIEW_debug
# NETVIEW_info_button
# NETVIEW_message_badge
# NETVIEW_image_link
# NETVIEW_image_link_located
# BUTTONS_resizegrip_se -------- Resize
# BUTTONS_tree 
# COMMON_opencolorio COP2_colorwheel - Nice color things

# vop_terminals_connected
# vop_terminals_collapsed
# --------------------------------------------------- Icons
# NOTE Icons ----------------------------------------------
ICON_SIZE = hou.ui.scaledSize(32)
EDIT_ICON_SIZE = hou.ui.scaledSize(28)

PATH = os.path.join(script_path, "images")
root = PATH.replace("\\", "/")

ABOUT_ICON1 = hou.ui.createQtIcon(
    'NETVIEW_info_button',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

BUG_ICON = hou.ui.createQtIcon(
    'NETVIEW_64bit_badge',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

COLLAPSE_ALL_ICON = hou.ui.createQtIcon(
    (root + "/collapse_all.png"),
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

COLLAPSE_ICON = hou.ui.createQtIcon(
    'BUTTONS_collapse_left',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

COLOR_ICON = hou.ui.createQtIcon(
    'BUTTONS_chooser_color',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

DOWN_ICON = hou.ui.createQtIcon(
    'BUTTONS_down',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

EXPAND_ALL_ICON = hou.ui.createQtIcon(
     (root + "/expand_all.png"),
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

EXPAND_ICON = hou.ui.createQtIcon(
    'BUTTONS_expand_right',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

FILE_ICON = hou.ui.createQtIcon(
    'BUTTONS_folder',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

HELP_ICON = hou.ui.createQtIcon(
    'BUTTONS_help',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

INFO_ICON = hou.ui.createQtIcon(
    'BUTTONS_info',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

# BUTTONS_pinned
PIN_IN_ICON = hou.ui.createQtIcon(
    'BUTTONS_pinned',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

PIN_OUT_ICON = hou.ui.createQtIcon(
    'BUTTONS_pin_out_mono',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

RESIZEL_ICON = hou.ui.createQtIcon(
    'BUTTONS_resizegrip_se',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

SEARCH_ICON = hou.ui.createQtIcon(
    'BUTTONS_search',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

SETTINGS_ICON = hou.ui.createQtIcon(
    'BUTTONS_gear',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

UP_ICON = hou.ui.createQtIcon(
    'BUTTONS_up',
    EDIT_ICON_SIZE,
    EDIT_ICON_SIZE
)

# !SECTION  UI Info 


# SECTION Widget Tools ---------------------------------------------------
def widgets_at(mainwindow, pos):
	"""Return ALL widgets at `pos`
	Arguments:
		pos (QPoint): Position at which to get widgets
	"""

	widgets = []
	widget_at = mainwindow.widgetAt(pos)

	while widget_at:
		widgets.append(widget_at)

		# Make widget invisible to further enquiries
		widget_at.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
		widget_at = mainwindow.widgetAt(pos)

	# Restore attribute
	for widget in widgets:
		widget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)

	return widgets

    # !SECTION Widget Tools 