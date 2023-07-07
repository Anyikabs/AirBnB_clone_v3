#!/usr/bin/python3
"""
    This script starts a Flask web application
"""

from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Returns Homepage"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns page for /hbnb"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """Returns page for /c/<text>"""
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text="is cool"):
    """Returns page for /python/<text>"""
    return "Python {}".format(text.replace('_', ' '))


# @app.route('/number/', strict_slashes=False)
@app.route('/number/<int:n>', strict_slashes=False)
def number_n(n):
    """Returns page for /number/<n> when n is an integer"""
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
