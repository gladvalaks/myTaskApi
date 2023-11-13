import database.entities.task as entities
import database.database as db
import models.responses.task as task_response
import datetime

def create_task(title, coins, user_id, is_daily, task_priority_id, description, session = db.create_session()):
    task = entities.Task(title, coins, user_id, is_daily, task_priority_id, description)
    session.add(task)
    session.commit()

def delete_task(id,session = db.create_session()):
    task = session.get(entities.Task,id)
    session.delete(task)
    session.commit()

def edit_task(id, title, coins, is_daily, task_priority_id, description,session = db.create_session()):
    task = session.get(entities.Task,id)
    task.edit(title, coins, is_daily, task_priority_id, description)
    session.commit()

def complete_task(id,session = db.create_session()):
    task = session.get(entities.Task,id)
    if(task.is_daily):
        create_task(*task.get_values())
    task.complete()
    session.commit()

def get_task(id,session = db.create_session()):
    return session.query(entities.Task).filter_by(id=id).first()

def get_task_response(task):
    finished_at = task.finished_at

    if finished_at:
        finished_at = int(round(finished_at.timestamp() * 1000))

    return task_response.Task(id=task.id,title=task.title,description=task.description,
                              task_priority_id=task.task_priority_id,is_daily=task.is_daily,
                              coins=task.coins, created_at=int(round(task.created_at.timestamp() * 1000)), 
                              finished_at=finished_at)


def get_serialized_today_tasks(user_id,session = db.create_session()):
    tasks = session.get(entities.Task)
    #tasks = session.query(entities.Task).filter_by(user_id=user_id).all()
    today = datetime.datetime.now().date()
    serialized_tasks = []
    for task in tasks:
        if(task.finished_at):
            if(task.finished_at.date() == today):
                serialized_tasks.append(get_task_response(task))
        else:
            serialized_tasks.append(get_task_response(task))        
    return serialized_tasks

def get_serialized_tasks(user_id,session = db.create_session()):
    tasks = session.query(entities.Task).filter_by(user_id=user_id).all()
    serialized_tasks = [get_task_response(task) for task in tasks]
    return serialized_tasks


def is_user_task(user_id, task_id):
    task = get_task(task_id)
    return user_id == task.user_id