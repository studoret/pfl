# module loopstation metronome
# author: S.Tudoret
# date: 06/06/2013
#

import pyo

from ls_metro import *

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
    self.count = 0 
    self.metro = metro
    self.metro.AddMonitor(self)
    controlPanel.AddManager(self)
    self.metroPanel = metroPanel
    self.metroPanel.RefreshTempo(str(metro.GetTempo()))
    self.metroPanel.RefreshMul(str(metro.GetMul()))
    self.metroPanel.RefreshBeat(str(metro.GetBeat()))
    
  def GetDownAction(self, buttonId, keyDownCount):
    if buttonId == 0:
      self.metro.TempoDown() 
    if buttonId == 1:
      self.metro.TempoUp() 
    if buttonId == 2:
      self.metro.StartPlayback() 
    if buttonId == 3:
      self.metro.StopPlayback() 

  def GetUpAction(self, buttonId, keyDownCount):
    pass
 
  def Refresh(self):
    self.metroPanel.RefreshTempo(str(self.metro.GetTempo()))
    self.metroPanel.RefreshMul(str(self.metro.GetMul()))
    self.metroPanel.RefreshBeat(str(self.metro.GetBeat()))

  def Tick(self):
    self.count += 1 
    beat = self.metro.GetBeat()
    if self.count > beat:
      self.count = 1
    if self.count == beat:
      color = "green"
    else:
      color = "blue"
    self.metroPanel.RefreshBeat(str(self.count), color)
      
                   
