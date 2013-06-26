# -*- coding: utf-8 -*-
"""
Main file of pfl application.

############
Copyright 2013 Stephane Tudoret

This file is part of pfl, a python foot looper application.

pfl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pfl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pfl.  If not, see http://www.gnu.org/licenses/.
"""

import pyo, wx
  
from metro.metro import *
from metro.panel import *
from metro.mgr import *
from pedals.panel import *

s = pyo.Server().boot()
s.start()
m = Metro()

class MyFrame(wx.Frame):
  def __init__(self, parent, title): 
    wx.Frame.__init__(self, parent, -1, title)
    self.fSizer = wx.BoxSizer(wx.VERTICAL)  
    self.pedalsPanel = PedalsPanel(self)
    self.fSizer.Add(self.pedalsPanel, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
      
    self.metroPanel = MetroPanel(self)
    self.fSizer.Add(self.metroPanel, 1, wx.EXPAND)
      
    self.SetSizer(self.fSizer)
    
    self.manager = MetroManager(self.pedalsPanel, m, self.metroPanel)
    self.manager.Select()
    self.Centre()
    self.Show()
    self.fSizer.Layout()
    wx.CallAfter(self.Fit)

# boilerplate to allow running as script directly
if __name__ == "__main__" and __package__ is None:
 
  app = wx.PySimpleApp()
  frame = MyFrame(None, 'Python Foot Looper: test metronome')
  app.MainLoop()
  m.StartPlayback()


