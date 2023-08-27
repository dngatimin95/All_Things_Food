from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "secret-key-goes-here"
app.config["MONGO_URI"] = "mongodb+srv://dngatimin95:3GkTWNDnaWtsZ71R@foodrecocluster.pvwbqzo.mongodb.net/places"

# Setup MongoDB connection
mongo = PyMongo(app)
