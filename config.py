class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:123@127.0.0.1:3306/gms"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
