import os

from dotenv import load_dotenv
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_migrate import Migrate

from app import db
from app.errors import init_error_handeler
from app.resources.auth.auth import Auth
# from app.resources.datastore.mongodb import Mongodb
from app.routes import v1
from app.utils.ma import ma
from config import app_config

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object(app_config[os.environ.get("APP_CONFIG", "production")])

Auth(app)

db.sqlAlchemydb.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db.sqlAlchemydb)

# mongo = Mongodb(app)
init_error_handeler(app)
CORS(app, resources={r'/*': {'origins': '*'}})


app.app_context().push()


@app.before_first_request
def create_tables():
    # db.sqlAlchemydb.create_all()
    pass
    # StaffModel.calculate_credit_all()
    # prune_database()


for blueprint in vars(v1).values():
    if isinstance(blueprint, Blueprint):
        app.register_blueprint(blueprint, url_prefix="/api/v1")
        print(blueprint.name)
