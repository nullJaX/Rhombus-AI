# coding=utf-8
# Citation: Box Of Hats (https://github.com/Box-Of-Hats )

from win32api import GetAsyncKeyState

keyList = [char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\"]


def key_check():
    return [key for key in keyList if GetAsyncKeyState(ord(key))]
