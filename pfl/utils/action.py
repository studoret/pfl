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

  def Select(self):
    pass

  def Reverse(self):
    pass

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
