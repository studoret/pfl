"""
module pfl.metro.metro 
A metronome based on pyo.

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
import pyo

class Metro():
  def __init__(self):
    self.__monitors = []
    self.__tempoTab = [ 40,  42,  44,  46,  48, 
                        50,  52,  54,  56,  58, 
                        60,  63,  66,  69,  72, 
                        76,  80,  84,  88,  92, 
                        96, 100, 104, 108, 112, 
                       116, 120, 126, 132, 138,  
                       144, 152, 160, 168, 176,  
                       184, 192, 200, 208, 216, 
                    ]
    self.__tempoIdx = 19
    self.__beat = 4
    self.__tick = 0 
    self.__currentBeat = 0
    self.__mul = 0.5
    self.__freq = 700
    self.__dur = 0.01
    time = 60. / self.__tempoTab[self.__tempoIdx]
    self.__metro = pyo.Metro(time).play()
    self.__wave = pyo.SquareTable(size=10)
    self.__amp = pyo.TrigEnv(self.__metro, table=self.__wave, dur=self.__dur)
    self.__trig = pyo.TrigFunc(self.__metro, function=self.Tick)
    self.__output = pyo.Osc(table=self.__wave, freq=self.__freq,  mul=self.__amp * self.__mul)
    self.__emphasize = pyo.Osc(table=self.__wave, freq=self.__freq*2,  mul=self.__amp * self.__mul)

  def StartPlayback(self):
    self.__output.out()

  def StopPlayback(self):
    self.__output.stop()

  def TempoUp(self):
    if self.__tempoIdx < (len(self.__tempoTab) - 1):
      self.__tempoIdx += 1
      time = 60. / self.__tempoTab[self.__tempoIdx]
      self.__metro.setTime(time)
      self.RefreshMonitors()

  def TempoDown(self):
    if self.__tempoIdx > 0:
      self.__tempoIdx -= 1
      time = 60. / self.__tempoTab[self.__tempoIdx]
      self.__metro.setTime(time)
      self.RefreshMonitors()

  def MulUp(self):
    if self.__mul < 1:
      self.__mul += 0.1
      self.__metro.setMul(self.__mul)
      self.RefreshMonitors()

  def MulDown(self):
    if self.__mul > 0:
      self.__mul -= 0.1
      self.__metro.setMul(self.__mul)
      self.RefreshMonitors()

  def BeatUp(self):
    if self.__beat < 16:
      self.__beat += 1
      self.RefreshMonitors()

  def BeatDown(self):
    if self.__beat > 2:
      self.__beat -= 1
      self.RefreshMonitors()

  def GetTempo(self):
    return self.__tempoTab[self.__tempoIdx]

  def GetMul(self):
    return self.__mul

  def GetBeat(self):
    return self.__beat

  def GetTick(self):
    return self.__tick

  def AddMonitor(self, monitor):
    self.__monitors.append(monitor)

  def RefreshMonitors(self):
    for monitor in self.__monitors:
      monitor.Refresh()

  def Tick(self): 
    self.__tick += 1 
    if self.__tick > self.__beat:
      self.__tick = 1
    if self.__tick == 1:
      if self.__output.isOutputting():
        self.__emphasize.out()
    else:
      self.__emphasize.stop()
    for monitor in self.__monitors:
      monitor.Tick()
    

