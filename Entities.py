from Consts import Base
from datetime import datetime
from sqlalchemy import Integer, String, Text, Boolean, Column, DateTime, ForeignKey


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


class TaskPriority(Base):
    __tablename__ = "task_priorities"

    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    order = Column(Integer(), nullable=False)

    def __init__(self, title, order):
        self.title = title
        self.order = order

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'order': self.order
        }


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    description = Column(Text())
    coins = Column(Integer(), nullable=False)
    user_id = Column(Integer(), ForeignKey("users.id"))
    is_daily = Column(Boolean(), default=False)
    task_priority_id = Column(Integer(), ForeignKey("task_priorities.id"))
    created_at = Column(DateTime(), default=datetime.now())
    finished_at = Column(DateTime())

    def __init__(self, title, coins, user_id, is_daily, task_priority_id, description):
        self.edit(title, coins,  is_daily, task_priority_id, description)
        self.user_id = user_id

    def edit(self, title, coins, is_daily, task_priority_id, description):
        self.title = title
        self.description = description
        self.coins = coins
        self.is_daily = is_daily
        self.task_priority_id = task_priority_id
    
    def complete(self):
        self.finished_at = datetime.now()

    def serialize(self):
        finished_at = self.finished_at
        if not finished_at:
            finished_at = 0
        else:
            finished_at = int(round(finished_at.timestamp() * 1000))
        return {
            'id': self.id,
            "task_body": {
                'title': self.title,
                'description': self.description,
                'coins': self.coins,
                'user_id': self.user_id,
                'is_daily': self.is_daily,
                'task_priority_id': self.task_priority_id
            },
            'created_at': int(round(self.created_at.timestamp() * 1000)),
            'finished_at':  finished_at
        }
