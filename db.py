from flask_sqlalchemy import SQLAlchemy
from os import getenv
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

#Virheilmoituksen poisto
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)