from app import app
from flask import Flask, redirect, render_template, session, request
import user

@app.route("/")
def index():
    if session.get("username"):
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
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

@app.route("/create", methods=["POST"])
def create():
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