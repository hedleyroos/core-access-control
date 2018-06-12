Changelog
=========

1.2.1
-----
Fixed bug in `/ops/get_sites_for_domain/{domain_id}` API call which resulted in the site ID that was returned actually being the domain_id value.

1.2.0
-----
Added `/ops/get_sites_for_domain/{domain_id}` API call.

1.1.2
-----
1. Seed data updated.
2. Added helper scripts to bootstrap the Management Portal and a user with the `tech_admin` role.

1.1.1
-----
Reworked healthcheck end-point to not use pkg_resources.

1.1.0
-----
Added healthcheck end-point

1.0.0
-----
Initial release
