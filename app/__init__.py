# app/__init__.py

# # Imports

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

# # Initialize application

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from config import BASE_DIR
from app import models, viewer
