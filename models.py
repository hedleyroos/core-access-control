import datetime
import os
import uuid

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

from settings import settings


APP = Flask(__name__)

# TODO Move to settings and make env driven.
APP.config["SQLALCHEMY_DATABASE_URI"] = "postgres+psycopg2://core-access-control:core-access-control@localhost:5432/core-access-control"
    #os.environ.get(
DB = SQLAlchemy(APP)
migrate = Migrate(APP, DB)


class Domain(DB.Model):
    domain = DB.relationship("Domain", backref="domain", lazy=True)
    id = DB.Column(DB.Integer, primary_key=True)
    parent_id = DB.Column(DB.Integer, DB.ForeignKey("domain.id"), nullable=True)
    name = DB.Column(DB.VARCHAR(30), unique=True, index=True)
    description = DB.Column(DB.Text)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "<Domain(%s)>" % self.name


class Role(DB.Model):
    role = DB.relationship("Role", backref="role", lazy=True)
    id = DB.Column(DB.Integer, primary_key=True)
    label = DB.Column(DB.VARCHAR(30), unique=True, index=True)
    description = DB.Column(DB.Text)
    requires_2fa = DB.Column(DB.Boolean())
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "<Role(%s-%s)>" % (self.label, self.requires_2fa)


class Permission(DB.Model):
    permission = DB.relationship("Permission", backref="permission", lazy=True)
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.Text, unique=True)
    description = DB.Column(DB.Text)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "<Permission(%s)>" % self.name


class Resource(DB.Model):
    resource = DB.relationship("Resource", backref="resource", lazy=True)
    id = DB.Column(DB.Integer, primary_key=True)
    urn = DB.Column(DB.VARCHAR(100), unique=True, index=True)
    description = DB.Column(DB.Text)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "<Resource(%s)>" % self.urn


class RoleResourcePermission(DB.Model):
    role_id = DB.Column(DB.Integer, DB.ForeignKey("role.id"), primary_key=True)
    permission_id = DB.Column(DB.Integer, DB.ForeignKey("permission.id"), primary_key=True)
    resource_id = DB.Column(DB.Integer, DB.ForeignKey("resource.id"), primary_key=True)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "<RoleResourcePermission(%s-%s-%s)>" % (
            self.role_id, self.resource_id, self.permission_id
        )


class Site(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    domain_id = DB.Column(DB.Integer, DB.ForeignKey("domain.id"), index=True)
    description = DB.Column(DB.Text)
    client_id = DB.Column(DB.Integer, unique=True, index=True)
    is_active = DB.Column(DB.Boolean(), default=True)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "<Site(%s-%s-%s)>" % (
            self.client_id, self.is_active, self.domain_id
        )


class DomainRole(DB.Model):
    domain_id = DB.Column(
        DB.Integer, DB.ForeignKey("domain.id"), primary_key=True
    )
    role_id = DB.Column(
        DB.Integer, DB.ForeignKey("role.id"), primary_key=True
    )
    grant_implicitly = DB.Column(DB.Boolean(), default=False)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "<DomainRole(%s-%s-%s)>" % (
            self.domain_id, self.role_id, self.grant_implicitly
        )


class SiteRole(DB.Model):
    site_id = DB.Column(
        DB.Integer, DB.ForeignKey("site.id"), primary_key=True
    )
    role_id = DB.Column(
        DB.Integer, DB.ForeignKey("role.id"), primary_key=True
    )
    grant_implicitly = DB.Column(DB.Boolean(), default=False)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "<SiteRole(%s-%s-%s)>" % (
            self.site_id, self.role_id, self.grant_implicitly
        )

class UserSiteRole(DB.Model):
    user_id = DB.Column(UUID, primary_key=True)
    site_id = DB.Column(
        DB.Integer, primary_key=True
    )
    role_id = DB.Column(
        DB.Integer, primary_key=True
    )
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    __table_args__ = (
        DB.ForeignKeyConstraint(
            [site_id, role_id],
            [SiteRole.site_id, SiteRole.role_id]
        ), {}
    )

    def __repr__(self):
        return "<UserSiteRole(%s-%s-%s)>" % (
            self.user_id, self.site_id, self.role_id
        )


class UserDomainRole(DB.Model):
    user_id = DB.Column(UUID, primary_key=True)
    domain_id = DB.Column(
        DB.Integer, primary_key=True
    )
    role_id = DB.Column(
        DB.Integer, primary_key=True
    )
    grant_implicitly = DB.Column(DB.Boolean(), default=False)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    __table_args__ = (
        DB.ForeignKeyConstraint(
            [domain_id, role_id],
            [DomainRole.domain_id, DomainRole.role_id]
        ), {}
    )

    def __repr__(self):
        return "<UserDomainRole(%s-%s-%s)>" % (
            self.user_id, self.domain_id, self.role_id
        )


class Invitation(DB.Model):
    id = DB.Column(UUID, default=uuid.uuid1(), primary_key=True)
    first_name = DB.Column(DB.Text)
    last_name = DB.Column(DB.Text)
    email = DB.Column(DB.VARCHAR(100), unique=True, index=True)
    expires_at = DB.Column(DB.DateTime)
    invitor_id = DB.Column(UUID, default=uuid.uuid1())
    is_system_user = DB.Column(DB.Boolean(), default=False)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "<Invitation(%s-%s)>" % (self.email, self.expires_at)


class InvitationDomainRole(DB.Model):
    invitation_id = DB.Column(
        UUID, DB.ForeignKey("invitation.id"), primary_key=True
    )
    domain_id = DB.Column(
        DB.Integer, primary_key=True
    )
    role_id = DB.Column(
        DB.Integer, primary_key=True
    )
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    __table_args__ = (
        DB.ForeignKeyConstraint(
            [domain_id, role_id],
            [DomainRole.domain_id, DomainRole.role_id]
        ), {}
    )

    def __repr__(self):
        return "<InvitationDomainRole(%s-%s)>" % (self.domain_id, self.role_id)


class InvitationSiteRole(DB.Model):
    invitation_id = DB.Column(
        UUID, DB.ForeignKey("invitation.id"), primary_key=True
    )
    site_id = DB.Column(
        DB.Integer, primary_key=True
    )
    role_id = DB.Column(
        DB.Integer, primary_key=True
    )
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    __table_args__ = (
        DB.ForeignKeyConstraint(
            [site_id, role_id],
            [SiteRole.site_id, SiteRole.role_id]
        ), {}
    )

    def __repr__(self):
        return "<InvitationSiteRole(%s-%s)>" % (self.domain_id, self.role_id)
