import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        'mysql+mysqlconnector://admin:FxNc10082002*@marketplace-create.ctymya2qk1r6.us-east-1.rds.amazonaws.com:3306/createdb'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False