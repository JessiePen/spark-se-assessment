import os
from pickle import FALSE
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'sqlite:///'
database_name = 'diagnostic'

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'diagnostic_secret')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name
    ALLOWED_HOSTS = ['pengyh-spark519-assessment.herokuapp.com', '127.0.0.1']


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test.db'
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'diagnostic_secret'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///diagnostic'
