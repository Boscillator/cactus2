import os
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

# Force UTC
os.environ['TZ'] = 'Europe/London'
time.tzset()

# initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'insecure key'
app.config['TITLE'] = 'CACTUS 2'

# initialize database
POSTGRES_USER = 'admin'
POSTGRES_PW = 'fredbuchanan'
POSTGRES_DB = 'cactus2'
DB_URL = 'postgres://{user}:{pw}@757c31c1-3144-4eee-905b-633638896b16.8f7bfd8f3faa4218aec56e069eb46187.databases.appdomain.cloud:32282/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, db=POSTGRES_DB)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# initialize admin
app.config['MAPBOX_MAP_ID'] = 'streets-v11'
app.config['MAPBOX_ACCESS_TOKEN'] = 'pk.eyJ1IjoiYm9zY2lsbGF0b3IiLCJhIjoiY2oya3F1bzQzMDBrbjMzczVoNjk5NzE4dCJ9.IGqUQQ3XNps5MVol_Raikg'
app.config['DEFAULT_CENTER_LONG'] = -73.678172
app.config['DEFAULT_CENTER_LAT'] = 42.729340
admin = Admin(app, name="Cactus", template_mode='bootstrap4')

import application.views
import application.api
import application.models
import application.cli
import application.admin