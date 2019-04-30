class Config(object):
    pass

class ProdConfig(Config):
    pass
    
class DevConfig(Config):
    TEST = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:Frankline@localhost/waitercallerdb"
    SECRET_KEY = "Lf0g43zfaz5jrRLbJRzqzPdpRz6SLx0R4sns7oht9wkwAjy9xNWCbxipIWZ7x9uMMLSiQI3DAbzpGvaLWDNHgOa4rje8Vga/jjs"
    SQLALCHEMY_TRACK_MODIFICATIONS =True
    base_url = "http://127.0.0.1:5000/"