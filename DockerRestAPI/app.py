import flask
from flask import Flask, request, jsonify, Response, flash, redirect, url_for, render_template
import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta
import acp_times
import json
import csv
from io import StringIO
import os
import logging
import config

app = Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

# Connect to MongoDB
client = MongoClient('mongo', 27017)
db = client.brevetdb
controls = db.controls

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

@app.route("/_calc_times")
def _calc_times():
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist_km = request.args.get('brevet_dist_km', type=int)
    brevet_start_time = request.args.get('start_time', type=str)
    
    opening_time = acp_times.open_time(km, brevet_dist_km, brevet_start_time)
    closing_time = acp_times.close_time(km, brevet_dist_km, brevet_start_time)

    result = {"open": opening_time, "close": closing_time}
    return jsonify(result=result)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    if not data or not data["controls"]:
        flash("No data was entered. Please fill in the form.", "error")
        return jsonify({"message": "No data was entered. Please fill in the form."}), 400
    
    for control in data["controls"]:
        controls.insert_one(control)
    flash("Data successfully saved!", "success")
    return jsonify({"message": "Data successfully saved!"})

@app.route("/display", methods=["GET"])
def display():
    all_controls = list(controls.find())
    return render_template('display.html', controls=all_controls)

@app.route('/listAll', methods=['GET'])
@app.route('/listAll/<fmt>', methods=['GET'])
def list_all(fmt=None):
    return list_controls(fmt, 'all')

@app.route('/listOpenOnly', methods=['GET'])
@app.route('/listOpenOnly/<fmt>', methods=['GET'])
def list_open_only(fmt=None):
    return list_controls(fmt, 'open')

@app.route('/listCloseOnly', methods=['GET'])
@app.route('/listCloseOnly/<fmt>', methods=['GET'])
def list_close_only(fmt=None):
    return list_controls(fmt, 'close')

def list_controls(fmt, control_type):
    top = request.args.get('top', None)
    query = {}
    projection = {'_id': 0}
    
    if control_type == 'open':
        projection['open'] = 1
    elif control_type == 'close':
        projection['close'] = 1
    
    data = list(controls.find(query, projection))
    
    if top:
        data = data[:int(top)]
    
    if fmt == 'csv':
        return Response(to_csv(data, control_type), mimetype='text/csv')
    else:  # default to json
        return jsonify(brevets=data)

def to_csv(data, control_type):
    si = StringIO()
    cw = csv.writer(si)
    
    cw.writerow(['brevet_dist_km', 'km', 'open', 'close', 'location', 'miles'])

    for brevet in data:
        cw.writerow([
            brevet.get('brevet_dist_km', ''),
            brevet.get('km', ''),
            brevet.get('open', ''),
            brevet.get('close', ''),
            brevet.get('location', ''),
            brevet.get('miles', '')
        ])
    
    return si.getvalue()

if __name__ == '__main__':
    app.run(host='0.0.0.0')