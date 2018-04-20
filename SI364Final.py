## used code from homework4 to compare and check login process

import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import re
# Imports for login management
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
####################################
#special modules#
from flickrapi import FlickrAPI
from pprint import pprint
from keys import FLICKR_PUBLIC, FLICKR_SECRET
############################
# Application configurations
############################
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string from si364'
## TODO 364: Create a database in postgresql in the code line below, and fill in your app's database URI. It should be of the format: postgresql://localhost/YOUR_DATABASE_NAME

## Your final Postgres database should be your uniqname, plus HW5, e.g. "jczettaHW5" or "maupandeHW5"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:guest@localhost:5432/final"
## Provided:
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

##################
### App setup ####
##################
# App addition setups
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) # set up login manager

#flickr setup 
flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
#########################
##### Set up Models #####
#########################


#association table
#saved_photos = db.Table('saved_photos',db.Column('Photos',db.Integer, db.ForeignKey('Photos.id')),db.Column('User',db.Integer, db.ForeignKey('User.id')))
#users_in_convo = db.Table('users_in_convo', db.Column('Conversation', db.Integer, db.ForeignKey('Conversation.id')), db.Column('User', db.Integer, db.ForeignKey('User.id')))
camera_collection = db.Table('user_collection', db.Column('Cameras', db.Integer, db.ForeignKey('Cameras.id')), db.Column('cameraCollection', db.Integer, db.ForeignKey('cameraCollection.id')))

class User(UserMixin, db.Model):
	__tablename__ = 'User'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(225), unique = True)
	email = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	first_name = db.Column(db.String(225))
	last_name = db.Column(db.String(225))
	pics = db.relationship('Photos', backref = 'User')
	collections = db.relationship('cameraCollection', backref = 'User')

	#special properties for passwords and loggin in
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

## DB load function
## Necessary for behind the scenes login manager that comes with flask_login capabilities! Won't run without this.
@login_manager.user_loader
def load_user(user_id):
	return User.query.filter_by(id = user_id).first() # returns User object or None

class Photos(db.Model): #table of saved photos, has many-many relationship with users
	__tablename__ = 'Photos'
	id = db.Column(db.Integer, primary_key = True)
	pic_url = db.Column(db.String)
	title = db.Column(db.String)
	#many-to-many relationship with users
	user = db.Column(db.Integer, db.ForeignKey('User.id'))

class cameraCollection(db.Model):
    __tablename__ = 'cameraCollection'
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.Integer, db.ForeignKey('User.id'))
    # This model should also have a many to many relationship with the Camera model (one camera might be in many personal collections, one personal collection could have many cameras in it).
    cameras = db.relationship('Cameras', secondary = camera_collection, backref = db.backref('cameraCollection', lazy = 'dynamic'), lazy = 'dynamic')



class Messages(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	image = db.Column(db.String)
	text = db.Column(db.String)
	sender = db.Column(db.String) #username of sending users
	reciever = db.Column(db.String) #username of recieving user
	#conversation = db.Column(db.Integer, db.ForeignKey('Conversation.id')) #links messages to conversation


##possibly convert to many-many for personal not shared list of saved cams
class Cameras(db.Model):
	__tablename__ = 'Cameras'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String)
	votes = db.Column(db.Integer)
	rating= db.Column(db.Integer)




	


########################
##### Set up Forms #####
########################
#login form

def password_length(form, field):
	password = field.data
	if len(password) < 7:
		raise ValidationError('Password must be more than 7 characters long')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1,64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')


#user registration from, used in create account view
class RegistrationForm(FlaskForm):
	email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
	first_name = StringField('First Name', validators = [Required()])
	last_name = StringField('Last Name', validators = [Required()])
	username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
	password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match"), password_length])
	password2 = PasswordField("Confirm Password:",validators=[Required(), password_length])
	submit = SubmitField('Register User')

	#Additional checking methods for the form
	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already taken')

class PhotoForm(FlaskForm):
	search = StringField('Search', validators = [Required()])
	submit = SubmitField('Search')

def message_length(form, field):
	message = field.data
	if len(message) > 100:
		raise ValidationError('Message must be less than 100 characters long')

class SendForm(FlaskForm):
	recipient = StringField('Who would you like to send this form to? Please enter their username.', validators = [Required()])
	message = StringField('Add a message:', validators = [Required(), message_length])
	submit = SubmitField('Send')



class CameraForm(FlaskForm):
	rate = IntegerField('rate this camera', validators = [Required()])
	submit = SubmitField('Rate')


################################
####### Helper Functions #######
################################

##bring up list of camaeras flicker knows about
def see_cameras():
	cameras = flickr.cameras.getBrands()
	return cameras['brands']['brand']


#will be used to get models and display them on a page. some will get stored in a database
def see_models(brand):
	models = flickr.cameras.getBrandModels(brand = brand)
	
	return models['cameras']['camera']

def add_photo(user, url, title):

	pic = Photos.query.filter_by(pic_url = url, user = user.id).first()

	if not pic:
		pic = Photos(pic_url = url, title = title, user = user.id)
		db.session.add(pic)
		db.session.commit()

		return pic

	else:
		flash('You\'ve already saved ' + title)
	
def create_message(sender, recipient, message, photo): #takes id of two users
	
	message = Messages(image = photo, text = message, sender = sender, reciever = recipient)
	db.session.add(message)
	db.session.commit()
	return message

def get_or_create_collection(user):

    collection = cameraCollection.query.filter_by(user = user.id).first()
    # In other words, based on the input to this function, if there exists a collection with the input name, associated with the current user, then this function should return that PersonalGifCollection instance.
    if collection:
        return collection
    # However, if no such collection exists, a new PersonalGifCollection instance should be created, and each Gif in the gif_list input should be appended to it (remember, there exists a many to many relationship between Gifs and PersonalGifCollections).
    else:
        collection = cameraCollection(user = current_user.id)        
        db.session.add(collection)
        db.session.commit()
        return collection

def get_or_create_camera(name, rating):
	camera = Cameras.query.filter_by(name = name).first()

	if not camera:
		camera = Cameras(name = name, votes = 1, rating = rating)
		db.session.add(camera)
		db.session.commit()

		return camera
	else:
		votes = camera.votes
		camera.votes = int(votes) + 1
		camera.rating = (int(camera.rating) + int(rating)) / camera.votes
		db.session.add(camera)
		db.session.commit()
		return camera


###################################
##### Routes & view functions #####
###################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods = ['POST','GET'])
def login():
	#will return login template and process login. links to create account
	form = LoginForm()
	# flash('loaded')
	if request.method == 'POST':
		# flash('post')
		if form.validate_on_submit():
			# flash('validated')
			user = User.query.filter_by(email=form.email.data).first()
			if user is not None and user.verify_password(form.password.data):
				login_user(user, form.remember_me.data)
				return redirect(url_for('index'))
			flash('Invalid username or password.')
		else:
			flash('Username is invalid.')
	return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))

@app.route('/home', methods = ['POST','GET'])
# @login_required
def index():
	form = PhotoForm()
	return render_template('home.html', form = form)
	#home pag. returns home templater. eturns form to search for pictures. can redirect to search results. Lihnks to saved photos, messages, cameras, and all_models.

@app.route('/saved_photos', methods = ['POST','GET'])
@login_required
def saved():
	

	if request.method == 'POST':
		photo = request.form.get('delete')
		thisphoto = Photos.query.filter_by(id = int(photo)).first()

		db.session.delete(thisphoto)
		db.session.commit()

	photos = Photos.query.filter_by(user = current_user.id).all()

	return render_template('saved_photos.html', photos = photos)
		# returns template to show all photos saved by user. returns form to unsave or to send photos. send photo redirects to messages

@app.route('/register', methods = ['POST', 'GET'])
def register():
		#returns create account template. returns form to create new user. redirects to login page.
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,username=form.username.data,password=form.password.data, first_name = form.first_name.data, last_name=form.last_name.data)
		db.session.add(user)
		db.session.commit()
		flash('You can now log in!')
		return redirect(url_for('login'))
	else:
		flash('Error with form submission, try again. Be sure email is valid and passwords match')
	errors = [v for v in form.errors.values()]
	if len(errors) > 0:
		flash(errors[0][0])

	return render_template('registration.html',form=form)

@app.route('/search_results', methods = ['POST', 'GET'])
@login_required
def search_results():
	#return template based on input from search photos form. shows 30 pics and can return for to save or send photos. save reedirects
	#to same page, send redirects to send page

	term = request.args.get('search')

	callback = flickr.photos.search(text=term, per_page=30, extras=extras)
	photos = callback['photos']

	pics = []
	for each in photos['photo']:
		
		pics.append((each['url_sq'], each['title']))

	if request.method =='POST':
		photo = request.form.get('photo')

		tings = re.findall(r'\'(.*?)\'', photo)
		picture = add_photo(current_user, tings[0], tings[1])	

		if picture:
			flash(picture.title + ' has been saved')

	return render_template('search_photos.html', term = term, results = pics)


@app.route('/messages', methods = ['POST', 'GET'])
@login_required
def messages():
	#returns template for conversations. if i have time, i will implement jquery to make experience better. will display all conversations
	recieved = Messages.query.filter_by(reciever = current_user.username).all()
	sent = Messages.query.filter_by(sender = current_user.username).all()


	return render_template('messages.html', sent = sent, recieved = recieved)


@app.route('/send_photo<photoID>', methods = ['POST', 'GET'])
@login_required
def send_photo(photoID):
	#returns template to let user send photo to another user. will be appended to conversations database
	
	photo = Photos.query.filter_by(id = photoID).first()
	form = SendForm()

	if form.validate_on_submit():
		user1 = current_user
		user2 = User.query.filter_by(username = form.recipient.data).first()
		# flash(user1.id)
		# flash(user2.id)
		# flash(photo.id)
		if not user2:
			flash('This username is incorrect or does not exist, try again')
			
		else:
			message = create_message(sender = user1.username, photo = photo.pic_url, message = form.message.data, recipient = user2.username )
			flash('Message successfully sent to ' + user2.first_name + ' ' + user2.last_name)
	
	errors = [v for v in form.errors.values()]
	if len(errors) > 0:
		flash(errors[0][0])

	return render_template('send_photo.html', form = form, photo = photo)


@app.route('/cameras', methods = ['POST', 'GET'])
@login_required
def cameras():
	#will return template with list of all brands flickr knows about. will return form if user selects a brand a will redirect to models

	cameras = see_cameras()

	return(render_template('cameras.html', cameras = cameras))


@app.route('/models<brand>', methods = ['POST', 'GET'])
@login_required
def models(brand):
	#will return list of models of a certain brand. will return form that allows users to add a model to a public "reccomended" forum.
	models = see_models(brand)
	form = CameraForm()

	return render_template('models.html', brand = brand, models = models, form = form)

@app.route('/all_models', methods = ['POST', 'GET'])
@login_required
def all_models():
	#will return a template with a list of all reccomended cameras and thier vote score.
	cameras = Cameras.query.all()
	return render_template('all_cameras.html', cameras = cameras)
@app.route('/your_models<camName>', methods = ['POST', 'GET'])
@login_required
def your_models(camName):
	
	if request.form:
		rating = request.form.get('rate')

	camera = get_or_create_camera(camName, rating = rating) #adds camera to database / adjusts rating
	
	collection = get_or_create_collection(user = current_user) #gets cameras of user or creates collection

	collection.cameras.append(camera)
	db.session.add(collection)
	db.session.commit()

	user_cameras = collection.cameras.all()	
	
	return render_template('your_models.html', cameras = user_cameras)




if __name__ == "__main__":
	db.create_all()
	manager.run()
