import subprocess
import os
import sys
from tempfile import SpooledTemporaryFile as tempfile

script_path = os.path.dirname(os.path.realpath(__file__))

if sys.platform == "win32":
    CREATE_NEW_PROCESS_GROUP = subprocess.CREATE_NEW_PROCESS_GROUP
else:
    CREATE_NEW_PROCESS_GROUP = None


class GoException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GoFunctions(object):
    def __init__(self):
        self.a = 1
        self.execlocation = os.environ["HOUDINI_USER_PREF_DIR"]

    def callgofunction(self, cmd, params):
        houdinienv = os.environ.copy()
        path = os.path.join(script_path, "go\searcher.exe")

        if len(params) > 0:
            cmdpayload = [path, cmd, params]
        else:
            cmdpayload = [path, cmd]

        try:
            r = subprocess.Popen(
                cmdpayload,
                env=houdinienv,
                shell=True,
                creationflags=CREATE_NEW_PROCESS_GROUP,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ).communicate()
            if len(r[1]) != 0:
                raise GoException(r[1])
            print (r[0], r[1])

        except Exception:
            import sys

            print sys.exc_info()[1]

