from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from pathlib import Path

basedir = Path(__file__).resolve().parent.parent

app = Flask(__name__)

# Basic Config
app.config['SECRET_KEY'] = 'change_me'
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'admin'

# Database Config
DATABASE = "flaskr.db"
url = os.getenv("DATABASE_URL", f"sqlite:///{basedir / DATABASE}")
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# Register models
from project import models
