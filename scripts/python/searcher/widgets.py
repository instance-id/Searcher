from past.builtins import basestring
import hou
import platform
from hutil import py23
from hutil.Qt import QtWidgets
from hutil.Qt import QtCore
from hutil.Qt import QtGui

# -------------------------------------------------------------- Borrowed from Houdini keybinding menu files

# See UI/UI_KeyBindings.h, I didn't want to #include that here
#define			 COMMAND_KEY_BIT		0x40000000
#define			   OTHER_KEY_BIT		0x20000000
#define			   ARROW_KEY_BIT		0x10000000
#define			FUNCTION_KEY_BIT		0x08000000
#define			     ALT_KEY_BIT		0x04000000
#define			    CTRL_KEY_BIT		0x02000000
#define			   SHIFT_KEY_BIT		0x01000000
#define			CONFLICT_KEY_BIT		0x00800000	// Special bit for the hotkey manager
#define	       CONFLICT_ANCESTOR_KEY_BIT		0x00400000	// Special bit for the hotkey manager
#define	     CONFLICT_DESCENDANT_KEY_BIT		0x00200000	// Special bit for the hotkey manager

ShiftKeyBit             = 0x01000000
AltKeyBit               = 0x04000000
ControlKeyBit           = 0x02000000
CommandKeyBit           = 0x40000000
ConflictBit             = 0x00800000
ConflictAncestorBit     = 0x00400000
ConflictDescendantBit   = 0x00200000


class ClickableLineEdit(QtWidgets.QLineEdit):
    right_clicked = QtCore.Signal()
    double_clicked = QtCore.Signal()

    def mouseDoubleClickEvent(self, e):
        self.double_clicked.emit()
        self.deselect()

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.QEvent.RightButton:
            self.right_clicked.emit()

    def contextMenuEvent(self, event):
        pass

class RawKeyCapture(QtWidgets.QLineEdit):
    cancel = QtCore.Signal()

    def keyPressEvent(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            # TO DO:
            #  - handle the Break key (i.e. Ctrl-Break)
            keystring = event.text()

            keystring = hou.qt.qtKeyToString(event.key(), int(event.modifiers()), event.text())
            # print "Line ", get_linenumber(), "-", keystring, "-", event.text()
            if keystring == "Esc":
                self.cancel.emit()
            elif keystring:
                self.setText(keystring)

class KeyCaptureWidget(QtWidgets.QFrame):
    accept = QtCore.Signal(str)
    changed = QtCore.Signal(str)
    cancel = QtCore.Signal()

    @QtCore.Slot(str)
    def setText(self, text):
        self.capturekey.setText(text)

    def text(self):
        return self.capturekey.text()

    special_items = ["Esc", "Tab", "Enter", "Del", "Backspace"]

    def __init__(self, accept_label, parent=None):
        super(KeyCaptureWidget, self).__init__(parent)
        self.capturekey = RawKeyCapture()
        self.capturekey.setPlaceholderText("Press a Key")
        self.capturekey.textChanged.connect(self._action_key_changed)
        self.capturekey.cancel.connect(self._action_cancel)

        self.specialsbutton = QtWidgets.QToolButton()
        #self.specialsbutton.setMaximumSize(the_scaled_icon_size, the_scaled_icon_size)
        self.specialsmenu = QtWidgets.QMenu(self.specialsbutton)
        self.specialsbutton.setMenu(self.specialsmenu)
        self.specialsbutton.setObjectName("drop-down-arrow")
        self.specialsbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        self.specialsmenu.triggered.connect( lambda action:
                                             self.capturekey.setText(fromKeyDisplayString(action.text()))
                                             )
        self.specialsmenu.aboutToShow.connect(self._update_dropdown_menu)
        # bug-workaround: If the menu is empty then it never gets its style applied
        self.specialsmenu.addAction("<Placeholder...>")

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.capturekey)
        layout.addWidget(self.specialsbutton)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.capturekey.setFocus()
        self.setAutoFillBackground(True)

    def _update_dropdown_menu(self):
        self.specialsmenu.clear()
        modifier_text = ""
        # @TO DO: tweak for the Mac
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers & QtCore.Qt.ShiftModifier:
            modifier_text += "Shift+"
        if modifiers & (QtCore.Qt.AltModifier):
            modifier_text += "Alt+"
        if platform.system() == "Darwin":
            if modifiers & QtCore.Qt.ControlModifier:
                modifier_text += "Cmd+"
            if modifiers & (QtCore.Qt.MetaModifier):
                modifier_text += "Ctrl+"
        else:
            if modifiers & QtCore.Qt.ControlModifier:
                modifier_text += "Ctrl+"
        for special in self.special_items:
            keystr = toKeyDisplayString(modifier_text + special)
            self.specialsmenu.addAction(keystr)
        self.specialsmenu.update()

    def _action_key_changed(self, key):
        self.changed.emit(key)

    def _action_cancel(self):
        self.cancel.emit()

    def _action_accept(self):
        key = self.capturekey.text()
        self.accept.emit(key)


# -------------------------------------------------------------------
def toKeyDisplayString(keystr):
    if platform.system() != "Darwin":
        return keystr
    outkeystr = py23.unicodeType(keystr)
    outkeystr = outkeystr.replace(u"Cmd+", u"\u2318")
    outkeystr = outkeystr.replace(u"Alt+", u"\u2325")
    outkeystr = outkeystr.replace(u"Shift+", u"\u21e7")
    outkeystr = outkeystr.replace(u"Ctrl+", u"\u2303")

    if not outkeystr or (keystr == outkeystr):
        return keystr
    else:
        return outkeystr

def fromKeyDisplayString(keystr):
    if platform.system() != "Darwin":
        return keystr
    outkeystr = py23.unicodeType(keystr).replace(u"\u2318", "Cmd+", 1)
    outkeystr = outkeystr.replace(u"\u2325", "Alt+", 1)
    outkeystr = outkeystr.replace(u"\u21e7", "Shift+", 1)
    outkeystr = outkeystr.replace(u"\u2303", "Ctrl+", 1)
    return outkeystr

