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

# Pedal 1, reserved
# Pedal 2, DownAction => nothing
#          UpAction + keyDownCount < 2   => incremente or decremente the position in action table
#          UpAction + keyDownCount >= 2  => change incremente to decremente mode in vice et versa

# Pedal 3, DownAction => nothing
#          UpAction + keyDownCount < 2   => incremente or decremente the value 
#          UpAction + keyDownCount >=   => change incremente to decremente mode in vice et versa

# Pedal 4, DownAction => play or stop
#          UpAction  => nothing

class MetroManager():
  def __init__(self, controlPanel, metro, metroPanel):
#    self.__actions = [["Tempo", self.SelectTempo], 
#                      ["Mul", self.SelectMul], 
#                      ["Beat", self.SelectBeat]]
#    self.__actionIdx = 0
    self.metro = metro
    self.metro.AddMonitor(self)
    controlPanel.AddManager(self)
    self.metroPanel = metroPanel
    self.Refresh()
    
  def GetDownAction(self, pedalId, keyDownCount):
    if pedalId == 0:
      self.metro.TempoDown() 
    if pedalId == 1:
      self.metro.TempoUp() 
    if pedalId == 2:
      self.metro.StartPlayback() 
    if pedalId == 3:
      self.metro.StopPlayback() 

  def GetUpAction(self, pedalId, keyDownCount):
    pass
 
  def Refresh(self):
    self.metroPanel.RefreshTempo(str(self.metro.GetTempo()))
    self.metroPanel.RefreshMul(str(self.metro.GetMul()))
    self.metroPanel.RefreshBeat(str(self.metro.GetBeat()))

  def Tick(self):
    tick = self.metro.GetTick()
    if tick == 1:
      color = "green"
    else:
      color = "blue"
    self.metroPanel.RefreshTick(str(tick), color)
      
                   
