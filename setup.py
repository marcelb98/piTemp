#! /usr/bin/env python3

import psycopg2

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
config = dbhost+','+dbuser+','+dbpass+','+dbname
f = open('~/.piTemp/db.conf','w')
f.write(config)
f.close()

print('Setting up database...')
# create table sensors
cursor.execute("CREATE TABLE sensors (sensor CHAR(15) PRIMARY KEY, name VARCHAR(40));")
# create table temps
cursor.execute('''CREATE TABLE temps (id SERIAL PRIMARY KEY, sensor CAHR(15) NOT NULL REFERENCES sensors (sensor),
value DECIMAL, time TIMESTAMP DEFAULT NOW() );''')


conn.close()
cursor.close()
print("Finished.")
