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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.secondrow = QtWidgets.QHBoxLayout()
        self.secondrow.setObjectName("secondrow")
        self.title = QtWidgets.QLineEdit(BugReport)
        self.title.setMinimumSize(QtCore.QSize(175, 0))
        self.title.setObjectName("title")
        self.secondrow.addWidget(self.title)
        self.verticalLayout.addLayout(self.secondrow)
        self.label = QtWidgets.QLabel(BugReport)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.headerrow = QtWidgets.QHBoxLayout()
        self.headerrow.setObjectName("headerrow")
        self.verticalLayout.addLayout(self.headerrow)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.logo = QtWidgets.QLabel(BugReport)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMaximumSize(QtCore.QSize(120, 120))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("C:/Users/mosthated/Downloads/483688212.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")
        self.horizontalLayout_3.addWidget(self.logo)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton = QtWidgets.QPushButton(BugReport)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.retranslateUi(BugReport)
        QtCore.QMetaObject.connectSlotsByName(BugReport)

    def retranslateUi(self, BugReport):
        _translate = QtCore.QCoreApplication.translate
        BugReport.setWindowTitle(_translate("BugReport", "Form"))
        self.title.setPlaceholderText(_translate("BugReport", "Issue Title:"))
        self.label.setText(_translate("BugReport", "TextLabel"))
        self.pushButton.setText(_translate("BugReport", "Submit Bug"))
