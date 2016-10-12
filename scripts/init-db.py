import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bookforex import db
from bookforex.model import Trade

db.drop_all()
db.create_all()
db.session.commit()
