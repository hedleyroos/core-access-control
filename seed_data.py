from flask import Flask

from ge_core_shared.db_actions import get_or_create, read_entry
from access_control.fixtures.domains import DOMAIN_HIERARCHY
from access_control.fixtures.permissions import PERMISSIONS
from access_control.fixtures.resources import RESOURCES
from access_control.fixtures.roles import ROLES
from access_control.fixtures.role_resource_permissions import ROLE_RESOURCE_PERMISSIONS
from access_control.models import Resource, Permission, Role, Domain, \
    DomainRole, RoleResourcePermission, Site, SiteRole

app = Flask(__name__)


class SeedDataLoader:

    def all(self):
        self.load_resources()
        self.load_permissions()
        self.load_roles()
        # Role resource permissions can only be loaded after roles,
        # resources and permissions have been loaded.
        self.load_role_resource_permissions()
        self.load_domain(DOMAIN_HIERARCHY)
        print("Done")

    @staticmethod
    def load_resources():
        print("Loading resources...")
        for resource in RESOURCES:
            instance, created = get_or_create(Resource, urn=resource,
                                              defaults={"description": ""})
            print("Resource %s loaded..." % instance.urn)
        print("Done")

    @staticmethod
    def load_permissions():
        print("Loading permissions...")
        for permission in PERMISSIONS:
            instance, created = get_or_create(Permission, name=permission,
                                              defaults={"description": ""})
            print("Permission %s loaded..." % instance.name)
        print("Done")

    @staticmethod
    def load_roles():
        print("Loading roles...")
        for role in ROLES:
            instance, created = get_or_create(Role, label=role,
                                              defaults={"description": ""})
            print("Role %s loaded..." % instance.label)
        print("Done")

    def load_domain(self, detail: dict, parent: Domain=None):
        for item in detail:
            print("Domain %s as child of %s loaded..." % (
                item.get("name"),
                parent.name if parent else None
            ))
            domain, created = get_or_create(
                Domain, name=item.get("name"),
                defaults={
                    "description": item.get("description") or "",
                    "parent_id": parent.id if parent else None
                }
            )

            roles = item.get("roles", [])
            for label in roles:
                role = Role.query.filter_by(label=label).first()
                domain_role, created = get_or_create(
                    DomainRole, domain_id=domain.id, role_id=role.id)

            subdomains = item.get("subdomains", {})
            if subdomains:
                self.load_domain(subdomains, domain)
            sites = item.get("sites", {})
            if sites:
                self.load_sites(sites, domain)

    @staticmethod
    def load_sites(sites_to_create: dict, domain: Domain=None):
        for site_to_create in sites_to_create:
            print("Site %s as child of Domain %s loaded..." % (
                site_to_create["name"],
                domain.name if domain else None
            ))
            site, created = get_or_create(
                Site, name=site_to_create["name"],
                defaults={
                    "description": site_to_create["description"] or "",
                    "domain_id": domain.id if domain else None
                }
            )
            roles = site_to_create.get("roles", [])
            for label in roles:
                role = Role.query.filter_by(label=label).first()
                site_role, created = get_or_create(
                    SiteRole, site_id=site.id, role_id=role.id
                )

    @staticmethod
    def load_role_resource_permissions():
        print("Loading role resource permissions...")
        for role_label, resource_permissions in ROLE_RESOURCE_PERMISSIONS.items():
            print(f"Role: {role_label}")
            role = read_entry(Role, query={"label": role_label})
            for resource_urn, permission_name in resource_permissions:
                print(f"* {resource_urn} ({permission_name})")
                resource = read_entry(Resource, query={"urn": resource_urn})
                permission = read_entry(Permission, query={"name": permission_name})
                get_or_create(RoleResourcePermission, role_id=role.id, resource_id=resource.id,
                              permission_id=permission.id)
        print("Done.")


loader = SeedDataLoader()
loader.all()
