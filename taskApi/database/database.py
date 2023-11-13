from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def create_db():
    Base.metadata.create_all(engine)
    
def create_session():
    return Session()

engine = create_engine('sqlite:///databaseV2.db')
Session = sessionmaker(engine)
Base = declarative_base()


