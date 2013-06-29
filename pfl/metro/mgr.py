"""
module pfl.metro.mgr
Manager of pfl.metro.metro object .

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

from metro import *
import time

class ActionTap(Action):
  subtitles = ["(", ")"]
  def __init__(self, setBpmFunction):
    self.__state = 0
    Action.__init__(self, "TAP     ", self.__class__.subtitles[self.__state])
    self.__begin = None
    self.__setBpm = setBpmFunction

  def Select(self):
    if self.__begin == None:
      self.__state = 1
      self.__begin = time.time()
      return
    self.__state = 0
    bpm = int(60 / (time.time() - self.__begin))
    self.__setBpm(bpm)
    self.__begin = None
    
  def GetSubtitle(self):
    return self.__class__.subtitles[self.__state]

class MetroManager():
  def __init__(self, controlPanel, metro, metroPanel):
    self.__metro = metro
    self.__selected = False
    self.__menu =  ActionMenu()
    self.__menu.Add(ActionCursor("TEMPO   ",self.__metro.TempoUp, self.__metro.TempoDown))
    self.__menu.Add(ActionCursor("BEAT    ",self.__metro.BeatUp, self.__metro.BeatDown))
    self.__menu.Add(ActionCursor("VOL.    ",self.__metro.MulUp, self.__metro.MulDown))
    self.__menu.Add(ActionTap(self.__metro.ForceTempo))
    self.__mute = ActionSwitch(0, "SOUND ON  ", "SOUND OFF ", self.__metro.StartPlayback, self.__metro.StopPlayback)
    self.__metro.AddMonitor(self)
    self.__cp = controlPanel
    self.__cp.AddManager(self)
    self.__metroPanel = metroPanel
    self.Refresh()

  def Select(self):
    self.__selected = True
    self.__cp.SetTitle(1, self.__menu.GetTitle())  
    self.__cp.SetSubtitle(1, self.__menu.GetSubtitle())  
    self.__cp.SetTitle(2, self.__menu.GetActionTitle()) 
    self.__cp.SetSubtitle(2, self.__menu.GetActionSubtitle()) 
    self.__cp.SetTitle(3, self.__mute.GetTitle()) 
    self.__cp.SetSubtitle(3, self.__mute.GetSubtitle())

  def Deselect(self):
    self.__selected = False

  def GetCurrentAction(self):
    return self.__actions[self.__actionIdx]

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
      self.__mute.Select()
      self.__cp.SetTitle(pedalId, self.__mute.GetTitle())

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
 
  def Refresh(self):
    self.__metroPanel.RefreshTempo(str(self.__metro.GetTempo()))
    self.__metroPanel.RefreshMul(str(self.__metro.GetMul()))
    beat = self.__metro.GetBeat()
    if beat < 10:
      beatStr = " "+str(beat)
    else:
      beatStr = str(beat)
    self.__metroPanel.RefreshBeat(beatStr)

  def Tick(self):
    tick = self.__metro.GetTick()
    if tick == 1:
      color = "green"
    else:
      color = "blue"
    self.__metroPanel.RefreshTick(str(tick), color)
      
                   
