class Config(object):
    pass

class ProdConfig(Config):
    pass
    
class DevConfig(Config):
    TEST = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:Frankline@localhost/waitercallerdb"