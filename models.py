import datetime
import os

from flask import Flask

from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

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
    name = DB.Column(DB.String(30), unique=True, index=True)
    description = DB.Column(DB.Text)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return self.name


class Site(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    domain_id = DB.Column(DB.Integer, DB.ForeignKey("domain.id"), index=True)
    description = DB.Column(DB.Text)
    client_id = DB.Column(DB.Integer, unique=True, index=True)
    is_active = DB.Column(DB.Boolean(), default=True)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "%s-%s-%s" % (self.client_id, self.is_active, self.domain_id)


class DomainRole(DB.Model):
    __table_args__ = (
        DB.ForeignKeyConstraint(
            [domain_id, role_id],
            [Domain.id, Role.id]
        ), {}
    )
    domain_id = DB.Column(DB.Integer, primary_key=True)
    role_id = DB.Column(DB.Integer, primary_key=True)
    grant_implicitly = DB.Column(DB.Boolean(), default=False)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "%s-%s-%s" % (
            self.domain_id, self.role_id, self.grant_implicitly
        )


class Role(DB.Model):
    role = DB.relationship("Role", backref="role", lazy=True)
    id = DB.Column(DB.Integer, primary_key=True)
    label = DB.Column(DB.String(30), unique=True, index=True)
    description = DB.Column(DB.Text)
    requires_2fa = DB.Column(DB.Boolean())
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return "%s-%s" % (self.label, self.requires_2fa)


class Permission(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.Text, unique=True)
    description = DB.Column(DB.Text)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return self.name


class Resource(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    urn = DB.Column(DB.String(100), unique=True, index=True)
    description = DB.Column(DB.Text)
    created_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow())
    updated_at = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return self.urn
