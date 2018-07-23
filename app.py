from flask import Flask, render_template, request, url_for, session, redirect, escape, flash
#from hashlib import md5
#from flask.sessions import Session
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import yaml
from forms import RegisterForm

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
	#form = LoginForm()
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
					error = "Wrong password"
		else:
			error = "Username not found"
	return render_template('login.html', error=error)

@app.route('/register', methods = ["GET","POST"]) 
def register():
	#form = RegisterForm()
	#justReg = False
	error = []
	isIssue = False
	if request.method == 'POST':
		# fetch form data
		userDetails = request.form
		username = userDetails['username']
		email = userDetails['email']
		password = userDetails['password']
		confirm_password = userDetails['confirm_password']

		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM user WHERE username = %s", [username])
		
		#error handling
		if cur.fetchone() is not None:
			error.append('Please choose a different username.')
			isIssue = True

		cur.execute("SELECT * FROM user WHERE email = %s", [email])
		
		if cur.fetchone() is not None:
			error.append('Email already registered.')
			isIssue = True

		if password != confirm_password:
			error.append('Passwords do not match.')
			isIssue = True

		if isIssue: # if any errors
			return render_template('register.html', error = error)

		# if no errors, add to database
		cur.execute("INSERT INTO user(email, username, password) VALUES(%s, %s, %s)", (email, username, password))
		mysql.connection.commit()
		cur.close() 
		flash('Congrats! You are now a registered hacker.')
		return redirect(url_for('login'))
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
		isError = False
		error = None
		username_session = escape(session['username']).capitalize()
		

		# Save form info
			# can be any number of submissions
			# limit # of selections to 3 per category?

			# easy fields 
		projIdea_form  = request.form['projIdea']
		compLevel_form = request.form['compLevel']
		gitLink_form = request.form['gitLink'] # unique
		resume_form = request.form['resume'] # unique

			# more selections hereeeeeeeeeeeeee
		hackathon_form  = request.form['hackathon']


		# Error handling (making sure unique entries are actually unique)
		cur = mysql.connection.cursor()

			# unique fields: git + resume links
				#NOT DONE
				# first check if links are duplicates
				# then update row
		cur.execute("SELECT * FROM user WHERE gitLink=%s", (gitLink_form))
		if cur.fetchone() is not None:
			error = 'GitHub link not unique.'
			isError = True
		else:
			cur.execute("UPDATE user SET gitLink=%s WHERE username=%s", (gitLink_form, username)) 
			mysql.connection.commit()

		cur.execute("SELECT * FROM user WHERE resume=%s", (resume_form))
		if cur.fetchone() is not None:
			error = 'Resume link not unique.'
			isError = True
		else:
			cur.execute("UPDATE user SET resume=%s WHERE username=%s", (resume_form, username)) 
			mysql.connection.commit()

	if isError:
		render_template('profile.html', username=username_session, error = error)

		#UPDATE database
		cur.execute("UPDATE user SET projIdea = %s, compLevel = %s WHERE username=%s", (projIdea_form, compLevel_form, username)) 
		mysql.connection.commit()


	# HACKATHON field
	# add hackathon (many to many relationship; insert in usertohackathon table)
		# select statements in user and hackathon tables first?

	# deal with multiselect fields
		# save as array/list
		# cycle through, add each one as a row in many-to-many table

	return render_template('profile.html', username=username_session)

app.secret_key = 'MVB79L'

if __name__ == '__main__':
	
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run(debug=True)
