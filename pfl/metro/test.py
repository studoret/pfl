# -*- coding: utf-8 -*-
"""
module pfl.metro.test
Standalone application to test pfl.metro modules.

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

# boilerplate to allow running as script directly
if __name__ == "__main__" and __package__ is None:
  import sys, os
  # The following assumes the script is in the top level of the package
  # directory.  We use dirname() to help get the parent directory to add to
  # sys.path, so that we can import the current package.  This is necessary 
  # since when invoked directly, the 'current' package is not automatically
  # imported.
  parent_dir =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
  sys.path.insert(0, parent_dir)
  import pfl
  __package__ = str("pfl")
  del sys, os

  from metro import *
  from mgr import *
  from panel import *
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
    

  app = wx.PySimpleApp()
  frame = MyFrame(None, 'Python Foot Looper: test metronome')
  app.MainLoop()
  m.StartPlayback()


