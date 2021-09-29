from db import db
from flask import session

def get_messages(thread_id):
    sql = "SELECT message, id, owner_id FROM messages WHERE thread_id =:thread_id"
    return db.session.execute(sql, {"thread_id":thread_id}).fetchall()

def get_all():
    sql = "SELECT message, id, owner_id FROM messages"
    return db.session.execute(sql).fetchall()

def create_message(thread_id, message):
    try:
        sql = "INSERT INTO messages (thread_id, message, owner_id) VALUES (:thread_id, :message, :owner_id)"
        db.session.execute(sql, {"thread_id":thread_id, "message":message, "owner_id": session["user_id"]})
        db.session.commit()
    except:
        return False
    return True

def search_messages(headword):
    sql = "SELECT id, thread_id, message FROM messages WHERE message LIKE :headword"
    result = db.session.execute(sql, {"headword":f"%{headword}%"})
    return result.fetchall()

def delete(message_id):
    sql = "DELETE FROM messages WHERE id=:id AND owner_id=:owner_id"
    db.session.execute(sql, {"id":message_id, "owner_id":session["user_id"]})
    db.session.commit()

def delete_admin(message_id):
    sql = "DELETE FROM messages WHERE id=:id"
    db.session.execute(sql, {"id":message_id})
    db.session.commit()