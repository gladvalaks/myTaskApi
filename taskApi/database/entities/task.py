from database.database import Base
from datetime import datetime
from sqlalchemy import Integer, String, Text, Boolean, Column, DateTime, ForeignKey

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

    def get_values(self):
        return [self.title, self.coins, self.user_id, self.is_daily, self.task_priority_id, self.description]
    def get_full_info(self):
        finished_at = self.finished_at
        if not finished_at:
            finished_at = 0
        else:
            finished_at = int(round(finished_at.timestamp() * 1000))

        return [self.title, self.coins, self.user_id, self.is_daily, 
                self.task_priority_id, self.description,self.created_at,finished_at]
