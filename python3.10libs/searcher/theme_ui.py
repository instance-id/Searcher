from hutil.Qt import QtCore, QtGui, QtWidgets
import os

scriptpath = os.path.dirname(os.path.realpath(__file__))


class Ui_Theme(object):
    def setupUi(self, Theme):
        Theme.setObjectName("Theme")
        Theme.setWindowModality(QtCore.Qt.NonModal)
        Theme.resize(450, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Theme.sizePolicy().hasHeightForWidth())
        Theme.setSizePolicy(sizePolicy)
        Theme.setMinimumSize(QtCore.QSize(100, 0))
        Theme.setBaseSize(QtCore.QSize(0, 0))
        Theme.setStyleSheet("") 
        self.gridLayout = QtWidgets.QGridLayout(Theme)
        self.gridLayout.setContentsMargins(-1, -1, -1, 6)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.r2 = QtWidgets.QVBoxLayout()
        self.r2.setObjectName("r2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.discardtheme = QtWidgets.QPushButton(Theme)
        self.discardtheme.setObjectName("discardtheme")
        self.horizontalLayout_2.addWidget(self.discardtheme)
        self.savetheme = QtWidgets.QPushButton(Theme)
        self.savetheme.setObjectName("savetheme")
        self.horizontalLayout_2.addWidget(self.savetheme)
        self.r2.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.r2, 2, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Theme)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.layoutWidget = QtWidgets.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 533, 164))
        self.layoutWidget.setObjectName("layoutWidget")
        self.r1 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.r1.setContentsMargins(6, 6, 6, 0)
        self.r1.setObjectName("r1")
        self.c1 = QtWidgets.QVBoxLayout()
        self.c1.setObjectName("c1")
        self.h4_c1 = QtWidgets.QHBoxLayout()
        self.h4_c1.setObjectName("h4_c1")
        self.text2_lbl = QtWidgets.QLabel(self.layoutWidget)
        self.text2_lbl.setObjectName("text2_lbl")
        self.h4_c1.addWidget(self.text2_lbl)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.h4_c1.addItem(spacerItem1)
        self.text2_btn = QtWidgets.QToolButton(self.layoutWidget)
        self.text2_btn.setText("")
        self.text2_btn.setObjectName("text2_btn")
        self.h4_c1.addWidget(self.text2_btn)
        self.text2 = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text2.sizePolicy().hasHeightForWidth())
        self.text2.setSizePolicy(sizePolicy)
        self.text2.setMinimumSize(QtCore.QSize(75, 0))
        self.text2.setMaximumSize(QtCore.QSize(75, 16777215))
        self.text2.setBaseSize(QtCore.QSize(75, 0))
        self.text2.setReadOnly(True)
        self.text2.setObjectName("text2")
        self.h4_c1.addWidget(self.text2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.h4_c1.addItem(spacerItem2)
        self.c1.addLayout(self.h4_c1)
        self.h1_c2 = QtWidgets.QHBoxLayout()
        self.h1_c2.setObjectName("h1_c2")
        self.tooltip_lbl = QtWidgets.QLabel(self.layoutWidget)
        self.tooltip_lbl.setObjectName("tooltip_lbl")
        self.h1_c2.addWidget(self.tooltip_lbl)
        self.tooltip_btn = QtWidgets.QToolButton(self.layoutWidget)
        self.tooltip_btn.setText("")
        self.tooltip_btn.setObjectName("tooltip_btn")
        self.h1_c2.addWidget(self.tooltip_btn)
        self.tooltip = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tooltip.sizePolicy().hasHeightForWidth())
        self.tooltip.setSizePolicy(sizePolicy)
        self.tooltip.setMinimumSize(QtCore.QSize(75, 0))
        self.tooltip.setMaximumSize(QtCore.QSize(75, 16777215))
        self.tooltip.setReadOnly(True)
        self.tooltip.setObjectName("tooltip")
        self.h1_c2.addWidget(self.tooltip)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.h1_c2.addItem(spacerItem3)
        self.c1.addLayout(self.h1_c2)
        self.h3_c1 = QtWidgets.QHBoxLayout()
        self.h3_c1.setObjectName("h3_c1")
        self.text1_lbl = QtWidgets.QLabel(self.layoutWidget)
        self.text1_lbl.setObjectName("text1_lbl")
        self.h3_c1.addWidget(self.text1_lbl)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.h3_c1.addItem(spacerItem4)
        self.text1_btn = QtWidgets.QToolButton(self.layoutWidget)
        self.text1_btn.setText("")
        self.text1_btn.setObjectName("text1_btn")
        self.h3_c1.addWidget(self.text1_btn)
        self.text1 = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text1.sizePolicy().hasHeightForWidth())
        self.text1.setSizePolicy(sizePolicy)
        self.text1.setMinimumSize(QtCore.QSize(75, 0))
        self.text1.setMaximumSize(QtCore.QSize(75, 16777215))
        self.text1.setBaseSize(QtCore.QSize(75, 0))
        self.text1.setReadOnly(True)
        self.text1.setObjectName("text1")
        self.h3_c1.addWidget(self.text1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.h3_c1.addItem(spacerItem5)
        self.c1.addLayout(self.h3_c1)
        self.h2_c1 = QtWidgets.QHBoxLayout()
        self.h2_c1.setObjectName("h2_c1")
        self.stats1_lbl = QtWidgets.QLabel(self.layoutWidget)
        self.stats1_lbl.setObjectName("stats1_lbl")
        self.h2_c1.addWidget(self.stats1_lbl)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.h2_c1.addItem(spacerItem6)
        self.stats1_btn = QtWidgets.QToolButton(self.layoutWidget)
        self.stats1_btn.setText("")
        self.stats1_btn.setObjectName("stats1_btn")
        self.h2_c1.addWidget(self.stats1_btn)
        self.stats1 = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stats1.sizePolicy().hasHeightForWidth())
        self.stats1.setSizePolicy(sizePolicy)
        self.stats1.setMinimumSize(QtCore.QSize(75, 0))
        self.stats1.setMaximumSize(QtCore.QSize(75, 16777215))
        self.stats1.setBaseSize(QtCore.QSize(75, 0))
        self.stats1.setReadOnly(True)
        self.stats1.setObjectName("stats1")
        self.h2_c1.addWidget(self.stats1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.h2_c1.addItem(spacerItem7)
        self.c1.addLayout(self.h2_c1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.c1.addItem(spacerItem8)
        self.r1.addLayout(self.c1)
        self.c2 = QtWidgets.QVBoxLayout()
        self.c2.setObjectName("c2")
        self.h1_c1 = QtWidgets.QHBoxLayout()
        self.h1_c1.setObjectName("h1_c1")
        self.stats2_lbl = QtWidgets.QLabel(self.layoutWidget)
        self.stats2_lbl.setObjectName("stats2_lbl")
        self.h1_c1.addWidget(self.stats2_lbl)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.h1_c1.addItem(spacerItem9)
        spacerItem10 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.h1_c1.addItem(spacerItem10)
        self.stats2_btn = QtWidgets.QToolButton(self.layoutWidget)
        self.stats2_btn.setText("")
        self.stats2_btn.setObjectName("stats2_btn")
        self.h1_c1.addWidget(self.stats2_btn)
        self.stats2 = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stats2.sizePolicy().hasHeightForWidth())
        self.stats2.setSizePolicy(sizePolicy)
        self.stats2.setMinimumSize(QtCore.QSize(75, 0))
        self.stats2.setMaximumSize(QtCore.QSize(75, 16777215))
        self.stats2.setBaseSize(QtCore.QSize(75, 0))
        self.stats2.setReadOnly(True)
        self.stats2.setObjectName("stats2")
        self.h1_c1.addWidget(self.stats2)
        self.c2.addLayout(self.h1_c1)
        self.h2_c2 = QtWidgets.QHBoxLayout()
        self.h2_c2.setObjectName("h2_c2")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.label_7.setEnabled(True)
        self.label_7.setObjectName("label_7")
        self.h2_c2.addWidget(self.label_7)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.h2_c2.addItem(spacerItem11)
        self.toolButton_6 = QtWidgets.QToolButton(self.layoutWidget)
        self.toolButton_6.setText("")
        self.toolButton_6.setObjectName("toolButton_6")
        self.h2_c2.addWidget(self.toolButton_6)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(75, 0))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(75, 16777215))
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.h2_c2.addWidget(self.lineEdit_3)
        self.c2.addLayout(self.h2_c2)
        self.h3_c2 = QtWidgets.QHBoxLayout()
        self.h3_c2.setObjectName("h3_c2")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.h3_c2.addWidget(self.label_6)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.h3_c2.addItem(spacerItem12)
        self.toolButton_7 = QtWidgets.QToolButton(self.layoutWidget)
        self.toolButton_7.setText("")
        self.toolButton_7.setObjectName("toolButton_7")
        self.h3_c2.addWidget(self.toolButton_7)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(75, 0))
        self.lineEdit_4.setMaximumSize(QtCore.QSize(75, 16777215))
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.h3_c2.addWidget(self.lineEdit_4)
        self.c2.addLayout(self.h3_c2)
        self.h4_c2 = QtWidgets.QHBoxLayout()
        self.h4_c2.setObjectName("h4_c2")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.h4_c2.addWidget(self.label_5)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.h4_c2.addItem(spacerItem13)
        self.toolButton_8 = QtWidgets.QToolButton(self.layoutWidget)
        self.toolButton_8.setText("")
        self.toolButton_8.setObjectName("toolButton_8")
        self.h4_c2.addWidget(self.toolButton_8)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(75, 0))
        self.lineEdit.setMaximumSize(QtCore.QSize(75, 16777215))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.h4_c2.addWidget(self.lineEdit)
        self.c2.addLayout(self.h4_c2)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.c2.addItem(spacerItem14)
        self.r1.addLayout(self.c2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Theme)
        self.setVisibility()
        QtCore.QMetaObject.connectSlotsByName(Theme)

    def retranslateUi(self, Theme):
        _translate = QtCore.QCoreApplication.translate
        Theme.setWindowTitle(_translate("Theme", "Form"))
        self.discardtheme.setText(_translate("Theme", "Discard"))
        self.savetheme.setText(_translate("Theme", "Save"))
        self.text2_lbl.setText(_translate("Theme", "Search Results Context"))
        self.tooltip_lbl.setText(_translate("Theme", "Tool Tip Info"))
        self.text1_lbl.setText(_translate("Theme", "Result Stats Text"))
        self.stats1_lbl.setText(_translate("Theme", "Result Stat Values"))
        self.stats2_lbl.setText(_translate("Theme", "Secondary Stat Values"))
        self.label_7.setText(_translate("Theme", "TextLabel"))
        self.label_6.setText(_translate("Theme", "TextLabel"))
        self.label_5.setText(_translate("Theme", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Theme", "Text"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Theme", "Window"))

    def setVisibility(self):
        self.label_7.setVisible(False)
        self.label_6.setVisible(False)
        self.label_5.setVisible(False)
        self.stats2_lbl.setVisible(False)

        self.lineEdit_4.setVisible(False)
        self.lineEdit_3.setVisible(False)     
        self.lineEdit.setVisible(False)
        self.stats2.setVisible(False)

        self.toolButton_6.setVisible(False)
        self.toolButton_7.setVisible(False)
        self.toolButton_8.setVisible(False)
        self.stats2_btn.setVisible(False)