import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DATABASE_URI = os.environ['DATABASE_URL']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)


# class Update(db.Model):
#     update_id = db.Column()