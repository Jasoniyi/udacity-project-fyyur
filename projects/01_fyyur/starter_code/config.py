import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = '<Put your local database url>'
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/fyyurDB'
# SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config:
    SECRET_KEY = 'wisdom'
    DEBUG = DEBUG
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/fyyurDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
