from hutil.Qt import QtCore, QtGui, QtWidgets


class Animator(QtWidgets.QWidget):
    def __init__(self, parent=None, close_cb=None, animationDuration=200):
        super(Animator, self).__init__(parent)

        self.animationDuration = animationDuration

        self.toggleAnimation = QtCore.QParallelAnimationGroup()
        if close_cb is not None:
            self.toggleAnimation.finished.connect(close_cb)

        self.contentArea = QtWidgets.QScrollArea(
            maximumHeight=0, minimumHeight=0, minimumWidth=500)
        self.contentArea.setStyleSheet(
            "QScrollArea { background-color: rgba(58 58, 58, 1); border: none;}")
        self.contentArea.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)

        toggleAnimation = self.toggleAnimation
        toggleAnimation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumHeight"))
        toggleAnimation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumHeight"))
        toggleAnimation.addAnimation(QtCore.QPropertyAnimation(
            self.contentArea, b"maximumHeight"))

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.contentArea)

    def start_animation(self, checked):
        direction = QtCore.QAbstractAnimation.Forward if checked else QtCore.QAbstractAnimation.Backward
        self.toggleAnimation.setDirection(direction)
        self.toggleAnimation.start()

    def setContentLayout(self, contentLayout):
        # Not sure if this is equivalent to self.contentArea.destroy()
        lay = self.contentArea.layout()
        del lay
        self.contentArea.setLayout(contentLayout)
        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()

        contentHeight = contentLayout.sizeHint().height()
        for i in range(self.toggleAnimation.animationCount()-1):
            expandAnimation = self.toggleAnimation.animationAt(i)
            expandAnimation.setDuration(self.animationDuration)
            expandAnimation.setStartValue(collapsedHeight)
            expandAnimation.setEndValue(collapsedHeight + contentHeight)

        contentAnimation = self.toggleAnimation.animationAt(
            self.toggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)
