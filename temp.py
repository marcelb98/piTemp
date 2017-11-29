#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import psycopg2

#global vars
conn = None
cursor = None

def setupDb():
	global conn
	global cursor

	# get db-settings
	config = None
	with open('~/.piTemp/db.conf') as f:
		config = f.read()
	if config == None:
		return False
	config = config.split(',')
	try:
		connect_str = "dbname='"+config[3]+"' user='"+config[1]+"' host='"+config[0]+"' password='"+config[2]+"'"
        	conn = psycopg2.connect(connect_str)
        	cursor = conn.cursor()
		return True
	except Exception as e:
		return False

def closeDB():
	cursor.close()
	conn.close()

def getSensors():
	with open('/etc/piTemp/sensors.csv') as f:
		config = f.readlines()
	sensors = []
	for sensor in config:
		sensor = sensor.split(",")
		if len(sensor) == 2:
			sensor[0] = sensor[0].rstrip()
			sensor[1] = sensor[1].rstrip()
			sensors.append(sensor)
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
	return 42

def nameSensor(sensor, name):
	# Configure or rename sensor
	# create/update db-entry in table 'sensors'.
	cursor.execute('SELECT count(name) FROM sensors WHERE sensor = %s LIMIT 1', (sensor))
	count = cursor.fetchall()[0][0]
	if count > 0:
		#we have to update
		cur.execute('UPDATE sensors SET name = %s WHERE sensor = %s', (name,sensor))
	else:
		#we have to configure
		cur.execute('INSERT INTO sensors (sensor,name) VALUES (%s, %s)', (sensor,name))
	return True;

