from db import db
from flask import session

def get_all():
    sql = "SELECT topic.title, topic.id, COUNT(thread.id), COUNT(messages.id) FROM topic LEFT JOIN thread ON thread.topic_id = topic.id LEFT JOIN messages ON messages.thread_id = thread.id GROUP BY topic.id;"
    return db.session.execute(sql).fetchall()

def create(title):
    try:
        sql = "INSERT INTO topic (owner_id, title) VALUES (:owner_id, :title)"
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
    sql = "SELECT title FROM topic WHERE id=:topic_id"
    return db.session.execute(sql, {"topic_id":topic_id}).fetchone()[0]
