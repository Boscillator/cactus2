from flask import jsonify, abort
from application import app
from models import Count, Router, Campus
import datetime

@app.route('/api/test')
def test_endpoint():
    return jsonify({'hello': 'world'})

@app.route('/api/count', methods=['POST'])
def add_count():
    if not request.json:
        abort(400)
    router_id = request.json['routerID']
    devices = request.json['clients']
    timestamp = request.json['timestamp']
    timestamp = datetime.datetime.fromtimestamp(timestamp)

    count = Count(timestamp=timestamp, devices=devices, router_id=router_id)
    db.session.add(count)
    db.session.commit()

    return 201