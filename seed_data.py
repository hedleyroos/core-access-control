# TODO: Rename file to something more appropriate
import sys
from flask import Flask
from flask_sqlalchemy import model
from sqlalchemy.exc import IntegrityError

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

    def update_or_create(self, instance, filter_field):
        try:
            DB.session.add(instance)
            DB.session.commit()
            if isinstance(instance, Domain):
                print("%s domain created as a child of %s" % (instance.name, instance.parent_id))
            print("%s %s created..." % (
                instance.__class__.__name__, getattr(instance, filter_field)))
        except IntegrityError:
            print("%s already exists!!" % instance)

    def load_resources(self):
        print("Loading resources...")
        for resource in RESOURCES:
            instance = Resource(urn=resource)
            self.update_or_create(instance, "urn")
        print("Done")

    def load_permissions(self):
        print("Loading permissions...")
        for permission in PERMISSIONS:
            instance = Permission(name=permission)
            self.update_or_create(instance, "name")
        print("Done")

    def load_roles(self):
        print("Loading roles...")
        for role in ROLES:
            instance = Role(label=role)
            self.update_or_create(instance, "label")
        print("Done")

    def load_domain(self, name: str, detail: dict, parent: Domain):
        print("Loading domain %s..." % name)
        domain = Domain(
            name=name, description=detail["description"], parent_id=parent
        )
        self.update_or_create(domain, "name")

        subdomains = detail.get("subdomains", {})
        for _name, _detail in subdomains.items():
            self.load_domain(_name, _detail, domain.id)

        roles = detail.get("roles", {})
        for label, defaults in roles.items():
            role = Role.query.filter_by(label=label).first_or_404()
            domain_role = DomainRole(
                domain=domain, role=role, defaults=defaults)
            self.update_or_create(domain_role, "domain")

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
