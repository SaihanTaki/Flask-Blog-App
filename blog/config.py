import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    """Base configuration."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASK_ADMIN_SWATCH = 'flatly'


class ProdConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +os.path.join(basedir, 'data.sqlite')


class DevConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +os.path.join(basedir, 'data.sqlite')


class TestConfig(BaseConfig):
    """Testing configuration."""
    SECRET_KEY = "test"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +os.path.join(basedir, 'test.sqlite')
    WTF_CSRF_ENABLED = False
    





