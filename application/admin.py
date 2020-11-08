from application import app, admin, db
from application.models import Count, Router, Campus, RouterAlias
from flask_admin.contrib.geoa import ModelView

admin.add_view(ModelView(Count, db.session))
admin.add_view(ModelView(Router, db.session))
admin.add_view(ModelView(Campus, db.session))
admin.add_view(ModelView(RouterAlias, db.session))