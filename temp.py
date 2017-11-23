#! /usr/bin/env python3
# -*- coding: utf-8 -*-

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
		

def getTemp(sensor):
	return 42

