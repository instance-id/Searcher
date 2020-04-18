# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bugreport.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BugReport(object):
    def setupUi(self, BugReport):
        BugReport.setObjectName("BugReport")
        BugReport.setWindowModality(QtCore.Qt.NonModal)
        BugReport.resize(393, 172)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BugReport.sizePolicy().hasHeightForWidth())
        BugReport.setSizePolicy(sizePolicy)
        BugReport.setMinimumSize(QtCore.QSize(100, 0))
        BugReport.setBaseSize(QtCore.QSize(0, 0))
        BugReport.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(BugReport)
        self.gridLayout.setContentsMargins(-1, -1, -1, 6)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.secondrow = QtWidgets.QHBoxLayout()
        self.secondrow.setObjectName("secondrow")
        self.title = QtWidgets.QLineEdit(BugReport)
        self.title.setMinimumSize(QtCore.QSize(175, 0))
        self.title.setObjectName("title")
        self.secondrow.addWidget(self.title)
        self.edittitle_btn = QtWidgets.QPushButton(BugReport)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edittitle_btn.sizePolicy().hasHeightForWidth())
        self.edittitle_btn.setSizePolicy(sizePolicy)
        self.edittitle_btn.setMaximumSize(QtCore.QSize(55, 16777215))
        self.edittitle_btn.setObjectName("edittitle")
        self.secondrow.addWidget(self.edittitle_btn)
        self.verticalLayout_4.addLayout(self.secondrow)
        self.webview = QtWidgets.QLabel(BugReport)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webview.sizePolicy().hasHeightForWidth())
        self.webview.setSizePolicy(sizePolicy)
        self.webview.setObjectName("webview")
        self.verticalLayout_4.addWidget(self.webview)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.continue_btn = QtWidgets.QPushButton(BugReport)
        self.continue_btn.setObjectName("continue_btn")
        self.horizontalLayout.addWidget(self.continue_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(BugReport)
        QtCore.QMetaObject.connectSlotsByName(BugReport)

    def retranslateUi(self, BugReport):
        _translate = QtCore.QCoreApplication.translate
        BugReport.setWindowTitle(_translate("BugReport", "Form"))
        self.title.setPlaceholderText(_translate("BugReport", "Please enter descriptive bug report title"))
        self.edittitle_btn.setText(_translate("BugReport", "Edit"))
        self.webview.setText(_translate("BugReport", "TextLabel"))
        self.continue_btn.setText(_translate("BugReport", "Continue"))
