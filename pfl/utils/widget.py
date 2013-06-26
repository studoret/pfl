"""
module pfl.utils.widgets

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
import wx.gizmos as  gizmos

class SelectablePanel(wx.Panel):
  def __init__(self, parent, boxLabel):
    wx.Panel.__init__(self, parent)
    self.boxLabel = boxLabel
    self.staticBox = wx.StaticBox(self, label=boxLabel)
    self.box = wx.StaticBoxSizer(self.staticBox, wx.HORIZONTAL)
    self.SetSizer(self.box)
  

class LedNumber(gizmos.LEDNumberCtrl):
  def __init__(self, parent, digits, color):
    gizmos.LEDNumberCtrl.__init__(self,parent, -1, size=(digits*27, 50), style = wx.BORDER_NONE)
    self.SetBackgroundColour("black")
    self.SetForegroundColour(color)
    self.SetDrawFaded(True)
    self.SetAlignment(gizmos.LED_ALIGN_CENTER)
    self.SetValue("0")

class LedPanel(wx.Panel):
  def __init__(self, parent, digits, color, title, subTitle=None):
    wx.Panel.__init__(self, parent, style = wx.BORDER_SUNKEN)
    self.SetBackgroundColour("black")
    self.SetForegroundColour(color)
    self.box = wx.BoxSizer(wx.HORIZONTAL)
    self.text = wx.StaticText(self, label=title)
    self.text.SetFont(wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))
    self.led = LedNumber(self, digits, color)
    self.box.Add(self.text, 0, wx.ALL | wx.ALIGN_TOP, 2)
    self.box.Add(self.led, 0, wx.ALL | wx.ALIGN_TOP | wx.FIXED_MINSIZE, 2)
    if subTitle != None:
      self.subTitle = wx.StaticText(self, label=subTitle)
      self.subTitle.SetFont(wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
      self.box.Add(self.subTitle, 0, wx.ALL | wx.ALIGN_BOTTOM | wx.FIXED_MINSIZE, 2)
    self.SetSizer(self.box)

  def SetSubTitle(self, subTitle):
     wx.CallAfter(self.subTitle.SetLabel,subTitle)

  def SetValue(self, value, color=None):
    if value != None:
     wx.CallAfter(self.led.SetValue,value)
    if color != None:
      wx.CallAfter(self.led.SetForegroundColour,color)
