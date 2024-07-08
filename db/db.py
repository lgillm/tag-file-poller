from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from settings.tokens import DbTokens


Base = declarative_base()

DATABASE_URL = f"postgresql://{DbTokens.USERNAME}:{DbTokens.PASSWORD}@{DbTokens.HOSTNAME}:5432/{DbTokens.CONNECTION_DB}"


def get_db():

    # SQLAlchemy database connection engine
    engine = create_engine(DATABASE_URL)
    async_db = Database(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_engine():
    return create_engine(DATABASE_URL)