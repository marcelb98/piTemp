#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

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

def configureSensor(sensor, name):
	# Configure sensor
	# create db-entry in table 'sensors'.

	return True;

