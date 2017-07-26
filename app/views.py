from flask import render_template, flash, redirect
from app import app, db, models
from .forms import submitStory



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
        s = models.Storia(autore=form.autore.data, storia=form.storia.data)
        db.session.add(s)
        db.session.commit()
        flash(form.storia.data)
        q.put((form.autore.data,form.storia.data))
        nick = form.autore.data
        return redirect('/index')
    return render_template('submit_story.html', title='', form=form)
