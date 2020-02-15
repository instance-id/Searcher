import os

from .. import database

db = database.Databases()


class DataHandler(object):
    """Loads data from Houdini config files"""

    def __init__(self):
        self.scriptpath = os.path.dirname(os.path.realpath(__file__))

    # ------------------------------------------------------------------------------------------------------------------ Function calls
    # --------------------------------------------------- Retrieve
    def getchangeindex(self):
        index = db.getchangeindex()
        return index

    def getdefaulthotkey(self):
        index = db.getdefhotkey()
        return index

    # --------------------------------------------------- Updates
    def updatechangeindex(self, indexval, new=False):
        db.updatechangeindex(indexval, new)
        return

    def updatedata(self):
        db.updatecontext()
        return

    def updatetmphotkey(self, tmpkey):
        db.updatetmphk(tmpkey)
        return

    @staticmethod
    def gethcontext():
        results = db.gethcontexts()
        return results

    def gethcontextod(self, inputtext):
        results = db.gethcontextod(inputtext)
        return results

    def searchtext(self, txt):
        results = db.searchresults(txt)
        return results
