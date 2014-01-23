import os

from flask.ext.basicauth import BasicAuth


class MyBasicAuth(BasicAuth):
    def __init__(self, app=None):
        super(MyBasicAuth, self).__init__(app)

    def check_credentials(self, username, password):
        usernames = os.environ.get("NBVIEWER_USERNAMES", '').split('/')
        passwords = os.environ.get("NBVIEWER_PASSWORDS", '').split('/')

        creds = {u: p for u, p in zip(usernames, passwords)}
        return username in creds and creds[username] == password
