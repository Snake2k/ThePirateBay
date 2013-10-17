'''
Main file for executing the GUI interface.
'''
import wx
from TBP import TPBFrame

if __name__ == '__main__':
    APP = wx.App()
    FRAME = TPBFrame(None)
    FRAME.Show()
    APP.MainLoop()
