# -*- coding: utf-8 -*- 

from flask import Flask
import time
import Queue
from app.bot import Concur
from app.bot import Controller

app = Flask(__name__)
app.config.from_object('config')
from app import views


q = Queue.Queue() # si istanzia la coda che servirà a inserire le storie
views.q = q # passiamo l'oggetto coda alle views importate
# questo thread si dovrà occupare di prendere i messaggi dalla coda e inviarli al plotter
# e dovrà istanziare e gestire l'oggetto plot
concur = Concur(q)
# questo thread invece controlla il precedente per fermarlo e farlo ripartire
# tramite una finestra pyGame, in modo da mettere in pausa la stampa
controller = Controller(concur)
concur.start() # chiama il metodo run() di concur
controller.start() # chiama il metodo run() di controller