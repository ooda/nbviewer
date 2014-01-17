"""
This module instantiates the Flask application and declares the main error
handling function ``make_json_error``.
"""

# IMPORTANT: updates to the following must also be done in setup.py.
__title__ = "nbviewer"
__version__ = "0.1.0"
__author__ = "Hugues Demers"
__email__ = "hugues.demers@ooda.ca"
__copyright__ = "Copyright 2014 OODA Technologies"
__license__ = "MIT"

import os
import traceback

from flask import Flask, jsonify, request
from flask.ext.basicauth import BasicAuth
from flask_sslify import SSLify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

from cloudly import logger
from cloudly.notify import notify as cloudly_notify
from nbviewer.metric import evt

FORMAT = "%(asctime)s] %(levelname)s %(module)s %(funcName)s: %(message)s"

# The application
app = Flask(__name__)

# Site-wide basic auth credentials
app.config['BASIC_AUTH_USERNAME'] = os.environ.get("NBVIEWER_USERNAME")
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("NBVIEWER_PASSWORD")
app.config['BASIC_AUTH_FORCE'] = True

# Debugging
app.debug = os.environ.get("FLASK_DEBUG", "").lower() == 'true'
app.debug_log_format = FORMAT
log = logger.init(__name__)

# Set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = os.environ.get("WEBAPP_SESSION_SECRET_KEY",
                                          'oftg09jW2FtbXfcud9OS')

# Add basic authentication site-wide.
basic_auth = BasicAuth(app)

# SSLify the app, will redirect all HTTP to HTTPS
sslify = SSLify(app)


# Make this app a JSON app.
# Inspired from cf. http://flask.pocoo.org/snippets/83/
def make_json_error(ex):
    log.error(ex)
    log.error(traceback.format_exc())
    message = ex.description if isinstance(ex, HTTPException) else str(ex)
    message = message.replace("<p>", "").replace("</p>", "") if message else ""
    code = ex.code if isinstance(ex, HTTPException) else 500
    response = jsonify(message=message, status_code=code)
    response.status_code = code

    if code in [500]:
        notify(ex, code)

    evt("error", {'code': code}, request=request)
    return response

for code in default_exceptions.iterkeys():
    app.error_handler_spec[None][code] = make_json_error


def notify(exception, code=None):
    if not code:
        code = exception.code if isinstance(exception, HTTPException) else 500
    cloudly_notify("Exception: {}".format(code), "{}\n\n{}".format(
        exception, traceback.format_exc(exception)))


import nbviewer.views  # noqa
