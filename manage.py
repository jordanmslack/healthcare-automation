from app import create_app, db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)


@manager.command
def createdb():
    db.create_all()


@manager.command
def dropdb():
    db.drop_all()


@manager.command
def resetdb():
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    manager.run()
