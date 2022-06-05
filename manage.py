
# flask_script is not working with flask 2. This not working
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from src.app import app
from src.db import sqlAlchemydb as db

app = app
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
