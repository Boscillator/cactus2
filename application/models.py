from geoalchemy2.types import Geography
from application import db

class Count(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    devices = db.Column(db.Integer)
    router_id = db.Column(db.Integer, db.ForeignKey('router.id'))
    router = db.relationship('Router')

class Router(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    geometry = db.Column(Geography(geometry_type='POLYGON', srid=4326))
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'))

class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
