import json
import datetime
from geoalchemy2.types import Geometry
from sqlalchemy import text
from application import db


class Count(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    devices = db.Column(db.Integer)
    router_id = db.Column(db.Integer, db.ForeignKey('router.id'))
    router = db.relationship('Router', backref=db.backref('counts', lazy=True))

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

    def counts_at_time(self, dt):
        query = text("""        
        SELECT count.timestamp, r.name, st_asgeojson(r.geometry), count.devices
        FROM count
                 JOIN (SELECT router_id, MAX(timestamp) AS ts FROM count WHERE timestamp < :dt GROUP BY router_id) t1
                      ON count.router_id = t1.router_id AND count.timestamp = t1.ts
        JOIN router r on count.router_id = r.id
        WHERE campus_id = :cid
        """)

        result = db.session.execute(query, {'cid': self.id, 'dt': dt})
        return list(result)

    def counts_as_geojson_at_time(self, dt):
        results = self.counts_at_time(dt)
        return {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'properties': {
                        'name': row['name'],
                        'devices': row['devices']
                    },
                    'geometry': json.loads(row['st_asgeojson'])
                } for row in results
            ]
        }

    def current_counts(self):
        return self.counts_at_time(datetime.datetime.now())

    def current_counts_as_geojson(self):
        return self.counts_as_geojson_at_time(datetime.datetime.now())

    def __repr__(self):
        return self.name
