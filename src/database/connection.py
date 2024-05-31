from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config


DATABASE_URL = Config.get_database_url()
engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()

    try:
        yield session
    finally:
        session.close()