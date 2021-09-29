from app import app
from flask import Flask, redirect, render_template, session, request
import user, thread, topic, messages
from werkzeug.exceptions import abort

@app.route("/")
def index():
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
    return render_template("threads.html", thread_list=thread.get_threads(topic_id), topic_id=topic_id, topic_title=topic.get_title(topic_id))

@app.route("/new_thread/<int:topic_id>")
def new_thread(topic_id):
    return render_template("new_thread.html", topic_id=topic_id)

@app.route("/create_thread/<int:topic_id>", methods=["POST"])
def create_thread(topic_id):
    user.csrf(request.form["csrf_token"])
    thread_topic = request.form["thread_topic"]

    if len(thread_topic) < 1 or len(thread_topic) > 100:
        return render_template("new_thread.html", topic_id=topic_id, message="Ketjun pituus pitää olla 1 - 100 merkkiä")

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

@app.route("/admin")
def admin():
    if user.is_admin(session["username"]):
        topics = topic.get_all()
        threads =  thread.get_all()
        all_messages = messages.get_all()
        users = user.get_all_users()
        return render_template("admin.html", topics=topics, thread_list=threads, messages=all_messages, users=users)
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
    try:
        if user.is_admin(session["username"]):
            thread.delete_admin(thread_id)
            return redirect("/admin")
    except:
        return redirect("/login")

@app.route("/delete_message_admin/<int:message_id>")
def delete_message_admin(message_id):
    try:
        if user.is_admin(session["username"]):
            messages.delete_admin(message_id)
            return redirect("/admin")
    except:
        return redirect("/login")

@app.route("/delete_user_admin/<int:user_id>")
def delete_user_admin(user_id):
    try:
        if user.is_admin(session["username"]):
            user.delete(user_id)
            return redirect("/admin")
    except:
        return redirect("/login")

@app.route("/return_user_admin/<int:user_id>")
def return_user_admin(user_id):
    try:
        if user.is_admin(session["username"]):
            user.return_user(user_id)
            return redirect("/admin")
    except:
        return redirect("/login")