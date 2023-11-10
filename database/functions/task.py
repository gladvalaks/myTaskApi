import database.entities.task as entities
import database.database as db

def create_task(title, coins, user_id, is_daily, task_priority_id, description,session = db.create_session()):
    task = entities.Task(title, coins, user_id, is_daily, task_priority_id, description)
    session.add(task)
    session.commit()

def delete_task(id,session = db.create_session()):
    task = session.query(entities.Task).filter_by(id=id).first()
    session.delete(task)
    session.commit()

def edit_task(id, title, coins, is_daily, task_priority_id, description,session = db.create_session()):
    task = session.query(entities.Task).filter_by(id=id).first()
    task.edit(title, coins, is_daily, task_priority_id, description)
    session.commit()


def complete_task(id,session = db.create_session()):
    task = session.query(entities.Task).filter_by(id=id).first()
    task.complete()
    session.commit()

def get_task(id,session = db.create_session()):
    return session.query(entities.Task).filter_by(id=id).first()


def get_tasks(user_id,session = db.create_session()):
    tasks = session.query(entities.Task).filter_by(user_id=user_id).all()
    serialized_tasks = [task.serialize() for task in tasks]
    return serialized_tasks


def is_user_task(user_id, task_id):
    task = get_task(task_id)
    return user_id == task.user_id