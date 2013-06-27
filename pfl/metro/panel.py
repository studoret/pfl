"""
module pfl.metro.panel
A graphical view of pfl.metro.metro .

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

import wx

import sys, os
parent_dir =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)
import pfl
__package__ = str("pfl")
del sys, os

from utils.widget import *
    
class TempoPanel(LedPanel):
  def __init__(self, parent):
    LedPanel.__init__(self, parent, 3, "blue", 'TEMPO', ' bpm')

class BeatPanel(LedPanel):
  def __init__(self, parent):
    LedPanel.__init__(self, parent, 3, "blue", 'BEAT','00 ')

class VolumePanel(LedPanel):
  def __init__(self, parent):
    LedPanel.__init__(self, parent, 4, "blue", 'VOL.','%')

class MetroPanel(SelectablePanel):
  def __init__(self, parent):
    SelectablePanel.__init__(self, parent, 'Metronome')
    self.__tempoPanel = TempoPanel(self)
    self.box.Add(self.__tempoPanel, 0, wx.ALL | wx.ALIGN_LEFT,5)
    self.__beatPanel = BeatPanel(self)
    self.box.Add(self.__beatPanel, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,5)
    self.__volumePanel = VolumePanel(self)
    self.box.Add(self.__volumePanel, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

  def RefreshTempo(self, value):
    self.__tempoPanel.SetValue(value)

  def RefreshMul(self, value):
    self.__volumePanel.SetValue(value)

  def RefreshTick(self, tick, color=None):
    self.__beatPanel.SetValue(tick, color)

  def RefreshBeat(self, beat):
    self.__beatPanel.SetSubTitle(beat)
