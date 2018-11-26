import datetime

from access_control import models


DB = models.DB


class SQLSiteLoader:
    """
    Class to help with testing data migration
    """

    def load(self):
        DB.session.execute(
            "INSERT INTO domain (id, name, description, created_at, updated_at)"
            f" VALUES ('1', 'ADomName', 'ADomDesc',"
            f" '{datetime.datetime(1970, 1, 1, 0, 0, 0).isoformat()}', '{datetime.datetime(1970, 1, 1, 0, 0, 0).isoformat()}');"
        )
        for index in range(1, 20):
            DB.session.execute(
                "INSERT INTO site (id, name, description, domain_id, is_active, created_at, updated_at)"
                f" VALUES ('{index}', 'Aname+{index}', 'ADesc+{index}', '1', 'false',"
                f" '{datetime.datetime(1970, 1, 1, 0, 0, 0).isoformat()}', '{datetime.datetime(1970, 1, 1, 0, 0, 0).isoformat()}');"
            )
        DB.session.commit()



loader = SQLSiteLoader()
loader.load()
