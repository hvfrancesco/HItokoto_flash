from app import db
from flask_user import UserMixin


class Autore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(255), index=True)
    storie = db.relationship('Storia', backref='autore', lazy='dynamic')

    def __repr__(self):
        return '<Autore %r>' % (self.nome)

class Storia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(64), index=True)
    body = db.Column(db.String(10000), index=True)
    timestamp = db.Column(db.DateTime)
    auth_id = db.Column(db.Integer, db.ForeignKey('autore.id'))

    def __repr__(self):
        return '<Storia %r>' % (self.body)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Ruolo %r>' % (self.name)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    # Ruolo
    roles = db.relationship('Role', secondary='user_roles', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.username)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))