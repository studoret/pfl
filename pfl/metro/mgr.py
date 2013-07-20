"""
module pfl.metro.mgr
Manager of pfl.metro.metro object .

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

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(
      os.path.abspath(__file__)))))

__package__ = str("pfl")
del sys, os

from utils.action import ActionSwitch, ActionTap
from utils.action import ActionMenu, ActionCursor

class MetroManager():
    """ Class that monitores a metronome and the control panel
        and manage a metro panel 
    """
    def __init__(self, control_panel, metro, metro_panel):
        self.__metro = metro
        self.__selected = False
        self.__menu =  ActionMenu()
        self.__menu.Add(ActionCursor("TEMPO   ",
                                     self.__metro.TempoUp,
                                     self.__metro.TempoDown))
        self.__menu.Add(ActionCursor("BEAT    ",
                                     self.__metro.BeatUp,
                                     self.__metro.BeatDown))
        self.__menu.Add(ActionCursor("VOL.    ",
                                     self.__metro.MulUp,
                                     self.__metro.MulDown))
        self.__menu.Add(ActionTap(self.__metro.ForceTempo))
        self.__mute = ActionSwitch(0, "SOUND ON  ", "SOUND OFF ", 
                                   self.__metro.StartPlayback,
                                   self.__metro.StopPlayback)
        self.__metro.AddMonitor(self)
        self.__cp = control_panel
        self.__cp.AddManager(self)
        self.__metro_panel = metro_panel
        self.Refresh()

    def Select(self):
        """ Select the manager 
        """ 
        self.__selected = True
        self.__cp.SetTitle(1, self.__menu.GetTitle())  
        self.__cp.SetSubtitle(1, self.__menu.GetSubtitle())  
        self.__cp.SetTitle(2, self.__menu.GetActionTitle()) 
        self.__cp.SetSubtitle(2, self.__menu.GetActionSubtitle()) 
        self.__cp.SetTitle(3, self.__mute.GetTitle()) 
        self.__cp.SetSubtitle(3, self.__mute.GetSubtitle())

    def Deselect(self):
        """ Select the manager 
        """ 
        self.__selected = False

    def PedalDown(self, pedal_id, key_down_count):
        """ PedalDown call back 
        """ 
        if self.__selected == False or pedal_id == 0:
            return
        if pedal_id == 1:
            if key_down_count >= 2:
                self.__menu.Reverse()
                self.__cp.SetSubtitle(pedal_id, self.__menu.GetSubtitle())
            return
        if pedal_id == 2:
            action = self.__menu.GetCurrentAction()
            if action != None:
                if key_down_count >= 2:
                    action.Reverse()
                    self.__cp.SetSubtitle(pedal_id, action.GetSubtitle())
            return
        if pedal_id == 3:
            self.__mute.Select()
            self.__cp.SetTitle(pedal_id, self.__mute.GetTitle())

    def PedalUp(self, pedal_id, key_down_count):
        """ PedalUp call back 
        """ 
        if self.__selected == False or pedal_id == 0:
            return
        if pedal_id == 1:
            if key_down_count < 2:
                self.__menu.Select()
                self.__cp.SetTitle(pedal_id + 1, 
                                   self.__menu.GetActionTitle())
                self.__cp.SetSubtitle(pedal_id + 1, 
                                      self.__menu.GetActionSubtitle())
            return
        if pedal_id == 2:
            action = self.__menu.GetCurrentAction()
            if action != None:
                if key_down_count < 2:
                    action.Select()
                    self.__cp.SetTitle(pedal_id, action.GetTitle())
                    self.__cp.SetSubtitle(pedal_id, action.GetSubtitle())
            return
 
    def Refresh(self):
        """ Refresh the metro panel
        """
        self.__metro_panel.RefreshTempo(str(self.__metro.GetTempo()))
        self.__metro_panel.RefreshMul(str(self.__metro.GetMul()))
        beat = self.__metro.GetBeat()
        if beat < 10:
            beat_str = " "+str(beat)
        else:
            beat_str = str(beat)
        self.__metro_panel.RefreshBeat(beat_str)

    def Tick(self):
        """ Tick callback
        """
        tick = self.__metro.GetTick()
        if tick == 1:
            color = "green"
        else:
            color = "blue"
        self.__metro_panel.RefreshTick(str(tick), color)
      
                   
