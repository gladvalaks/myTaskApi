import database.entities.user as entities
import database.database as db
import hasher.hasher as hasher

def get_username(id,session = db.create_session()):
    return session.query(entities.User).filter_by(id=id).first().username

def check_user_by_email(email,session = db.create_session()):
    return bool(session.query(entities.User).filter_by(email=email).first())

def create_new_user(email, username, password,session = db.create_session()):
    user = entities.User(email, username, hasher.hash_password(password))
    session.add(user)
    session.commit()

def is_user(id,session = db.create_session()):
    user = session.query(entities.User).filter_by(id=id).first()
    if user:
        return True
    return False

def auth(email, password,session = db.create_session()):
    user = session.query(entities.User).filter_by(email=email).first()
    if user:
        if hasher.compare(password, user.password):
            return user.id
        else:
            return False
    else:
        return False