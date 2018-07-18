from ctypes import pointer, windll, c_ushort, c_long, sizeof, POINTER, c_short, Structure, c_ulong, Union
from random import choice
from time import sleep

SendInput = windll.user32.SendInput

UP = 0xC8
DOWN = 0xD0
LEFT = 0xCB
RIGHT = 0xCD
SPACE = 0x39

# C struct redefinitions
PUL = POINTER(c_ulong)


class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
                ("wScan", c_ushort),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
                ("wParamL", c_short),
                ("wParamH", c_ushort)]


class MouseInput(Structure):
    _fields_ = [("dx", c_long),
                ("dy", c_long),
                ("mouseData", c_ulong),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(Structure):
    _fields_ = [("type", c_ulong),
                ("ii", Input_I)]


# Actuals Functions

def PressKey(hex_key_code):
    extra = c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008, 0, pointer(extra))
    x = Input(c_ulong(1), ii_)
    windll.user32.SendInput(1, pointer(x), sizeof(x))


def ReleaseKey(hex_key_code):
    extra = c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008 | 0x0002, 0, pointer(extra))
    x = Input(c_ulong(1), ii_)
    windll.user32.SendInput(1, pointer(x), sizeof(x))


def PressNRealese(hex_key_code):
    PressKey(hex_key_code)
    sleep(0.001)
    ReleaseKey(hex_key_code)


# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

if __name__ == '__main__':
    while True:
        key = choice([UP, DOWN, LEFT, RIGHT, SPACE])
        PressNRealese(key)
