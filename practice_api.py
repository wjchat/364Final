import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField, IntegerField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flickrapi import FlickrAPI
from pprint import pprint
from keys import FLICKR_PUBLIC, FLICKR_SECRET



flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')
extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string from si364'
## TODO 364: Create a database in postgresql in the code line below, and fill in your app's database URI. It should be of the format: postgresql://localhost/YOUR_DATABASE_NAME

## Your final Postgres database should be your uniqname, plus HW5, e.g. "jczettaHW5" or "maupandeHW5"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:guest@localhost:5432/HW5"
# ## Provided:
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

##################
### App setup ####
##################
manager = Manager(app)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)


#so this is just a test of how i will implement my api in the main project. basically, I'm gonna use form input from the user to send a request to 
#flickr's api and it will return about thirty pictures and their titles to be displayed on the screen. This information will have the option 
#to be saved and put into a database


##helper function

#will be used to get picturs and display them on a page. some will get stored in a database
def get_pics(term):

	cats = flickr.photos.search(text=term, per_page=5, extras=extras)
	photos = cats['photos']

	pics = []
	for each in photos['photo']:
		
		pics.append((each['url_sq'], each['title']))

	return(pics)

#will be used to get brands and display them on a page
def see_cameras():

	cameras = flickr.cameras.getBrands()

	return cameras['brands']['brand']


#will be used to get models and display them on a page. some will get stored in a database
def see_models(brand):

	models = flickr.cameras.getBrandModels(brand = brand)


	return models['cameras']['camera']

@app.route('/', methods = ["POST", "GET"])
def index():

	# cats = flickr.photos.search(text='plum', per_page=5, extras=extras)
	# photos = cats['photos']

	# pics = []
	# for each in photos['photo']:
		
	# 	pics.append((each['url_q'], each['title']))

	pics = get_pics('kitten')

	cameras = see_cameras()
	models = see_models('apple')

	return(render_template('index.html', photos = pics, cameras = cameras, models = models))


if __name__ == "__main__":
    # db.create_all()
    manager.run()
