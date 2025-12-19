import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    WTF_CSRF_ENABLED = True
    DEBUG = False
    TESTING = False