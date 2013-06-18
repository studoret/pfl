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

pedals = { 80: 0, # 'p'
           79: 1, # 'o'
           65: 2, # 'a'
           73: 3 } # 'i' 

class MyButton(wx.Button):
  def __init__(self, parent, id, label):
    wx.Button.__init__(self, parent, id, label)
    self.defaultColor = self.GetBackgroundColour()
    self.keyDownCount = 0

  def Light(self, color):
    wx.CallAfter(self.SetBackgroundColour, color)

  def Unlight(self):
    wx.CallAfter(self.SetBackgroundColour,self.defaultColor)
  
  def AddManager(self, manager):
    self.manager = manager

  def OnKeyDown(self):
    if self.keyDownCount == 0:
      action = self.manager.GetDownAction(self.GetId(), self.keyDownCount)
      if action != None:
        action.Do()
      self.Light(wx.GREEN)
    elif self.keyDownCount == 2:
      action = self.manager.GetDownAction(self.GetId(), self.keyDownCount)
      if action != None:
        action.Do()
      self.Light(wx.BLUE)
    self.keyDownCount += 1

  def OnKeyUp(self):
    action = self.manager.GetUpAction(self.GetId(), self.keyDownCount)
    if action != None:
      action.Do()
    self.keyDownCount = 0
    self.Unlight()

class ControlPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)
    self.SetBackgroundColour('#0000FF')
    self.SetFocusIgnoringChildren() 
    self.staticBox = wx.StaticBox(self, label='Pedals')
    self.box    = wx.StaticBoxSizer(self.staticBox,wx.HORIZONTAL)
    self.buttons = [ MyButton(self, 0, "Pedal 1"),
                     MyButton(self, 1, "Pedal 2"),
                     MyButton(self, 2, "Pedal 3"),
                     MyButton(self, 3, "Pedal 4") ]
    for button in self.buttons:
      self.box.Add(button, flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL )
    self.SetSizer(self.box)
    self.Bind(wx.EVT_KEY_DOWN, self.KeyDown)
    self.Bind(wx.EVT_KEY_UP, self.KeyUp)

  def GetBox(self):
    return self.box

  def AddManager(self, manager):
    for button in self.buttons:
      button.AddManager(manager)
    
  def KeyUp(self, evt):
    key = evt.GetKeyCode()
    self.buttons[pedals[key]].OnKeyUp()

  def KeyDown(self, evt):
    key = evt.GetKeyCode()
    self.buttons[pedals[key]].OnKeyDown()


        
