from hutil.Qt import QtWidgets
from hutil.Qt import QtCore
from hutil.Qt import QtGui


class InputLineEdit(QtWidgets.QLineEdit):
    double_clicked = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(InputLineEdit, self).__init__(parent)
        self.setPlaceholderText("Double click to change...")

    def mouseDoubleClickEvent(self, event):
        # if event.button() == QtCore.Qt.MouseButton.LeftButton:
        self.setPlaceholderText("Input key sequence")
        self.selectAll()
        self.double_clicked.emit(self.text())
