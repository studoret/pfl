"""
module pfl.track.mgr
Manager of pfl.track.track object .

"""

"""
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
along with pfl.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys, os
parent_dir =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)
import pfl
__package__ = str("pfl")
del sys, os

from utils.action import *
from track import *

class TracksManager():
  def __init__(self, controlPanel):
    self.__selected = False
    self.__menu =  ActionMenu()
    self.__menu.Add(ActionSwitch(0, "LOOP ON  ", "LOOP OFF ", self.LoopOn, self.LoopOff))
    self.__menu.Add(ActionCursor("VOL.     ", self.VolUp, self.VolDown))
    self.__playBack = ActionSwitch(0, "START    ", "STOP  ", self.StartPlayback, self.StopPlayback)
    self.__cp = controlPanel
    self.__cp.AddManager(self)

  def Select(self):
    self.__selected = True
    self.__cp.SetTitle(1, self.__menu.GetTitle())  
    self.__cp.SetSubtitle(1, self.__menu.GetSubtitle())  
    self.__cp.SetTitle(2, self.__menu.GetActionTitle()) 
    self.__cp.SetSubtitle(2, self.__menu.GetActionSubtitle()) 
    self.__cp.SetTitle(3, self.__playBack.GetTitle()) 
    self.__cp.SetSubtitle(3, self.__playBack.GetSubtitle())

  def Deselect(self):
    self.__selected = False

  def StartPlayback(self):
    print "StartPlayback"

  def StopPlayback(self):
    print "StopPlayback"

  def VolDown(self):
    print "VolDown"

  def VolUp(self):
    print "VolUp"

  def LoopOn(self):
    print "LoopOn"

  def LoopOff(self):
    print "LoopOff"

  def PedalDown(self, pedalId, keyDownCount):
    if self.__selected == False or pedalId == 0:
      return
    if pedalId == 1:
      if keyDownCount >= 2:
        self.__menu.Reverse()
        self.__cp.SetSubtitle(pedalId, self.__menu.GetSubtitle())
      return
    if pedalId == 2:
      action = self.__menu.GetCurrentAction()
      if action != None:
        if keyDownCount >= 2:
          action.Reverse()
          self.__cp.SetSubtitle(pedalId, action.GetSubtitle())
      return
    if pedalId == 3:
      self.__playBack.Select()
      self.__cp.SetTitle(pedalId, self.__playBack.GetTitle())

  def PedalUp(self, pedalId, keyDownCount):
    if self.__selected == False or pedalId == 0:
      return
    if pedalId == 1:
      if keyDownCount < 2:
        self.__menu.Select()
        self.__cp.SetTitle(pedalId + 1, self.__menu.GetActionTitle())
        self.__cp.SetSubtitle(pedalId + 1, self.__menu.GetActionSubtitle())
      return
    if pedalId == 2:
      action = self.__menu.GetCurrentAction()
      if action != None:
        if keyDownCount < 2:
          action.Select()
          self.__cp.SetTitle(pedalId,action.GetTitle())
          self.__cp.SetSubtitle(pedalId,action.GetSubtitle())
      return
