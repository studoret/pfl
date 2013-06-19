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

from metro import *

# Pedal 0, reserved
# Pedal 1, DownAction => nothing
#          UpAction + keyDownCount < 2   => incremente or decremente the position in action table
#          UpAction + keyDownCount >= 2  => change incremente to decremente mode in vice et versa

# Pedal 2, DownAction => nothing
#          UpAction + keyDownCount < 2   => do action 
#          UpAction + keyDownCount >=   => change incremente to decremente mode in vice et versa

# Pedal 3, DownAction => play or stop
#          UpAction  => nothing

class Action():
  def __init__(self, title, subtitle=""):
    self.__title = title
    self.__subtitle = subtitle

  def GetTitle(self):
    return self.__title

  def GetSubtitle(self):
    return self.__subtitle

class ActionMenu(Action):
  def __init__(self, title):
    Action.__init__(self, title, u'  \u21E9')
    self.__actions = []
    self.__idx = 0
    self.__increment = 1
    self.__subtitles = {-1:u'  \u21E7', 1:u'  \u21E9'}
  
  def Add(self, action):
    self.__actions.append(action)
  
  def GetCurrentAction(self):
    if len(self.__actions) > 0:
      return self.__actions[self.__idx]
    else:
      return None

  def GetActionTitle(self):
    if len(self.__actions) > 0:
      return self.__actions[self.__idx].GetTitle()

  def GetActionSubtitle(self):
    if len(self.__actions) > 0:
      return self.__actions[self.__idx].GetSubtitle()

  def Select(self):
    if len(self.__actions) > 0:
      self.__idx += self.__increment
      if self.__idx == -1:
        self.__idx += len(self.__actions) 
      else:
        if self.__idx == len(self.__actions):
          self.__idx = 0

  def Reverse(self):
    self.__increment *= -1

  def GetSubtitle(self):
    return self.__subtitles[self.__increment]
    

class MetroManager():
  def __init__(self, controlPanel, metro, metroPanel):
    self.__menu =  ActionMenu("MENU")
    self.__menu.Add(Action("TEMPO"))
    self.__menu.Add(Action("BEAT"))
    self.__menu.Add(Action("VOL"))

    self.__metro = metro
    self.__metro.AddMonitor(self)
    self.__cp = controlPanel
    self.__cp.AddManager(self)
    self.__metroPanel = metroPanel
    self.Refresh()

  def Select(self):
    self.__cp.SetTitle(1, self.__menu.GetTitle())  
    self.__cp.SetSubtitle(1, self.__menu.GetSubtitle())  
    self.__cp.SetTitle(2, self.__menu.GetActionTitle()) 
    self.__cp.SetSubtitle(2, self.__menu.GetActionSubtitle())    

  def GetCurrentAction(self):
    return self.__actions[self.__actionIdx]

  def PedalDown(self, pedalId, keyDownCount):
    if pedalId == 0:
      return # the first pedal is not used by the metronome
    if pedalId == 1:
      if keyDownCount >= 2:
        self.__menu.Reverse()
        self.__cp.SetSubtitle(pedalId, self.__menu.GetSubtitle())
      return

  def PedalUp(self, pedalId, keyDownCount):
    if pedalId == 0:
      return # the first pedal is not used by the metronome
    if pedalId == 1:
      if keyDownCount < 2:
        self.__menu.Select()
      self.__cp.SetTitle(pedalId + 1, str(self.__menu.GetActionTitle()))
      self.__cp.SetSubtitle(pedalId + 1, str(self.__menu.GetActionSubtitle()))
      return
    if pedalId == 2:
      if keyDownCount < 2:
        self.__metro.StartPlayback() 
    if pedalId == 3:
      self.__metro.StopPlayback() 
 
  def Refresh(self):
    self.__metroPanel.RefreshTempo(str(self.__metro.GetTempo()))
    self.__metroPanel.RefreshMul(str(self.__metro.GetMul()))
    self.__metroPanel.RefreshBeat(str(self.__metro.GetBeat()))

  def Tick(self):
    tick = self.__metro.GetTick()
    if tick == 1:
      color = "green"
    else:
      color = "blue"
    self.__metroPanel.RefreshTick(str(tick), color)
      
                   
