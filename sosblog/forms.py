from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email,EqualTo,ValidationError
from flask_login import current_user

class RegistrationForm(FlaskForm):
	username = StringField('Username',
					validators =[DataRequired(), Length(min =5, max = 20)])
	email = StringField('Email',
							validators = [DataRequired(),Email(), Length(max = 50)])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', 
					validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')


	def validate_username(self,username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username Already Exists')

	def validate_email(self,email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email Taken')


class LoginForm(FlaskForm):
	email = StringField('Email',
							validators = [DataRequired(),Email(), Length(max = 50)])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')



class UpdateAccountForm (FlaskForm):
	username = StringField('Username',
					validators =[DataRequired(), Length(min =5, max = 20)])
	email = StringField('Email',
							validators = [DataRequired(),Email(), Length(max = 50)])
	submit = SubmitField('Update')


	def validate_username(self,username):
		user = User.query.filter_by(username = form.username.data).first()
		if user:
			raise ValidationError('Username Already Exists')

	def validate_email(self,email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('Email Already Exists')
