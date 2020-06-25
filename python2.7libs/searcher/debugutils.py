from __future__ import print_function
from __future__ import division

from builtins import range
from past.utils import old_div
from hutil.Qt import QtCore
from hutil.Qt import QtGui
from hutil.Qt import QtWidgets


def dumpWidgetLayout(widget, prefix=''):
    """ Debug utility to print out tree of widgets with relevant layout
        properties
    """
    text = ""
    if not isinstance(widget, QtWidgets.QWidget) \
            and not isinstance(widget, QtWidgets.QDialog):
        return

    text += str((prefix, "* name:", str(widget.objectName())))
    text += str((prefix, "  visible:", str(widget.isVisible())))
    text += str((prefix, "  minimumSize:", str(widget.minimumSize())))
    text += str((prefix, "  minimumSizeHint:", str(widget.minimumSizeHint())))
    text += str((prefix, "  sizeHint:", str(widget.sizeHint())))
    text += str((prefix, "  contentsMargins:", str(widget.contentsMargins())))
    text += str((prefix, "  sizePolicy:", str(widget.sizePolicy())))
    if widget.layout():
        layout = widget.layout()
        text += str((prefix, "  layout.minimumSize:", str(widget.layout().minimumSize())))
        text += str((prefix, "  layout.sizeHint:", str(widget.layout().sizeHint())))
        text += str((prefix, "  layout.contentsMargins:", str(widget.layout().contentsMargins())))
        for i in range(0, layout.count()):
            item = layout.itemAt(i)
            dir_flag = item.expandingDirections()
            if (dir_flag & QtCore.Qt.Orientation.Horizontal):
               text += str((prefix, "  -> ", i, ": expand HORIZ"))
            elif (dir_flag & QtCore.Qt.Orientation.Vertical):
                text += str((prefix, "  -> ", i, ": expand VERTICAL"))
            else:
                text += str((prefix, "  -> ", i, ": NO expand"))
            text += str((prefix, "  -> ", i, ": sizeHint", str(item.sizeHint())))
            if item.widget():
                text += str((prefix, "  -> ", i, ": widget.sizeHint", str(item.widget().sizeHint())))
    text += str((prefix, "  numChildren:", len(widget.children())))
    for child in widget.children():
        dumpWidgetLayout(child, prefix + '  ')

    return text
