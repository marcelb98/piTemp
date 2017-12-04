#! /usr/bin/env python3
# -*- coding: utf-8 -*-

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
import psycopg2
from os.path import expanduser
import configparser
import re
import time

class piTemp:
		
	def __init__(self):
		#is configured?
		if os.path.isfile(os.path.expanduser("~")+'/.piTemp/piTemp.ini') == False:
			print("Please run setup.py!")
			sys.exit(1)
		
		# open config
		self.config = configparser.ConfigParser()
		self.config.read('/home/pi/.piTemp/piTemp.ini')
	
		# get db-settings
		try:
			connect_str = "dbname='"+self.config['DB']['dbname']+"' user='"+self.config['DB']['user']+"' host='"+self.config['DB']['host']+"' password='"+self.config['DB']['pass']+"'"
			self.conn = psycopg2.connect(connect_str)
			self.conn.autocommit = True
			self.cursor = self.conn.cursor()
			return None
		except Exception as e:
			print(e.message)
			print("Couldn't connect to DB...")
			self.conn = None
			self.cursor = None
			return None

	def closeDB(self):
		self.cursor.close()
		self.conn.close()

	def getSensors(self):
		# get configured sensors (from db)
		# RETURN: dictionary with sensor => name
		sensors = {}
	
		self.cursor.execute('SELECT sensor, name FROM sensors')
		result = self.cursor.fetchall()
		for row in result:
			sensors[ row[0] ] = row[1]
	
		return sensors
	
	def getHardwareSensors(self):
		# Detect sensors which are actually connected
		# RETURN: List of sensor-IDs [sensor1, sensor2, ...]
		sensors = []
		for subdir, dirs, files in os.walk('/sys/bus/w1/devices'):
			for sensor in dirs:
				if ( sensor != 'w1_bus_master1'):
					sensors.append(sensor)
		return sensors

	def getTemp(self,sensor):
		# get temp (as float), saves temp in db
		# returns temp on success or -100 (IOError) or -99 (temp==None)

		t = None
		try:
			f = open('/sys/bus/w1/devices/'+sensor+'/w1_slave', "r")
			line = f.readline()
			if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
				line = f.readline()
				m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
				if m:
					t = float(m.group(2)) / 1000.0
			f.close()
		except IOError as e:
			return -100
		if t == None:
			return -99
	
		# save temp
		try:
			time = str(int(time.time()))
			self.cursor.execute('INSERT INTO temps (sensor, value, time) VALUES (%s, %f, %d)', (sensor, t, time,))
		except Exception as e:
			print("Couldn't save temp to db")
	
		# return temp
		return t

	def nameSensor(self, sensor, name):
		# Configure or rename sensor
		# create/update db-entry in table 'sensors'.
	
		self.cursor.execute('SELECT count(name) FROM sensors WHERE sensor = %s LIMIT 1', (sensor,))
		count = self.cursor.fetchall()[0][0]
		if count > 0:
			#we have to update
			self.cursor.execute('UPDATE sensors SET name = %s WHERE sensor = %s', (name,sensor))
		else:
			#we have to configure
			self.cursor.execute('INSERT INTO sensors (sensor,name) VALUES (%s, %s)', (sensor,name))
		return True

	def deleteSensor(self, sensor):
		# Delete sensor and his data
		# returns True or False
		
		try:
			self.cursor.execute('DELETE FROM temp WHERE sensor = %s', (sensor,))
			self.cursor.execute('DELETE FROM sensors WHERE sensor = %s LIMIT 1', (sensor,))
		except Exception as e:
			return False

