import os
class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/Restaurante?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
    
config = {
    'development': DevelopmentConfig,
}