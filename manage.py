# All the imports and setup for migrations. flask_script allows for other
# management commands to be run or integrated.
if __name__ == "__main__":
    from flask_migrate import Migrate, MigrateCommand
    from flask_script import Manager

    import project.app
    # We _have_ to import models here. If not, the migrations will
    # think that all tables have been dropped.
    import access_control.models  # Do not remove

    APP = project.app.APP
    MIGRATE = Migrate(project.app.APP, project.app.DB)

    manager = Manager(APP)
    manager.add_command("db", MigrateCommand)

    manager.run()
