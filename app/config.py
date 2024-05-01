#!/usr/bin/python3
"""config file"""
from os import getenv
import secrets
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer


class Config:
    load_dotenv()
    SECRET_KEY = secrets.token_hex(16)
    SQL_USERNAME = getenv('SQL_USERNAME')
    SQL_PASS = getenv('SQL_PASS')
    SQLALCHEMY_DATABASE_URI = f"mysql://{SQL_USERNAME}:{SQL_PASS}@localhost/medical"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'cclogisticsapp@gmail.com'
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = ('Medicare', 'cclogisticsapp@gmail.com')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

def configure():
    load_dotenv()

serialize_token = URLSafeTimedSerializer(Config.SECRET_KEY)
