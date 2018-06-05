import sys
import uuid
from flask import Flask

from ge_core_shared.db_actions import get_or_create
from access_control.models import Role, Domain, DomainRole, UserDomainRole


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} user_uuid")
        exit()

    try:
        user_uuid = uuid.UUID(sys.argv[1])
    except ValueError:
        print("user_uuid must be a UUID")
        exit()

    app = Flask(__name__)

    domain, created = get_or_create(
        Domain, name="girl_effect_organisation",
        description="The top level of the organisation",
        parent_id=None
    )

    role, created = get_or_create(
        Role, label="tech_admin",
        description="The tech admin role",
        requires_2fa=True
    )

    domainrole, created = get_or_create(
        DomainRole,
        domain_id=domain.id,
        role_id=role.id,
    )

    userdomainrole, created = get_or_create(
        UserDomainRole,
        domain_id=domain.id,
        role_id=role.id,
        user_id=str(user_uuid)
    )

    print("Done")
