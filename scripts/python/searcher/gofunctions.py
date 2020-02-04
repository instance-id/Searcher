import subprocess
import os



class Databases(object):
    def __init__(self):
        self.a = 1
        self.independent_process = None
        self.execlocation = os.environ['HOUDINI_USER_PREF_DIR'] 
    
    def callgofunction(self, params):
        houdinienv = os.environ.copy()
        goargs = [params]
        self.independent_process = subprocess.Popen(
            self.execlocation + '/go/searcher.exe' + goargs[0],
            # 'C:\Users\mosthated\Documents\houdini18.0\Searcher\csv1.exe',
            env=houdinienv,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )