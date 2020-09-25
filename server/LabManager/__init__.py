import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = 'changeme' # Mandatory to change this on deploy
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
# app.config["IMG_DIR"] = os.path.join(app.root_path, "static", "images")
app.config["IMG_DIR"] = os.path.join("static", "images")
cors = CORS(app, resources={r'/*': {'origins': '*'}}) # Restrict to frontend host on production
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

# These imports below will avoid circular imports
from LabManager.auth.routes import auth
from LabManager.main.routes import main
from LabManager.personnel.routes import personnel
from LabManager.equipments.routes import equipments
from LabManager.fieldtrips.routes import fieldtrips
from LabManager.notices.routes import notices
from LabManager.calendar.routes import calendar
from LabManager.news.routes import news
from LabManager.utils.file_transfer.routes import file_transfer

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(personnel)
app.register_blueprint(equipments)
app.register_blueprint(fieldtrips)
app.register_blueprint(notices)
app.register_blueprint(calendar)
app.register_blueprint(news)
app.register_blueprint(file_transfer)
