from application import app, db

@app.cli.command('create-all')
def create_db():
    db.create_all()