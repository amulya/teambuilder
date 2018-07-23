from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import InputRequired, EqualTo, Email

class RegisterForm(FlaskForm): # new users
	username 	= StringField('Username', [InputRequired()])
	email 		= StringField('Email', [InputRequired(), Email()])
	password 	= PasswordField('Password', [InputRequired(), EqualTo('password', message = 'Passwords must match')])
	confirm_password = PasswordField('Confirm Password', [InputRequired()])
	submit 		= SubmitField('Register')

	#def validate_username(self, username):
		#cur = mysql.connection.cursor()
		#cur.execute("SELECT * FROM user WHERE username = %s", [username])
		#user = User.query.filter_by(username=username.data).first()
		#if cur.fetchone() is not None:
			#raise ValidationError('Please use a different username.')

class LoginForm(FlaskForm): # users
	#email = StringField('Email', validators=[DataRequired()])
	username = StringField('Username', [InputRequired()])
	password = PasswordField('Password', [InputRequired()])
	#remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class GatherForm(FlaskForm): # user profiles
	hackathon = StringField('Hackathon', [InputRequired()])
	# group =
	projIdea = StringField('Interests', [InputRequired()])
	tech = StringField('Technologies', [InputRequired()])
	interests = StringField('Interests', [InputRequired()])
	languages = StringField('Languages', [InputRequired()])
	# Competition level
	compLevel = RadioField('Seriousness', choices =[("casual", "casual"), ("competitive", "competitive")])
	exper = StringField('Experience level', [InputRequired()])
	hardware = RadioField('Hardware', [InputRequired()], choices =[("Yes", "yes"), ("No", "no")])
	hardwareType = StringField('Hardware type(s)', [InputRequired()])
	resume = StringField('Resume link', [InputRequired()])
