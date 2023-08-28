import os


# ISSUE -- Why bother storing environment variables if they only last a session. I tried to use settings to make them persist but had no luck, surely there is a better way to store these things rather than with env vars
class Config:
    # SECRET_KEY = os.environ.get("DRESSME_SECRET_KEY")
    SECRET_KEY = "nYCc1dL7mOhjvafDWRI8q37dqlYSxMB5"
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DRESSME_DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = "postgresql://dressme_db_user:nYCc1dL7mOhjvafDWRI8q37dqlYSxMB5@dpg-cjl00vtk5scs73dincd0-a.oregon-postgres.render.com/dressme_db"
