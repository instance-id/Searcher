import os
import sys
import platform
import ctypes

PLATFORM = None
SEARCHER_PATH = os.environ["SEARCHER"]

def get_platform():
    """Returns a string for the current platform"""
    global PLATFORM

    if PLATFORM is None:
        p = sys.platform
        if p == 'darwin':
            PLATFORM = 'darwin'
        elif p.startswith('win'):
            PLATFORM = 'windows'
        else:
            PLATFORM = 'unix'

    return PLATFORM

def get_sqlite():
    if  get_platform() == "Windows":
        path_sqlite_dll = os.path.join(SEARCHER_PATH, 'python27/dlls/sqlite3.dll')
        ctypes.cdll.LoadLibrary(path_sqlite_dll)
    elif  get_platform() == "Darwin":
        path_sqlite_dll = os.path.join(SEARCHER_PATH, 'python27/dlls/sqlite3.dll')
    else:
        path_sqlite_dll = os.path.join(SEARCHER_PATH, 'python27/dlls/sqlite3.dll')