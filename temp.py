#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import psycopg2
from os.path import expanduser
import configparser

#is configured?
if os.path.isfile(os.path.expanduser("~")+'/.piTemp/piTemp.ini') == False:
	print("Please run setup.py!")
	sys.exit(1)

#global vars
conn = None
cursor = None
config = configparser.ConfigParser()
config.read(expanduser("~")+'/piTemp.ini')

def setupDb():
	global conn
	global cursor
	global config

	# get db-settings
	try:
		connect_str = "dbname='"+config['DB']['dbname']+"' user='"+config['DB']['user']+"' host='"+['DB']['host']+"' password='"+config['DB']['pass']+"'"
        	conn = psycopg2.connect(connect_str)
        	cursor = conn.cursor()
		return True
	except Exception as e:
		return False

def closeDB():
	cursor.close()
	conn.close()

def getSensors():
	# get configured sensors (from db)
	# RETURN: dictionary with sensor => name
	sensors = {}

	cursor.execute('SELECT sensor, name FROM sensors', (sensor))
        result = cursor.fetchall()
	for row in result:
		sensors[ row[0] ] = row[1]

	# do some great stuff
	return sensors
	
def getHardwareSensors():
	# Detect sensors which are actually connected
	# RETURN: List of sensor-IDs [sensor1, sensor2, ...]
	sensors = []
	for subdir, dirs, files in os.walk('/sys/bus/w1/devices'):
		for sensor in dirs:
			if ( sensor != 'w1_bus_master1'):
				sensors.append(sensor)
	return sensors

def getTemp(sensor):
	# get temp, saves temp in db
	# returns temp on success or False
	temp = None
	try:
		f = open('/sys/bus/w1/devices/'+sensor+'/w1_slave', "r")
		line = f.readline()
		if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
			line = f.readline()
			m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
			if m:
				temp = str(float(m.group(2)) / 1000.0)
		f.close()
	except (IOError), e:
		return False
	if temp == None:
		return False

	# save temp
	try:
		cursor.execute('INSERT INTO temps (sensor, value, time) VALUES (%s, %f, %d)', (sensor, temp, time))
	except Exception e:
		return False

	# return temp
	return temp

def nameSensor(sensor, name):
	# Configure or rename sensor
	# create/update db-entry in table 'sensors'.
	cursor.execute('SELECT count(name) FROM sensors WHERE sensor = %s LIMIT 1', (sensor))
	count = cursor.fetchall()[0][0]
	if count > 0:
		#we have to update
		cursor.execute('UPDATE sensors SET name = %s WHERE sensor = %s', (name,sensor))
	else:
		#we have to configure
		cursor.execute('INSERT INTO sensors (sensor,name) VALUES (%s, %s)', (sensor,name))
	return True

def deleteSensor(sensor):
	# Delete sensor and his data
	# returns True or False
	try:
		cursor.execute('DELETE FROM temp WHERE sensor = %s', (sensor))
		cursor.execute('DELETE FROM sensors WHERE sensor = %s LIMIT 1', (sensor))
	except Exception e:
		return False

