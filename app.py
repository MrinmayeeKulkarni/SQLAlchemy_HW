import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
app = Flask(__name__)
start_date=dt.datetime(2016,8,23)
end_date=dt.datetime(2017,8,23)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precip():
    sel=[Measurement.date,Measurement.prcp]
    year_data=session.query(*sel).filter(func.strftime(Measurement.date>=start_date,Measurement.date<=end_date)).order_by(Measurement.date).all()
    all_precip = []
    for date,prcp in year_data:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["Precip"] = prcp
        all_precip.append(precipitation_dict)
        return jsonify(all_precip)
@app.route("/api/v1.0/stations")
def stations():
    sel1=[Measurement.station,func.count(Measurement.station)]
    temp=session.query(*sel1).group_by(Measurement.station).order_by((func.count(Measurement.station)).desc()).all()
    all_stations = list(np.ravel(temp))
    return jsonify(all_stations)
@app.route("/api/v1.0/tobs")
def temperatures():
    year_tobs=session.query(Measurement.tobs).filter(Measurement.station=="USC00519281").filter(func.strftime(Measurement.date>=start_date,Measurement.date<=end_date)).order_by(Measurement.tobs).all()
    list_temps=list(np.ravel(year_tobs))
    return jsonify(list_temps)
@app.route("/api/v1.0/start")
def calc_start_temp(start=None):
    start_temp_data=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    data_with_start=list(np.ravel(start_temp_data))
    return jsonify(data_with_start)
@app.route("/api/v1.0/start/end")
def calc_temps(start=None,end=None):
    temp_data=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    calc_temp=list(np.ravel(temp_data))
    return jsonify(calc_temp)

if __name__ == '__main__':
    app.run(debug=True)