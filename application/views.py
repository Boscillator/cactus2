import datetime
from flask import request, render_template, abort
from application import app
from application.models import Campus


@app.route('/')
def index():
    campuses = Campus.query.all()

    if request.args.get('t') is None:
        time = datetime.datetime.utcnow()
    else:
        try:
            time = datetime.datetime.fromtimestamp(int(request.args.get('t')))
        except ValueError:
            abort(400)
            return

    if request.args.get('campus') is None:
        current_campus: Campus = campuses[0]
    else:
        current_campus = Campus.query.filter_by(id=request.args.get('campus')).first_or_404()

    features = current_campus.counts_as_geojson_at_time(time)

    return render_template('index.html', current_campus=current_campus, campuses=campuses, features=features)
