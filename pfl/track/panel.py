"""
module pfl.track.panel
A graphical view of pfl track .

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

from utils.widget import SelectablePanel

class TrackPanel(SelectablePanel):
    """ Track panel
    """
    def __init__(self, parent):
        SelectablePanel.__init__(self, parent, 'Track')
    
    def RefreshDuration(self):
        """ Refresh duration panel
        """
        pass
