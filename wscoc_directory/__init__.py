import os
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('wscoc_directory.default_settings')
app.config.from_pyfile('wscoc_directory.cfg', silent=True)
app.config.from_envvar('WSCOC_DIRECTORY_SETTINGS', silent=True)

import wscoc_directory.views
