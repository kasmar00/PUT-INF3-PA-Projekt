from .car import Car

from flask import Flask, render_template, send_file
app = Flask(__name__)


@app.route('/')
def index():
    print("Wprowadź dane")

    return render_template("main.jinja2")


@app.route('/img/<alfa>/<start>/<end>/<kp>/<td>/<ti>/<area>/<ca>/<mass>/<fdmax>')
def img(start=0, end=0, alfa=0, kp=0, td=0, ti=0, area=0, ca=0, mass=0, fdmax=0):
    start = float(start)
    end = float(end)
    print(f"Start: {start} end: {end}")
    a = Car(start, end)
    a.alfa = float(alfa)
    a.kp = float(kp)
    a.td = float(td)
    a.ti = float(ti)
    a.area = float(area)
    a.ca = float(ca)
    a.mass = float(mass)
    a.fdmax = float(fdmax)
    a.sim()

    img = a.plots()
    return send_file(img, mimetype='image/png')
