from .car import Car

from flask import Flask, render_template, send_file
app = Flask(__name__)


@app.route('/')
def index():
    print("Wprowadź dane")

    return render_template("main.jinja2")


@app.route('/img/<x>/<y>')
def img(x, y):
    a = Car(int(x), int(y))
    a.sim()

    img = a.plots()
    return send_file(img, mimetype='image/png')
