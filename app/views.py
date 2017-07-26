from flask import render_template, flash, redirect
from app import app
from .forms import submitStory
import os
from .plot import plotter_virtuale

p = plotter_virtuale()
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
        q.put((form.autore.data,form.storia.data))
        y = 0
        for linea in form.storia.data.split(os.linesep):
            p.scrivi_linea(linea, y)
            y += 1
        nick = form.autore.data
        p.mostra_foglio()
        return redirect('/index')
    return render_template('submit_story.html', title='', form=form)
