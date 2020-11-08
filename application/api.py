from flask import jsonify, abort, request
from application import app, db
from application.models import Count, Router, Campus
import datetime

@app.route('/api/test')
def test_endpoint():
    return jsonify({'hello': 'world'})

@app.route('/api/count', methods=['POST'])
def add_count():
    if not request.json:
        abort(400)
    router_name = request.json['routerID']
    router_id = Router.query.filter_by(name=router_name).first().id
    
    devices = request.json['clients']
    
    timestamp = request.json['timestamp']
    timestamp = datetime.datetime.fromtimestamp(timestamp)

    count = Count(timestamp=timestamp, devices=devices, router_id=router_id)
    db.session.add(count)
    db.session.commit()

    return jsonify(success=True)