"""
module pfl.metro.metro 
A metronome based on pyo.

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

def enum(**enums):
    """ Define unums type
    """
    return type('Enum', (), enums)

RECORDER_STATES = enum(IDLE=0, STARTING=1, RUNNING=2, STOPPING=3)

class Recorder():
    """ Class used to record audio input to sound track
    """
    def __init__(self, metro, tracks_mgr):
        self.__metro = metro
        self.__tracks_mgr = tracks_mgr
        self.__input = pyo.Input(chnl=1)  # chnl=[0,1] for stereo input
        self.__state = RECORDER_STATES.IDLE
        self.__elapsed = 0
        self.__buffer_length = 300 # seconds
        self.__buffer = pyo.NewTable(self.__buffer_length)
        self.__table_rec = pyo.TableRec(self.__input, table=self.__buffer)
        self.__samples = []
        metro.AddMonitor(self)

    def Tick(self):
        """ tick of the clock of the recorder
        """
        if self.__state == RECORDER_STATES.RUNNING:
            if self.__elapsed < self.__buffer_length:
                self.__elapsed += self.__metro.GetTime()
                print "record time = "+str(self.__elapsed)
            else:
                print "Stop on buffer fool"
                self.__input.stop()
            return
        if self.__state == RECORDER_STATES.STARTING:
            self.__state = RECORDER_STATES.RUNNING
            self.__elapsed = 0
            del self.__samples[:]
            self.__input.play()
            self.__table_rec.play()
            return  
        if self.__state == RECORDER_STATES.STOPPING:
            self.__state = RECORDER_STATES.IDLE
            samples_len =  pyo.secToSamps(self.__elapsed)
            self.__table_rec.stop()
            self.__samples.extend(
                self.__buffer.getTable()[slice (0, samples_len)])
            self.__tracks_mgr.SetDataTable(
                pyo.DataTable(samples_len, init=self.__samples))
            return
  
    def Refresh(self):
        """ Refresh recorder monitors
        """
        pass

    def Start(self):
        """ Request a recording start
        """
        self.__state = RECORDER_STATES.STARTING

    def Stop(self):
        """ Request a recording stop
        """
        self.__state = RECORDER_STATES.STOPPING
