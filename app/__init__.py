from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery


app = Flask(__name__)
app.config.from_object(Config)

celery = Celery(
    __name__,
    broker="redis://bastelbot:6379/0",
    backend="redis://bastelbot:6379/0"
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

bootstrap = Bootstrap(app)