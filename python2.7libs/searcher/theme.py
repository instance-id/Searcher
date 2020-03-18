from __future__ import print_function
from __future__ import absolute_import

from searcher import theme_ui
from searcher import util
from searcher import searcher_data

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
else:
    from PyQt5 import QtGui
    from PyQt5 import QtCore
    from PyQt5 import QtWidgets

scriptpath = os.path.dirname(os.path.realpath(__file__))

def name(**variables):
    return [x for x in variables]

def getHexColor(color):
    if isinstance(color, hou.Color):
        color = color.rgb()

    rgb = [('00' + hex(int(v * 0xff))[2:])[-2:] for v in color[:3]]
    return "#" + ''.join(rgb)

def getRGBColor(hex):
     hex = hex.lstrip('#')
     hlen = len(hex)
     return tuple(int(hex[i:i+hlen/3], 16) / 255.0 for i in range(0, hlen, hlen/3))

class Theme(QtWidgets.QWidget):
    """ Searcher coloring"""

    # --------------------------------------------------------------- Init
    # SECTION Init -------------------------------------------------------
    def __init__(self, parent=None):
        super(Theme, self).__init__(parent=parent)
        self.setParent(parent)
        self.parent = parent
        self.ui = theme_ui.Ui_Theme()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.settings = util.get_settings()
        self.colors = self.settings[util.SETTINGS_KEYS[14]]

        self.tabpanel = self.ui.tabWidget
        self.tabpanel.currentChanged.connect(self.curTabChange)

        self.tab1 = self.ui.tab
        self.tab1.setLayout(self.ui.r1)

        # --------------------------------------------------- Build Fields
        # SECTION Build Fields -------------------------------------------
        for i in range(len(util.COLORFIELDS)):
            # ---------------------------------- Colorfield
            # NOTE Colorfield -----------------------------
            v = getattr(self.ui, util.COLORFIELDS[i])
            v.setText(self.settings[util.SETTINGS_KEYS[14]][util.COLORFIELDS[i]])
            v.setVisible(True)

            # --------------------------- Colorfield Button
            # NOTE Colorfield Button ----------------------
            v_btn = getattr(self.ui, util.COLORFIELDS[i] + '_btn') 
            v_btn.setStyleSheet("background-color:" + v.text())
            v_btn.setAutoFillBackground(True)
            v_btn.clicked.connect(self.chooseColor)
            v_btn.setObjectName(util.COLORFIELDS[i])
            v_btn.setVisible(True)

            # ---------------------------- Colorfield Label
            # NOTE Colorfield Label -----------------------
            v_lbl = getattr(self.ui, util.COLORFIELDS[i] + '_lbl') 
            v_lbl.setVisible(True) 

        # !SECTION Build Fields

        self.save = self.ui.savetheme
        self.save.pressed.connect(self.save_cb)

        self.curTabChange(0)  
        self.installEventFilter(self)    

        # !SECTION Init              

    # ------------------------------------------------------------- Callbacks
    # SECTION Callbacks -----------------------------------------------------
    # ---------------------------------------- curTabChange
    # NOTE curTabChange -----------------------------------
    def curTabChange(self, index):
        for i in range(self.tabpanel.count()):
            if i == index:
                self.tabpanel.widget(i).setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            else:
                self.tabpanel.widget(i).setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)

    def save_cb(self):
        for i in range(len(util.COLORFIELDS)):
            self.settings[util.SETTINGS_KEYS[14]][util.COLORFIELDS[i]] = getattr(self.ui, util.COLORFIELDS[i]).text()
        
        searcher_data.savesettings(self.settings)
        self.parent.themebtn.setChecked(False)
        self.close()

    def chooseColor(self):
        sender = self.sender()
        name = sender.objectName()
        colorfield = getattr(self.ui, name)
        qcolor = QtGui.QColor()
        qcolor.setNamedColor(colorfield.text())
        color = hou.Color()
        color.setRGB((
            qcolor.redF(), 
            qcolor.greenF(), 
            qcolor.blueF())
        )

        result = hou.ui.selectColor(initial_color = color)
        
        if result:
            rgb = result.rgb()
            newcolor = QtGui.QColor(
                rgb[0]*255, 
                rgb[1]*255, 
                rgb[2]*255
            )
            
            if newcolor.isValid():
                colorfield.setText(newcolor.name())
                sender.setStyleSheet("background-color:" + colorfield.text())
    
    # !SECTION Callbacks

    # ------------------------------------------------------------- Events
    # SECTION Events -----------------------------------------------------
    def eventFilter(self, obj, event):
        # ------------------------------------------ Window
        # NOTE Window -------------------------------------
        if event.type() == QtCore.QEvent.Show:
            self.parent.ui.save_btn.setVisible(False)
            self.parent.ui.discard_btn.setVisible(False)
        if event.type() == QtCore.QEvent.Close:
            self.parent.ui.save_btn.setVisible(True)
            self.parent.ui.discard_btn.setVisible(True)

        return QtCore.QObject.eventFilter(self, obj, event)
    
    # !SECTION Events