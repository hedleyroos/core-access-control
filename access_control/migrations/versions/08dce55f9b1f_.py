"""empty message

Revision ID: 08dce55f9b1f
Revises: a5e2677741fd
Create Date: 2018-08-08 13:27:44.810620

"""
import datetime
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session

from access_control.models import Domain, Invitation, \
    Permission, Resource, Role, Site

# revision identifiers, used by Alembic.
revision = '08dce55f9b1f'
down_revision = 'a5e2677741fd'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    now = "'{}'".format(datetime.datetime.now().isoformat())
    empty_uuid = "'{}'".format("00000000-0000-0000-0000-000000000000")
    empty_name = "'No one'"
    empty_description = "'No Description'"
    # EDITED MIGRATION: Updates on existing fields where null are populated.
    sql = "UPDATE {table} SET {column} = {value} WHERE {column} IS NULL;"
    session.execute(sql.format(table="domain", column="created_at", value=now))
    session.execute(sql.format(table="domain", column="description", value=empty_description))
    # cobusc: Removed model instances that were being created as it breaks when new
    # columns are added in later migrations.
    # domains = session.query(Domain).filter(Domain.name.is_(None)).all()
    # for domain in domains:
    #     domain.name = str(uuid.uuid4())[:30]
    session.execute(sql.format(table="domain", column="updated_at", value=now))
    session.execute(sql.format(table="domain_role", column="created_at", value=now))
    session.execute(sql.format(table="domain_role", column="grant_implicitly", value="false"))
    session.execute(sql.format(table="domain_role", column="updated_at", value=now))
    session.execute(sql.format(table="invitation", column="created_at", value=now))
    # cobusc: Removed model instances that were being created as it breaks when new
    # columns are added in later migrations.
    # invitations = session.query(Invitation).filter(Invitation.email.is_(None)).all()
    # for invitation in invitations:
    #     invitation.email = "placeholder@{uuid}.com".format(uuid=str(uuid.uuid4()))
    session.execute(sql.format(table="invitation", column="first_name", value=empty_name))
    session.execute(sql.format(table="invitation", column="invitor_id", value=empty_uuid))
    session.execute(sql.format(table="invitation", column="last_name", value=empty_name))
    session.execute(sql.format(table="invitation", column="organisation_id", value="-1"))
    session.execute(sql.format(table="invitation", column="updated_at", value=now))
    session.execute(sql.format(table="invitation_domain_role", column="created_at", value=now))
    session.execute(sql.format(table="invitation_domain_role", column="updated_at", value=now))
    session.execute(sql.format(table="invitation_site_role", column="created_at", value=now))
    session.execute(sql.format(table="invitation_site_role", column="updated_at", value=now))
    session.execute(sql.format(table="permission", column="created_at", value=now))
    session.execute(sql.format(table="permission", column="description", value=empty_description))
    # cobusc: Removed model instances that were being created as it breaks when new
    # columns are added in later migrations.
    # permissions = session.query(Permission).filter(Permission.name.is_(None)).all()
    # for permission in permissions:
    #     permission.name = str(uuid.uuid4())[:30]
    session.execute(sql.format(table="permission", column="updated_at", value=now))
    session.execute(sql.format(table="resource", column="created_at", value=now))
    session.execute(sql.format(table="resource", column="description", value=empty_description))
    session.execute(sql.format(table="resource", column="updated_at", value=now))
    # cobusc: Removed model instances that were being created as it breaks when new
    # columns are added in later migrations.
    # resources = session.query(Resource).filter(Resource.urn.is_(None)).all()
    # for resource in resources:
    #     resource.urn = str(uuid.uuid4())
    session.execute(sql.format(table="role", column="created_at", value=now))
    session.execute(sql.format(table="role", column="description", value=empty_description))
    # cobusc: Removed model instances that were being created as it breaks when new
    # columns are added in later migrations.
    # roles = session.query(Role).filter(Role.label.is_(None)).all()
    # for role in roles:
    #     role.label = str(uuid.uuid4())[:30]
    session.execute(sql.format(table="role", column="requires_2fa", value="false"))
    session.execute(sql.format(table="role", column="updated_at", value=now))
    session.execute(sql.format(table="role_resource_permission", column="created_at", value=now))
    session.execute(sql.format(table="role_resource_permission", column="updated_at", value=now))
    session.execute(sql.format(table="site", column="created_at", value=now))
    session.execute(sql.format(table="site", column="description", value=empty_description))
    # All sites without a domain_id should be set to the parent domain and can be manually corrected.
    # cobusc: Removed model instances that were being created as it breaks when new
    # columns are added in later migrations.
    # sites = session.query(Site).filter(Site.name.is_(None)).all()
    # if sites:
    #     parent_domain = session.query(Domain).filter(Domain.parent_id.is_(None)).first()
    #     if not parent_domain:
    #         parent_domain = session.query(Domain).first()
    #         # If there are sites and no domains, make a dud domain, to be removed when the
    #         if not parent_domain:
    #             parent_domain = Domain(
    #                 name="Placeholder",
    #                 description="A placeholder for sites that had no domain."
    #                             "Please move the sites under this domain then remove this domain."
    #             )
    #             session.add(parent_domain)
    #             session.commit()
    #     domain_id = parent_domain.id
    #     session.execute(sql.format(
    #         table="site", column="domain_id", value="{domain_id}".format(domain_id=domain_id)))
    #     session.execute(sql.format(table="site", column="is_active", value="false"))
    #
    #     for site in sites:
    #         site.name = str(uuid.uuid4())[:30]
    #     session.execute(sql.format(table="site", column="updated_at", value=now))
    session.execute(sql.format(table="site_role", column="created_at", value=now))
    session.execute(sql.format(table="site_role", column="grant_implicitly", value="false"))
    session.execute(sql.format(table="site_role", column="updated_at", value=now))
    session.execute(sql.format(table="user_domain_role", column="created_at", value=now))
    session.execute(sql.format(table="user_domain_role", column="updated_at", value=now))
    session.execute(sql.format(table="user_site_role", column="created_at", value=now))
    session.execute(sql.format(table="user_site_role", column="updated_at", value=now))

    session.commit()
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('domain', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('domain', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('domain', 'name',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.alter_column('domain', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('domain_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('domain_role', 'grant_implicitly',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('domain_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('invitation', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('invitation', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('invitation', 'first_name',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('invitation', 'invitor_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('invitation', 'last_name',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('invitation', 'organisation_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('invitation', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('invitation_domain_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('invitation_domain_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('invitation_site_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('invitation_site_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('permission', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('permission', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('permission', 'name',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.alter_column('permission', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('resource', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('resource', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('resource', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('resource', 'urn',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.alter_column('role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('role', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('role', 'label',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.alter_column('role', 'requires_2fa',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('role_resource_permission', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('role_resource_permission', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('site', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('site', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('site', 'domain_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('site', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('site', 'name',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.alter_column('site', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('site_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('site_role', 'grant_implicitly',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('site_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('user_domain_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('user_domain_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('user_site_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('user_site_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_site_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('user_site_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('user_domain_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('user_domain_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('site_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('site_role', 'grant_implicitly',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('site_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('site', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('site', 'name',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    op.alter_column('site', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('site', 'domain_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('site', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('site', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('role_resource_permission', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('role_resource_permission', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('role', 'requires_2fa',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('role', 'label',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    op.alter_column('role', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('resource', 'urn',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('resource', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('resource', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('resource', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('permission', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('permission', 'name',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    op.alter_column('permission', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('permission', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('invitation_site_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('invitation_site_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('invitation_domain_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('invitation_domain_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('invitation', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('invitation', 'organisation_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('invitation', 'last_name',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('invitation', 'invitor_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('invitation', 'first_name',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('invitation', 'email',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('invitation', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('domain_role', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('domain_role', 'grant_implicitly',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('domain_role', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('domain', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('domain', 'name',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    op.alter_column('domain', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('domain', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
