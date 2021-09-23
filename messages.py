from db import db

def create_message(id):
    sql = "INSERT INTO messages (thread_id, message) VALUES (:thread_id, :message)"
    db.session.execute(sql, {})
    db.session.commit()