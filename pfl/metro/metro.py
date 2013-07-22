# -*- coding: utf-8 -*-
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

class Metro():
    """The Metronome class
    """
    def __init__(self):
        self.__monitors = []
        self.__tempo_tab = [ 40,  42,  44,  46,  48, 
                            50,  52,  54,  56,  58, 
                            60,  63,  66,  69,  72, 
                            76,  80,  84,  88,  92, 
                            96, 100, 104, 108, 112, 
                           116, 120, 126, 132, 138,  
                           144, 152, 160, 168, 176,  
                           184, 192, 200, 208, 216 ]
        self.__tempo_idx = 19
        self.__beat = 4
        self.__tick = 0 
        self.__current_beat = 0
        self.__mul = 50 # percent
        self.__freq = 700
        self.__dur = 0.01
        self.__time = 60. / self.__tempo_tab[self.__tempo_idx]
        self.__metro = pyo.Metro(self.__time).play()
        wave = pyo.SquareTable(size=10)
        self.__amp = pyo.TrigEnv(self.__metro, table=wave, dur=self.__dur)
        mul = self.__amp * self.__mul/100.0
        self.__output = pyo.Osc(table=wave, freq=self.__freq,  mul=mul)
        self.__emphasize = pyo.Osc(table=wave, freq=self.__freq*2,  mul=mul)
        self.__trig = pyo.TrigFunc(self.__metro, function=self.Tick)

    def StartPlayback(self):
        """ Used to turn on metronome tick sounds
        """
        self.__output.out()

    def StopPlayback(self):
        """ Used to turn off metronome tick sounds
        """
        self.__emphasize.stop()
        self.__output.stop()

    def TempoUp(self):
        """ Used to increase the tempo
        """
        if self.__tempo_idx < (len(self.__tempo_tab) - 1):
            self.__tempo_idx += 1
            self.__time = 60. / self.__tempo_tab[self.__tempo_idx]
            self.__metro.setTime(self.__time)
            self.RefreshMonitors()

    def TempoDown(self):
        """ Used to decrease the tempo
        """
        if self.__tempo_idx > 0:
            self.__tempo_idx -= 1
            self.__time = 60. / self.__tempo_tab[self.__tempo_idx]
            self.__metro.setTime(self.__time)
            self.RefreshMonitors()

    def ForceTempo(self, bpm):
        """ Set a given tempo
        """
        self.__tempo_idx = 0
        for tempo in self.__tempo_tab:
            if bpm < tempo:
                bpm = tempo
                break
            self.__tempo_idx += 1
        if self.__tempo_idx == len(self.__tempo_tab):
            self.__tempo_idx -= 1
        self.__time = 60. / bpm
        self.__metro.setTime(self.__time)
        self.RefreshMonitors()
    
    def MulUp(self):
        """ Used to increase the tick sound volume
        """
        if self.__mul < 100:
            self.__mul += 5
            mul = self.__amp * self.__mul/100.0
            self.__output *= mul
            self.__emphasize *= mul
            self.RefreshMonitors()

    def MulDown(self):
        """ Used to decrease the tick sound volume
        """
        if self.__mul > 0:
            self.__mul -= 5
            mul = self.__amp * self.__mul/100.0
            self.__output *= mul
            self.__emphasize *= mul
            self.RefreshMonitors()

    def BeatUp(self):
        """ Used to increase the beat
        """
        if self.__beat < 16:
            self.__beat += 1
            self.RefreshMonitors()

    def BeatDown(self):
        """ Used to decrease the beat
        """
        if self.__beat > 2:
            self.__beat -= 1
            self.RefreshMonitors()

    def GetTempo(self):
        """ Get the tempo value
        """
        return self.__tempo_tab[self.__tempo_idx]

    def GetMul(self):
        """ Get the volume value
        """
        return self.__mul

    def GetBeat(self):
        """ Get the beat value
        """
        return self.__beat

    def GetTick(self):
        """ Used to retreive the current tick number
        That returns a value between 1 and self.__beat
        """
        return self.__tick

    def GetTime(self):
        """ Used to retreive the tick period value
        """
        return self.__time

    def AddMonitor(self, monitor):
        """ Add a monitor
        """
        self.__monitors.append(monitor)

    def RefreshMonitors(self):
        """ Call Refresh methods of all monitors
        """
        for monitor in self.__monitors:
            monitor.Refresh()

    def Tick(self): 
        """ Tick call back
        """
        self.__tick += 1 
        if self.__tick > self.__beat:
            self.__tick = 1
        if self.__output.isOutputting(): 
            if self.__tick == 1:
                self.__emphasize.out()
            else:     
                self.__emphasize.stop()
        for monitor in self.__monitors:
            monitor.Tick()
    

