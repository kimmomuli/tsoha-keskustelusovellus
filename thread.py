from db import db
from flask import session

def get_threads(topic_id):
    sql = "SELECT thread_title, id FROM thread WHERE thread.topic_id = :topic_id"
    return db.session.execute(sql, {"topic_id":topic_id}).fetchall()

def add_thread(topic_id, thread_title):
    try:
        sql = "INSERT INTO thread (topic_id, thread_title, created_at, owner_id) VALUES (:topic_id, :thread_title, NOW(), :owner_id)"
        db.session.execute(sql, {"topic_id":topic_id, "thread_title":thread_title, "owner_id":session["user_id"]})
        db.session.commit()
    except:
        return False
    return True