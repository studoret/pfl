"""
module pfl.track.mgr
Manager of pfl.track.track object .

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

from utils.action import *
from track import *
from recorder.recorder import *
from datetime import *

class Track():
  def __init__(self, panel):
    self.__panel = panel
    self.__dataTable = None
    self.__outStream = None
 
  def HasRecord(self):
    return self.__dataTable != None
    
  def Save(self, fileName):
    self.__dataTable.save(path=fileName, format=0, sampletype = 1)

  def SetDataTable(self, dataTable):
    print "SetDataTable"
    self.__dataTable = dataTable
    self.Save("test_"+ datetime.now().strftime("%Y%m%d-%H%M%S") + ".wav")

  def StartPlayback(self):
    if self.__dataTable != None:
      print "StartPlayback"  
      freq = self.__dataTable.getRate()
      self.__outStream = pyo.TableRead(table=self.__dataTable, freq=freq, interp=1, loop=True, mul=0.5).play()
    else :
      print "No record"

  def StopPlayback(self):
    if self.__outStream != None:
      print "StopPlayback"
      self.__outStream.stop()

class TracksManager():
  def __init__(self, metro, panelMgr, controlPanel):
    self.__selected = False
    self.__panelMgr = panelMgr # not used at this time
    self.__menu = ActionMenu()
    self.__menu.Add(ActionLong("START RECORD  ", self.StartRecord, self.StopRecord))
    self.__menu.Add(ActionSwitch(0, "LOOP ON  ", "LOOP OFF ", self.LoopOn, self.LoopOff))
    self.__menu.Add(ActionCursor("VOL.     ", self.VolUp, self.VolDown))
    self.__playBack = ActionSwitch(0, "START    ", "STOP  ", self.StartPlayback, self.StopPlayback)
    self.__cp = controlPanel
    self.__cp.AddManager(self)
    self.__tracks = []
    self.__currentTrackId = -1
    self.__recorder = Recorder(metro, self)

  def Select(self):
    self.__selected = True
    self.__cp.SetTitle(1, self.__menu.GetTitle())  
    self.__cp.SetSubtitle(1, self.__menu.GetSubtitle())  
    self.__cp.SetTitle(2, self.__menu.GetActionTitle()) 
    self.__cp.SetSubtitle(2, self.__menu.GetActionSubtitle()) 
    self.__cp.SetTitle(3, self.__playBack.GetTitle()) 
    self.__cp.SetSubtitle(3, self.__playBack.GetSubtitle())

  def Deselect(self):
    self.__selected = False

  def SetCurrentTrackID(self, trackId):
    self.__currentTrackId = trackId

  def AddTrack(self, track):
    self.__tracks.append(track)    

  def SetDataTable(self, dataTable): 
    if  self.__currentTrackId >= 0 :
      self.__tracks[self.__currentTrackId].SetDataTable(dataTable)

  def StartRecord(self):
    self.__recorder.Start()

  def StopRecord(self):
    self.__recorder.Stop()

  def StartPlayback(self):
    print "__currentTrack = "+str(self.__currentTrackId)
    if  self.__currentTrackId >= 0 :
      self.__tracks[self.__currentTrackId].StartPlayback()

  def StopPlayback(self):
    if  self.__currentTrackId >= 0 :
      self.__tracks[self.__currentTrackId].StopPlayback()

  def VolDown(self):
    print "VolDown"

  def VolUp(self):
    print "VolUp"

  def LoopOn(self):
    print "LoopOn"

  def LoopOff(self):
    print "LoopOff"

  def PedalDown(self, pedalId, keyDownCount):
    if self.__selected == False or pedalId == 0:
      return
    if pedalId == 1:
      if keyDownCount >= 2:
        self.__menu.Reverse()
        self.__cp.SetSubtitle(pedalId, self.__menu.GetSubtitle())
      return
    if pedalId == 2:
      action = self.__menu.GetCurrentAction()
      if action != None:
        action.Down()
        if keyDownCount >= 2:
          action.Reverse()
          self.__cp.SetSubtitle(pedalId, action.GetSubtitle())
      return
    if pedalId == 3:
      self.__playBack.Select()
      self.__cp.SetTitle(pedalId, self.__playBack.GetTitle())

  def PedalUp(self, pedalId, keyDownCount):
    if self.__selected == False or pedalId == 0:
      return
    if pedalId == 1:
      if keyDownCount < 2:
        self.__menu.Select()
        self.__cp.SetTitle(pedalId + 1, self.__menu.GetActionTitle())
        self.__cp.SetSubtitle(pedalId + 1, self.__menu.GetActionSubtitle())
      return
    if pedalId == 2:
      action = self.__menu.GetCurrentAction()
      if action != None:
        action.Up()
        if keyDownCount < 2:
          action.Select()
          self.__cp.SetTitle(pedalId,action.GetTitle())
          self.__cp.SetSubtitle(pedalId,action.GetSubtitle())
      return
