from flask import render_template, flash, redirect
from app import app, db, models
from flask_user import login_required, roles_required, current_user

from .forms import submitStory
import datetime
import os


q = None
c = None
nick = 'autore'

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': nick}
    return render_template('index.html', title='Hitokoto Flash', user=user)

@app.route('/controllo/<comando>')
@roles_required('admin')
def get(comando):
    if (comando == 'pausa'):
        c.pausa()
        if c.condition:
            flash("sto lavorando")
        else:
            flash("in pausa")
        return redirect('/index')
    elif (comando == 'titolo'):
        c.stampa_titolo_tavola()
        flash("titolo stampato sul nuovo foglio")
        return redirect('/index')
    elif (comando == 'autopdf'):
        c.toggle_auto_pdf()
        if c.worker.auto_pdf:
            flash("auto PDF abilitato")
        else:
            flash("auto PDF disabilitato")
        return redirect('/index')
    elif (comando == 'pdf'):
        c.produci_pdf()
        flash("prodotto un nuovo PDF")
        return redirect('/index')
    else:
        flash("comando "+comando+" sconosciuto")
        return redirect('/index')

@app.route('/storia', methods=['GET', 'POST'])
@login_required
def invia_storia():
    form = submitStory()
    if form.validate_on_submit():
        flash('storia inviata da %s' % form.autore.data)
        u = models.Autore.query.filter_by(nome = form.autore.data).first()
        if (not u):
            if current_user.is_authenticated:
                u_mail = current_user.email
            else:
                u_mail = ''
            u = models.Autore(nome=form.autore.data, email=u_mail)
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
