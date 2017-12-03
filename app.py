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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

#is configured?
if os.path.isfile(os.path.expanduser("~")+'/.piTemp/piTemp.ini') == False:
	print("Please run setup.py!")
	sys.exit(1)

from flask import Flask, request, render_template
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
	#get dictionary with sensors
	sensors = temp.getSensors()

	# DATA-Structure:
	# rows = []
	# temp1 = ["Temp1",13.37]
	# temp2 = ["Temp2",3.14]
	# rows.append([temp1,temp2,None])

	rows = []
	col = []
	for sensor, name in d.items():
		#get temp
		temp = temp.getTemp(sensor)
		col.append([name,temp])
		#create new row, if 3rd col
		if len(col) == 3:
			rows.append(col)
			col = []
	if len(col) == 1:
		col.append(None)
		col.append(None)
		rows.append(col)
	elif len(col) == 2:
		col.append(None)
		rows.append(col)
	
	return render_template('index.html',rows=rows)

@app.route('/sensors')
def sensors():
	sensors = temp.getHardwareSensors()
	configured_sensors = temp.getSensors()
	return render_template('sensors.html',sensors=sensors,configured_sensors=configured_sensors)

##
## Site the user doesn't see...

@app.route('/static/<string:filename>')
def staticfile(filename):
        #return filename
        return app.send_static_file(filename)

@app.route('/configureSensor/<string:sensor>/<string:name>')
def configureSensor(sensor,name):
	# insert to db
	if temp.nameSensor(sensor, name):
		# redirect to /sensors
		return redirect(url_for('sensors'))
	else:
		return render_template('error.html',error="Couldn't register sensor...")

@app.route('/deleteSensor/<string:sensor>')
def deleteSensor(sensor):
	if temp.deleteSensor(sensor):
		return redirect(url_for('sensors'))
	else:
		return render_template('error.html',error="Couldn't delete sensor...")

if __name__ == "__main__":
	app.run('0.0.0.0',port=8080)

