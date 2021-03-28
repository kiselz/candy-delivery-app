"""Different application configurations"""
import os


class Config:
    """Base configuration"""

    SECRET_KEY = 'justrandomstring'
    SERVER_DIR = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.join(SERVER_DIR, os.pardir)
    DB_SCHEMA_PATH = os.path.join(PROJECT_ROOT, 'database/', 'schema.sql')


class DevConfig(Config):
    """Development configuration"""
    DEBUG = True
    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)


class ProdConfig(Config):
    """Production configuration"""
    ENV = 'production'
    DB_NAME = 'really_serious_name.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)


class TestConfig(Config):
    """Test configuration"""
    TESTING = True
    DEBUG = True
    DB_NAME = 'test.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
