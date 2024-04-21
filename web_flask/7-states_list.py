#!/usr/bin/python3
"""Write a script that starts a Flask web application"""

from flask import Flask, render_template
from models.state import State
from models import storage

app = Flask(__name__)


@app.route('/states_list', strict_slashes = False)
def states_list():
    """/states_list: display a HTML page: (inside the tag BODY:"""
    state_all = list(storage.all().values())
    states = sorted(state_all, key=lambda i: i.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext(strict_slashes = False)
def teardown(exception):
    """Declare a method to handle @app.teardown_appcontext"""
    storage.close()


if __name__ == "__main__":
    """run it"""
    app.run(host='0.0.0.0', port=5000)
