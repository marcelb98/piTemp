#! /usr/bin/env python3

# https://pythonspot.com/en/flask-web-app-with-python/

from flask import Flask, request, render_template
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
	rows = []
	temp1 = ["Innen",20.1]
	temp2 = ["Außen",2.3]
	rows.append([temp1,temp2,None])
	return render_template('index.html',rows=rows)

@app.route('/static/<string:filename>')
def staticfile(filename):
	#return filename
	return app.send_static_file(filename)

@app.route('/sensors')
def test():
	sensors = ["a","b"]
	return render_template('sensors.html',sensors=sensors)

@app.route('/configureSensor/<string:sensor>/<string:name>')
def configureSensor(sensor,name):
	# insert to db
	if temp.configureSensor(sensor, name):
		# redirect to /sensors
	else:
		return render_template('error.html',error="Couldn't register sensor...")

if __name__ == "__main__":
	app.run('0.0.0.0',port=8080)

