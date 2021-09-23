from db import db

def get_all():
    sql = "SELECT title, id FROM topic"
    return db.session.execute(sql).fetchall()

def create(title):
    try:
        sql = "INSERT INTO topic (created_at, title) VALUES (NOW(), :title)"
        db.session.execute(sql, {"title": title})
        db.session.commit()
    except:
        return False
    return True
