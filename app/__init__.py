# -*- coding: utf-8 -*- 

from flask import Flask, request
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
import time
import Queue
from app.bot import Worker
from app.bot import Controller
import flask_restless

app = Flask(__name__)
app.config.from_object('config')

# Initialize Flask-Babel
babel = Babel(app)

# Use the browser's language preferences to select an available translation
@babel.localeselector
def get_locale():
    translations = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(translations)


db = SQLAlchemy(app)
mail = Mail(app)

from app import views, models
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(models.Autore, methods=['GET', 'POST', 'DELETE'], results_per_page=0)
manager.create_api(models.Storia, methods=['GET'], results_per_page=0)

db_adapter = SQLAlchemyAdapter(db, models.User)
user_manager = UserManager(db_adapter, app)

q = Queue.Queue() # si istanzia la coda che servirà a inserire le storie
views.q = q # passiamo l'oggetto coda alle views importate
# questo thread si dovrà occupare di prendere i messaggi dalla coda e inviarli al plotter
# e dovrà istanziare e gestire l'oggetto plot
worker = Worker(q)
# questo thread invece controlla il precedente per fermarlo e farlo ripartire
# tramite una finestra pyGame, in modo da mettere in pausa la stampa
controller = Controller(worker)
worker.start() # chiama il metodo run() di worker
controller.start() # chiama il metodo run() di controller
