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
import psycopg2
from os.path import expanduser
import configparser

#is configured?
if os.path.exists(expanduser("~")+'/.piTemp') == False:
	print("Creating config-dir ~/.piTemp ...")
	os.mkdir(expanduser("~")+'/.piTemp')
if os.path.isfile(expanduser("~")+'/piTemp.ini') == False:
	f = open(expanduser("~")+'/.piTemp/piTemp.ini', 'w')
	f.write('')
	f.close()

#open config
config = configparser.ConfigParser()
config.read(expanduser("~")+'/.piTemp/piTemp.ini')

#input
print('We need an postgresql-database...')
dbname=input('Database: ')
dbuser=input('Username: ')
dbpass=input('Password: ')
dbhost=input('Host: ')

print('Connecting to database...')
try:
	connect_str = "dbname='"+dbname+"' user='"+dbuser+"' host='"+dbhost+"' password='"+dbpass+"'"
	conn = psycopg2.connect(connect_str)
	cursor = conn.cursor()
except Exception as e:
	print("There was an error while connecting to the database.")
	sys.exit(1)

# set database-settings in config
if ('DB' in config) == False:
	print('Creating DB-settings in config')
	config.add_section('DB')
else:
	print('Updateing DB-settings in config')
config['DB']['host'] = dbhost
config['DB']['user'] = dbuser
config['DB']['pass'] = dbpass
config['DB']['dbname'] = dbname

print('Setting up database...')
# create table sensors
cursor.execute("CREATE TABLE IF NOT EXISTS sensors (sensor CHAR(15) PRIMARY KEY, name VARCHAR(40));")
# create table temps
cursor.execute('''CREATE TABLE IF NOT EXISTS temps (id SERIAL PRIMARY KEY, sensor CHAR(15) NOT NULL REFERENCES sensors (sensor),
value DECIMAL, time TIMESTAMP DEFAULT NOW() );''')


conn.close()
cursor.close()

# write config to file
with open(expanduser("~")+'/.piTemp/piTemp.ini', 'w') as configfile:
	config.write(configfile)

print("Finished.")
