# -*- coding: utf-8 -*- 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
import Queue
from app.bot import Worker
from app.bot import Controller
import flask_restless

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(models.Autore, methods=['GET', 'POST', 'DELETE'])
manager.create_api(models.Storia, methods=['GET'])

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
