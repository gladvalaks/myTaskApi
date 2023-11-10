from database.database import Base
from sqlalchemy import Integer, String,  Column

class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    email = Column(String(), nullable=False)
    username = Column(String(), nullable=False)
    password = Column(String(), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password


