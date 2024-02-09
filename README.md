# Project Description

Python application that reads a Google spreadsheet, calculate the columns "Situação" and "Nota para Aprovação Final" based on the data and finally write it back.

This project comprises the programming challenge proposed by Tunts.Rocks and was done in the Python programming language.

## Set Up environment
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the Google client library for Python. To do this, open the terminal and type:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Set up the credentials for access Google Sheets following the [instructions](https://developers.google.com/sheets/api/quickstart/python#set_up_your_environment) in Google Workspace documentation. Important: Do not forget to enter your email address during the configuration of the OAuth consent screen, otherwise Google will not allow you to access the data.

At the end of this process you should have the "credentials.json" file in the working directory and the Google client library for Python installed.

## Usage
To use this script, just open the terminal and run the following code:

```bash
python3 chalenge_students.py
```
The script will return log lines to monitor the application's activities and the results can be checked in the spreadsheet.