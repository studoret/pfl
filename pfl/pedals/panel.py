"""
module pfl.pedals.panel used to show four foot pedal actions.

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

import wx

PEDALS_MAP = { 80: 0, # 'p'
              79: 1, # 'o'
              65: 2, # 'a'
              73: 3 } # 'i' 

class Pedal(wx.Panel):
    """ Pedal panel
    """
    def __init__(self, parent, pedal_id, title, subtitle=""):
        wx.Panel.__init__(self, parent, pedal_id, style = wx.BORDER_SUNKEN)
        self.__box = wx.BoxSizer(wx.HORIZONTAL)
        self.SetBackgroundColour("black")
        self.__default_color = self.GetBackgroundColour()
        self.SetForegroundColour("yellow")
        self.__key_down_count = 0
        self.__title = wx.StaticText(self, label=title)
        self.__title.SetFont(wx.Font(16, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))
        self.__box.Add(self.__title, 0, wx.ALL | wx.ALIGN_TOP, 2)
        self.__subtitle = wx.StaticText(self, label=subtitle)
        self.__subtitle.SetFont(wx.Font(14, 
                                        wx.DECORATIVE, wx.NORMAL, wx.NORMAL))
        self.__box.Add(self.__subtitle, 0, wx.ALL | wx.ALIGN_BOTTOM, 2)
        self.SetSizer(self.__box)
        self.__listeners = []

    def SetTitle(self, title):
        """ Set the title
        """
        wx.CallAfter(self.__title.SetLabel, title)

    def SetSubtitle(self, subtitle):
        """ Set the subtitle
        """
        wx.CallAfter(self.__subtitle.SetLabel, subtitle)

    def Light(self, color):
        """ Change the background color
        """
        wx.CallAfter(self.SetBackgroundColour, color)

    def Unlight(self):
        """ Reset the background color to the default color
        """
        wx.CallAfter(self.SetBackgroundColour, self.__default_color)
  
    def AddListener(self, listener):
        """ Add a listener that will call back on pedal events
        """
        self.__listeners.append(listener)

    def OnKeyDown(self):
        """ Call when pedal is pushed
        """
        for listener in self.__listeners:
            if self.__key_down_count == 0:
                listener.PedalDown(self.GetId(), self.__key_down_count)
                self.Light(wx.GREEN)
            elif self.__key_down_count == 2:
                listener.PedalDown(self.GetId(), self.__key_down_count)
                self.Light(wx.BLUE)
        self.__key_down_count += 1

    def OnKeyUp(self):
        """ Call when pedal is released
        """
        for listener in self.__listeners:
            action = listener.PedalUp(self.GetId(), self.__key_down_count)
            if action != None:
                action.Do()
        self.__key_down_count = 0
        self.Unlight()

class PedalsPanel(wx.Panel):
    """ Panel that shows the pedal panels
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetFocusIgnoringChildren() 
        static_box = wx.StaticBox(self, label='Pedals')
        self.box    = wx.StaticBoxSizer(static_box, wx.HORIZONTAL)
        self.__pedals = [ Pedal(self, 0, "Pedal 0",""),
                          Pedal(self, 1, "Pedal 1",""),
                          Pedal(self, 2, "Pedal 2",""),
                          Pedal(self, 3, "Pedal 3","") ]
        for pedal in self.__pedals:
            self.box.Add(pedal, 0, 
                         wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetSizer(self.box)
        self.Bind(wx.EVT_KEY_DOWN, self.KeyDown)
        self.Bind(wx.EVT_KEY_UP, self.KeyUp)

    def GetBox(self):
        """ Return the static box sizer
        """
        return self.box

    def AddListener(self, listener):
        """ Add a listener in the list
        """
        for pedal in self.__pedals:
            pedal.AddListener(listener)
    
    def KeyUp(self, evt):
        """ Pedal released event
        """
        key = evt.GetKeyCode()
        self.__pedals[PEDALS_MAP[key]].OnKeyUp()

    def KeyDown(self, evt):
        """ Pedal pushed event
        """
        key = evt.GetKeyCode()
        self.__pedals[PEDALS_MAP[key]].OnKeyDown()

    def SetTitle(self, pedal_idx, title):
        """ Set the title of a given pedal
        """
        self.__pedals[pedal_idx].SetTitle(title)

    def SetSubtitle(self, pedal_idx, subtitle):
        """ Set the subtitle of a given pedal
        """
        self.__pedals[pedal_idx].SetSubtitle(subtitle)

        
