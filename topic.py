from db import db

def get_all():
    sql = "SELECT topic.title, topic.id, COUNT(thread.id), COUNT(messages.id) FROM topic LEFT JOIN thread ON thread.topic_id = topic.id LEFT JOIN messages ON messages.thread_id = thread.id GROUP BY topic.id;"
    return db.session.execute(sql).fetchall()

def create(title):
    try:
        sql = "INSERT INTO topic (created_at, title) VALUES (NOW(), :title)"
        db.session.execute(sql, {"title": title})
        db.session.commit()
    except:
        return False
    return True
