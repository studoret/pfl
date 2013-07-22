"""
module pfl.track.mgr
Manager of pfl.track.track object .

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

import pyo

from utils.action import ActionSwitch, ActionLong
from utils.action import ActionMenu, ActionCursor
from recorder.recorder import Recorder
from datetime import datetime

class Track():
    """ Sound track manager
    """
    def __init__(self, panel):
        self.__panel = panel
        self.__data_table = None
        self.__out_stream = None
 
    def HasDataTable(self):
        """ Return True if the track has a data table
        """
        return self.__data_table != None
    
    def Save(self, file_name):
        """ Save the track in a file
        """
        if self.__data_table != None:
            self.__data_table.save(path=file_name, format=0, sampletype = 1)

    def SetDataTable(self, data_table):
        """ Set data table
        """
        print "SetDataTable"
        self.__data_table = data_table
        self.Save("test_"+ datetime.now().strftime("%Y%m%d-%H%M%S") + ".wav")

    def StartPlayback(self):
        """ Start play back the data table
        """
        if self.__data_table != None:
            print "StartPlayback"  
            freq = self.__data_table.getRate()
            self.__out_stream = pyo.TableRead(table=self.__data_table, 
                                             freq=freq, interp=1, 
                                             loop=True, mul=0.5).play()
        else :
            print "No record"

    def StopPlayback(self):
        """ Stop play back the data table
        """
        if self.__out_stream != None:
            print "StopPlayback"
            self.__out_stream.stop()

class TracksManager():
    """ Class that monitores sound tracks and the control panel
        and manage a sound track panels 
    """
    def __init__(self, metro, panel_mgr, control_panel):
        self.__selected = False
        self.__panel_mgr = panel_mgr # not used at this time
        self.__menu = ActionMenu()
        self.__menu.Add(ActionLong("START RECORD  ", 
                                   self.StartRecord, self.StopRecord))
        self.__menu.Add(ActionSwitch("LOOP ON  ", "LOOP OFF ", 
                                     self.LoopOn, self.LoopOff))
        self.__menu.Add(ActionCursor("VOL.     ", 
                                     self.VolUp, self.VolDown))
        self.__play_back = ActionSwitch("START    ", "STOP  ", 
                                       self.StartPlayback, self.StopPlayback)
        self.__cp = control_panel
        self.__cp.AddListener(self)
        self.__tracks = []
        self.__current_track_id = -1
        self.__recorder = Recorder(metro, self)

    def Select(self):
        """ Select the manager 
        """ 
        self.__selected = True
        self.__cp.SetTitle(1, self.__menu.GetTitle())  
        self.__cp.SetSubtitle(1, self.__menu.GetSubtitle())  
        self.__cp.SetTitle(2, self.__menu.GetActionTitle()) 
        self.__cp.SetSubtitle(2, self.__menu.GetActionSubtitle()) 
        self.__cp.SetTitle(3, self.__play_back.GetTitle()) 
        self.__cp.SetSubtitle(3, self.__play_back.GetSubtitle())

    def Deselect(self):
        """ Select the manager 
        """ 
        self.__selected = False

    def SetCurrentTrackID(self, track_id):
        """ Change the current track id
        """
        self.__current_track_id = track_id

    def AddTrack(self, track):
        """ Add a track
        """
        self.__tracks.append(track)    

    def SetDataTable(self, data_table): 
        """ Set data table of the current track
        """
        if  self.__current_track_id >= 0 :
            self.__tracks[self.__current_track_id].SetDataTable(data_table)

    def StartRecord(self): 
        """ Start recording
        """
        self.__recorder.Start()

    def StopRecord(self):
        """ Stop recording
        """
        self.__recorder.Stop()

    def StartPlayback(self):
        """ Start play back the data table of the current track
        """
        print "__currentTrack = "+str(self.__current_track_id)
        if  self.__current_track_id >= 0 :
            self.__tracks[self.__current_track_id].StartPlayback()

    def StopPlayback(self):
        """ Stop play back the data table of the current track
        """
        if  self.__current_track_id >= 0 :
            self.__tracks[self.__current_track_id].StopPlayback()

    def VolDown(self):
        """ Decrease the volume
        """
        print "VolDown"

    def VolUp(self):
        """ Increase the volume
        """
        print "VolUp"

    def LoopOn(self):
        """ Set loop on mode
        """
        print "LoopOn"

    def LoopOff(self):
        """ Set loop off mode
        """
        print "LoopOff"

    def PedalDown(self, pedal_id, key_down_count):
        """ PedalDown call back 
        """ 
        if (not self.__selected) or (pedal_id == 0):
            return
        if pedal_id == 1:
            if key_down_count >= 2:
                self.__menu.Reverse()
                self.__cp.SetSubtitle(pedal_id, self.__menu.GetSubtitle())
            return
        if pedal_id == 2:
            action = self.__menu.GetCurrentAction()
            if action != None:
                action.Down()
                if key_down_count >= 2:
                    action.Reverse()
                    self.__cp.SetSubtitle(pedal_id, action.GetSubtitle())
            return
        if pedal_id == 3:
            self.__play_back.Select()
            self.__cp.SetTitle(pedal_id, self.__play_back.GetTitle())

    def PedalUp(self, pedal_id, key_down_count):
        """ PedalUp call back 
        """ 
        if (not self.__selected) or (pedal_id == 0):
            return
        if pedal_id == 1:
            if key_down_count < 2:
                self.__menu.Select()
                self.__cp.SetTitle(pedal_id + 1, self.__menu.GetActionTitle())
                self.__cp.SetSubtitle(pedal_id + 1, self.__menu.GetActionSubtitle())
            return
        if pedal_id == 2:
            action = self.__menu.GetCurrentAction()
            if action != None:
                action.Up()
                if key_down_count < 2:
                    action.Select()
                    self.__cp.SetTitle(pedal_id, action.GetTitle())
                    self.__cp.SetSubtitle(pedal_id, action.GetSubtitle())
            return
