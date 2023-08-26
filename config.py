import os


class Config:
    SECRET_KEY = os.environ.get("RUNWAY_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("RUNWAY_DATABASE_URL")
