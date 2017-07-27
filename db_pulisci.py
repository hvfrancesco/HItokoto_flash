#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from app import db, models

autori = models.Autore.query.all()
for a in autori:
    db.session.delete(a)

storie = models.Storia.query.all()
for s in storie:
    db.session.delete(s)

db.session.commit()