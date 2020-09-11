import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations:<br/>"
        f"/api/v1.0/tobs:<br/>"
        f"/api/v1.0/<start>:<br/>"
        f"/api/v1.0/<start>/<end>:<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
   results = session.query(Measurement.prcp , Measurement.date).\
       filter(Measurement.date >= '2016-08-23').all()
   temp_dict = [{element[0]:element[1]} for element in results]
   return jsonify(temp_dict)

@app.route("/api/v1.0/stations")

def station():
    results = session.query(Station.station).all()
    all_names = list(np.ravel(results))
    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    one_year_dt = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.tobs).\
    filter(Measurement.date >= one_year_dt).filter(Measurement.station == "USC00519281").all()
    list_temp_obs = list(np.ravel(results))
    return jsonify(list_temp_obs)

@app.route("/api/v1.0/<start>")
def begin(start):
    temp_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(temp_results)

@app.route("/api/v1.0/<start_dt>/<end_dt>")
def finish(start_dt,end_dt):
    temp_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_dt).filter(Measurement.date <= end_dt).all()
    return jsonify(temp_results)

if __name__ == '__main__':
     app.run(debug=True)
