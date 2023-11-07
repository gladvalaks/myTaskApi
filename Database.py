from Consts import *
from Entities import *
import Hasher


def create_db():
    Base.metadata.create_all(engine)


def check_user_by_email(email):
    return bool(session.query(User).filter_by(email=email).first())


def create_new_user(email, username, password):
    user = User(email, username, Hasher.hash_password(password))
    session.add(user)
    session.commit()


def auth(email, password):
    user = session.query(User).filter_by(email=email).first()
    if user:
        if Hasher.compare(password, user.password):
            return user.id
        else:
            return False
    else:
        return False


def create_task_priority(title, order):
    task_priority = TaskPriority(title, order)
    session.add(task_priority)
    session.commit()


def get_priorities():
    priorities = session.query(TaskPriority).all()
    serialized_priorities = [priority.serialize() for priority in priorities]
    return serialized_priorities


def create_task(title, coins, user_id, is_daily, task_priority_id, description):
    task = Task(title, coins, user_id, is_daily, task_priority_id, description)
    session.add(task)
    session.commit()


def edit_task(id, title, coins, is_daily, task_priority_id, description):
    task = get_task(id)
    task.edit(title, coins, is_daily, task_priority_id, description)
    session.commit()


def complete_task(id):
    task = get_task(id)
    task.complete()
    session.commit()


def get_task(id):
    return session.query(Task).filter_by(id=id).first()


def get_tasks(user_id):
    tasks = session.query(Task).filter_by(user_id=user_id).all()
    serialized_tasks = [task.serialize() for task in tasks]
    return serialized_tasks


def is_user_task(user_id, task_id):
    task = get_task(task_id)
    return user_id == task.user_id
