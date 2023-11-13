import database.entities.task_priority as entities
import database.database as db
import models.responses.task_priority as task_priority_response

def create_task_priority(title, order,session = db.create_session()):
    task_priority = entities.TaskPriority(title, order)
    session.add(task_priority)
    session.commit()

def get_serialized_priority(priority):
    return task_priority_response.Task_priority(id = priority.id, title= priority.title, order=priority.order)

def get_priorities(session = db.create_session()):
    priorities = session.query(entities.TaskPriority).all()
    serialized_priorities = [get_serialized_priority(priority) for priority in priorities]
    return serialized_priorities
