from flask import Flask
from flask import request

from aplotter import *
from youtube_demo.pull_youtube_data import *

app = Flask(__name__)

@app.route("/")
def list_of_demos():
    return "Coming Soon: a List of A-Plotter Demos!"

@app.route("/congress")
def congress_demo():
	return "Coming Soon: Congress Demo"

@app.route("/youtube")
def youtube_demo():
	term = request.args.get('q')
	if term:
		data_string = get_youtube_data_string_for_search_term(term,100)
		return update_html_template(data_string,"'videos'","'subs'","'views'")
	else:
		return "Coming Soon: Input for Query Terms"

# temporary - clear this after better data access system is set up
@app.route("/youtube-test")
def youtube_test():
	data_string = get_test_youtube_data_string()
	return update_html_template(data_string,"'videos'","'subs'","'views'")