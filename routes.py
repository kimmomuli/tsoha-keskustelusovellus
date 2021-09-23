from app import app
from flask import Flask, redirect, render_template, session, request
import user, thread, topic
from werkzeug.exceptions import abort

@app.route("/")
def index():
    return render_template("index.html", topics = topic.get_all())

@app.route("/login", methods=["GET", "POST"])
def login():
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
    return render_template("new_user.html")

@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "GET":
        return render_template("new_user.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("new_user.html", message="Salasanat eivät ole samat")
            
        if user.create(username, password1):
            return redirect("/")
        else:
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
    if 0 < len(title) < 200:
        if topic.create(title):
            return redirect("/")
        return render_template("new_topic.html", message="Aiheen luonnissa tapahtui virhe")
    else:
        return render_template("new_topic.html", message="Aiheen pituus pitää olla 1-200")

@app.route("/threads/<int:topic_id>")
def threads(topic_id):
    return render_template("threads.html", thread_list=thread.get_threads(topic_id), topic_id=topic_id)

@app.route("/new_thread/<int:topic_id>")
def new_thread(topic_id):
    return render_template("new_thread.html", topic_id=topic_id)

@app.route("/create_thread/<int:topic_id>", methods=["POST"])
def create_thread(topic_id):
    user.csrf(request.form["csrf_token"])
    thread_topic = request.form["thread_topic"]

    if not thread.add_thread(topic_id, thread_topic):
        return render_template("new_thread.html", topic_id=topic_id, message = "Viestiketjun lisääminen ei onnistunut")
    return redirect(f"/threads/{topic_id}")