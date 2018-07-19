from flask import Flask, render_template, request, url_for, session, redirect, escape
#from hashlib import md5
#from flask.sessions import Session
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

#Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

#login_manager = LoginManager()
#login_manager.init_app(app)

@app.route('/', methods = ["GET"]) 
def index():
	if 'username' in session:
		username_session = escape(session['username']).capitalize()
		return render_template('index.html', username=username_session)
		#return redirect(url_for('profile'))
	return render_template('index.html')

@app.route('/login', methods = ["GET", "POST"]) 
def login():
	error = None
	if 'username' in session:
		return redirect(url_for('index'))
	if request.method == 'POST':
		username_form  = request.form['username']
		password_form  = request.form['password']
		cur = mysql.connection.cursor()
		cur.execute("SELECT COUNT(1) FROM user WHERE username = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
		mysql.connection.commit()
		if cur.fetchone()[0]:
			cur.execute("SELECT password FROM user WHERE username = %s;", [username_form]) # FETCH THE PASSWORD
			mysql.connection.commit()
			for row in cur.fetchall():
				if password_form== row[0]:
					session['username'] = request.form['username']
					return redirect(url_for('index'))
				else:
					error = "Invalid Credential"
		else:
			error = "Invalid Credential"
	return render_template('login.html', error=error)

@app.route('/register', methods = ["GET","POST"]) 
def register():
	if request.method == 'POST':
		# fetch form data
		userDetails = request.form
		username = userDetails['username']
		password = userDetails['password']
		email = userDetails['email']
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO user(email, username, password) VALUES(%s, %s, %s)", (email, username, password))
		mysql.connection.commit()
		cur.close() 
		return redirect(url_for('profile'))
	return render_template('register.html')

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/profile')
def profile():
	if 'username' not in session:
		return render_template('index.html')
	if request.method == 'POST':
		# can be any number of submissions
			# limit # of selections to 3 per category?


		hackathon_form  = request.form['hackathon']
		projIdea_form  = request.form['projIdea']

		# more selections hereeeeeeeeeeeeee

		gitLink_form = request.form['gitLink']
		resume_form = request.form['resume']


		cur = mysql.connection.cursor()
		cur.execute("SELECT COUNT(1) FROM user WHERE username = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
		mysql.connection.commit()
		if cur.fetchone()[0]:
			cur.execute("SELECT password FROM user WHERE username = %s;", [username_form]) # FETCH THE PASSWORD
			mysql.connection.commit()
			for row in cur.fetchall():
				if password_form== row[0]:
					session['username'] = request.form['username']
					return redirect(url_for('index'))
				else:
					error = "Invalid Credential"
		else:
			error = "Invalid Credential"
	username_session = escape(session['username']).capitalize()
	return render_template('profile.html', username=username_session)

app.secret_key = 'MVB79L'

if __name__ == '__main__':
	
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run(debug=True)
