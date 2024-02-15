import os
import json
import datetime
from flask import Flask, request, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler

from crawler import crawl_website
from preprocessor import preprocess, inverted_indexer
from query_processor import search_publications


SCHEDULE_INTERVAL = 7
URL = "https://pureportal.coventry.ac.uk/en/organisations/centre-for-health-and-life-sciences/publications"
publications = []

#Flask application instance
app = Flask(__name__)


def crawl_and_scrape():
    #crawl publications website and save in json file
    publications = crawl_website(URL)
    with open("./data/publications.json", "w") as fp:
        json.dump(publications, fp)  

    #pre-processing the title of publication
    processed_tokens = []
    for publication in publications:
        processed_tokens.append(preprocess(publication["title"]))
    with open("./data/processed_tokens.json", "w") as ft:
        json.dump(processed_tokens, ft)

    #inverted indexing
    inverted_index = inverted_indexer(processed_tokens)
    with open("./data/inverted_index.json", "w") as fi:
        json.dump(inverted_index, fi)


def main():
    global inverted_index, processed_tokens, publications

    with open("./data/publications.json", "r") as fp:
        publications = json.loads(fp.read())

    with open("./data/processed_tokens.json", "r") as ft:
        processed_tokens = json.loads(ft.read())

    with open("./data/inverted_index.json", "r") as fi:
        inverted_index = json.loads(fi.read())

    # Running the Flask app
    app.run(debug=True) 


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    # if not query:
    #     return f'<h1>Search Results for: {jsonify([{"Result": ""}])}</h1>'
    search_results = search_publications(query, processed_tokens, inverted_index, publications)

    return render_template('index.html', user_query=query, search_results_list = search_results)


# Create an instance of scheduler
scheduler = BackgroundScheduler()

# Add a job to the scheduler to run gather_and_store function every week
scheduler.add_job(crawl_and_scrape, 'interval', days = SCHEDULE_INTERVAL)

# Start the scheduler
scheduler.start()

if __name__ == '__main__':
    main()