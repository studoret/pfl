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
import sys, os
parent_dir =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)
import pfl
__package__ = str("pfl")
del sys, os

import pyo
from metro import *

def enum(**enums):
    return type('Enum', (), enums)

RecorderStates = enum(idle=0, starting=1, running=2, stopping=3)

class Recorder():
  def __init__(self, metro, tracksMgr):
    self.__metro = metro
    self.__tracksMgr = tracksMgr
    self.__input = pyo.Input(chnl=1)  # chnl=[0,1] for stereo input
    self.__state = RecorderStates.idle
    self.__elapsed = 0
    self.__bufferLength = 300 # seconds
    self.__buffer = pyo.NewTable(self.__bufferLength)
    self.__tableRec = pyo.TableRec(self.__input, table=self.__buffer)
    self.__samples = []
    metro.AddMonitor(self)

  def Tick(self):
    if self.__state == RecorderStates.running:
      if self.__elapsed < self.__bufferLength:
        self.__elapsed += self.__metro.GetTime()
        print "record time = "+str(self.__elapsed)
      else:
        print "Stop on buffer fool"
        self.__input.stop()
      return
    if self.__state == RecorderStates.starting:
      self.__state = RecorderStates.running
      self.__elapsed = 0
      del self.__samples[:]
      self.__input.play()
      self.__tableRec.play()
      return  
    if self.__state == RecorderStates.stopping:
      self.__state = RecorderStates.idle
      samplesLen =  pyo.secToSamps(self.__elapsed)
      self.__tableRec.stop()
      sl = slice (0, samplesLen)
      tmpBuffer = self.__buffer.getTable()[sl]
      self.__samples.extend(tmpBuffer)
      self.__tracksMgr.SetDataTable(pyo.DataTable(samplesLen, init=self.__samples))
      return
  
  def Refresh(self):
    pass

  def Start(self):
    self.__state = RecorderStates.starting

  def Stop(self):
    self.__state = RecorderStates.stopping
