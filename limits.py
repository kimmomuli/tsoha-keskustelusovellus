from db import db
from flask import session

def get_users():
    sql = "SELECT users.username, users.id, limits.topic_id FROM users LEFT JOIN limits ON limits.user_id=users.id"
    return db.session.execute(sql).fetchall()

def add_pemission(user_id, topic_id):
    sql = "INSERT INTO limits (topic_id, user_id) VALUES (:topic_id, :user_id)"
    db.session.execute(sql, {"topic_id":topic_id, "user_id":user_id})
    db.session.commit()

def remove_permission(user_id, topic_id):
    sql = "DELETE FROM limits WHERE topic_id=:topic_id AND user_id=:user_id"
    db.session.execute(sql, {"topic_id":topic_id, "user_id":user_id})
    db.session.commit()

def get_limited_topics(user_id):
    sql ="SELECT topic.title, topic.id FROM topic, limits WHERE limits.user_id=:user_id AND topic.is_limited=TRUE"
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def have_permission(user_id, topic_id):
    sql = "SELECT id FROM limits WHERE user_id=:user_id AND topic_id=:topic_id"
    result = db.session.execute(sql, {"user_id":user_id, "topic_id":topic_id}).fetchone()[0]
    return result is not None