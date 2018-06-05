import sys
from flask import Flask

from ge_core_shared.db_actions import get_or_create, read_entry
from access_control.fixtures.load_domains import DOMAIN_HIERARCHY
from access_control.fixtures.load_permissions import PERMISSIONS
from access_control.fixtures.load_resources import RESOURCES
from access_control.fixtures.load_roles import ROLES
from access_control.fixtures.load_role_resource_permissions import ROLE_RESOURCE_PERMISSIONS
from access_control.models import Resource, Permission, Role, Domain, \
    DomainRole, RoleResourcePermission, Site


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
        description="The top level of the organisation",
        parent_id=None
    )

    site, created = get_or_create(
        Site, name="Management Portal",
        description="The Management Portal",
        client_id=client_id,
        domain_id=domain.id
    )

    print("Done")
