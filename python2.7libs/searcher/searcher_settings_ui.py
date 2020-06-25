# -*- coding: utf-8 -*-
import os
hver = 0
if os.environ["HFS"] != "":
    ver = os.environ["HFS"]
    # hver = int(ver[ver.rindex('.')+1:])
    from hutil.Qt import QtGui
    from hutil.Qt import QtCore
    from hutil.Qt import QtWidgets
else:
    from qtpy import QtGui
    from qtpy import QtCore
    from qtpy import QtWidgets

def bc(v):
    return str(v).lower() in ("yes", "true", "t", "1")


class Ui_SearcherSettings(object):
    def setupUi(self, SearcherSettings, width, height, animated):
        self.width = width
        self.height = height
        self.animated = animated

        SearcherSettings.setObjectName("SearcherSettings")
        SearcherSettings.setWindowModality(QtCore.Qt.NonModal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SearcherSettings.sizePolicy().hasHeightForWidth())
        SearcherSettings.setSizePolicy(sizePolicy)
        SearcherSettings.setMinimumSize(QtCore.QSize(width, height))
        SearcherSettings.setBaseSize(QtCore.QSize(0, 0))

        self.gridLayout = QtWidgets.QGridLayout(SearcherSettings)
        self.gridLayout.setContentsMargins(-1, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.verticallayout = QtWidgets.QVBoxLayout()
        self.verticallayout.setObjectName("verticalLayout")
        self.verticallayout.setSpacing(10)

        # ------------------------------------------------- headerrow
        # NOTE headerrow --------------------------------------------
        self.headerrow = QtWidgets.QHBoxLayout()
        self.headerrow.setObjectName("headerrow")

        self.projectTitle = QtWidgets.QLabel(SearcherSettings)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.projectTitle.setFont(font)
        self.projectTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.projectTitle.setObjectName("projectTitle")
        self.headerrow.addWidget(self.projectTitle)

        spaceritem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.headerrow.addItem(spaceritem)

        self.animatedsettings_chk = QtWidgets.QCheckBox(SearcherSettings)
        self.animatedsettings_chk.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.animatedsettings_chk.setObjectName("animatedsettings_chk")
        self.headerrow.addWidget(self.animatedsettings_chk)

        self.windowsize_chk = QtWidgets.QCheckBox(SearcherSettings)
        self.windowsize_chk.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.windowsize_chk.setObjectName("windowsize_chk")
        self.headerrow.addWidget(self.windowsize_chk)
        self.verticallayout.addLayout(self.headerrow)

        self.line = QtWidgets.QFrame(SearcherSettings)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticallayout.addWidget(self.line)

        # ------------------------------------------------- secondrow
        # NOTE Second Row -------------------------------------------
        self.secondrow = QtWidgets.QHBoxLayout()
        self.secondrow.setObjectName("secondrow")

        # self.lang_cbox = QtWidgets.QComboBox(SearcherSettings)
        # self.lang_cbox.setObjectName("lang_cbox")
        # self.lang_cbox.addItem("")
        # self.secondrow.addWidget(self.lang_cbox)

        spaceritem = QtWidgets.QSpacerItem(
            40, 20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.secondrow.addItem(spaceritem)

        self.maxresults_lbl = QtWidgets.QLabel(SearcherSettings)
        self.maxresults_lbl.setObjectName("maxresults_lbl")
        self.secondrow.addWidget(self.maxresults_lbl)
        self.maxresults_txt = QtWidgets.QSpinBox(SearcherSettings)
        self.maxresults_txt.setMinimum(1)
        self.maxresults_txt.setMaximum(9999)
        self.maxresults_txt.setObjectName("maxresults_txt")
        self.secondrow.addWidget(self.maxresults_txt)

        self.inmemory_chk = QtWidgets.QCheckBox(SearcherSettings)
        self.inmemory_chk.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.inmemory_chk.setTristate(False)
        self.inmemory_chk.setObjectName("inmemory_chk")
        self.secondrow.addWidget(self.inmemory_chk)

        self.verticallayout.addLayout(self.secondrow)

        # -------------------------------------------------- thirdrow
        # NOTE Third Row --------------------------------------------
        self.thirdrow = QtWidgets.QHBoxLayout()
        self.thirdrow.setObjectName("thirdrow")

        self.defaulthotkey_lbl = QtWidgets.QLabel(SearcherSettings)
        self.defaulthotkey_lbl.setObjectName("defaulthotkey_lbl")
        self.thirdrow.addWidget(self.defaulthotkey_lbl)

        self.defaulthotkey_txt = QtWidgets.QLineEdit(SearcherSettings)
        self.defaulthotkey_txt.setToolTip("")
        self.defaulthotkey_txt.setReadOnly(True)
        self.defaulthotkey_txt.setObjectName("defaulthotkey_txt")
        self.thirdrow.addWidget(self.defaulthotkey_txt)

        self.hotkey_icon = QtWidgets.QToolButton(SearcherSettings)
        self.hotkey_icon.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.hotkey_icon.setObjectName("hotkey_icon")
        self.thirdrow.addWidget(self.hotkey_icon)
        self.verticallayout.addLayout(self.thirdrow)

        # ------------------------------------------------- fourthrow
        # NOTE Fourth Row -------------------------------------------
        self.fourthrow = QtWidgets.QHBoxLayout()
        self.fourthrow.setObjectName("fourthrow")

        self.dbpath_lbl = QtWidgets.QLabel(SearcherSettings)
        self.dbpath_lbl.setObjectName("dbpath_lbl")
        self.fourthrow.addWidget(self.dbpath_lbl)

        self.databasepath_txt = QtWidgets.QLineEdit(SearcherSettings)
        self.databasepath_txt.setObjectName("databasepath_txt")
        self.fourthrow.addWidget(self.databasepath_txt)

        self.dbpath_icon = QtWidgets.QToolButton(SearcherSettings)
        self.dbpath_icon.setObjectName("dbpath_icon")
        self.fourthrow.addWidget(self.dbpath_icon)

        self.verticallayout.addLayout(self.fourthrow)

        # -------------------------------------------------- fifthrow
        # NOTE Fifth Row --------------------------------------------
        self.fifthrow = QtWidgets.QHBoxLayout()
        self.fifthrow.setObjectName("fifthrow")

        # self.maint_lbl = QtWidgets.QLabel(SearcherSettings)
        # self.maint_lbl.setObjectName("maint_lbl")
        # self.fifthrow.addWidget(self.maint_lbl)

        # self.metrics_chk = QtWidgets.QCheckBox(SearcherSettings)
        # self.metrics_chk.setLayoutDirection(QtCore.Qt.RightToLeft)
        # self.metrics_chk.setTristate(False)
        # self.metrics_chk.setObjectName("metrics_chk")
        # self.fifthrow.addWidget(self.metrics_chk)

        # self.cleardata_btn = QtWidgets.QPushButton(SearcherSettings)
        # self.cleardata_btn.setObjectName("cleardata_btn")
        # self.fifthrow.addWidget(self.cleardata_btn)

        # self.verticallayout.addLayout(self.fifthrow)

        # ---------------------------------------------------- Spacer
        self.line2 = QtWidgets.QFrame(SearcherSettings)
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setObjectName("line2")
        self.verticallayout.addWidget(self.line2)
        # ---------------------------------------------------- Spacer

        # -------------------------------------------------- sixthrow
        # NOTE Sixth Row --------------------------------------------
        self.sixthrow = QtWidgets.QHBoxLayout()
        self.sixthrow.setObjectName("sixthrow")

        self.about_btn = QtWidgets.QToolButton(SearcherSettings)
        self.about_btn.setObjectName("about")
        self.sixthrow.addWidget(self.about_btn)

        self.bug_btn = QtWidgets.QToolButton(SearcherSettings)
        self.bug_btn.setObjectName("bugreport")
        self.sixthrow.addWidget(self.bug_btn)

        self.theme_btn = QtWidgets.QToolButton(SearcherSettings)
        self.theme_btn.setObjectName("theme")
        self.sixthrow.addWidget(self.theme_btn)

        spacerItem1 = QtWidgets.QSpacerItem(40, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.sixthrow.addItem(spacerItem1)


        self.metrics_chk = QtWidgets.QCheckBox(SearcherSettings)
        self.metrics_chk.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.metrics_chk.setTristate(False)
        self.metrics_chk.setObjectName("metrics_chk")
        self.sixthrow.addWidget(self.metrics_chk)


        self.debuglevel_cbx = QtWidgets.QComboBox(SearcherSettings)
        self.debuglevel_cbx.setObjectName("debuglevel_cbx")
        self.sixthrow.addWidget(self.debuglevel_cbx)

        self.debugflag_chk = QtWidgets.QCheckBox(SearcherSettings)
        self.debugflag_chk.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.debugflag_chk.setObjectName("debugflag_chk")
        self.sixthrow.addWidget(self.debugflag_chk)

        self.discard_btn = QtWidgets.QPushButton(SearcherSettings)
        self.discard_btn.setObjectName("discard_btn")
        self.sixthrow.addWidget(self.discard_btn)

        self.save_btn = QtWidgets.QPushButton(SearcherSettings)
        self.save_btn.setObjectName("save_btn")
        self.sixthrow.addWidget(self.save_btn)

        self.verticallayout.addLayout(self.sixthrow)

        if not self.animated:
            self.gridLayout.addLayout(self.verticallayout, 1, 0, 1, 1)

        # -----------------------------------------------------------
        self.retranslateUi(SearcherSettings)
        QtCore.QMetaObject.connectSlotsByName(SearcherSettings)

    def retranslateUi(self, SearcherSettings):
        _translate = QtCore.QCoreApplication.translate
        SearcherSettings.setWindowTitle(_translate("SearcherSettings", "Form"))

        # ------------------------------------------------- headerrow
        self.projectTitle.setText(_translate("SearcherSettings", "Settings"))
        self.animatedsettings_chk.setText(_translate("SearcherSettings", "Use Animated Menus:"))
        self.windowsize_chk.setText(_translate("SearcherSettings", "Remember Search Window Size"))

        # ------------------------------------------------- secondrow
        self.maxresults_lbl.setText(_translate("SearcherSettings", "Maximum Search Results"))
        self.inmemory_chk.setText(_translate("SearcherSettings", "Use In-Memory Database"))

        # -------------------------------------------------- thirdrow
        # self.label_3.setText(_translate("SearcherSettings", "Language:"))
        # self.lang_cbox.setCurrentText(_translate("SearcherSettings", "English"))
        # self.lang_cbox.setItemText(0, _translate("SearcherSettings", "English"))
        self.defaulthotkey_lbl.setText(_translate("SearcherSettings", "Hotkey to use for opening unassigned items: "))
        self.defaulthotkey_txt.setPlaceholderText(_translate("SearcherSettings", "Double Click"))
        self.hotkey_icon.setText(_translate("SearcherSettings", "..."))

        # ------------------------------------------------- fourthrow
        self.dbpath_lbl.setText(_translate("SearcherSettings", "Database location: "))
        self.dbpath_icon.setText(_translate("SearcherSettings", "..."))

        # -------------------------------------------------- fifthrow
        # self.maint_lbl.setText(_translate("SearcherSettings", "Maintenance utilities:"))
        # self.cleardata_btn.setText(_translate("SearcherSettings", "Clear Data"))

        # ------------------------------------------------- sixthrow
        self.about_btn.setText(_translate("SearcherSettings", "..."))
        self.bug_btn.setText(_translate("SearcherSettings", "..."))
        self.theme_btn.setText(_translate("SearcherSettings", "..."))
        self.metrics_chk.setText(_translate("SearcherSettings", "Metrics"))
        self.debugflag_chk.setText(_translate("SearcherSettings", "Debug Mode"))
        self.discard_btn.setText(_translate("SearcherSettings", "Discard"))
        self.save_btn.setText(_translate("SearcherSettings", "Save"))

