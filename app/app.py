from .car import Car

import json
from bokeh.embed import json_item
from bokeh.resources import CDN
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("main.html")


@app.route('/api')
def api():
    start = float(request.args.get("start", 0))
    end = float(request.args.get("end", 30.556))

    a = Car(start, end)
    settable = ["alfa", "kp", "Td", "Ti", "A", "Ca", "m", "Fdmax"]
    for i in request.args:
        if i in settable:
            a.__setattr__(i, float(request.args.get(i)))
    a.sim()

    plot = a.plots()
    return json.dumps(json_item(plot))
    # https://stackoverflow.com/a/24803830
