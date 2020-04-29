import os

current_path = os.path.dirname(os.path.realpath(__file__))


class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('STEPIK_DELIVERY_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db' # os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
