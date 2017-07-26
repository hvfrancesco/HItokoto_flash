from app import db

class Storia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    autore = db.Column(db.String(64), index=True, unique=False)
    storia = db.Column(db.String(10000), index=True, unique=True)

    def __repr__(self):
        return '<Autore %r>' % (self.autore)
