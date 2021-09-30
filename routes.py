from app import app
from flask import Flask, redirect, render_template, session, request
import user, thread, topic, messages, limits
from werkzeug.exceptions import abort

@app.route("/")
def index():
    try:
        limited = limits.get_limited_topics(session["user_id"])
        return render_template("index.html", topics = topic.get_all(), limited=limited)
    except:
        return render_template("index.html", topics = topic.get_all())


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        username = session["username"]
        return redirect("/")
    except:
        if request.method == "GET":
            return render_template("login.html")

        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if user.login(username,password):
                return redirect("/")
            else:
                return render_template("login.html", message="Väärä käyttäjätunnus tai salasana")

@app.route("/new_user")
def new_user():
    try:
        username = session["username"]
        return redirect("/")
    except:
        return render_template("new_user.html")

@app.route("/create", methods=["POST"])
def create():
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        
        if len(username) < 3 or 30 < len(username):
             return render_template("new_user.html", message="Käyttäjätunnuksen pitää olla 3 - 30 merkkiä")
        elif password1 != password2:
             return render_template("new_user.html", message="Salasanat eivät ole samat")
        elif len(password1) < 10 or 100 < len(password1):
                 return render_template("new_user.html", message="Salasanan pitää olla 10 - 100 merkkiä")
        elif user.exist(username):
            return render_template("new_user.html", message="Käyttäjätunnus on varattu")

        if user.create(username, password1):
            return redirect("/")
        return render_template("new_user.html", message="Tilin luonti ei onnistunut")

@app.route("/log_out")
def log_out():
    user.log_out()
    return redirect("/")

@app.route("/new_topic")
def new_topic():
    return render_template("new_topic.html")

@app.route("/create_topic", methods=["POST"])
def create_topic():
    user.csrf(request.form["csrf_token"])
    title = request.form["topic"]
    if 1 > len(title) or len(title) > 100:
        return render_template("new_topic.html", message="Aiheen pituus pitää olla 1-100")
    
    if topic.create(title):
        return redirect("/")
    return render_template("new_topic.html", message="Aiheen luonnissa tapahtui virhe")

@app.route("/threads/<int:topic_id>")
def threads(topic_id):
    if not topic.is_topic_limited(topic_id):
        return render_template("threads.html", thread_list=thread.get_threads(topic_id), topic_id=topic_id, topic_title=topic.get_title(topic_id))
    return render_template("threads.html", thread_list=thread.get_threads(topic_id), topic_id=topic_id, topic_title=topic.get_limited_title(topic_id))
    

@app.route("/new_thread/<int:topic_id>")
def new_thread(topic_id):
    return render_template("new_thread.html", topic_id=topic_id)

@app.route("/create_thread/<int:topic_id>", methods=["POST"])
def create_thread(topic_id):
    user.csrf(request.form["csrf_token"])
    thread_topic = request.form["thread_topic"]

    if len(thread_topic) < 1 or len(thread_topic) > 100:
        return render_template("new_thread.html", topic_id=topic_id, message="Ketjun pituus pitää olla 1 - 100 merkkiä")

    if topic.is_topic_limited(topic_id):
        try:
            if limits.have_permission(session["user_id"], topic_id):
                return redirect(f"/get_limited_threads/{topic_id}")
        except:
            return("/login")

    if not thread.add_thread(topic_id, thread_topic):
        return render_template("new_thread.html", topic_id=topic_id, message = "Viestiketjun lisääminen ei onnistunut")
    return redirect(f"/threads/{topic_id}")

@app.route("/get_messages/<int:thread_id>")
def get_messages(thread_id):
    return render_template("messages.html", messages=messages.get_messages(thread_id), thread_id=thread_id, thread_title=thread.get_title(thread_id), topic_id=thread.get_topic_id(thread_id))

@app.route("/new_message/<int:thread_id>")
def new_message(thread_id):
    return render_template("new_message.html", thread_id=thread_id)

@app.route("/create_message/<int:thread_id>", methods=["POST"])
def create_message(thread_id):
    user.csrf(request.form["csrf_token"])
    message = request.form["message"]

    if len(message) < 1 or len(message) > 500:
        return render_template("new_message.html", thread_id=thread_id, error="Viestin pituus pitää olla 1 - 500 merkkiä")

    if not messages.create_message(thread_id, message):
        return render_template("new_message.html", error="Viestin lähetys ei onnistunut")
    return redirect(f"/get_messages/{thread_id}")

@app.route("/edit_thread_title/<int:thread_id>")
def edit_thread_title(thread_id):
    topic_id = thread.get_topic_id(thread_id)
    if topic.is_topic_limited(topic_id):
        try:
            if limits.have_permission(session["user_id"], topic_id):
                return render_template("edit_thread.html", thread_id=thread_id)
        except:
            return("/login")
    return render_template("edit_thread.html", thread_id=thread_id)

@app.route("/update_thread_title/<int:thread_id>", methods=["POST"])
def update_thread_title(thread_id):
    user.csrf(request.form["csrf_token"])
    new_title = request.form["thread_title"]

    if 1 > len(new_title) or len(new_title) > 100:
        return render_template("edit_thread.html", thread_id= thread_id, message="Aiheen pituus pitää olla 1-100")

    if not thread.update_title(thread_id, new_title):
        return render_template("edit_thread.html", message="Otsikon muuttaminen epäonnistui", thread_id= thread_id)
    topic_id = thread.get_topic_id(thread_id)
    return redirect(f"/threads/{topic_id}")

@app.route("/delete_thread/<int:thread_id>")
def delete_thread(thread_id):
    try:
        user_id = session["user_id"]
        topic_id = thread.get_topic_id(thread_id)
        if topic.is_topic_limited(topic_id):
            if limits.have_permission(user_id, topic_id):
                thread.delete(thread_id, user_id)
                return redirect("/")
        thread.delete(thread_id, user_id)
        return redirect("/")
    except:
        return redirect("/login")
    
@app.route("/result", methods=["GET"])
def result():
    try:
        username = session["username"]
        headword = request.args["query"]
        results = messages.search_messages(headword)
        return render_template("search_result.html", search_messages=results)
    except:
        return redirect("/")

def is_admin():
    try:
        if user.is_admin(session["username"]):
            return True
    except:
        return False
    return True

@app.route("/admin")
def admin():
    if is_admin():
        topics = topic.get_all()
        threads =  thread.get_all()
        all_messages = messages.get_all()
        users = user.get_all_users()
        limited_topics = topic.get_limited_topics()
        return render_template("admin.html", topics=topics, thread_list=threads, messages=all_messages, users=users, limited_topics = limited_topics)
    return redirect("/")

@app.route("/delete_topic/<int:topic_id>")
def delete_topic(topic_id):
    if user.is_admin(session["username"]):
        topic.delete(topic_id)
        return redirect("/admin")
    return redirect("/")
    
@app.route("/delete_message/<int:message_id>")
def delete_message(message_id):
    try:
        user_id = session["user_id"]
        messages.delete(message_id)
        return redirect("/")
    except:
        return redirect("/login")

@app.route("/delete_thread_admin/<int:thread_id>")
def delete_thread_admin(thread_id):
    if is_admin():
        thread.delete_admin(thread_id)
        return redirect("/admin")
    return redirect("/login")

@app.route("/delete_message_admin/<int:message_id>")
def delete_message_admin(message_id):
    if is_admin():
        messages.delete_admin(message_id)
        return redirect("/admin")
    return redirect("/login")

@app.route("/delete_user_admin/<int:user_id>")
def delete_user_admin(user_id):
    if is_admin():
        user.delete(user_id)
        return redirect("/admin")
    return redirect("/login")

@app.route("/return_user_admin/<int:user_id>")
def return_user_admin(user_id):
    if is_admin():
        user.return_user(user_id)
        return redirect("/admin")
    return redirect("/login")

@app.route("/new_limited_topic")
def new_limited_topic():
    if is_admin():
        return render_template("new_limited_topic.html")
    return redirect("/login")

@app.route("/create_limited_topic", methods=["POST"])
def create_limited_topic():
    user.csrf(request.form["csrf_token"])
    try:
        if user.is_admin(session["username"]):
            title = request.form["topic"]
        if 1 > len(title) or len(title) > 100:
            return render_template("new_topic.html", message="Aiheen pituus pitää olla 1-100")
    
        if topic.create_limited_topic(title):
            return redirect("/admin")
        return render_template("new_limited_topic.html", message="Aiheen luonnissa tapahtui virhe")
    except:
        return redirect("/login")

@app.route("/add_user_permissions/<int:topic_id>")
def add_user_permissions(topic_id):
    if is_admin():
        users = limits.get_users()
        return render_template("add_permissions.html", topic_id=topic_id, users=users)
    return redirect("/login")

@app.route("/remove_topic_permission/<int:user_id>/<int:topic_id>")
def remove_topic_permission(user_id, topic_id):
    if is_admin():
        limits.remove_permission(user_id, topic_id)
        return redirect(f"/add_user_permissions/{topic_id}")
    return redirect("/login")

@app.route("/add_topic_permission/<int:user_id>/<int:topic_id>")
def add_topic_permission(user_id, topic_id):
    if is_admin():
        limits.add_pemission(user_id, topic_id)
        return redirect(f"/add_user_permissions/{topic_id}")
    return redirect("/login")

@app.route("/get_limited_threads/<int:topic_id>")
def get_limited_threads(topic_id):
        try:
            if topic.is_topic_limited(topic_id):
                if limits.have_permission(session["user_id"], topic_id):
                    return render_template("threads.html", thread_list=thread.get_threads(topic_id), topic_id=topic_id, topic_title=topic.get_limited_title(topic_id))        
            return redirect("/")
        except:
            return redirect("/login")
