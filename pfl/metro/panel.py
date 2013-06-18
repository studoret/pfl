# module loopstation metronome
# author: S.Tudoret
# date: 06/06/2013
#

import wx
import wx.gizmos as  gizmos

class LedNumber(gizmos.LEDNumberCtrl):
  def __init__(self, parent, digits, color):
    gizmos.LEDNumberCtrl.__init__(self,parent, -1, size=(digits*27, 50), style = wx.BORDER_NONE)
    self.SetBackgroundColour("black")
    self.SetForegroundColour(color)
    self.SetDrawFaded(True)
    self.SetAlignment(gizmos.LED_ALIGN_CENTER)
    self.SetValue("0")
    
class LedPanel(wx.Panel):
  def __init__(self, parent, digits, color, title, unity=None):
    wx.Panel.__init__(self, parent, style = wx.BORDER_SUNKEN)
    self.SetBackgroundColour("black")
    self.SetForegroundColour(color)
    self.box = wx.BoxSizer(wx.HORIZONTAL)
    self.text = wx.StaticText(self, label=title)
    self.text.SetFont(wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))
    self.led = LedNumber(self, digits, color)
    self.box.Add(self.text, 0, wx.ALL | wx.ALIGN_TOP, 2)
    self.box.Add(self.led, 0, wx.ALL | wx.ALIGN_TOP | wx.FIXED_MINSIZE, 2)
    if unity != None:
      self.unity = wx.StaticText(self, label=unity)
      self.unity.SetFont(wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
      self.box.Add(self.unity, 0, wx.ALL | wx.ALIGN_BOTTOM, 2)
    self.SetSizer(self.box)

  def SetValue(self, value, color=None):
    if color != None:
      self.led.SetForegroundColour(color)
    self.led.SetValue(value)
    
class TempoPanel(LedPanel):
  def __init__(self, parent):
    LedPanel.__init__(self, parent, 3, "blue", 'TEMPO', 'bpm')

class BeatPanel(LedPanel):
  def __init__(self, parent):
    LedPanel.__init__(self, parent, 2, "blue", 'BEAT')

class VolumePanel(LedPanel):
  def __init__(self, parent):
    LedPanel.__init__(self, parent, 2, "blue", 'VOL.')

class MetroPanel(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)
    self.staticBox = wx.StaticBox(self, label='Metronome')
    self.box = wx.StaticBoxSizer(self.staticBox, wx.HORIZONTAL)
    self.tempoPanel = TempoPanel(self)
    self.box.Add(self.tempoPanel, 0, wx.ALL | wx.ALIGN_LEFT,5)
    self.beatPanel = BeatPanel(self)
    self.box.Add(self.beatPanel, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,5)
    self.volumePanel = VolumePanel(self)
    self.box.Add(self.volumePanel, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
    self.SetSizer(self.box)

  def RefreshTempo(self, value):
    self.tempoPanel.SetValue(value)

  def RefreshMul(self, value):
    self.volumePanel.SetValue(value)

  def RefreshBeat(self, value, color=None):
    self.beatPanel.SetValue(value, color)
