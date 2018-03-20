import uuid

from flask_migrate import Migrate
from sqlalchemy import types
from sqlalchemy.dialects.postgresql import UUID, CHAR
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import TypeDecorator

import project.app
from project import settings

DB = project.app.DB
MIGRATE = Migrate(project.app.APP, DB)

# func.utc_timestamp() it is only supported by MySQL out of the box.
# http://docs.sqlalchemy.org/en/latest/core/compiler.html#utc-timestamp-function
class utcnow(expression.FunctionElement):
    type = types.DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


# Copied wholesale from SQLAlchemy docs.
# http://docs.sqlalchemy.org/en/latest/core/custom_types.html?highlight=guid#backend-agnostic-guid-type
class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = UUID

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class Domain(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    parent_id = DB.Column(DB.Integer, DB.ForeignKey("domain.id"), nullable=True)
    name = DB.Column(DB.VARCHAR(30), unique=True, index=True)
    description = DB.Column(DB.Text)
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

    def __repr__(self):
        return "<Domain(%s)>" % self.name


class Role(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    label = DB.Column(DB.VARCHAR(30), unique=True, index=True)
    description = DB.Column(DB.Text)
    requires_2fa = DB.Column(DB.Boolean, default=True)
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

    def __repr__(self):
        return "<Role(%s-%s)>" % (self.label, self.requires_2fa)


class Permission(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.VARCHAR(30), unique=True, index=True)
    description = DB.Column(DB.Text)
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

    def __repr__(self):
        return "<Permission(%s)>" % self.name


class Resource(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    urn = DB.Column(DB.VARCHAR(100), unique=True, index=True)
    description = DB.Column(DB.Text)
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

    def __repr__(self):
        return "<Resource(%s)>" % self.urn


class RoleResourcePermission(DB.Model):
    role_id = DB.Column(DB.Integer, DB.ForeignKey("role.id"), primary_key=True)
    resource_id = DB.Column(
        DB.Integer, DB.ForeignKey("resource.id"), primary_key=True
    )
    permission_id = DB.Column(
        DB.Integer, DB.ForeignKey("permission.id"), primary_key=True
    )
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

    def __repr__(self):
        return "<RoleResourcePermission(%s-%s-%s)>" % (
            self.role_id, self.resource_id, self.permission_id
        )


class Site(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.VARCHAR(30), unique=True, index=True)
    domain_id = DB.Column(DB.Integer, DB.ForeignKey("domain.id"), index=True)
    description = DB.Column(DB.Text)
    client_id = DB.Column(DB.VARCHAR(255), unique=True, index=True)
    is_active = DB.Column(DB.Boolean, default=True)
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

    def __repr__(self):
        return "<Site(%s-%s-%s-%s)>" % (
            self.name, self.client_id, self.is_active, self.domain_id
        )


class DomainRole(DB.Model):
    domain_id = DB.Column(
        DB.Integer, DB.ForeignKey("domain.id"), primary_key=True
    )
    role_id = DB.Column(
        DB.Integer, DB.ForeignKey("role.id"), primary_key=True
    )
    grant_implicitly = DB.Column(DB.Boolean, default=False)
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

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
    grant_implicitly = DB.Column(DB.Boolean, default=False)
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

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
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

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
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

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
    id = DB.Column(GUID(), default=uuid.uuid1, primary_key=True)
    first_name = DB.Column(DB.Text)
    last_name = DB.Column(DB.Text)
    email = DB.Column(DB.VARCHAR(100), unique=True, index=True)
    expires_at = DB.Column(DB.DateTime)
    invitor_id = DB.Column(UUID)
    is_system_user = DB.Column(DB.Boolean, default=False)
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

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
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

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
    created_at = DB.Column(DB.DateTime, default=utcnow())
    updated_at = DB.Column(
        DB.DateTime,
        default=utcnow(),
        onupdate=utcnow()
    )

    __table_args__ = (
        DB.ForeignKeyConstraint(
            [site_id, role_id],
            [SiteRole.site_id, SiteRole.role_id]
        ), {}
    )

    def __repr__(self):
        return "<InvitationSiteRole(%s-%s)>" % (self.domain_id, self.role_id)
