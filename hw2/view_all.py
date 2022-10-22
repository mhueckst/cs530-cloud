from flask import render_template
from flask.views import MethodView
import serv_model

# View_All is a simple duplicate of the index class, to view all submitted entries on a separate page

class View_All(MethodView):
    def get(self):
        model = serv_model.get_model()
        entries = [dict(name=row[0], services=row[1], location=row[2], hours=row[3], phone=row[4], review=row[5] ) for row in model.select()]
        return render_template('view_all.html',entries=entries)
