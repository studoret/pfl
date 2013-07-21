"""
module pfl.utils.actions

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

import time

class Action():
    """ Action base class
    """
    def __init__(self, title, subtitle=""):
        self.__title = title
        self.__subtitle = subtitle

    def GetTitle(self):
        """ Return the title
        """
        return self.__title

    def GetSubtitle(self):
        """ Return the subtitle
        """
        return self.__subtitle

    def Select(self):
        """ Abstract method 
        used to call a callback
        """
        pass

    def Reverse(self):
        """ Abstract method 
        Used to change the callback that will be used 
        in next Select call. 
        """
        pass

class ActionLong(Action):
    """ Action with start and stop callbacks
    """
    def __init__(self, title, start_callback, stop_callback):
        Action.__init__(self, title)
        self.__actions = [start_callback, stop_callback]

    def Down(self):
        """ Call the start callback
        """
        self.__actions[0]()

    def Up(self):
        """ Call the stop callback
        """
        self.__actions[1]()

class ActionCursor(Action):
    """ Action with increment and decrement callbacks
    """
    subtitles = {-1:u'\u21E7', 1:u'\u21E9'}

    def __init__(self, title, inc_callback, dec_callback):
        self.__increment = 1
        Action.__init__(self, title, self.__class__.subtitles[self.__increment])
        self.actions = {-1: inc_callback, 1: dec_callback}

    def Select(self):
        """ Call increment or decrement callback 
        according to the current increment direction
        """
        self.actions[self.__increment]()

    def Reverse(self):
        """ Reverse the current direction
        """
        self.__increment *= -1

    def GetSubtitle(self):
        """ Return the subtitle
        """
        return self.__class__.subtitles[self.__increment]

class ActionSwitch(Action):
    """ Action that actes as a switch button 
    """
    def __init__(self, on_title, off_title, on_callback, off_callback):
        self.__titles = [on_title, off_title]
        self.__state = 0
        Action.__init__(self, self.__titles[self.__state])
        self.__actions = [off_callback, on_callback]
    
    def Select(self):
        """ Call On callback if state is off 
        and call Off callback if state is on 
        """
        self.__state += 1
        self.__state %= 2
        self.__actions[self.__state]()

    def GetTitle(self):
        """ Return the title
        """
        return self.__titles[self.__state] 

class ActionMenu(Action):
    """ Action used to select an action from a list of actions
    """
    subtitles = {-1:u'\u21E7', 1:u'\u21E9'}

    def __init__(self):
        self.__increment = 1
        Action.__init__(self, "MENU    ", 
                        self.__class__.subtitles[self.__increment])
        self.__actions = []
        self.__idx = 0
  
    def Add(self, action):
        """ Add an action in the menu
        """
        self.__actions.append(action)
  
    def GetCurrentAction(self):
        """ Return the current action
        """
        if len(self.__actions) > 0:
            return self.__actions[self.__idx]
        else:
            return None

    def GetActionTitle(self):
        """ Return the title of the current action
        """
        if len(self.__actions) > 0:
            return self.__actions[self.__idx].GetTitle()

    def GetActionSubtitle(self):
        """ Return the subtitle of the current action
        """
        if len(self.__actions) > 0:
            return self.__actions[self.__idx].GetSubtitle()

    def Select(self):
        """ Change the current action
        """
        if len(self.__actions) > 0:
            self.__idx += self.__increment
            if self.__idx == -1:
                self.__idx += len(self.__actions) 
            else:
                if self.__idx == len(self.__actions):
                    self.__idx = 0

    def Reverse(self):
        """ Reverse the current direction for throwing the menu
        """
        self.__increment *= -1

    def GetSubtitle(self):
        """ Return the subtitle
        """
        return self.__class__.subtitles[self.__increment]
    
class ActionTap(Action):
    """Action class used to mesure speed of taping in bpm
    """
    subtitles = ["(", ")"]
    def __init__(self, bpm_callback):
        self.__state = 0
        Action.__init__(self, "TAP     ", 
                        self.__class__.subtitles[self.__state])
        self.__begin = None
        self.__bpm_function = bpm_callback

    def Select(self):
        """ Used to start or stop mesure
        """
        if self.__begin == None:
            self.__state = 1
            self.__begin = time.time()
            return
        self.__state = 0
        bpm = int(60 / (time.time() - self.__begin))
        self.__bpm_function(bpm)
        self.__begin = None
    
    def GetSubtitle(self):
        """ Return the subtitle
        """
        return self.__class__.subtitles[self.__state]
