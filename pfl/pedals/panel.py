"""
module pfl.pedals.panel used to show four foot pedal actions.

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

pedalsMap = { 80: 0, # 'p'
              79: 1, # 'o'
              65: 2, # 'a'
              73: 3 } # 'i' 

class Pedal(wx.Panel):
  def __init__(self, parent, id, title, subtitle=""):
    wx.Panel.__init__(self, parent, id, style = wx.BORDER_SUNKEN)
    self.__box = wx.BoxSizer(wx.HORIZONTAL)
    self.SetBackgroundColour("black")
    self.__defaultColor = self.GetBackgroundColour()
    self.SetForegroundColour("yellow")
    self.__keyDownCount = 0
    self.__title = wx.StaticText(self, label=title)
    self.__title.SetFont(wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))
    self.__box.Add(self.__title, 0, wx.ALL | wx.ALIGN_TOP, 2)
    self.__subtitle = wx.StaticText(self, label=subtitle)
    self.__subtitle.SetFont(wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
    self.__box.Add(self.__subtitle, 0, wx.ALL | wx.ALIGN_BOTTOM, 2)
    self.SetSizer(self.__box)

  def SetTitle(self, title):
     wx.CallAfter(self.__title.SetLabel,title)

  def SetSubtitle(self, subtitle):
     wx.CallAfter(self.__subtitle.SetLabel,subtitle)

  def Light(self, color):
    wx.CallAfter(self.SetBackgroundColour, color)

  def Unlight(self):
    wx.CallAfter(self.SetBackgroundColour,self.__defaultColor)
  
  def AddManager(self, manager):
    self.manager = manager

  def OnKeyDown(self):
    if self.__keyDownCount == 0:
      self.manager.PedalDown(self.GetId(), self.__keyDownCount)
      self.Light(wx.GREEN)
    elif self.__keyDownCount == 2:
      self.manager.PedalDown(self.GetId(), self.__keyDownCount)
      self.Light(wx.BLUE)
    self.__keyDownCount += 1

  def OnKeyUp(self):
    action = self.manager.PedalUp(self.GetId(), self.__keyDownCount)
    if action != None:
      action.Do()
    self.__keyDownCount = 0
    self.Unlight()

class PedalsPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)
    self.SetFocusIgnoringChildren() 
    self.staticBox = wx.StaticBox(self, label='Pedals')
    self.box    = wx.StaticBoxSizer(self.staticBox,wx.HORIZONTAL)
    self.__pedals = [ Pedal(self, 0, "Pedal 0",""),
                     Pedal(self, 1, "Pedal 1",""),
                     Pedal(self, 2, "Pedal 2",""),
                     Pedal(self, 3, "Pedal 3","") ]
    for pedal in self.__pedals:
      self.box.Add(pedal, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL,5 )
    self.SetSizer(self.box)
    self.Bind(wx.EVT_KEY_DOWN, self.KeyDown)
    self.Bind(wx.EVT_KEY_UP, self.KeyUp)

  def GetBox(self):
    return self.box

  def AddManager(self, manager):
    for pedal in self.__pedals:
      pedal.AddManager(manager)
    
  def KeyUp(self, evt):
    key = evt.GetKeyCode()
    self.__pedals[pedalsMap[key]].OnKeyUp()

  def KeyDown(self, evt):
    key = evt.GetKeyCode()
    self.__pedals[pedalsMap[key]].OnKeyDown()

  def SetTitle(self, pedalIdx, title):
    self.__pedals[pedalIdx].SetTitle(title)

  def SetSubtitle(self, pedalIdx, subtitle):
    self.__pedals[pedalIdx].SetSubtitle(subtitle)

        
