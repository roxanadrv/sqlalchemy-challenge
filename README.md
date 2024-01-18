# SurfUp: Hawaii Climate Analysis API
## Overview
SurfUp is a Flask-based API designed to serve climate data analysis for Honolulu, Hawaii. The project entails detailed climate analysis using Python, SQLAlchemy, and Flask, and presents the findings through a web API. The analysis focuses on precipitation trends, station data, and temperature observations.

## Features
    Precipitation Analysis: Retrieve the last 12 months of precipitation data.
    Station Analysis: List all weather observation stations.
    Temperature Observations: Fetch the last year of temperature data for the most active station.
    Temperature Statistics: Provide temperature statistics (min, max, avg) for a given date range.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
    Python 3.x
    Flask
    SQLAlchemy
    SQLite
    
## Installation
Clone the repository to your local machine:

git clone https://github.com/yourusername/SurfUp.git


## Navigate to the cloned directory:
cd SurfUp

## Install the required Python packages:
pip install -r requirements.txt

## Running the Application
Start the Flask server:
python app.py
Access the API through http://127.0.0.1:5000/ on your browser or use a tool like Postman to interact with the API.

## API Endpoints
/api/v1.0/precipitation: Returns precipitation data for the last year.
/api/v1.0/stations: Provides a list of weather observation stations.
/api/v1.0/tobs: Retrieves the last year of temperature observations from the most active station.
/api/v1.0/<start> and /api/v1.0/<start>/<end>: Temperature statistics for a specified date range.

## Built With
Python - The programming language used.
Flask - The web framework used.
SQLAlchemy - The database toolkit used.
SQLite - The database engine used.
