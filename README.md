# Bank Statement Processor

## Description

This is a bank statement processor that scrapes a pdf bank statement document and stores that information in a database that can be viewed using a [React](https://github.com/facebook/create-react-app) frontend. Account and transaction information is stored.

## Setup

Firstly install all requirements for the pdf scraper. This can be done by using the requirements.txt file.

Execute this command. `pip install -r requirements.txt`

I would reccomend doing this in a python virtual environment (venv).

Secondly install all node dependancies by navigating to the frontend using this command. `cd .\frontend\bank-statement-processor` and then executing this command `npm install`.

## Execution

Run the python backend by executing this command. `py .\backend\app.py`. This will create create a Flask application that is ready to listen for API endpoints. It will be run on localhost (127.0.0.1) and on port 5000 by default.

Run the React frontend application by executing the command. `npm start` (assuming you are in the .\frontend\bank-statement-processor directory).

## Usage

Upload a statement from the files folder provided using the upload statement button. This will save the account and transactions information in a SQLite database. The information will then be displayed. If you look at the terminal where the backend was launched you will be able to see all API calls made. You can return to the upload button where there are now two options. You may upload another statement or view the same statement you uploaded.
