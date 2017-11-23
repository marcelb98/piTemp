#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import temp

sensors = temp.getSensors()
for sensor in sensors:
	print("SENSOR: addr:"+sensor[0]+" name:"+sensor[1])

