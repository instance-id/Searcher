from __future__ import print_function
from ctypes import *

lib = cdll.LoadLibrary("./readfile.so")


# define class GoString to map:
# C type struct { const char *p; GoInt n; }
class GoString(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]


# describe and call Log()
lib.ReadKeyFile.argtypes = [GoString]
lib.ReadKeyFile.restype = c_longlong
msg = GoString(b"Parsing hotkey file complete.", 13)
print("Running: %d"% lib.ReadKeyFile(msg))

