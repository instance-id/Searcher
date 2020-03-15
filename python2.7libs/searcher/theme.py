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
    if hver >= 395:
        from hutil.Qt import QtUiTools
    elif hver <= 394 and hver >= 391:
        from hutil.Qt import _QtUiTools
    elif hver < 391 and hver >= 348:
        from hutil.Qt import QtUiTools

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

    def __init__(self, parent=None):
        super(Theme, self).__init__(parent=parent)
        self.setParent(parent)
        self.ui = theme_ui.Ui_Theme()
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)

        self.settings = util.get_settings()
        self.colors = self.settings[util.SETTINGS_KEYS[14]]
        
        self.text1 = self.ui.text1
        self.text1.setText(self.settings[util.SETTINGS_KEYS[14]]['text1'])
        self.text1btn = self.ui.text1btn
        self.text1btn.setStyleSheet("background-color:" + self.text1.text())
        self.text1btn.setAutoFillBackground(True)
        self.text1btn.clicked.connect(self.chooseColor)
        
        self.text2 = self.ui.text2
        self.text2.setText(self.settings[util.SETTINGS_KEYS[14]]['text2'])
        self.text2btn = self.ui.text2btn
        self.text2btn.setStyleSheet("background-color:" + self.text2.text())
        self.text2btn.setAutoFillBackground(True)
        self.text2btn.clicked.connect(self.chooseColor)

        self.stats1 = self.ui.stats1
        self.stats1.setText(self.settings[util.SETTINGS_KEYS[14]]['stats1'])
        self.stats1btn = self.ui.stats1btn
        self.stats1btn.setStyleSheet("background-color:" + self.stats1.text())
        self.stats1btn.setAutoFillBackground(True)
        self.stats1btn.clicked.connect(self.chooseColor)

        self.stats2 = self.ui.stats2
        self.stats2.setText(self.settings[util.SETTINGS_KEYS[14]]['stats2'])
        self.stats2btn = self.ui.stats2btn
        self.stats2btn.setStyleSheet("background-color:" + self.stats2.text())
        self.stats2btn.setAutoFillBackground(True)
        self.stats2btn.clicked.connect(self.chooseColor)
                      
        self.save = self.ui.savetheme



        self.save.pressed.connect(self.save_cb)

    def save_cb(self):
        self.settings[util.SETTINGS_KEYS[14]]['text1'] = self.text1.text()
        self.settings[util.SETTINGS_KEYS[14]]['text2'] = self.text2.text()
        self.settings[util.SETTINGS_KEYS[14]]['stats1'] = self.stats1.text()
        self.settings[util.SETTINGS_KEYS[14]]['stats2'] = self.stats2.text()

        searcher_data.savesettings(self.settings[util.SETTINGS_KEYS[14]])

    def button1_cb(self):
        new_color = hou.ui.selectColor()
        self.button1.set

        color = hou.qt.toQColor(new_color)
        self.colorfield.setColor(color)
        hou.Color
        print(new_color)
        print(new_color.rgb())
        c = getHexColor(new_color)
        print(c)
        print(getRGBColor(c))

    def chooseColor(self):
        sender = self.sender()
        name = sender.objectName()
        colorfield = getattr(self, name)

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

