from flask_sqlalchemy import SQLAlchemy
from os import getenv
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
#Vaihda alempi kun pusket herokuun. Paikallisesti pitää käyttää ylempää
#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql://", 1)

#Virheilmoituksen poisto
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)