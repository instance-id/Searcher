import os
import re
import csv as read
from itertools import dropwhile

from .. import database

db = database.Databases()

def normalize_whitespace(stri):
    """Remove whitespace from import"""
    stri = stri.strip()
    stri = re.sub(r'\s+', ' ', stri)
    return stri

class ParseData(object):
    """Loads data from Houdini config files"""
    def __init__(self):
        self.scriptpath = os.path.dirname(os.path.realpath(__file__))
        self.hotkeypath = (os.environ['HFS'] + '/houdini/config/Hotkeys/')
        self.hotkeyfields = ['hotkey_symbol', 'label', 'description', 'assignments']
        self.remove_comments = ['//']

    def iteratekeyfiles(self, filename):
        keyslist = []
        with open(self.hotkeypath + filename, 'rb') as hotkeyfile:
            start = dropwhile(lambda L: not L.lower().lstrip().startswith('//'), hotkeyfile)
            reader = read.DictReader(((normalize_whitespace(line)) for line in start), fieldnames=self.hotkeyfields, delimiter=' ')
            for row in reader:
                column = row['hotkey_symbol']
                if not any(remove_word in column for remove_word in self.remove_comments):
                    for idx, val in enumerate(row):
                        if val is None:
                            row.__setitem__(self.hotkeyfields[idx], [row['assignments'], row[val][0]])
                    keyslist.append([row['hotkey_symbol'], row['label'], row['description'], row['assignments']])

        hotkeyfile.close()
        result = {filename: keyslist}
        return result

    def parseHotKeys(self, filename):
            result = self.iteratekeyfiles(filename)
            return result

    def saveHotKeys(self):
        #for filename in os.listdir(self.hotkeypath):
        data = self.parseHotKeys("h.pane")
        db.savetodatabase(data)

    def searchText(self, txt):
        results = self.loaddata(txt)
        return results

    def loaddata(self, txt):
        result = db.searchresults(txt)
        return result

    def indexText(self):
        result = db.performindex()


# Tests ------
# keyfiles = data.keys()
# for keys in keyfiles:
#     print ("Adding " + keys + " to database")
#     for i in range(len(data[keys])):
#         if data[keys][i][0] == "HCONTEXT":
#             print ("HEADER: ", data[keys][i][0])
#         else:
#             print ("DATA: ", data[keys][i][0])  