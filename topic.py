from db import db
from flask import session

def get_all():
    sql = "SELECT topic.title, topic.id FROM topic WHERE is_limited=FALSE"
    return db.session.execute(sql).fetchall()

def create(title):
    try:
        sql = "INSERT INTO topic (owner_id, title, is_limited) VALUES (:owner_id, :title, FALSE)"
        db.session.execute(sql, {"owner_id":session["user_id"], "title": title})
        db.session.commit()
    except:
        return False
    return True

def delete(topic_id):
    sql = "DELETE FROM topic WHERE id=:topic_id"
    db.session.execute(sql, {"topic_id":topic_id})
    db.session.commit()

def get_title(topic_id):
    sql = "SELECT title FROM topic WHERE id=:topic_id AND is_limited=FALSE"
    return db.session.execute(sql, {"topic_id":topic_id}).fetchone()[0]

def get_limited_title(topic_id):
    sql = "SELECT title FROM topic WHERE id=:topic_id AND is_limited=TRUE"
    return db.session.execute(sql, {"topic_id":topic_id}).fetchone()[0]

def get_limited_topics():
    sql = "SELECT topic.title, topic.id FROM topic WHERE is_limited=TRUE"
    return db.session.execute(sql).fetchall()

def create_limited_topic(title):
    try:
        sql = "INSERT INTO topic (owner_id, title, is_limited) VALUES (:owner_id, :title, TRUE)"
        db.session.execute(sql, {"owner_id":session["user_id"], "title": title})
        db.session.commit()
    except:
        return False
    return True

def is_topic_limited(topic_id):
    sql = "SELECT is_limited FROM topic WHERE id=:topic_id"
    return db.session.execute(sql, {"topic_id":topic_id}).fetchone()[0]
