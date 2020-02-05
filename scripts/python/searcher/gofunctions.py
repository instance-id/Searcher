import subprocess
import os

script_path = os.path.dirname(os.path.realpath(__file__))


class GoFunctions(object):
    def __init__(self):
        self.a = 1
        self.execlocation = os.environ['HOUDINI_USER_PREF_DIR']

    def callgofunction(self, params):
        houdinienv = os.environ.copy()
        path = os.path.join(script_path, 'go/searcher.exe')
        print self.execlocation
        print params
        goargs = [path, params]
        p = subprocess.Popen(
            goargs,
            # 'C:\Users\mosthated\Documents\houdini18.0\Searcher\csv1.exe',
            env=houdinienv,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        stdout, stderr = p.communicate()
        print (stdout, stderr)
