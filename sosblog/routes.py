from sosblog.models import User, Post
from sosblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask import render_template, url_for,flash, redirect, request
from sosblog import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required

posts = [
	{

	'author':'Gabby',
	'title':'BlogPost 1',
	'content':'This right here is my first post',
	'date':'November 15, 2020'
	},

	{

	'author':'Funmi',
	'title':'BlogPost 2',
	'content':'This right here is my second post',
	'date':'November 16, 2020'

	}
]


cust = [
	
	{
	'agent': 'Moji',
	'service': 'Account Enquiries',
	'phone' : '+2347032648886',
	'available' : 'Monday - Friday, 8am - 5pm'
	},


	{
	'agent': 'Deji',
	'service': 'Login issues',
	'phone' : '+2348132546178',
	'available' : 'Monday - Friday, 8am - 5pm'
	},


	{
	'agent': 'Shola',
	'service': 'Other Packages',
	'phone' : '+2348066973530',
	'available' : 'Monday - Friday, 8am - 5pm'
	},






]

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html',posts = posts, title = 'Home')

@app.route('/about')
def about():
	return render_template('about.html',title = 'About')
@app.route('/ccu')
def ccu():
	return render_template('ccu.html',care=cust, title = 'Customer Care Unit')


@app.route('/register', methods = ['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data , password=hashed_pw )
		db.session.add(user)
		db.session.commit()

		flash('Account created for {}! You can now login'. format(form.username.data), 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title = 'Register', form = form)


@app.route('/login', methods = ['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember = form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect (url_for('home'))
		else:
			flash('Login Unsucessful. Please check email and password', 'danger')
	return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home')) 



@app.route("/account",  methods = ['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated successfully!', 'success')
		return redirect (url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
	return render_template('account.html', title = 'Account', 
							image_file = image_file, form = form)