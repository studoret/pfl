# -*- coding: utf-8 -*-
"""
Main file of pfl application.

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
along with pfl.  If not, see http://www.gnu.org/licenses/.
"""

import pyo, wx
  
from metro.metro import Metro
from metro.panel import MetroPanel
from metro.mgr import MetroManager
from pedals.panel import PedalsPanel
from track.panel import TrackPanel
from track.mgr import Track
from track.mgr import TracksManager
from utils.action import ActionCursor

SERVER = pyo.Server().boot()
SERVER.start()
METRO = Metro()

class PanelsManager():
    """Manage all panels
    """
    PEDALS_PANEL = 0
    METRO_PANEL  = 1
    FIRST_SOUNDTRACK_PANEL = 2
    def __init__(self, frame):
        self.__tracks_panel = [TrackPanel(frame)]
        self.__current_track_id = self.__class__.METRO_PANEL
        self.__increment = 1
        self.__panels = [PedalsPanel(frame), MetroPanel(frame)]
        metro_panel = self.__panels[self.__class__.METRO_PANEL]
        control_panel = self.__panels[self.__class__.PEDALS_PANEL]
        self.__panels.extend(self.__tracks_panel)
        for panel in self.__panels:
            frame.fsizer.Add(panel, 1, wx.ALL | 
                             wx.EXPAND | 
                             wx.ALIGN_CENTER_HORIZONTAL)
        self.__action = ActionCursor("TRACK    ", self.TrackUp, self.TrackDown)
        control_panel.SetTitle(0, self.__action.GetTitle())  
        control_panel.SetSubtitle(0, self.__action.GetSubtitle())  
        control_panel.AddManager(self)
        self.metro_manager = MetroManager(control_panel, METRO, metro_panel)
        self.tracks_manager = TracksManager(METRO, self, control_panel)
        self.tracks_manager.AddTrack(Track(self.__tracks_panel[0]))
        self.DoSelection(self.__current_track_id)

    def DoSelection(self, track_id):
        """Deselect the previous selected panel
        and select the new one
        """
        self.__panels[track_id].OnSelect()
        if track_id == self.__class__.METRO_PANEL:
            self.tracks_manager.Deselect()
            self.metro_manager.Select()
        else:
            self.metro_manager.Deselect()
            self.tracks_manager.Select()
        sound_track_id = track_id - self.__class__.FIRST_SOUNDTRACK_PANEL
        self.tracks_manager.SetCurrentTrackID(sound_track_id)
    
    def ChangeSelection(self):
        """Update the __current_track_id variable
        """
        old_id = self.__current_track_id
        self.__current_track_id += self.__increment
        if self.__current_track_id == self.__class__.PEDALS_PANEL:
            self.__current_track_id = len(self.__panels) - 1
        if self.__current_track_id == len(self.__panels):
            self.__current_track_id = self.__class__.PEDALS_PANEL + 1
        self.__panels[old_id].OnDeselect()
        self.DoSelection(self.__current_track_id)

    def TrackUp(self):
        """Select a new track
        """
        self.__increment = 1
        self.ChangeSelection()

    def TrackDown(self):
        """Select a new track
        """
        self.__increment = -1
        self.ChangeSelection()

    def PedalDown(self, pedal_id, key_down_count):
        """Do action on pedal down
        """
        print "pedalDown = " + str(pedal_id) + " " + str(key_down_count)
        if pedal_id == 0 and key_down_count >= 2:
            self.__action.Reverse()

    def PedalUp(self, pedal_id, key_down_count):
        """Do action on pedal up
        """
        print "pedalUp = " + str(pedal_id) + " " + str(key_down_count)
        if pedal_id == 0 and key_down_count < 2:
            self.__action.Select()


class MyFrame(wx.Frame):
    """The main frame
    """
    def __init__(self, parent, title): 
        wx.Frame.__init__(self, parent, -1, title)
        self.fsizer = wx.BoxSizer(wx.VERTICAL) 
        self.mgr = PanelsManager(self) 
      
        self.SetSizer(self.fsizer)
    
        self.Centre()
        self.Show()
        self.fsizer.Layout()
        wx.CallAfter(self.Fit)

# boilerplate to allow running as script directly
if __name__ == "__main__" and __package__ is None:
    APP = wx.PySimpleApp()
    MyFrame(None, 'Python Foot Looper: test metronome')
    APP.MainLoop()
    METRO.StartPlayback()


