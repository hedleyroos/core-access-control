from flask import Flask

from ge_core_shared.db_actions import get_or_create
from access_control.fixtures.load_domains import DOMAIN_HIERARCHY
from access_control.fixtures.load_permissions import PERMISSIONS
from access_control.fixtures.load_resources import RESOURCES
from access_control.fixtures.load_roles import ROLES
from access_control.models import DB, Resource, Permission, Role, Domain, \
    DomainRole

app = Flask(__name__)


class SeedDataLoader:

    def all(self):
        self.load_resources()
        self.load_permissions()
        self.load_roles()
        self.load_domain(DOMAIN_HIERARCHY, None)
        print("Done")

    def load_resources(self):
        print("Loading resources...")
        for resource in RESOURCES:
            instance, created = get_or_create(Resource, urn=resource)
            print("Resource %s loaded..." % instance.urn)
        print("Done")

    def load_permissions(self):
        print("Loading permissions...")
        for permission in PERMISSIONS:
            instance, created = get_or_create(Permission, name=permission)
            print("Permission %s loaded..." % instance.name)
        print("Done")

    def load_roles(self):
        print("Loading roles...")
        for role in ROLES:
            instance, created = get_or_create(Role, label=role)
            print("Role %s loaded..." % instance.label)
        print("Done")

    def load_domain(self, detail: dict, parent: Domain):
        for item in detail:
            print("Domain %s as child of %s loaded..." % (
                item.get("name"),
                parent.name if parent else None
            ))
            domain, created = get_or_create(
                Domain, name=item.get("name"),
                description=item.get("description"),
                parent_id=parent.id if parent else None
            )

            roles = item.get("roles", [])
            for label in roles:
                role = Role.query.filter_by(label=label).first()
                domain_role, created = get_or_create(
                    DomainRole, domain_id=domain.id, role_id=role.id)

            subdomains = item.get("subdomains", {})
            if subdomains:
                self.load_domain(subdomains, domain)


loader = SeedDataLoader()
loader.all()
