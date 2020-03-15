
# region Imports
from __future__ import print_function
from __future__ import absolute_import
import weakref
import hou
import os
import sys

hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    hver = int(ver[ver.rindex('.')+1:])
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets

# ----------------------------------------------------------------- Help
# NOTE -----------------------------------------------------------------


class HelpButton(QtWidgets.QPushButton):
    """Generic Help button."""

    def __init__(self, name, tooltip, size, parent=None):
        super(HelpButton, self).__init__(
            hou.qt.createIcon("BUTTONS_help"), "", parent=parent
        )

        self._name = name
        self.setToolTip(tooltip)
        self.setIconSize(QtCore.QSize(size, size))
        self.setMaximumSize(QtCore.QSize(size, size))
        self.setFlat(True)

        self.clicked.connect(self.display_help)

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
            browser = desktop.createFloatingPaneTab(
                hou.paneTabType.HelpBrowser)

        browser.displayHelpPath("/searcher/{}".format(self._name))
