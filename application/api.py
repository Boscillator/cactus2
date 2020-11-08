from flask import jsonify, abort, request
from application import app, db
from application.models import Count, Router, Campus
from datetime import datetime, timedelta
import time
import numpy as np
from statsmodels.tsa.arima_model import ARIMA


@app.route('/api/test')
def test_endpoint():
    return jsonify({'hello': 'world'})


@app.route('/api/campus/<int:campus_id>')
def get_counts(campus_id):
    campus = Campus.query.filter_by(id=campus_id).first_or_404()
    try:
        timestamp = int(request.args['t'])
        time = datetime.fromtimestamp(timestamp)
        print(time)
    except ValueError:
        abort(400)
        return

    return jsonify(campus.counts_as_geojson_at_time(time))


@app.route('/api/count', methods=['POST'])
def add_count():
    if not request.json:
        abort(400)
    
    router_name = request.json['routerID']
    router_id = Router.query.filter_by(name=router_name).first().id

    devices = request.json['clients']

    timestamp = request.json['timestamp']
    timestamp = datetime.fromtimestamp(timestamp)

    count = Count(timestamp=timestamp, devices=devices, router_id=router_id)
    db.session.add(count)
    db.session.commit()

    return jsonify(success=True)

@app.route('/api/external_query', methods=['POST'])
def get_stats():
    if not request.args:
        abort(400)

    router_name = request.args.get('loc')

    router_id = Router.query.filter_by(name=router_name).first().id
    data = Count.query.filter_by(router_id=router_id).all()

    # Get the last recorded amount of people
    last_count = data[-1].devices

    # Get historical high/medium/low rating
    current_time = datetime.today()
    last_month = current_time.replace(day=1) - timedelta(days=1)

    past_counts = np.array([x.devices for x in data if x.timestamp >= last_month])
    std = np.std(past_counts)

    ind = np.argmin([np.abs(last_count - x) for x in [np.max(past_counts), np.median(past_counts), np.min(past_counts)]])
    if ind == 0:
        state = 'high'
    elif ind == 1:
        state = 'medium'
    else: # ind == 1
        state = 'low'

    # Predict upcoming trend
    try: 
        train = list(np.copy(past_counts))
    
        predictions = []
        for i in range(3):
            model = ARIMA(train, order=(4,1,1))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0][0]
            predictions.append(yhat)
            train.append(yhat)

        trend_val = predictions[-1] - last_count
    except:
        trend_val = past_counts[-1] - np.mean(past_counts)

    if np.sign(trend_val) > 0:
        if trend_val > std:
            trend = 'increasing'
        else:
            trend = 'slightly increasing'
    else:
        if np.abs(trend_val) > std:
            trend = 'decreasing'
        else:
            trend = 'slightly decreasing'
    

    res = {'num': last_count, 'state': state, 'trend': trend}

    return res
