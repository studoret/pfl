#! /usr/bin/env python
import pyo, wx
from ls_metro import *
from ls_metro_mgr import *
from ls_metro_panel import *
from ls_cp import *

s = pyo.Server().boot()
s.start()

m = Metro()
    

class MyFrame(wx.Frame):
  def __init__(self, parent, title): 
    wx.Frame.__init__(self, parent, -1, title)
    self.fSizer = wx.BoxSizer(wx.VERTICAL)

    self.controlPanel = ControlPanel(self)
    self.fSizer.Add(self.controlPanel, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)

    self.metroPanel = MetroPanel(self)
    self.fSizer.Add(self.metroPanel, 1, wx.EXPAND)

    self.SetSizer(self.fSizer)

    self.manager = MetroManager(self.controlPanel, m, self.metroPanel)
    self.Centre()
    self.Show()
    self.fSizer.Layout()
    wx.CallAfter(self.Fit)


app = wx.PySimpleApp()
frame = MyFrame(None, 'LoopStation')
app.MainLoop()

m.StartPlayback()

s.gui(locals)

