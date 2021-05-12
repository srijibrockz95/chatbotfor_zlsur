"""
app config initialization
"""

from datetime import timedelta
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from Chatbotforwip import configs

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'AhkjshjaskjJDJhshdjk'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

if configs.dev_configs_from_file:
    for m in configs.dev_configs_from_file:
        app.config.update(m)

app.config['SQLALCHEMY_DATABASE_URI'] += '?check_same_thread=False'

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)
