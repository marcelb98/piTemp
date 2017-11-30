#! /usr/bin/env python3

import os
import psycopg2
from os.path import expanduser

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

# write database-settings
if os.path.exists(expanduser("~")+'/.piTemp') == False:
	print("Creating config-dir ~/.piTemp ...")
	os.mkdir(expanduser("~")+'/.piTemp')
config = dbhost+','+dbuser+','+dbpass+','+dbname
f = open(expanduser("~")+'/.piTemp/db.conf','w')
f.write(config)
f.close()

print('Setting up database...')
# create table sensors
cursor.execute("CREATE TABLE IF NOT EXISTS sensors (sensor CHAR(15) PRIMARY KEY, name VARCHAR(40));")
# create table temps
cursor.execute('''CREATE TABLE IF NOT EXISTS temps (id SERIAL PRIMARY KEY, sensor CHAR(15) NOT NULL REFERENCES sensors (sensor),
value DECIMAL, time TIMESTAMP DEFAULT NOW() );''')


conn.close()
cursor.close()
print("Finished.")
