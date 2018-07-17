# Done by Frannecklp

from cv2 import cvtColor, COLOR_BGRA2RGB
from numpy import fromstring
from win32api import GetSystemMetrics
from win32con import SM_CXVIRTUALSCREEN, SM_CYVIRTUALSCREEN, SM_YVIRTUALSCREEN, SRCCOPY, SM_XVIRTUALSCREEN
from win32ui import CreateDCFromHandle, CreateBitmap
from win32gui import GetDesktopWindow, DeleteObject, GetWindowDC, ReleaseDC


def grab_screen(region=None):
    hwin = GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = GetSystemMetrics(SM_CXVIRTUALSCREEN)
        height = GetSystemMetrics(SM_CYVIRTUALSCREEN)
        left = GetSystemMetrics(SM_XVIRTUALSCREEN)
        top = GetSystemMetrics(SM_YVIRTUALSCREEN)

    hwindc = GetWindowDC(hwin)
    srcdc = CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), SRCCOPY)

    signed_ints_array = bmp.GetBitmapBits(True)
    img = fromstring(signed_ints_array, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    ReleaseDC(hwin, hwindc)
    DeleteObject(bmp.GetHandle())

    return cvtColor(img, COLOR_BGRA2RGB)
