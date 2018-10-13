from flask import Flask
from flask import request

from aplotter import *

app = Flask(__name__)

@app.route("/")
def list_of_demos():
    return "Coming Soon: a List of A-Plotter Demos!"

@app.route("/congress")
def congress_demo():
	return "Coming Soon: Congress Demo"

@app.route("/youtube")
def youtube_demo():
	query = request.args.get('q')
	if query is None:
		return "Coming Soon: Input for Query Terms"
	else:
		return "Coming Soon: Viz for {}".format(query)