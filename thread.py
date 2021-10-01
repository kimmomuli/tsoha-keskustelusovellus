from flask import session
from db import db

def get_threads(topic_id):
    sql = "SELECT thread_title, id, owner_id " \
          "FROM thread " \
          "WHERE thread.topic_id = :topic_id"
    return db.session.execute(sql,
                            {"topic_id":topic_id}).fetchall()

def get_title(thread_id):
    sql = "SELECT thread_title FROM thread WHERE id=:id"
    return db.session.execute(sql,
                            {"id":thread_id}).fetchone()

def add_thread(topic_id, thread_title):
    try:
        sql = "INSERT INTO thread (topic_id, thread_title, created_at, owner_id)" \
              "VALUES (:topic_id, :thread_title, NOW(), :owner_id)"
        db.session.execute(sql,
                        {"topic_id":topic_id,
                         "thread_title":thread_title,
                         "owner_id":session["user_id"]})
        db.session.commit()
        return True
    except:
        return False

def update_title(thread_id, new_title):
    try:
        if is_my_thread(thread_id):
            sql = "UPDATE thread " \
                  "SET thread_title=:new_title " \
                  "WHERE id=:thread_id"
            db.session.execute(sql,
                            {"new_title":new_title,
                             "thread_id":thread_id})
            db.session.commit()
            return True
    except:
        return False
    return False


def get_topic_id(thread_title):
    sql = "SELECT topic_id " \
          "FROM thread " \
          "WHERE thread_title=:thread_title"
    return db.session.execute(sql,
                            {"thread_title":thread_title}).fetchone()[0]

def get_topic_id(thread_id):
    sql = "SELECT topic_id " \
          "FROM thread " \
          "WHERE id=:thread_id"
    return db.session.execute(sql,
                            {"thread_id":thread_id}).fetchone()[0]

def delete(thread_id, user_id):
    sql = "DELETE FROM thread " \
          "WHERE id=:id AND owner_id=:owner_id"
    db.session.execute(sql,
                    {"id":thread_id,
                     "owner_id":user_id})
    db.session.commit()

def get_all():
    sql = "SELECT thread_title, id, owner_id " \
          "FROM thread"
    return db.session.execute(sql).fetchall()

def delete_admin(thread_id):
    sql = "DELETE FROM thread " \
          "WHERE id=:id"
    db.session.execute(sql,
                    {"id":thread_id})
    db.session.commit()

def is_my_thread(thread_id):
    try:
        sql = "SELECT id " \
              "FROM thread " \
              "WHERE id=:thread_id AND owner_id=:user_id"
        result = db.session.execute(sql,
                                    {"thread_id":thread_id,
                                     "user_id":session["user_id"]}).fetchone()
        return result is not None
    except:
        return False
    return False
