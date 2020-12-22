from .car import Car

from flask import Flask, render_template, send_file
app = Flask(__name__)


@app.route('/')
def index():
    print("Wprowadź dane")

    return render_template("main.jinja2")


@app.route('/img/<int:start>/<int:end>')
def img(start=0, end=0):
    print(f"Start: {start} end: {end}")
    a = Car(start, end)
    a.sim()

    img = a.plots()
    return send_file(img, mimetype='image/png')
