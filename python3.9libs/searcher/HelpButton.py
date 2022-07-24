from __future__ import print_function
from __future__ import absolute_import
from searcher import util

import hou
import os

hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    # hver = int(ver[ver.rindex('.')+1:])
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets
else:
    from qtpy import QtCore
    from qtpy import QtWidgets


# ---------------------------------------------------- Help
# NOTE Help -----------------------------------------------
class HelpButton(QtWidgets.QToolButton):
    """Generic Help button."""

    def __init__(self, name, tooltip, size, searcher, parent=None):
        super(HelpButton, self).__init__(parent=parent)

        self.parentWindow = searcher
        self._name = name
        self.setToolTip(tooltip)
        self.clicked.connect(self.display_help)
        help_button_size = hou.ui.scaledSize(size)
        self.setProperty("flat", True)
        self.setIcon(hou.qt.createIcon(util.get_path(["images", "help1.png"])))
        self.setIconSize(QtCore.QSize(
            help_button_size,
            help_button_size
        ))

    def display_help(self):
        """Display help panel."""
        # Look for an existing, float help browser.
        for pane_tab in hou.ui.paneTabs():
            if isinstance(pane_tab, hou.HelpBrowser):
                if pane_tab.isFloating():
                    browser = pane_tab
                    break

        # Didn't find one, so create a new floating browser.
        else:
            desktop = hou.ui.curDesktop()

            posx = self.parentWindow.pos().x()
            posy = self.parentWindow.pos().y()
            sizew = self.parentWindow.width()
            sizeh = self.parentWindow.height()

            browser = desktop.createFloatingPaneTab(
                hou.paneTabType.HelpBrowser, position=(posx + sizew / 8, posy - (sizeh / 2)), size=(805, 650))
            self.parentWindow.close()

        browser.displayHelpPath("/searcher/{}".format(self._name))
