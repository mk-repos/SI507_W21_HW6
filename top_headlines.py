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


def get_nyt_articles():
    """Get technology headlines from NYT

    Returns
    -------
    list
        list of resulting dictionaries of each article
    """
    baseurl = "https://api.nytimes.com/svc/topstories/v2/technology.json"
    params = {"api-key": API_KEY}
    response = make_request(baseurl, params)
    return response["results"]


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
    response = get_nyt_articles()
    # extract titles
    headlines = []
    for article in response[:5]:
        headlines.append(article['title'])

    return render_template("headlines.html", name=nm, headlines=headlines)


@app.route('/links/<nm>')
def links(nm):
    # API call
    response = get_nyt_articles()
    # extract titles and links
    hyperlinks = {}
    for article in response[:5]:
        hyperlinks[article['title']] = article['url']

    return render_template("links.html", name=nm, hyperlinks=hyperlinks)


@app.route('/images/<nm>')
def images(nm):
    # API call
    response = get_nyt_articles()
    # extract titles, links, thumbnails
    articles = []
    for article in response[:5]:
        articles.append({"title": article['title'],
                         "url": article['url'],
                         "thumbnail": article['multimedia'][0]['url']})

    return render_template("images.html", name=nm, articles=articles)


if __name__ == '__main__':
    app.run(debug=True)