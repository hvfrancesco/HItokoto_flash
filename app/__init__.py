# -*- coding: utf-8 -*- 

from flask import Flask, request, flash
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_user import login_required, roles_required, UserManager, UserMixin, SQLAlchemyAdapter, passwords
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
from wtforms.fields import PasswordField, TextAreaField
from wtforms.widgets import TextArea
from flask_user import current_user
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

# Si istanzia l'APIManager di FLask-Restless per l'API di accesso al database
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(models.Autore, methods=['GET', 'POST', 'DELETE'], results_per_page=0)
manager.create_api(models.Storia, methods=['GET'], results_per_page=0)

db_adapter = SQLAlchemyAdapter(db, models.User) # necessario per UserManager
user_manager = UserManager(db_adapter, app)


# campi per admin con uso di ckeditor, per ora disabilitato
class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


# CLasse custom per il modello User per SQL-Admin
class UserAdmin(ModelView):
    create_modal = True
    edit_modal = True
    # Don't display the password on the list of Users
    column_exclude_list = ('password',)
    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)
    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True
 # Prevent administration of Users unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        try:
            return current_user.has_role('admin')
        except:
            return False
    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):
        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()
        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class
    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes are
    # committed to the database.
    def on_model_change(self, form, model, is_created):
        # If the password field isn't blank...
        if len(model.password2):
            # ... then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = passwords.hash_password(user_manager, model.password2)


# Classe custom generica per SQL-Admin
class DbAdmin(ModelView):
    #extra_js = ['/static/js/ckeditor/ckeditor.js']
    #form_overrides = {'body' : CKTextAreaField}
    form_overrides = {'body' : TextAreaField}
    #create_modal = True
    #edit_modal = True
    # Prevent administration of tables unless the currently logged-in user has the "admin" role
    def is_accessible(self):
        try:
            return current_user.has_role('admin')
        except:
            return False

# classe custom per fare l'override del controllo di accessibilità su FileAdmin
class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        try:
            return current_user.has_role('admin')
        except:
            return False

# si istanzia l'interfaccia amministrativa e si aggiungono le relative view
admin = Admin(app, name='HITOKOTO Flash', template_mode='bootstrap3')
#admin.add_view(ModelView(models.User, db.session))
admin.add_view(DbAdmin(models.Autore, db.session))
admin.add_view(DbAdmin(models.Storia, db.session))
admin.add_view(UserAdmin(models.User, db.session, name="Utenti"))
admin.add_view(DbAdmin(models.Role, db.session, name="Ruoli"))
# amministrazione dei files statici
path_statico = op.join(op.dirname(__file__), 'static')
admin.add_view(CustomFileAdmin(path_statico, '/static/', name='Files Statici'))

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

views.c = controller
