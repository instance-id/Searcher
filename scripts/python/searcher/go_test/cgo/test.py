from __future__ import print_function
from ctypes import *

lib = cdll.LoadLibrary("./readfile.so")


# define class GoString to map:
# C type struct { const char *p; GoInt n; }
# class GoString(Structure):
#     _fields_ = [("p", c_char_p)]


# describe and call Log()
lib.ReadKeyFile.argtypes = None
lib.ReadKeyFile.restype = None
# msg = GoString(b"Parsing hotkey file complete.")
print("Running: ")
lib.ReadKeyFile()

