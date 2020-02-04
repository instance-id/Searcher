from __future__ import print_function
import ctypes

lib = ctypes.cdll.LoadLibrary("./readfile.so")


# define class GoString to map:
# C type struct { const char *p; GoInt n; }
# class GoString(Structure):
#     _fields_ = [("p", c_char_p)]


def runcode():
    # msg = GoString(b"Parsing hotkey file complete.")
    print("Running: ")
    lib.ReadKeyFile()

