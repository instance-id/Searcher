from __future__ import print_function
from __future__ import absolute_import

from searcher import theme_ui
from searcher import util
from searcher import settings_data
from searcher import style

import os
import sys

import hou
import hdefereval as hd
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
        self.parentwindow = parent
        self.ui = theme_ui.Ui_Theme()
        # !SECTION Init      
        

        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.colorfield = {}
        self.settings = util.get_settings()
        self.colors = self.settings[util.SETTINGS_KEYS[14]]
        self.coloreditor = None

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

        self.discard = self.ui.discardtheme
        self.discard.pressed.connect(self.discard_cb)

    def initmenu(self):
        self.curTabChange(0)  
        self.installEventFilter(self)    

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

    # --------------------------------------------- save_cb
    # NOTE save_cb ----------------------------------------
    def save_cb(self):
        for i in range(len(util.COLORFIELDS)):
            self.settings[util.SETTINGS_KEYS[14]][util.COLORFIELDS[i]] = getattr(self.ui, util.COLORFIELDS[i]).text()
        
        settings_data.savesettings(self.settings)
        self.parentwindow.themebtn.setChecked(False)
        self.close()

    # ------------------------------------------ discard_cb
    # NOTE discard_cb -------------------------------------
    def discard_cb(self):
        self.parentwindow.themebtn.setChecked(False)
        self.close()

    #-------------------------------------- colorchange_cb
    # NOTE colorchange_cb ---------------------------------
    def colorchange_cb(self, color, alpha=1.0):
        rgb = color.rgb()
        newcolor = QtGui.QColor(
            rgb[0]*255, 
            rgb[1]*255, 
            rgb[2]*255
        )

        if newcolor.isValid():
            demotext = ""
            self.colorfield[self.name][0].setText(newcolor.name())
            self.colorfield[self.name][1].setStyleSheet("background-color:" + self.colorfield[self.name][0].text())
            
            if self.colorfield[self.name][0] == getattr(self.ui, util.COLORFIELDS[0]):
                outdata = [0.100, 0.200, 0.300, 0.400, 0.500]
                demotxt = (("<font color='%s'>Search Regex <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(self.colorfield[self.name][0].text()), str(getattr(self.ui, util.COLORFIELDS[2]).text()), outdata[0])) 
              + ("<font color='%s'>Context Search <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(self.colorfield[self.name][0].text()), str(getattr(self.ui, util.COLORFIELDS[2]).text()), outdata[1])) 
              + ("<font color='%s'>Hotkey Search <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(self.colorfield[self.name][0].text()), str(getattr(self.ui, util.COLORFIELDS[2]).text()), outdata[2])) 
              + ("<font color='%s'>Tree build <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(self.colorfield[self.name][0].text()), str(getattr(self.ui, util.COLORFIELDS[2]).text()), outdata[3]))
              + ("<font color='%s'>Total : <font color='%s'> <b>%0.4f</b> </font> ms</font> " % (str(self.colorfield[self.name][0].text()), str(getattr(self.ui, util.COLORFIELDS[2]).text()), outdata[4])))
                self.parentwindow.parentwindow.infolbl.setText(demotxt)
                
            elif self.colorfield[self.name][0] == getattr(self.ui, util.COLORFIELDS[2]):
                outdata = [0.100, 0.200, 0.300, 0.400, 0.500]
                demotxt = (("<font color='%s'>Search Regex <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(getattr(self.ui, util.COLORFIELDS[0]).text()), str(self.colorfield[self.name][0].text()), outdata[0])) 
              + ("<font color='%s'>Context Search <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(getattr(self.ui, util.COLORFIELDS[0]).text()), str(self.colorfield[self.name][0].text()), outdata[1])) 
              + ("<font color='%s'>Hotkey Search <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(getattr(self.ui, util.COLORFIELDS[0]).text()), str(self.colorfield[self.name][0].text()), outdata[2])) 
              + ("<font color='%s'>Tree build <font color='%s'> <b>%0.4f</b> </font> ms</font> | " % (str(getattr(self.ui, util.COLORFIELDS[0]).text()), str(self.colorfield[self.name][0].text()), outdata[3]))
              + ("<font color='%s'>Total : <font color='%s'> <b>%0.4f</b> </font> ms</font> " % (str(getattr(self.ui, util.COLORFIELDS[0]).text()), str(self.colorfield[self.name][0].text()), outdata[4])))
                self.parentwindow.parentwindow.infolbl.setText(demotxt)

            elif self.colorfield[self.name][0] == getattr(self.ui, util.COLORFIELDS[4]):
                text = "This is an example of how the ToolTip text will look with this particular color"
                demotxt = ("<font color='%s'>%s</font>" % (self.colorfield[self.name][0].text(), text))
                self.parentwindow.parentwindow.infolbl.setText(demotxt)
            

    def _opencoloreditor(self, color):
        allWidgets = QtWidgets.QApplication.allWidgets()
        for w in allWidgets:
            if "Select Color" in w.windowTitle():
                self.coloreditor = w
                break

        if self.coloreditor:
            pos = self.parentwindow.mapToGlobal(
                QtCore.QPoint(self.parentwindow.width(), self.parentwindow.height()))
            self.coloreditor.setGeometry(
                pos.x() - ((self.parentwindow.width() * 1.55 ) + 20 ),
                pos.y() - self.parentwindow.height(),
                ((self.parentwindow.width() * 0.5) + 44),
                ((self.parentwindow.height() * 1.2) + 86)
            )
        self.parentwindow.parentwindow.activateWindow()  
        
    # ----------------------------------------- chooseColor
    # NOTE chooseColor ------------------------------------
    def chooseColor(self):
        sender = self.sender()
        
        self.name = sender.objectName()
        self.colorfield[self.name] = (getattr(self.ui, self.name), sender)
        
        qcolor = QtGui.QColor()
        qcolor.setNamedColor(self.colorfield[self.name][0].text())

        colord = QtWidgets.QColorDialog(self)
        colord.setModal(False)
        pos = self.parentwindow.mapToGlobal(
            QtCore.QPoint(self.parentwindow.width(), self.parentwindow.height()))
        colord.move(
            pos.x() + 300,
            pos.y(),
        )
        c = colord.getColor(
            initial=qcolor, 
            parent=self,
            options=QtWidgets.QColorDialog.DontUseNativeDialog
        )
        hcolor = hou.qt.fromQColor(c)

        self.colorchange_cb(hcolor[0])

    # !SECTION Callbacks

    # ------------------------------------------------------------- Events
    # SECTION Events -----------------------------------------------------
    def eventFilter(self, obj, event):
        event_type = event.type()

        # ------------------------------------------- Mouse
        # SECTION Mouse -----------------------------------
        # ----------------------- MouseButtonPress
        # NOTE MouseButtonPress ------------------
        # --- Empty for now ---
        # !SECTION Mouse

        # ------------------------------------------ Window
        # NOTE Window -------------------------------------
        if event_type == QtCore.QEvent.Show:
            self.parentwindow.ui.save_btn.setVisible(False)
            self.parentwindow.ui.discard_btn.setVisible(False)
        if event_type == QtCore.QEvent.Close:
            self.parentwindow.ui.save_btn.setVisible(True)
            self.parentwindow.ui.discard_btn.setVisible(True)

        # ---------------------------------------- Keypress
        # NOTE Keypress -----------------------------------
        if event_type == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                self.parentwindow.closeroutine()
                return True

        return QtCore.QObject.eventFilter(self, obj, event)

    # !SECTION Events