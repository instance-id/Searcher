import hou
import os
from hutil.Qt.QtCore import *
from hutil.Qt.QtGui import *
from hutil.Qt.QtWidgets import *
# import hutil.Qt
from parse import parsers
from . import database
from . import gofunctions

reload(parsers)
reload(database)
reload(gofunctions)

scriptpath = os.path.dirname(os.path.realpath(__file__))


class Searcher(QtWidgets.QWidget):
    """instance.id Searcher for Houdini"""
    def __init__(self):
        super(Searcher, self).__init__()

        self.proj = hou.getenv('JOB') + '/'
        self.scriptpath = os.path.dirname(os.path.realpath(__file__))
        self.parser = parsers.ParseData()

        # Load UI File
        loader = QtUiTools.QUiLoader()

        self.ui = loader.load(self.scriptpath +'/searcher.ui')

        # Get UI Elements
        self.setproject = self.ui.findChild(QtWidgets.QPushButton, "setproject")
        self.getpreferences = self.ui.findChild(QtWidgets.QPushButton, "test1_btn")
        self.getmenuitems = self.ui.findChild(QtWidgets.QPushButton, "test2_btn")
        self.callgo = self.ui.findChild(QtWidgets.QPushButton, "callGo_btn")
        self.gethotkeys = self.ui.findChild(QtWidgets.QPushButton, "getHotkeys_btn")
        self.savehotkeys = self.ui.findChild(QtWidgets.QPushButton, "saveHotkeys_btn")
        self.loadhotkeys = self.ui.findChild(QtWidgets.QPushButton, "loadHotkeys_btn")
        self.projectPath_lbl = self.ui.findChild(QtWidgets.QLabel, "projectPath_lbl")
        self.projectName_lbl = self.ui.findChild(QtWidgets.QLabel, "projectName_lbl")
        self.scenelist = self.ui.findChild(QtWidgets.QListWidget, "sceneList_lst")
        self.searchresultslst = self.ui.findChild(QtWidgets.QListWidget, "searchresults_lst")
        self.searchresultstbl = self.ui.findChild(QtWidgets.QTableWidget, "searchresults_tbl")        
        self.searchbox = self.ui.findChild(QtWidgets.QLineEdit, "searchbox")

        # Create Connections
        self.setproject.clicked.connect(self.setprojectfolder)
        self.getpreferences.clicked.connect(self.getpreferencenames_cb)
        self.getmenuitems.clicked.connect(self.indexitems_cb)
        self.gethotkeys.clicked.connect(self.gethotkeys_cb)
        self.savehotkeys.clicked.connect(self.savehotkeys_cb)
        self.loadhotkeys.clicked.connect(self.loadhotkeys_cb)
        self.callgo.clicked.connect(self.callgo_cb)
        self.searchbox.textChanged.connect(self.textchange_cb)
        
        # Layout
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)

    # ------------------------------------------------------------------------------------------------------------------ Interface Callbacks
    def getpreferencenames_cb(self):
        self.outputlist.clear()
        prefnames = hou.getPreferenceNames()
        for preference in prefnames:
            self.outputlist.addItem(preference)
        self.outputlist.doubleClicked.connect(self.preferenceItemDoubleClicked)   

    def indexitems_cb(self):
        self.parser.indexText()

    def gethotkeys_cb(self):
        data = self.parser.parseHotKeys()
        print data

    def savehotkeys_cb(self):
        data = self.parser.saveHotKeys()

    def loadhotkeys_cb(self):
        self.parser.parseHotKeys()

    def textchange_cb(self, text):
        self.searchresultslst.clear()
        if len(text) > 1:
            txt = self.parser.searchText(text)
            for line in txt:
                self.searchresultslst.addItem(str(line))
            self.searchtablepopulate(txt)
        else:
            self.searchresultstbl.clearContents()
            self.searchresultslst.clear()

    def searchclick_cb(self):
        self.searchresultslst.clear()
        return

    def callgo_cb(self):
        return
        # parsers.ParseData.parseHotKeys(self)

    def preferenceItemDoubleClicked(self, item):
        data = item.data()
        pref = hou.getPreference(data)
        print pref
        hou.ui.displayMessage(pref)
        hou.me

    def menuItemDoubleClicked(self, item):
        data = item.data()
        pref = hou.getPreference(data)
        print pref
        hou.ui.displayMessage(pref)

    # ------------------------------------------------------------------------------------------------------------------ Interface Actions
    def setprojectfolder(self):
        setJob = hou.ui.selectFile(title="Set Project", file_type=hou.fileType.Directory)
        hou.hscript("setenv JOB=" + setJob)
        self.proj = hou.getenv('JOB') + '/'

        projectname = setJob.split('/')[-2]
        setJob = os.path.dirname(setJob)
        projpath = os.path.split(setJob)[0]

        self.projectPath_lbl.setText(projpath + '/')
        self.projectName_lbl.setText(projectname)

        self.createinterface()
        
    def searchtablepopulate(self, data):
        rows = len(data)
        if rows > 0:
            cols=len(data[0])
            self.searchresultstbl.clearContents()
            self.searchresultstbl.setHorizontalHeaderLabels(['Label', 'Description', 'Assignments','Context'])
            self.searchresultstbl.setRowCount(rows)
            self.searchresultstbl.setColumnCount(cols)
            self.searchresultstbl.setColumnWidth(0, 100)
            self.searchresultstbl.setColumnWidth(1, 250)
            self.searchresultstbl.setColumnWidth(2, 100)
            self.searchresultstbl.setColumnWidth(3, 150)
            for i in range(rows):
                for j in range(cols):
                    newitem =  QTableWidgetItem(str(data[i][j]))
                    self.searchresultstbl.setItem(i,j,newitem)


    def openscene(self, item):
        hipFile = self.proj + item.data()
        hou.hipFile.load(hipFile)

    def createinterface(self):
        self.scenelist.clear()
        self.searchresultslst.clear()

        for file in os.listdir(self.proj):
            if file.endswith(".hiplc") or file.endswith(".hip"):
                self.scenelist.addItem(file)

        # Connect list items to function
        self.scenelist.doubleClicked.connect(self.openscene)
        self.searchresultslst.doubleClicked.connect(self.searchclick_cb)
        self.searchresultstbl.doubleClicked.connect(self.searchclick_cb)


def setup(self):
        return