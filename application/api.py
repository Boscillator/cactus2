from flask import jsonify
from application import app

@app.route('/api/test')
def test_endpoint():
    return jsonify({'hello': 'world'})