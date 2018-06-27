# gbapp

A simple application to create a DB table and load data from csv files 
(GB coding challenge)

## Getting started

Clone this project locally

```

git clone git@github.com:vishket/gbapp.git

```

### Pre requisites

1) This application requires **Python 2.7 +**, stable version of **Flask**
, the Python library for postgres **psycopg2** and the dotenv module
**python-dotenv**

These dependencies can be easily installed by running the requirement.txt
 file like so...
 
```
 pip install -r requirements.txt
```

2) Database connection parameters

Enter your database connection values in the .env file which resides at
the root of the application folder

## Run

Once you have all the dependencies installed, simply...

```
cd gbapp/gbapp

python app.py

```

This will launch the application and start serving locally on the 
default port 5000

To view the app go to http://localhost:5000/

## Features

This application provides two endpoints

- Create a Database table: http://localhost:5000/create_table

The *create_table* endpoint creates a new table based on the schema 
defined in the 'schema.csv' file. You can also navigate to the same 
endpoint from the hyperlink on the home page.

WARNING: Creating a table with the same name as an existing one would 
result in an error. You will either have to DROP the existing table OR 
rename the new table in the .env file
 
- Load data into table: http://localhost:5000/load_data
 
The *load_data* endpoint loads data from 'data.csv' into an existing 
database table.

## Examples

The drop_data folder consists of a couple of sample schema,data csv 
pairs. By default, the app will look for files named "schema.csv" and 
"data.csv". In order to run the second pair of files, you will have
to swap the filenames


## Tests

Unit tests can be found in the test folder. Tests can be executed by 
simply running...

```
pytest
```

## Questions & Assumptions

1) Column width:

The "width" field in the example schema.csv file seemed a bit 
confusing. Although the width for the author_name column seems to be 
set to 10, the output table still has records with data in the 
author_name column having greater than 10 characters. Also, for INTEGER
the width appears to be set to 2. However, for Postgresql it does not 
allow setting a max size for INTEGER and for MySQL, it sets the byte 
size but not width. 

So, I decided to choose VARCHAR instead of CHAR for the author_name 
column and the default INT
 
2) Drop_data folder:
 
I am assuming the "drop_data" folder to be static. To make it dynamic,
I would've created a HTML form and asked the user to insert the folder
path
 

  