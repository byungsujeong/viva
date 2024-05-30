from dotenv import load_dotenv
from os import path, environ


base_dir = path.dirname(path.dirname(path.abspath(__file__)))
load_dotenv(path.join(base_dir, ".env"))

class Config:

    """ Call Environment """

    def get_database_url():
        return environ.get("DATABASE_URL")

    def get_secret_key():
        return environ.get("SECRET_KEY")


    
    

