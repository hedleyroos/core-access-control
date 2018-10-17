Changelog
=========

next
----
- Update authentication middleware implementation.

1.3.0
-----
- Added model, migration, definitions, etc. for invitation redirect URLs.

1.2.6
-----
- Updated version of core-shared library and modified all usages of the `get_or_create()` function to use the new `defaults` argument.

1.2.5
-----
- Updated documentation
- Use new version of core_shared library and decorate unit tests accordingly.

1.2.4
-----
- Exception handler status code and message updates.

1.2.3
-----
- Added metrics endpoint along with middleware and controller decorators.
- Process number set to 1, thread number set to 4.

1.2.2
-----
#. Update models to use organisation instead of is_system_user flag
#. Created invite related tables.
#. Added API CRUD endpoints and functionality for invites.
#. Added invite redeem endpoint and functionality.
#. Added expired invite purge endpoint and functionality.
#. Resource list updates to include `urn:ge:identity_provider:organisation`
#. Files renamed
    - access_control/fixtures/load_domains.py → access_control/fixtures/domains.py
    - access_control/fixtures/load_permissions.py → access_control/fixtures/permissions.py
    - access_control/fixtures/load_resources.py → access_control/fixtures/resources.py
    - access_control/fixtures/load_role_resource_permissions.py → access_control/fixtures/role_resource_permissions.py
    - access_control/fixtures/load_roles.py → access_control/fixtures/roles.py
#. Update Sentry config

1.2.1
-----
- Fixed bug in `/ops/get_sites_for_domain/{domain_id}` API call which resulted in the site ID that was returned actually being the domain_id value.

1.2.0
-----
- Added `/ops/get_sites_for_domain/{domain_id}` API call.

1.1.2
-----
#. Seed data updated.
#. Added helper scripts to bootstrap the Management Portal and a user with the `tech_admin` role.

1.1.1
-----
- Reworked healthcheck end-point to not use pkg_resources.

1.1.0
-----
- Added healthcheck end-point

1.0.0
-----
- Initial release

