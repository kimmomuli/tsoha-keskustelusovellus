from db import db

def get_messages(thread_id):
    sql = "SELECT message, id FROM messages WHERE thread_id =:thread_id"
    return db.session.execute(sql, {"thread_id":thread_id}).fetchall()

def create_message(thread_id, message):
    try:
        sql = "INSERT INTO messages (thread_id, message) VALUES (:thread_id, :message)"
        db.session.execute(sql, {"thread_id":thread_id, "message":message})
        db.session.commit()
    except:
        return False
    return True