"""
module pfl.metro.panel
A graphical view of pfl.metro.metro .

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
along with pfl.  If not, see <http://www.gnu.org/licenses/>.
"""

import wx

from utils.widget import SelectablePanel, LedPanel
    
class TempoPanel(LedPanel):
    """ Tempo panel
    """
    def __init__(self, parent):
        LedPanel.__init__(self, parent, 3, "blue", 'TEMPO', ' bpm')

class BeatPanel(LedPanel):
    """ Beat panel
    """
    def __init__(self, parent):
        LedPanel.__init__(self, parent, 3, "blue", 'BEAT','00 ')

class VolumePanel(LedPanel):
    """ Volume panel
    """
    def __init__(self, parent):
        LedPanel.__init__(self, parent, 4, "blue", 'VOL.','%')

class MetroPanel(SelectablePanel):
    """ Metro panel
    """
    def __init__(self, parent):
        SelectablePanel.__init__(self, parent, 'Metronome')
        self.__tempo_panel = TempoPanel(self)
        self.box.Add(self.__tempo_panel, 0, 
                     wx.ALL | wx.ALIGN_LEFT, 5)
        self.__beat_panel = BeatPanel(self)
        self.box.Add(self.__beat_panel, 0, 
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.__volume_panel = VolumePanel(self)
        self.box.Add(self.__volume_panel, 0, 
                     wx.ALL | wx.ALIGN_RIGHT, 5)

    def RefreshTempo(self, value):
        """ Refresh tempo panel
        """
        self.__tempo_panel.SetValue(value)

    def RefreshMul(self, value):
        """ Refresh volume panel
        """
        self.__volume_panel.SetValue(value)

    def RefreshTick(self, tick, color=None):
        """ Refresh tick panel
        """
        self.__beat_panel.SetValue(tick, color)

    def RefreshBeat(self, beat):
        """ Refresh beat panel
        """
        self.__beat_panel.SetSubTitle(beat)
