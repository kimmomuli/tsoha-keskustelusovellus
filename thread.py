from db import db
from flask import session

def get_threads(topic_id):
    sql = "SELECT thread_title, id, owner_id FROM thread WHERE thread.topic_id = :topic_id"
    return db.session.execute(sql, {"topic_id":topic_id}).fetchall()

def get_title(thread_id):
    sql = "SELECT thread_title FROM thread WHERE id=:id"
    return db.session.execute(sql, {"id":thread_id}).fetchone()

def add_thread(topic_id, thread_title):
    try:
        sql = "INSERT INTO thread (topic_id, thread_title, created_at, owner_id) VALUES (:topic_id, :thread_title, NOW(), :owner_id)"
        db.session.execute(sql, {"topic_id":topic_id, "thread_title":thread_title, "owner_id":session["user_id"]})
        db.session.commit()
        return True
    except:
        return False

def update_title(id, new_title):
    try:
        sql = "UPDATE thread SET thread_title=:new_title WHERE id=:id"
        db.session.execute(sql, {"new_title":new_title, "id":id})
        db.session.commit()
    except:
        return False
    return True

def get_topic_id(thread_title):
    sql = "SELECT topic_id FROM thread WHERE thread_title=:thread_title"
    return db.session.execute(sql, {"thread_title":thread_title}).fetchone()[0]

def delete(thread_id, user_id):
    sql = "DELETE FROM thread WHERE id=:id AND owner_id=:owner_id"
    db.session.execute(sql, {"id":thread_id, "owner_id":user_id})
    db.session.commit()

def get_topic_id(thread_id):
    sql = "SELECT topic_id FROM thread WHERE id=:thread_id"
    return db.session.execute(sql, {"thread_id":thread_id}).fetchone()[0]

def get_all():
    sql = "SELECT thread_title, id, owner_id FROM thread"
    return db.session.execute(sql).fetchall()

def delete_admin(thread_id):
    sql = "DELETE FROM thread WHERE id=:id"
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()