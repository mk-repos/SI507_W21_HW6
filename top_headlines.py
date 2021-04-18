#########################################
##### Name:     Moeki Kurita        #####
##### Uniqname: mkurita             #####
#########################################

import secrets
import json
import requests
from flask import Flask, render_template

# API key ---------------------------------------------------------------------
API_KEY = secrets.api_key


# helper funcs ----------------------------------------------------------------
def make_request(baseurl: str, params: dict):
    '''Make a request to the Web API

    Parameters
    ----------
    baseurl: str
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs

    Returns
    -------
    dict
        the data returned from making the request
    '''
    response = requests.get(baseurl, params=params)
    return response.json()


# flask app -------------------------------------------------------------------

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/name/<nm>')
def hello_name(nm):
    return render_template('name.html', name=nm)


@app.route('/headlines/<nm>')
def headlines(nm):
    # API call
    baseurl = "https://api.nytimes.com/svc/topstories/v2/technology.json"
    params = {"api-key": API_KEY}
    response = make_request(baseurl, params)
    response = response["results"]
    # extract titles
    headlines = []
    for article in response[:5]:
        headlines.append(article['title'])

    return render_template("headlines.html", name=nm, headlines=headlines)


if __name__ == '__main__':
    app.run(debug=True)