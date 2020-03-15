# coding=utf-8
import os
import sys

hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    hver = int(ver[ver.rindex('.')+1:])
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets
else:
    from PyQt5 import QtGui
    from PyQt5 import QtCore
    from PyQt5 import QtWidgets

class ResizeHandle(QtWidgets.QSizeGrip):
    def __init__(self, parent, target):
        """ ResizeHandle has separate parent widget and target widget. They can be same,
        of course, but this allows more freedom in placement of resizehandles.
        :param parent: parent widget to host the handle widget
        :param target: target widget which is affected by resizing
        """
        super(ResizeHandle, self).__init__(parent)
        self.target = target
        self.pressed = False
        self.adjust = None

    def mousePressEvent(self, e):
        self.pressed = True
        grandparent = self.target.parent()
        rrect = self.target.geometry()
        bottom_right = grandparent.mapToGlobal(rrect.bottomRight())
        self.adjust = bottom_right - e.globalPos()

    def mouseReleaseEvent(self, e):
        self.pressed = False
        self.adjust = None

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return
        if not self.pressed:
            return
        gp = e.globalPos()
        size = self.target.size()
        rrect = self.target.geometry()
        grandparent = self.target.parent()
        bottom_right = grandparent.mapToGlobal(rrect.bottomRight())
        size_diff = bottom_right - gp - self.adjust
        nw = max(16, size.width() - size_diff.x())
        nh = max(16, size.height() - size_diff.y())
        self.target.setMinimumSize(nw, nh)
        pw = self.parentWidget()
        if hasattr(pw, 'update_size'):
            pw.update_size()
            self.resizable.resize(size.width() - size_diff.x(), size.height() - size_diff.y())

    def eventFilter(self, obj, event):
        """ Remove check for hiding size grip on full screen --
        widgets should be always resizable.
        :param obj:
        :param event:
        :return:
        """
        return False


class GraphicsResizeHandle(QtWidgets.QSizeGrip):
    def __init__(self, view, host):
        QtWidgets.QSizeGrip.__init__(self, view)
        self.pressed = False
        self.adjust = None
        self.update_position()
        self.show()

    def update_position(self):
        v = ctrl.graph_view
        br = self.host.sceneBoundingRect().bottomRight()
        bottom_right = v.mapFromScene(br)
        self.move(bottom_right)

    def mousePressEvent(self, e):
        self.pressed = True
        v = ctrl.graph_view
        br = self.host.sceneBoundingRect().bottomRight()
        global_bottom_right = v.mapToGlobal(v.mapFromScene(br))
        self.adjust = global_bottom_right - e.globalPos()

    def mouseReleaseEvent(self, e):
        self.pressed = False
        self.adjust = None

    def mouseMoveEvent(self, e):
        """ Implements dragging the handle (if handle is pressed)
        :param e:
        :return:
        """
        if e.buttons() != QtCore.Qt.LeftButton:
            return
        if not self.pressed:
            return
        gp = e.globalPos()
        h = self.host
        br = h.sceneBoundingRect().bottomRight()
        global_bottom_right = ctrl.graph_view.mapToGlobal(ctrl.graph_view.mapFromScene(br))
        size_diff = global_bottom_right - gp - self.adjust
        new_width = h.width - size_diff.x()
        new_height = h.height - size_diff.y()
        h.set_user_size(new_width, new_height)
        h.update_label()
        self.update_position()
        ctrl.forest.draw()

    def eventFilter(self, obj, event):
        """ Remove check for hiding size grip on full screen --
        widgets should be always resizable.
        :param obj:
        :param event:
        :return:
        """
        return False