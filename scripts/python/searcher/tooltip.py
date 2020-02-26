""" Originally from : houdini\python2.7libs\houpythonportion\qt\ToolTip.py """

import hou

from hutil.Qt import QtCore
from hutil.Qt import QtWidgets


class ToolTip(QtWidgets.QWidget):
    """
hou.qt.ToolTip

A tooltip window with the Houdini look and feel that can be used for
hover tooltips.

This class inherits from Qt's QtWidgets.QWidget class.

EXAMPLES

    This example demonstrates creating a tooltip window and attaching it
    to a button:

  > 
  > tooltip = hou.qt.ToolTip()
  > tooltip.setTitle(\"Tooltip Example - SOP Torus Help\")
  > tooltip.setText(\"This tooltip links to the SOP Torus help page.\")
  > tooltip.setHotkey(\"Shift+H\")
  > tooltip.setHelpUrl(\"/nodes/sop/torus\")
  > 
  > btn = QtWidgets.QPushButton(\"Hover Me\")
  > tooltip.setTargetWidget(btn)

"""
    __module__ = "hou.qt"

    def __init__(self):
        """
__init__(self)

    Create and return a new tooltip window.

"""
        QtWidgets.QWidget.__init__(self, None, QtCore.Qt.ToolTip)
        self.setProperty("houdiniToolTip", True)
        self.targetWidget = None

        # Title widgets.
        self.titleWidget = QtWidgets.QLabel()
        self.titleWidget.setProperty("houdiniToolTipTitle", True)
        self.separator = hou.qt.createSeparator()
        self.separator.setProperty("houdiniToolTipSeparator", True)

        # Text widget.
        self.textWidget = QtWidgets.QLabel()
        self.textWidget.setProperty("houdiniToolTipText", True)
        self.textWidget.setMinimumWidth(hou.ui.scaledSize(200))
        self.textWidget.setWordWrap(True)

        # Hotkey text widget.
        self.hotkeyWidget = QtWidgets.QLabel()
        self.hotkeyWidget.setProperty("houdiniToolTipHotkeyText", True)
        self.hotkeyWidget.setAlignment(
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # Layout text widgets.
        text_layout = QtWidgets.QHBoxLayout()
        text_layout.addWidget(self.textWidget)
        text_layout.addWidget(self.hotkeyWidget)

        # Extra help widgets.
        MARGIN_SIZE = 2
        help_icon = hou.qt.createIcon("BUTTONS_help")
        help_icon_size = hou.ui.scaledSize(16)
        help_icon_pixmap = help_icon.pixmap(
            QtCore.QSize(help_icon_size, help_icon_size))
        self.extraHelpIconWidget = QtWidgets.QLabel()
        self.extraHelpIconWidget.setProperty("houdiniToolTipExtra", True)
        self.extraHelpIconWidget.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        self.extraHelpIconWidget.setPixmap(help_icon_pixmap)
        self.extraHelpIconWidget.setContentsMargins(
            MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE)
        self.extraHelpTextWidget = QtWidgets.QLabel()
        self.extraHelpTextWidget.setProperty("houdiniToolTipExtra", True)
        self.helpHotkey = hou.ui.hotkeys("h.context_help")[0]
        self.extraHelpTextWidget.setText(
            "Press %s for more help." % self.helpHotkey)
        self.extraHelpTextWidget.setContentsMargins(
            MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE, MARGIN_SIZE)
        extra_help_layout = QtWidgets.QHBoxLayout()
        extra_help_layout.setSpacing(0)
        extra_help_layout.setContentsMargins(0, 0, 0, 0)
        extra_help_layout.addWidget(self.extraHelpIconWidget)
        extra_help_layout.addWidget(self.extraHelpTextWidget)

        # Hide all widgets by default.
        self.titleWidget.hide()
        self.separator.hide()
        self.textWidget.hide()
        self.hotkeyWidget.hide()
        self.extraHelpIconWidget.hide()
        self.extraHelpTextWidget.hide()

        # Add widgets to main layout.
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.titleWidget)
        main_layout.addWidget(self.separator)
        main_layout.addLayout(text_layout)
        main_layout.addLayout(extra_help_layout)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(main_layout)
        self.setStyleSheet(hou.qt.styleSheet())

    def __del__(self):
        self._detachFromTargetWidget()

    def setTitle(self, title):
        """
setTitle(self, title)

    Set the tooltip's title. The title appears at the top of the window.
    If no title is set then the tooltip window does not display the
    title area.

"""
        self.titleWidget.setText(title)

        # Show or hide the title area.
        if title != "":
            self.titleWidget.show()
            self.separator.show()
        else:
            self.titleWidget.hide()
            self.separator.hide()

    def setText(self, text):
        """
setText(self, text)

    Set the tooltip's main text.

"""
        self.textWidget.setText(text)
        self._showOrHideTextArea()

    def setHotkey(self, hotkey):
        """
setHotkey(self, hotkey)

    Sets a hotkey to display in the tooltip.

    hotkey must be a key sequence such as \"G\", \"Shift+G\" or \"Cmd+G\".

"""
        self.hotkeyWidget.setText(hotkey)
        self._showOrHideTextArea()

    def setHelpUrl(self, help_url):
        """
setHelpUrl(self, help_url)

    Link the tooltip to the given help web page. When a help URL is set
    then the user can press F1 while the tooltip is visible to open the
    help web page.

    help_url can be either a fully qualified URL or a Houdini help path.
    For example, passing in \"/nodes/sop/torus\" as the help URL will
    cause the tooltip window to open the SOP Torus help page when F1 is
    pressed.

"""
        self.helpUrl = help_url

        if help_url != "":
            self.extraHelpIconWidget.show()
            self.extraHelpTextWidget.show()
        else:
            self.extraHelpIconWidget.hide()
            self.extraHelpTextWidget.hide()

    def setTargetWidget(self, widget):
        """
setTargetWidget(self, widget)

    Sets the widget that the tooltip is attached to. When the cursor is
    hovered over the target widget then the tooltip window is opened.
    And when the cursor is moved outside of the target widget's area
    then the tooltip window is closed.

    Setting the target widget will cause the tooltip to detach itself
    from any previous target widget.

"""
        # Detach from previous target widget.
        self._detachFromTargetWidget()

        self.targetWidget = widget
        if self.targetWidget:
            # Listen for events on the target widget so we know when
            # to show and hide the tooltip.
            self.targetWidget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj != self.targetWidget:
            return False

        if event.type() == QtCore.QEvent.Type.ToolTip:
            self.move(event.globalX() + 20, event.globalY())
            self.show()
        elif event.type() == QtCore.QEvent.Type.Leave:
            self.hide()
        elif event.type() == QtCore.QEvent.Type.KeyPress:
            if self.isVisible() \
                and (
                    (self.helpHotkey == "F1"
                        and event.key() == QtCore.Qt.Key_F1)
                    or (event.key() == self.helpHotkey)
            ):
                self._displayHelpPage()

        return False

    def _detachFromTargetWidget(self):
        if self.targetWidget is None:
            return

        self.targetWidget.removeEventFilter(self)
        self.targetWidget = None

    def _showOrHideTextArea(self):
        if self.textWidget.text() != "" \
                or self.hotkeyWidget.text() != "":
            self.textWidget.show()
            self.hotkeyWidget.show()
        else:
            self.textWidget.hide()
            self.hotkeyWidget.hide()

    def _displayHelpPage(self):
        desktop = hou.ui.curDesktop()
        help_browser = desktop.paneTabOfType(hou.paneTabType.HelpBrowser)
        if help_browser is None:
            help_browser = desktop.displaySideHelp()

        help_browser.displayHelpPath(self.helpUrl)


hou.qt.ToolTip = ToolTip
