import os


# Config object to store and use config settings
class Config:
    # SECRET_KEY = os.environ.get("DRESSME_SECRET_KEY")
    SECRET_KEY = "nYCc1dL7mOhjvafDWRI8q37dqlYSxMB5"
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DRESSME_DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = "postgresql://dressme_db_user:nYCc1dL7mOhjvafDWRI8q37dqlYSxMB5@dpg-cjl00vtk5scs73dincd0-a.oregon-postgres.render.com/dressme_db"
