import os

from .. import database

db = database.Databases()


class DataHandler(object):
    """Loads data from Houdini config files"""
    def __init__(self):
        self.scriptpath = os.path.dirname(os.path.realpath(__file__))

    # ------------------------------------------------------------------------------------------------------------------ Function calls
    def updatehotkeys(self):
        # for filename in os.listdir(self.hotkeypath):
        return
    
    

    @staticmethod
    def searchtext(txt):
        results = db.searchresults(txt)
        return results
