from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import secrets
import limits

def login(username, password):
    sql = "SELECT password, id, admin " \
          "FROM users " \
          "WHERE username=:username AND visible = 1"
    result = db.session.execute(sql,
                                {"username":username})
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
        sql = "INSERT INTO users (username, password, admin, visible) " \
            "VALUES (:username, :password, :admin, :visible)"
        db.session.execute(sql,
                        {"username":username,
                         "password":hash_value,
                         "admin":0, "visible":1})
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
    sql = "SELECT username " \
          "FROM users "\
          "WHERE username=:username"
    result = db.session.execute(sql,
                            {"username":username}).fetchone()
    return result is not None

def is_admin(username):
    sql = "SELECT admin " \
          "FROM users " \
          "WHERE username=:username AND visible=1"
    result = db.session.execute(sql,
                                {"username":username}).fetchone()
    if result is None:
        return False
    return result[0] == 1

def get_all_users():
    sql = "SELECT username, id, visible " \
          "FROM users"
    return db.session.execute(sql).fetchall()

def delete(user_id):
    sql = "UPDATE users SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":user_id})
    db.session.commit()

def return_user(user_id):
    sql = "UPDATE users SET visible=1 WHERE id=:id"
    db.session.execute(sql, {"id":user_id})
    db.session.commit()

def is_admin_in():
    try:
        if is_admin(session["username"]):
            return True
    except:
        return False
    return True

def user_permission(topic_id):
    try:
        if limits.have_permission(session["user_id"], topic_id):
            return True
    except:
        return False
    return False
