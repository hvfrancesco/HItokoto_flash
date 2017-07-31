from flask import render_template, flash, redirect
from app import app, db, models
from .forms import submitStory
import datetime
import os


q = None
nick = 'autore'

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': nick}
    return render_template('index.html', title='Hitokoto Flash', user=user)

@app.route('/storia', methods=['GET', 'POST'])
def invia_storia():
    form = submitStory()
    if form.validate_on_submit():
        flash('storia inviata da %s' % form.autore.data)
        u = models.Autore.query.filter_by(nome = form.autore.data).first()
        if (not u):
            u = models.Autore(nome=form.autore.data)
            db.session.add(u)
            db.session.commit()
        s = models.Storia(body=form.storia.data, titolo=form.titolo.data, timestamp=datetime.datetime.now(), autore=u)
        db.session.add(s)
        db.session.commit()
        # aggiunge un messaggio alla coda messaggi
        if form.titolo.data != "":
            flash(form.titolo.data)
        flash(form.storia.data)
        # mette i dati della storia in coda per il plottaggio
        q.put((form.autore.data,form.storia.data))
        nick = form.autore.data
        return redirect('/index')
    return render_template('submit_story.html', title='', form=form)
