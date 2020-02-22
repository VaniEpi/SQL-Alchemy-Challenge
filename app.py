import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only
from sqlalchemy import create_engine, func, distinct
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


app = Flask(__name__)

hello_dict = {"Hello": "World!"}


@app.route("/")
def home():
    return (
        f"Welcome to the Weather Info API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    last_measurement = session.query(Measurement).order_by(Measurement.id.desc()).first()
    # Calculate the date 1 year ago from the last data point in the database
    end_date = last_measurement.date
    start_date = '2016-08-23'
    # Perform a query to retrieve the data and precipitation scores
    precip_12_months = (session.query(Measurement.date, Measurement.prcp)
                        .filter(Measurement.date >= start_date, Measurement.date <= end_date)
    )

    session.close()

    # Create a dictionary from the row data and append to list of precipitation results
    precip_results = []
    for date, prcp in precip_12_months:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_results.append(precip_dict)

    return jsonify(precip_results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    most_active_stations = (session.query(Measurement.station, func.count(Measurement.station))
                        .group_by(Measurement.station)
                        .order_by(func.count(Measurement.station).desc())
                        .all())

    session.close()

    # Create a dictionary from the row data and append to a list of weather stations
    station_results = []
    for station, count in most_active_stations:
        station_dict = {}
        station_dict["station"] = station
        station_dict["count"] = count
        station_results.append(station_dict)

    return jsonify(station_results)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    last_measurement = session.query(Measurement).order_by(Measurement.id.desc()).first()
    # Calculate the date 1 year ago from the last data point in the database
    end_date = last_measurement.date
    start_date = '2016-08-23'
    # Perform a query to retrieve the data and precipitation scores
    temp_12_months = (session.query(Measurement.date, Measurement.tobs)
                      .filter(Measurement.date >= start_date, Measurement.date <= end_date)
                      .filter(Measurement.station == 'USC00519281')
    )

    session.close()

    # Create a dictionary from the row data and append to a list of temperatures
    temp_results = []
    for date, tobs in temp_12_months:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_results.append(temp_dict)

    return jsonify(temp_results)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stats = (session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))
        .group_by(Measurement.station)
        .filter(Measurement.date >= start)
    )

    session.close()

    # Create a dictionary from the row data and append to a list of stations
    stat_results = []
    for station, tmin, tmax, tavg in stats:
        stat_dict = {}
        stat_dict["STATION"] = station
        stat_dict["TMIN"] = tmin
        stat_dict["TMAX"] = tmax
        stat_dict["TAVG"] = tavg
        stat_results.append(stat_dict)

    return jsonify(stat_results)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stats = (session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))
        .group_by(Measurement.station)
        .filter(Measurement.date >= start, Measurement.date <= end)
    )


    session.close()

    # Create a dictionary from the row data and append to a list of stations
    stat_results = []
    for station, tmin, tmax, tavg in stats:
        stat_dict = {}
        stat_dict["STATION"] = station
        stat_dict["TMIN"] = tmin
        stat_dict["TMAX"] = tmax
        stat_dict["TAVG"] = tavg
        stat_results.append(stat_dict)

    return jsonify(stat_results)



if __name__ == "__main__":
    app.run(debug=True)
