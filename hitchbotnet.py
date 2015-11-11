# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash, json, jsonify
from contextlib import closing

# configuration
DATABASE = '/tmp/hitchbotnet.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# connect to db
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# initalize the database
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()


# default view /
@app.route('/')
def map_view():
	cur = g.db.execute('select timestamp, latitude, longitude, gpsaccuracy from entries order by id desc')
	entries = [dict(timestamp=row[0], latitude=row[1], longitude=row[2], gpsaccuracy=row[3]) for row in cur.fetchall()]
	return render_template('map.html', entries=entries)


# map JSON points
@app.route('/_mappoints.json')
def map_points():
	cur = g.db.execute('select timestamp, latitude, longitude from entries order by id desc')
	entries = [dict(information=row[0], latitude=row[1], longitude=row[2]) for row in cur.fetchall()]
	return jsonify(markers=entries)


# entries view
@app.route('/entries')
def show_entries():
	if not session.get('logged_in'):
		abort(401)
	cur = g.db.execute('select timestamp, latitude, longitude, gpsaccuracy, battery, temperature, lastwake, recieved from entries order by id desc')
	entries = [dict(timestamp=row[0], latitude=row[1], longitude=row[2], gpsaccuracy=row[3],
				battery=row[4], temperature=row[5], lastwake=row[6], recieved=row[7]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)
	

# /checkin
@app.route('/checkin', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	#TODO: Authenciation for HitchDroid client
	g.db.execute('insert into entries (timestamp, latitude, longitude, gpsaccuracy, battery, temperature, lastwake) values (?, ?, ?, ?, ?, ?, ?)',
				[request.form['timestamp'], request.form['latitude'], request.form['longitude'], request.form['gpsaccuracy'], request.form['battery'], request.form['temperature'], request.form['lastwake']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('map_view'))
	return render_template('login.html', error=error)


#logout
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('map_view'))


if __name__ == '__main__':
	app.run()
	# DO NOT RUN WITH THIS IN DEBUG MODE
	#app.run(host='0.0.0.0')
	
	