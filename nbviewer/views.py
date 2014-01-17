"""
URL routes declarations.

All views are currently declared here.

"""
import os

from flask import render_template, make_response

from nbviewer import app, make_json_error, github
from cloudly import logger

log = logger.init(__name__)


@app.errorhandler(Exception)
def error_handler(error):
    return make_json_error(error)


@app.route('/')
def index():
    listing = github.get_listing()
    webapp_config = {
    }
    return render_template('index.html', config=webapp_config, listing=listing)


@app.route('/notebook/<repo>/<name>')
def notebook(repo, name):
    return render_template('notebook.html', repo=repo, name=name)


@app.route('/raw/<repo>/<name>')
def raw(repo, name):
    content = github.get_content(repo, name)
    # Re-write custom.css path
    content = content.replace("custom.css", "/static/css/custom.css")
    return make_response(content)


def in_production():
    return os.environ.get("IS_PRODUCTION", "").lower() in ['true', 'yes']
