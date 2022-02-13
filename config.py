import os
from dotenv import load_dotenv  

# provides access to project in any OS
basedir = os.path.abspath(os.path.dirname(__file__))  

# allows outside files/folders to be added to project from directory
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    """
    Set Config variables for the flask app. Using environment variables where available.
    Where otherwise, create config Config variable if not done already.
    """

    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Random string here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # turn off update messages from SQL