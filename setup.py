#! /usr/bin/env python3

import psycopg2

print('We need an postgresql-database...')
dbname='temp'
dbuser='temp'
dbpass='temp'
dbhost='localhost'

print('Connecting to database...')
try:
	connect_str = "dbname='"+dbname+"' user='"+dbuser"' host='"+dbhost+"' password='"+dbpass+"'"
	conn = psycopg2.connect(connect_str)
	cursor = conn.cursor()
except Exception as e:
	print("There was an error while connecting to the database.")
	sys.exit(1)

print('Setting up database...')
# create table sensors
cursor.execute("""CREATE TABLE sensors (sensor char(15), name char(40));""")
# create table temps
cursor.execute("""CREATE TABLE temps (id SERIAL PRIMARY KEY, sensor char(15), value DECIMAL, time TIMESTAMP DEFAULT NOW() );""")