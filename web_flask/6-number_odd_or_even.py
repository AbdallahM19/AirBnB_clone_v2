#!/usr/bin/python3
"""Write a script that starts a Flask web application"""

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays 'Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hi_hbnb():
    """/hbnb: display “HBNB”"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def C_text(text):
    """
    /c/<text>: display “C ”,
    followed by the value of the text variable
    (replace underscore _ symbols with a space )
    """
    return "C {}".format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is_cool'):
    """
    /python/(<text>): display “Python ”,
    followed by the value of the text variable
    (replace underscore _ symbols with a space )
    """
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def n_text(n):
    """
    /number/<n>: display
    “n is a number” only if n is an integer
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def template_n(n):
    """
    /number_template/<n>:
    display a HTML page only if n is an integer:
    H1 tag: “Number: n” inside the tag BODY
    """
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def template_n_odd_or_even(n):
    """
    /number_odd_or_even/<n>:
    display a HTML page only if n is an integer:
    H1 tag: “Number: n is even|odd” inside the tag BODY
    """
    return render_template(
        '6-number_odd_or_even.html', n=n, type_n=(
            "even" if n % 2 == 0 else "odd"
        )
    )


if __name__ == "__main__":
    """run it"""
    app.run(host="0.0.0.0", port=5000)
