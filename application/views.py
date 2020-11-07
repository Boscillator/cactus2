from flask import request, render_template
from application import app
from application.models import Campus


@app.route('/')
def index():
    if request.args.get('campus') is None:
        current_campus = Campus.query.first()
    else:
        current_campus = Campus.query.filter_by(id=request.args.get('campus')).first_or_404()

    campuses = Campus.query.all()

    return render_template('index.html', current_campus=current_campus, campuses=campuses)
