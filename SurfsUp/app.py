import sys; print(sys.executable)

# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func
import datetime as dt
import numpy as np 


#################################################
# Database Setup
#################################################
engine=create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app=Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    """List of all available API routes."""
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # Calculate the date one year ago from the last data point in the database
    last_date = session.query(func.max(Measurement.date)).scalar()
    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= last_year).all()
    session.close()

    # Convert the query results to a dictionary
    precipitation_data = dict(results)
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    stations = [station[0] for station in results]
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Query the last year of temperature data for the most active station
    most_active_station = session.query(Measurement.station).\
                          group_by(Measurement.station).\
                          order_by(func.count(Measurement.station).desc()).first()[0]

    last_date = session.query(func.max(Measurement.date)).scalar()
    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
              filter(Measurement.station == most_active_station).\
              filter(Measurement.date >= last_year).all()
    session.close()

    temperatures = [temp[0] for temp in results]
    return jsonify(temperatures)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end=None):
    session = Session(engine)

    # Convert start and end to datetime objects
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d') if end else None

    # Construct the base query
    query = session.query(func.min(Measurement.tobs), 
                          func.avg(Measurement.tobs), 
                          func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date)

    # Extend the query if an end date is provided
    if end_date:
        query = query.filter(Measurement.date <= end_date)

    results = query.all()
    session.close()

    # Check if results are empty
    if not results or not any(results[0]):
        return jsonify({"error": "No data found for the given date range."}), 404

    temp_stats = list(np.ravel(results))
    return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)