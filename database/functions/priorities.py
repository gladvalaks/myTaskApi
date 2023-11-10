import database.entities.task_priority as entities
import database.database as db

def create_task_priority(title, order,session = db.create_session()):
    task_priority = entities.TaskPriority(title, order)
    session.add(task_priority)
    session.commit()


def get_priorities(session = db.create_session()):
    priorities = session.query(entities.TaskPriority).all()
    serialized_priorities = [priority.serialize() for priority in priorities]
    return serialized_priorities
