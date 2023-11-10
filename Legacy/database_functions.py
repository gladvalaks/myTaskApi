from consts import *
from taskApi.entities import *
import taskApi.hasher.hasher as hasher


def create_db():
    Base.metadata.create_all(engine)

def create_session():
    return Session()

def get_username(id,session = create_session()):
    return session.query(User).filter_by(id=id).first().username

def check_user_by_email(email,session = create_session()):
    return bool(session.query(User).filter_by(email=email).first())

def create_new_user(email, username, password,session = create_session()):
    user = User(email, username, hasher.hash_password(password))
    session.add(user)
    session.commit()

def is_user(id,session = create_session()):
    user = session.query(User).filter_by(id=id).first()
    if user:
        return True
    return False

def auth(email, password,session = create_session()):
    user = session.query(User).filter_by(email=email).first()
    if user:
        if hasher.compare(password, user.password):
            return user.id
        else:
            return False
    else:
        return False



def create_task_priority(title, order,session = create_session()):
    task_priority = TaskPriority(title, order)
    session.add(task_priority)
    session.commit()


def get_priorities(session = create_session()):
    priorities = session.query(TaskPriority).all()
    serialized_priorities = [priority.serialize() for priority in priorities]
    return serialized_priorities


def create_task(title, coins, user_id, is_daily, task_priority_id, description,session = create_session()):
    task = Task(title, coins, user_id, is_daily, task_priority_id, description)
    session.add(task)
    session.commit()

def delete_task(id,session = create_session()):
    task = session.query(Task).filter_by(id=id).first()
    session.delete(task)
    session.commit()

def edit_task(id, title, coins, is_daily, task_priority_id, description,session = create_session()):
    task = session.query(Task).filter_by(id=id).first()
    task.edit(title, coins, is_daily, task_priority_id, description)
    session.commit()


def complete_task(id,session = create_session()):
    task = session.query(Task).filter_by(id=id).first()
    task.complete()
    session.commit()

def get_task(id,session = create_session()):
    return session.query(Task).filter_by(id=id).first()


def get_tasks(user_id,session = create_session()):
    tasks = session.query(Task).filter_by(user_id=user_id).all()
    serialized_tasks = [task.serialize() for task in tasks]
    return serialized_tasks


def is_user_task(user_id, task_id):
    task = get_task(task_id)
    return user_id == task.user_id

