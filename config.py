

class Config(object):
    SECRET_KEY = '91149ecd255191465c7d465ac23837ff4b422d6c'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/Central Library'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp@gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'madrid1902fan@gmail.com'
    MAIL_PASSWORD = 'madrid1902'