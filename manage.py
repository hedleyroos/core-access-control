# All the imports and setup for migrations. flask_script allows for other
# management commands to be run or integrated.
if __name__ == "__main__":
    import os

    from flask import Flask
    from flask_migrate import Migrate, MigrateCommand
    from flask_sqlalchemy import SQLAlchemy
    from flask_script import Manager

    import project.app
    from access_control import models


    APP = project.app.APP
    MIGRATE = Migrate(project.app.APP, project.app.DB)

    manager = Manager(APP)
    manager.add_command("db", MigrateCommand)

    manager.run()
