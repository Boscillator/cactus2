from geoalchemy2.types import Geometry
from application import db

class Count(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    devices = db.Column(db.Integer)
    router_id = db.Column(db.Integer, db.ForeignKey('router.id'))
    router = db.relationship('Router')

    def __repr__(self):
        return f'{self.router}@{self.timestamp}={self.devices}'

class Router(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    geometry = db.Column(Geometry(geometry_type='POLYGON', srid=4326))
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'), nullable=False)
    campus = db.relationship('Campus', backref=db.backref('routers', lazy=True))

    def __repr__(self):
        return self.name

class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))

    def __repr__(self):
        return self.name
