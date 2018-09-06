import sys
from flask import Flask

from ge_core_shared.db_actions import get_or_create
from access_control.models import Domain, Site


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} management_portal_client_id")
        exit()

    try:
        client_id = int(sys.argv[1])
    except ValueError:
        print("management_portal_client_id must be an integer")
        exit()

    app = Flask(__name__)

    domain, created = get_or_create(
        Domain, name="girl_effect_organisation",
        defaults={
            "description": "The top level of the organisation",
            "parent_id": None
        }
    )

    site, created = get_or_create(
        Site, name="Management Portal",
        defaults={
            "description": "The Management Portal",
            "client_id": client_id,
            "domain_id": domain.id
        }
    )

    print("Done")
