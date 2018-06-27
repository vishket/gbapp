#!/usr/bin/env python

# This application allows users to create a Table and load data into it using the functions defined in this file.
# It uses 3 basic functions: parse_schema(), create_table(), load_data()
#
# For the purpose of this app, we are using static directories to store the schema & data csv files
#
# Database information and credentials are passed using environment variables

import os
import csv
import psycopg2

from flask import Flask
from dotenv import load_dotenv

# Create a Flask app object
app = Flask(__name__)

# Configure app root directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Set path to the .env file to load DB connection parameters
dotenv_path = basedir + '/../.env'

# Load DB env variables
load_dotenv(dotenv_path)

# Configure absolute path to input files
SCHEMA_FILE = basedir + "/../drop_data/schema.csv"
DATA_FILE = basedir + "/../drop_data/data.csv"

# Get database information
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
TABLE_NAME = os.getenv('DB_TABLE')


def parse_schema(filename):
    """
    A helper function to parse csv input data and generate a sql query string.
    :param str filename: The input filename
    :return: Return the SQL query string to execute and None. Returns None, err in case input file does not exist
    """
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)

            # Extract headers fields
            fields = reader.next()

            query = ""
            # Query structure
            # query = ( column_name datatype )
            # Example: query = (name CHAR, id INT, ...)

            for row in reader:
                query += row[0] + " " + row[2] + ", "

        return query[:-2], None

    except IOError as e:
        print "[Error] Parsing input data failed with error: {}\n".format(e)
        return None, e


@app.route('/create-table')
def create_table():
    """
    Function to create a database table.  Parses data from the schema file and builds a SQL query
    Tries connecting to the DB and executes the query
    Raises exception if error encountered during table creation
    """
    # Fetch table schema
    query, err = parse_schema(SCHEMA_FILE)
    if query is not None:
        try:
            # Establish DB connection
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cur = conn.cursor()

            # Create TABLE
            cur.execute("CREATE TABLE {} ({});".format(TABLE_NAME, query))
            cur.close()
            conn.commit()
            print "[INFO] Successfully created new table: {}".format(TABLE_NAME)
            return "<h>{} successfully created</h> <br /><br /> <a href='http://localhost:5000/load-data'>Load Data" \
                   "</a><br /><br /> <a href='http://localhost:5000'>Home Page </a>".format(TABLE_NAME)

        except psycopg2.DatabaseError as e:
            print "[Error] Creating table {}, failed with error: {}".format(TABLE_NAME, e)
            return "<h>Error creating {}: {}</h><br /><br /><a href='http://localhost:5000'>Home Page</a>".\
                format(TABLE_NAME, e)
    else:
        print "[Error] Creating table {}, failed with error: {}".format(TABLE_NAME, err)
        return "<h>Error creating {}: {}</h><br /><br /><a href='http://localhost:5000'>Home Page</a>". \
            format(TABLE_NAME, err)


@app.route('/load-data')
def load_data():
    """
    Loads data from CSV file into database table
    :return: Return boolean indicating success of failure
    """
    try:
        # Establish DB connection
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()

        cur.execute("COPY {} FROM '{}' DELIMITER ',' CSV HEADER".format(TABLE_NAME, DATA_FILE))
        cur.close()
        conn.commit()
        print "[INFO] Successfully loaded data to {}".format(TABLE_NAME)
        return "<h>Successfully loaded data into {}</h><br /><br /><a href='http://localhost:5000'>Home Page " \
               "</a>".format(TABLE_NAME)

    except psycopg2.DatabaseError as e:
        print "[Error] loading data to {}, failed with error: {}".format(TABLE_NAME, e)
        return "<h>Error loading data into {}: {}</h> <br /><br /> <a href='http://localhost:5000'>Home Page " \
               "</a>".format(TABLE_NAME, e)


# Application home page with links to create a new table or load data to an existing table
@app.route('/')
def run():
    return "<h><b>Guidebook sample APP!</b></h> <br /><br /><a href='http://localhost:5000/create-table'>Create Table" \
           "</a><br /> <a href='http://localhost:5000/load-data'>Load Data</a>"


if __name__ == '__main__':
    app.run(debug=True)

