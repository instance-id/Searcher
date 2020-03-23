from __future__ import absolute_import
from searcher import bugreport_ui
from searcher import util
import os
import sys

import hou
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

scriptpath = os.path.dirname(os.path.realpath(__file__))


class BugReport(QtWidgets.QWidget):
    """ Searcher Settings and Debug Menu"""

    def __init__(self, parent=None):
        super(BugReport, self).__init__(parent=parent)
        self.setParent(parent)
        self.parentwindow = parent
        self.ui = bugreport_ui.Ui_BugReport()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.installEventFilter(self)

    # ------------------------------------------------------------- Events
    # SECTION Events -----------------------------------------------------
    def eventFilter(self, obj, event):
        event_type = event.type()

        # ---------------------------------------- Keypress
        # NOTE Keypress -----------------------------------
        if event_type == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                self.parentwindow.closeroutine()

        return QtCore.QObject.eventFilter(self, obj, event)