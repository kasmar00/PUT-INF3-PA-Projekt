from .car import Car

from flask import Flask, render_template, send_file, request
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("main.html")


@app.route('/api')
def api():
    start = float(request.args.get("start", 0))
    end = float(request.args.get("end", 20))

    a = Car(start, end)
    settable = ["alfa", "kp", "Td", "Ti", "A", "Ca", "m", "Fdmax"]
    for i in request.args:
        if i in settable:
            a.__setattr__(i, float(request.args.get(i)))
    a.sim()

    img = a.plots()
    return send_file(img, mimetype='image/png')
