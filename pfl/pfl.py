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
from track.panel import *
from track.mgr import *

from utils.action import *

s = pyo.Server().boot()
s.start()
m = Metro()

class PanelManager():
  PEDALS_PANEL = 0
  METRO_PANEL  = 1
  FIRST_SOUNDTRACK_PANEL = 2
  def __init__(self, frame):
    self.__tracksPanel = [TrackPanel(frame)]
    self.__currentTrackId = self.__class__.METRO_PANEL
    self.__increment = 1
    self.__panels = [PedalsPanel(frame), MetroPanel(frame)]
    controlPanel = self.__panels[self.__class__.PEDALS_PANEL]
    self.__panels.extend(self.__tracksPanel)
    for panel in self.__panels:
      frame.fSizer.Add(panel, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
    self.__action = ActionCursor("TRACK    ",self.TrackUp, self.TrackDown)
    controlPanel.SetTitle(0, self.__action.GetTitle())  
    controlPanel.SetSubtitle(0, self.__action.GetSubtitle())  
    controlPanel.AddManager(self)
    self.metroManager = MetroManager(controlPanel, m, self.__panels[self.__class__.METRO_PANEL])
    self.tracksManager = TracksManager(m, self, controlPanel)
    self.tracksManager.AddTrack(Track(self.__tracksPanel[0]))
    self.DoSelection(self.__currentTrackId)

  def DoSelection(self, trackId):
    self.__panels[trackId].Select()
    if trackId == self.__class__.METRO_PANEL:
      self.tracksManager.Deselect()
      self.metroManager.Select()
    else:
      self.metroManager.Deselect()
      self.tracksManager.Select()
    self.tracksManager.SetCurrentTrackID(trackId - self.__class__.FIRST_SOUNDTRACK_PANEL)
    
  def ChangeSelection(self):
    oldId = self.__currentTrackId
    self.__currentTrackId += self.__increment
    if self.__currentTrackId == self.__class__.PEDALS_PANEL:
      self.__currentTrackId = len(self.__panels) - 1
    if self.__currentTrackId == len(self.__panels):
      self.__currentTrackId = self.__class__.PEDALS_PANEL + 1
    self.__panels[oldId].Deselect()
    self.DoSelection(self.__currentTrackId)

  def TrackUp(self):
    self.__increment = 1
    self.ChangeSelection()

  def TrackDown(self):
    self.__increment = -1
    self.ChangeSelection()

  def PedalDown(self, pedalId, keyDownCount):
    print "pedalDown = " + str(pedalId) + " " + str(keyDownCount)
    if pedalId == 0 and keyDownCount >= 2:
      self.__action.Reverse()

  def PedalUp(self, pedalId, keyDownCount):
    print "pedalUp = " + str(pedalId) + " " + str(keyDownCount)
    if pedalId == 0 and keyDownCount < 2:
      self.__action.Select()


class MyFrame(wx.Frame):
  def __init__(self, parent, title): 
    wx.Frame.__init__(self, parent, -1, title)
    self.fSizer = wx.BoxSizer(wx.VERTICAL) 
    self.mgr = PanelManager(self) 
      
    self.SetSizer(self.fSizer)
    
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


