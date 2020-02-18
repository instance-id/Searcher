# region Imports
from sys import platform
from typing import Tuple
import os
import hou
if os.environ["HFS"] != "":
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets
    from hutil.Qt import QtUiTools
else:
    os.environ['QT_API'] = 'pyside2'
    from PySide import QtUiTools
    from qtpy import QtGui
    from qtpy import QtCore
    from qtpy import QtWidgets
# endregion

SequenceT = Tuple[str, ...]

keyconversions = {
    "DownArrow":  "down",
    "UpArrow":    "up",
    "LeftArrow":  "left",
    "RightArrow": "right"
}

# Used to detect if a keypress was just a modifier
MODIFIER_KEYS = {
    QtCore.Qt.Key_Shift:    "s",
    QtCore.Qt.Key_Control:  "C",
    QtCore.Qt.Key_Alt:      "M",
    QtCore.Qt.Key_AltGr:    "M",
    QtCore.Qt.Key_Meta:     "Meta",
    QtCore.Qt.Key_Super_L:  "S",
    QtCore.Qt.Key_Super_R:  "S"
}

# Used for bitmasking to determine modifiers
MODIFIERS = {}
# Used for constructing a bitmasked modifier
REVERSE_MODIFIERS = {}

# Special keys for Next
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

if platform == "linux" or platform == "linux2":
    tmp = {QtCore.Qt.ShiftModifier:     "s",
           QtCore.Qt.ControlModifier:   "C",
           QtCore.Qt.AltModifier:       "M",
           QtCore.Qt.MetaModifier:      "M"}
    MODIFIERS.update(tmp)
    tmp = {"s": QtCore.Qt.ShiftModifier,
           "C": QtCore.Qt.ControlModifier,
           "M": QtCore.Qt.MetaModifier}
    REVERSE_MODIFIERS.update(tmp)
elif platform == "darwin":
    tmp = {QtCore.Qt.ShiftModifier:     "s",
           QtCore.Qt.ControlModifier:   "S",
           QtCore.Qt.AltModifier:       "M",
           QtCore.Qt.MetaModifier:      "C"}
    MODIFIERS.update(tmp)
    tmp = {"s": QtCore.Qt.ShiftModifier,
           "S": QtCore.Qt.ControlModifier,
           "M": QtCore.Qt.AltModifier,
           "C": QtCore.Qt.MetaModifier}
    REVERSE_MODIFIERS.update(tmp)
elif platform == "win32" or platform == "win64":
    tmp = {QtCore.Qt.ShiftModifier:     "s",
           QtCore.Qt.ShiftModifier:     "Shift",
           QtCore.Qt.ControlModifier:   "C",
           QtCore.Qt.ControlModifier:   "Ctrl",
           QtCore.Qt.AltModifier:       "M",
           QtCore.Qt.AltModifier:       "Alt",
           QtCore.Qt.MetaModifier:      "M"}
    MODIFIERS.update(tmp)
    tmp = {"s":     QtCore.Qt.ShiftModifier,
           "Shift": QtCore.Qt.ShiftModifier,
           "C":     QtCore.Qt.ControlModifier,
           "Ctrl":  QtCore.Qt.ControlModifier,
           "M":     QtCore.Qt.MetaModifier,
           "Alt":   QtCore.Qt.AltModifier}
    REVERSE_MODIFIERS.update(tmp)

MODIFIERS = {
    "Shift":        QtCore.Qt.ShiftModifier,
    "Control":      QtCore.Qt.ControlModifier,
    "Ctrl":         QtCore.Qt.ControlModifier,
    "Meta":         QtCore.Qt.MetaModifier,
    "Alt":          QtCore.Qt.AltModifier,
}

KEY_DICT = {
    # Grey keys
    "Escape":       QtCore.Qt.Key_Escape,
    "Tab":          QtCore.Qt.Key_Tab,
    "Backtab":      QtCore.Qt.Key_Backtab,
    "Backspace":    QtCore.Qt.Key_Backspace,
    "Return":       QtCore.Qt.Key_Return,
    "Enter":        QtCore.Qt.Key_Enter,
    "Insert":       QtCore.Qt.Key_Insert,
    "Delete":       QtCore.Qt.Key_Delete,
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
    # Regular keys
    "Space":        QtCore.Qt.Key_Space,
    "Exclam":       QtCore.Qt.Key_Exclam,
    "QuoteDbl":     QtCore.Qt.Key_QuoteDbl,
    "NumberSign":   QtCore.Qt.Key_NumberSign,
    "Dollar":       QtCore.Qt.Key_Dollar,
    "Percent":      QtCore.Qt.Key_Percent,
    "Ampersand":    QtCore.Qt.Key_Ampersand,
    "Apostrophe":   QtCore.Qt.Key_Apostrophe,
    "ParenLeft":    QtCore.Qt.Key_ParenLeft,
    "ParenRight":   QtCore.Qt.Key_ParenRight,
    "Asterisk":     QtCore.Qt.Key_Asterisk,
    "Plus":         QtCore.Qt.Key_Plus,
    "Comma":        QtCore.Qt.Key_Comma,
    "Minus":        QtCore.Qt.Key_Minus,
    "Period":       QtCore.Qt.Key_Period,
    "Slash":        QtCore.Qt.Key_Slash,
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
    "Semicolon":    QtCore.Qt.Key_Semicolon,
    "Less":         QtCore.Qt.Key_Less,
    "Equal":        QtCore.Qt.Key_Equal,
    "Greater":      QtCore.Qt.Key_Greater,
    "Question":     QtCore.Qt.Key_Question,
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
    "Backslash":    QtCore.Qt.Key_Backslash,
    "BracketRight": QtCore.Qt.Key_BracketRight,
    "AsciiCircum":  QtCore.Qt.Key_AsciiCircum,
    "_":            QtCore.Qt.Key_Underscore,
    "Underscore":   QtCore.Qt.Key_Underscore,
    "QuoteLeft":    QtCore.Qt.Key_QuoteLeft,
    "BraceLeft":    QtCore.Qt.Key_BraceLeft,
    "Bar":          QtCore.Qt.Key_Bar,
    "BraceRight":   QtCore.Qt.Key_BraceRight,
    "AsciiTilde":   QtCore.Qt.Key_AsciiTilde,
}

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

PANETYPES = {
    hou.paneTabType.AssetBrowser: ["h.pane.projectm"],
    hou.paneTabType.BundleList: ["h.pane.bundle"],
    hou.paneTabType.ChannelEditor: ["h.pane.chedit", "h.pane.chedit.dope", "h.pane.chedit.dope.py", "h.pane.chedit.graph", "h.pane.chedit.graph.py", "h.pane.chedit.table", "h.pane.chedit.table.py"],
    hou.paneTabType.ChannelList: ["h.pane.chlist", "h.pane.chlist.ch", "h.pane.chlist.layers", "h.pane.chlist.parmbox"],
    hou.paneTabType.ChannelViewer: ["h.pane.gview.selmodechview"],
    hou.paneTabType.CompositorViewer: ["h.pane.imgui.state", "h.pane.imgui.state.cop"],
    hou.paneTabType.DetailsView: ["h.pane.details"],
    hou.paneTabType.HandleList: ["h.pane.manip"],
    hou.paneTabType.HelpBrowser: [""],
    hou.paneTabType.IPRViewer: ["h.pane.ipr"],
    hou.paneTabType.LightLinker: ["h.pane.linkeditor", "h.pane.linkeditor.sheet", ],
    hou.paneTabType.MaterialPalette: ["h.pane.material"],
    hou.paneTabType.NetworkEditor: ["h.pane.wsheet"],
    hou.paneTabType.OutputViewer: ["h.pane.outputsview"],
    hou.paneTabType.Parm: ["h.pane.editparms", "h.pane.parms"],
    hou.paneTabType.ParmSpreadsheet: ["h.pane.parmsheet"],
    hou.paneTabType.PerformanceMonitor: ["h.pane.perfmon"],
    hou.paneTabType.PythonPanel: ["h.pane.pythonshell", "h.py"],
    hou.paneTabType.SceneViewer: ["h.pane.gview.selmode", "h.pane.gview.state.select"],
    hou.paneTabType.TakeList: ["h.pane.take", "h.pane.take.content", "h.pane.take.list"],
    hou.paneTabType.Textport: ["h.pane.textport"],
    hou.paneTabType.TreeView: ["tree"],
}
