# All the imports and setup for migrations. flask_script allows for other
# management commands to be run or integrated.
if __name__ == "__main__":
    import os
    import logging

    from raven.contrib.flask import Sentry
    from flask_migrate import Migrate, MigrateCommand
    from flask_script import Manager

    import project.app
    # Do not import settings, as it requires the API config which we do not
    # want to specify when running migrations.

    APP = project.app.APP
    MIGRATE = Migrate(project.app.APP, project.app.DB)
    SENTRY = Sentry(dsn=os.environ.get("SENTRY_DSN"))
    SENTRY.init_app(APP, level=os.environ.get("SENTRY_LOG_LEVEL", logging.ERROR))

    manager = Manager(APP)
    manager.add_command("db", MigrateCommand)

    manager.run()
