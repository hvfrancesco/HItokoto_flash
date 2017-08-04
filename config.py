import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'HITOKOTO-RULEZ'

CSRF_ENABLED = True

# Flask-Mail settings
MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'hito@hitokoto.xyz')
MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'hitokoto_14')
MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"HITOKOTO" <hito@hitokoto.xyz>')
MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp1.servage.net')
MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

# Flask-User settings
USER_APP_NAME        = "HITOKOTO Flash"                # Used by email templates
