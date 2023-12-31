from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import serv_model

class Sign(MethodView):
    def get(self):
        return render_template('sign.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        model = serv_model.get_model()
        model.insert(request.form['name'], request.form['services'], request.form['location'], request.form['hours'], request.form['phone'], request.form['review'])
        return redirect(url_for('index'))
