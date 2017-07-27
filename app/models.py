from app import db

class Autore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True, unique=True)
    storie = db.relationship('Storia', backref='autore', lazy='dynamic')

    def __repr__(self):
        return '<Autore %r>' % (self.nome)

class Storia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(10000), index=True, unique=True)
    timestamp = db.Column(db.DateTime)
    auth_id = db.Column(db.Integer, db.ForeignKey('autore.id'))

    def __repr__(self):
        return '<Storia %r>' % (self.body)