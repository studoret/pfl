"""
module pfl.utils.actions

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

class Action():
  def __init__(self, title, subtitle=""):
    self.__title = title
    self.__subtitle = subtitle

  def GetTitle(self):
    return self.__title

  def GetSubtitle(self):
    return self.__subtitle

  def Begin(self):
    pass

  def End(self):
    pass

  def Select(self):
    pass

  def Reverse(self):
    pass

class ActionLong(Action):
  def __init__(self, title, startFunction, stopFunction):
    Action.__init__(self, title)
    self.__actions = [startFunction, stopFunction]

  def Down(self):
    self.__actions[0]()

  def Up(self):
    self.__actions[1]()

class ActionCursor(Action):
  subtitles = {-1:u'\u21E7', 1:u'\u21E9'}
  
  def __init__(self, title, incFunction, decFunction):
    self.__increment = 1
    Action.__init__(self, title, self.__class__.subtitles[self.__increment])
    self.actions = {-1: incFunction, 1: decFunction}

  def Select(self):
    self.actions[self.__increment]()

  def Reverse(self):
    self.__increment *= -1

  def GetSubtitle(self):
    return self.__class__.subtitles[self.__increment]

class ActionCursor(Action):
  subtitles = {-1:u'\u21E7', 1:u'\u21E9'}
  
  def __init__(self, title, incFunction, decFunction):
    self.__increment = 1
    Action.__init__(self, title, self.__class__.subtitles[self.__increment])
    self.actions = {-1: incFunction, 1: decFunction}

  def Select(self):
    self.actions[self.__increment]()

  def Reverse(self):
    self.__increment *= -1

  def GetSubtitle(self):
    return self.__class__.subtitles[self.__increment]


class ActionSwitch(Action):
  def __init__(self, state, onTitle, offTitle, onFunction, offFunction):
    self.__titles = {0: onTitle, 1: offTitle}
    self.__state = state
    Action.__init__(self, self.__titles[self.__state])
    self.__actions = {0: offFunction, 1: onFunction}
    self.__actions[(state + 1)%2]
    
  def Select(self):
    self.__state += 1
    self.__state %= 2
    self.__actions[self.__state]()

  def GetTitle(self):
    return self.__titles[self.__state] 

class ActionMenu(Action):
  subtitles = {-1:u'\u21E7', 1:u'\u21E9'}

  def __init__(self):
    self.__increment = 1
    Action.__init__(self, "MENU    ", self.__class__.subtitles[self.__increment])
    self.__actions = []
    self.__idx = 0
  
  def Add(self, action):
    self.__actions.append(action)
  
  def GetCurrentAction(self):
    if len(self.__actions) > 0:
      return self.__actions[self.__idx]
    else:
      return None

  def GetActionTitle(self):
    if len(self.__actions) > 0:
      return self.__actions[self.__idx].GetTitle()

  def GetActionSubtitle(self):
    if len(self.__actions) > 0:
      return self.__actions[self.__idx].GetSubtitle()

  def Select(self):
    if len(self.__actions) > 0:
      self.__idx += self.__increment
      if self.__idx == -1:
        self.__idx += len(self.__actions) 
      else:
        if self.__idx == len(self.__actions):
          self.__idx = 0

  def Reverse(self):
    self.__increment *= -1

  def GetSubtitle(self):
    return self.__class__.subtitles[self.__increment]
    
