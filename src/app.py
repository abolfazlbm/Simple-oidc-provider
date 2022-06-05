import os

from dotenv import load_dotenv
from flask import Flask, Blueprint
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import app_config
from src import db
from src.errors import init_error_handeler
from src.resources.auth.auth import Auth
# from app.resources.datastore.mongodb import Mongodb
from src.routes import v1, pages
from src.utils.ma import ma

app = Flask(__name__, template_folder="templates")
load_dotenv(".env", verbose=True)
app.config.from_object(app_config[os.environ.get("APP_CONFIG", "production")])

Auth(app)
csrf = CSRFProtect(app)

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
    # prune_database()
    pass


# Api Blueprint
for blueprint in vars(v1).values():
    if isinstance(blueprint, Blueprint):
        app.register_blueprint(blueprint, url_prefix="/api/v1")
        csrf.exempt(blueprint)
        print(blueprint.name)

# Pages Blueprint
app.register_blueprint(pages.PAGES_BLUEPRINT, url_prefix="/")
