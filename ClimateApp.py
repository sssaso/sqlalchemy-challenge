# Use Flask to create your routes.
### 1. import modules ######################################
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


### 2.Database Setup  #######################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
### reflect an existing database into a new model  
Base = automap_base()
### reflect the tables 
Base.prepare(engine, reflect=True)
### Save reference to the table  
Measurement = Base.classes.measurement
Station = Base.classes.station

### 3.Flask Setup  ###########################################
# Create an app
app = Flask(__name__)

# 3.1. Create Route: Home route
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )

# 3.2. Precipitation route
@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation for the last 12 months"""
    # Query all precipitation data
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23')

    session.close()

    # Convert list of tuples into normal list
    # precipitation_list = list(np.ravel(prcp_results))

    # Create a dictionary from the row data and append to the list
    prcp_list = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


# 3.3. Stations route
@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station name and station number"""
    # Query all stations
    stat_results = session.query(Station.station, Station.name, \
        Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to the list
    stat_list = []
    for station, name, lat, log, elev in stat_results:
        stat_dict = {}
        stat_dict["station"] = station
        stat_dict["name"] = name
        stat_list.append(stat_dict)

    return jsonify(stat_list) 

# 3.4. TOBS route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature for the last 12 months"""
    # Query all tobs data
    temp_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23')

    session.close()

    # Create a dictionary from the row data and append to the list
    tobs_list=[]
    for date, tobs in temp_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

# 3.5. Start route

@app.route("/api/v1.0/<start>")
def start_date(start):
   # Using TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
   # return TMIN, TAVG, TMAX
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
        func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    # convert list of tuples into normal list
    temp_start =  list(np.ravel(results))

    return jsonify(temp_start)

# 3.6. start & end 
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
   # Using TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
   # return TMIN, TAVG, TMAX
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # convert list of tuples into normal list
    tobs_start_end = list(np.ravel(results))

    return jsonify(tobs_start_end)

if __name__ == "__main__":
    app.run(debug=True)

