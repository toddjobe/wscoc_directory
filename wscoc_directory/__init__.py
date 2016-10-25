import os
from flask import Flask

# from wscoc_directory.database import db_session

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('wscoc_directory.default_settings')
app.config.from_pyfile('wscoc_directory.cfg', silent=True)
app.config.from_envvar('WSCOC_DIRECTORY_SETTINGS', silent=True)

#@app.teardown_appcontext
#def shutdown_session(exception=None):
    #db_session.remove()

import wscoc_directory.views
