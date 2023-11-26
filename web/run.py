from flask import Flask
import os
from reversi_app import reversi_app

basedir = os.path.abspath(os.path.dirname('__file__'))

app = Flask(__name__, template_folder='templates', static_folder='static', instance_relative_config=True)

from flask_jsglue import JSGlue

jsglue = JSGlue(app)

app.register_blueprint(reversi_app, url_prefix='/')

app.config.from_object('config')
app.config.from_pyfile('config.py')

SIJA_path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

try:
    from flask_debugtoolbar import DebugToolbarExtension

    toolbar = DebugToolbarExtension(app)
except ImportError:
    toolbar = None

if __name__ == '__main__':
    app.run(host="localhost", port=2333, threaded=True)
