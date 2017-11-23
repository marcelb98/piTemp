#! /usr/bin/env python3

# https://pythonspot.com/en/flask-web-app-with-python/

from flask import Flask, request, render_template
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/static/<string:filename>')
def staticfile(filename):
	#return filename
	return app.send_static_file(filename)

@app.route('/test/<string:txt>/')
def test(txt):
	return render_template('test.html',txt=txt)

if __name__ == "__main__":
	app.run('0.0.0.0',port=8080)

