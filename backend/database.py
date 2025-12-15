from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import register
from config import Config

engine = create_engine(Config.DATABASE_URL, echo=True)
session_factory = sessionmaker(bind=engine)
DBSession = scoped_session(session_factory)
register(DBSession)
Base = declarative_base()

def init_db():
    import models
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")

def get_session():
    return DBSession()