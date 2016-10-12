from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('../config/bookforex.cfg')

db = SQLAlchemy(app)

import bookforex.view
import bookforex.model


