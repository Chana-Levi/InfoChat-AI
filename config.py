import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 123)
    GOOGLE_CLIENT_ID = '65139853999-4r04livdor493u1gkpvu9deakh3lcq09.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

config = Config()