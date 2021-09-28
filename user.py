from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import secrets

def login(username, password):
    sql = "SELECT password, id, admin FROM users WHERE username=:username AND visible = 1"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        if check_password_hash(user[0], password):
            session["username"] = username
            session["user_id"] = user[1]
            if user[2] == 1:
                session["admin"] = True
            session["csrf_token"] = secrets.token_hex(16)
            return True
    return False
            
def create(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, admin, visible) VALUES (:username, :password, :admin, :visible)"
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":0, "visible":1})
        db.session.commit()
    except:
        return False
    return login(username, password)

def log_out():
    session.clear()

def csrf(csrf_token):
    if session["csrf_token"] != csrf_token:
        abort(403)

def exist(username):
    sql = "SELECT COUNT(*) FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username}).fetchone()
    if result[0] == 1:
        return True
    return False


def is_admin(username):
    sql = "SELECT COUNT(*) FROM users WHERE username=:username AND admin=1"
    result = db.session.execute(sql, {"username":username}).fetchone()
    if result[0] == 1:
        return True
    return False