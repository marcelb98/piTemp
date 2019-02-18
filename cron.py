#! /usr/bin/env python3

# Copyright 2017 Marcel Beyer
#
# This file is part of piTemp.
#
# piTemp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# piTemp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with piTemp.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from temp import piTemp

#is configured?
if os.path.isfile(os.path.expanduser("~")+'/.piTemp/piTemp.ini') == False:
	print("Please run setup.py!")
	sys.exit(1)
	
temp = piTemp()

sensors = temp.getSensors()

for sensor, name in sensors.items():
	#get temp
	t = temp.getTemp(sensor)
	if temp.saveTemp(sensor,t):
		print(sensor+' OK '+str(t))

		temp.sendTemp(sensor,t)
	else:
		print(sensor+' ERR '+str(t))

temp.closeDB()
