# TODO: Rename file to something more appropriate
import sys
from flask import Flask
from sqlalchemy import inspect
from sqlalchemy.sql import ClauseElement

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
        self.load_domain("Girl Effect Organisation", DOMAIN_HIERARCHY, None)

    def get_or_create(self, model, **kwargs):
        instance = DB.session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            DB.session.add(instance)
            DB.session.commit()
            return instance

    def load_resources(self):
        print("Loading resources...")
        for resource in RESOURCES:
            instance = self.get_or_create(Resource, urn=resource)
            print("Resource %s loaded..." % instance.urn)
        print("Done")

    def load_permissions(self):
        print("Loading permissions...")
        for permission in PERMISSIONS:
            instance = self.get_or_create(Permission, name=permission)
            print("Permission %s loaded..." % instance.name)
        print("Done")

    def load_roles(self):
        print("Loading roles...")
        for role in ROLES:
            instance = self.get_or_create(Role, label=role)
            print("Role %s loaded..." % instance.label)
        print("Done")

    def load_domain(self, name: str, detail: dict, parent: Domain):
        print("Loading domain %s..." % name)
        domain = self.get_or_create(
            Domain, name=name,
            description=detail["description"],
            parent_id=parent
        )

        subdomains = detail.get("subdomains", {})
        for _name, _detail in subdomains.items():
            self.load_domain(_name, _detail, domain.id)

        roles = detail.get("roles", {})
        for label, defaults in roles.items():
            role = Role.query.filter_by(label=label).first_or_404()
            domain_role = self.get_or_create(DomainRole, domain=domain, role=role, defaults=defaults)

        print("Done")


loader = SeedDataLoader()
if len(sys.argv) == 2:
    seed = sys.argv[1]
    func = getattr(loader, "load_%s" % seed)
    if seed == "domain":
        func("Girl Effect Organisation", DOMAIN_HIERARCHY, None)
    else:
        func()
else:
    loader.all()
