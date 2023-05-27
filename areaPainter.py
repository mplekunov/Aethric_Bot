import win32con
import win32gui
import win32api

import ctypes

from area import Area

class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [
        ("BlendOp", ctypes.c_byte),
        ("BlendFlags", ctypes.c_byte),
        ("SourceConstantAlpha", ctypes.c_byte),
        ("AlphaFormat", ctypes.c_byte)
    ]

class AreaPainter(object):
    def __init__(self, window_name):
        self.window_name = window_name
    
    def draw_border(self, area: Area, border_width=1):
        hwnd = win32gui.FindWindow(self.window_name, None)
        dc = win32gui.GetWindowDC(hwnd)

        # Set the blend function for transparency
        blend_func = BLENDFUNCTION()
        blend_func.BlendOp = win32con.AC_SRC_OVER
        blend_func.BlendFlags = 0
        blend_func.SourceConstantAlpha = 0
        blend_func.AlphaFormat = win32con.AC_SRC_ALPHA

        # Create a pen for the border
        pen_color = win32api.RGB(0, 255, 0)
        pen = win32gui.CreatePen(win32con.PS_SOLID, border_width, pen_color)

        # Set the device context properties
        win32gui.SetBkMode(dc, win32con.TRANSPARENT)
        win32gui.SetTextColor(dc, pen_color)
        win32gui.SelectObject(dc, win32gui.GetStockObject(win32con.DEVICE_DEFAULT_FONT))
        win32gui.SelectObject(dc, pen)
        win32gui.SetGraphicsMode(dc, win32con.GM_ADVANCED)

        # Draw the rectangle with the border
        rect = (area.top_left.x, area.top_left.y, area.bottom_right.x, area.bottom_right.y)
        win32gui.FrameRect(dc, rect, pen)

        win32gui.DrawText(dc, "{:.2f}".format(area.confidence), -1, rect, win32con.DT_LEFT | win32con.DT_LEFT | win32con.DT_SINGLELINE)

        # Cleanup
        win32gui.DeleteObject(pen)
        win32gui.ReleaseDC(hwnd, dc)
    
    def clean_window(self):
        hwnd = win32gui.FindWindow(self.window_name, None)        
        win32gui.InvalidateRect(hwnd, None, True)
        