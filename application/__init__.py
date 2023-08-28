from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = ""
app.config["MONGO_URI"] = ""

# Setup MongoDB connection
mongo = PyMongo(app)
