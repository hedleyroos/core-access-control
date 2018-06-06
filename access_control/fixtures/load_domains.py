# Domain hierarchy based on:
# https://praekelt.atlassian.net/wiki/spaces/GEM/pages/215515423/Roles+Permissions+Guidelines?preview=/55574535/118751390/Domain%20Hierarchy%20(5).png
from access_control.fixtures import ROLES

ROLES_SANS_TECH_ADMIN = [role for role in ROLES if role != "tech_admin"]

DOMAIN_HIERARCHY = [
    {
        "name": "girl_effect_organisation",
        "description": "The top level of the organisation",
        "roles": ["tech_admin"],
        "sites": [
            {
                "name": "ge_corporate",
                "description": "GE Corporate Site",
                "roles": ROLES_SANS_TECH_ADMIN
            },
            {
                "name": "girl_connect",
                "description": "Girl Connect",
                "roles": ROLES_SANS_TECH_ADMIN
            },
            {
                "name": "gmp",
                "description": "Global Management Portal",
                "roles": ROLES_SANS_TECH_ADMIN
            },
            {
                "name": "impact_dash",
                "description": "Impact Dashboard",
                "roles": ROLES_SANS_TECH_ADMIN
            },
            {
                "name": "event_log",
                "description": "Event Log",
                "roles": ROLES_SANS_TECH_ADMIN
            }
        ],
        "subdomains": [
            {
                "name": "springster",
                "description": "springster",
                "roles": ROLES_SANS_TECH_ADMIN,
                "subdomains": [
                    {
                        "name": "a_markets",
                        "description": "A Markets",
                        "roles": ROLES_SANS_TECH_ADMIN,
                        "sites": [
                            {
                                "name": "philippines",
                                "description": "Philippines",
                                "roles": ROLES_SANS_TECH_ADMIN
                            },
                            {
                                "name": "south_africa",
                                "description": "South Africa",
                                "roles": ROLES_SANS_TECH_ADMIN
                            },
                            {
                                "name": "nigeria",
                                "description": "Nigeria",
                                "roles": ROLES_SANS_TECH_ADMIN
                            }
                        ]
                    },
                    {
                        "name": "c_markets",
                        "description": "C Markets",
                        "roles": ROLES_SANS_TECH_ADMIN,
                        "sites": [
                            {
                                "name": "algeria",
                                "description": "Algeria",
                                "roles": ROLES_SANS_TECH_ADMIN
                            },
                            {
                                "name": "angola",
                                "description": "Angola",
                                "roles": ROLES_SANS_TECH_ADMIN
                            },
                            {
                                "name": "benin",
                                "description": "Benin",
                                "roles": ROLES_SANS_TECH_ADMIN
                            },
                            {
                                "name": "cape_verde",
                                "description": "Cape Verde",
                                "roles": ROLES_SANS_TECH_ADMIN
                            },
                            {
                                "name": "chad",
                                "description": "Chad",
                                "roles": ROLES_SANS_TECH_ADMIN
                            },
                            {
                                "name": "congo",
                                "description": "DRC",
                                "roles": ROLES_SANS_TECH_ADMIN
                            },
                            {
                                "name": "gabon",
                                "description": "Gabon",
                                "roles": ROLES_SANS_TECH_ADMIN
                            },
                            {
                                "name": "ghana",
                                "description": "Ghana",
                                "roles": ROLES_SANS_TECH_ADMIN
                            },
                            {
                                "name": "guinea",
                                "description": "Guinea",
                                "roles": ROLES_SANS_TECH_ADMIN
                            },
                        ]
                    }
                ]
            },
            {
                "name": "tega",
                "description": "TEGA",
                "sites": [
                    {
                        "name": "tega_nigeria",
                        "description": "Nigeria"
                    },
                    {
                        "name": "tega_malawi",
                        "description": "Malawi"
                    },
                    {
                        "name": "tega_rwanda",
                        "description": "Rwanda"
                    },
                    {
                        "name": "tega_idia",
                        "description": "India"
                    },
                    {
                        "name": "tega_usa",
                        "description": "United States of America"
                    },
                    {
                        "name": "tega_bangladesh",
                        "description": "bangladesh"
                    },
                ]
            },
            {
                "name": "yegna",
                "description": "YEGNA",
                "sites": [
                    {
                        "name": "yegna_ethiopia",
                        "description": "Ethiopia"
                    }
                ]
            },
            {
                "name": "zathu",
                "description": "ZATHU",
                "sites": [
                    {
                        "name": "zathu_malawi",
                        "description": "Malawi"
                    }
                ]
            },
            {
                "name": "india",
                "description": "India (Brand TBC)",
                "sites": [
                    {
                        "name": "india_india",
                        "description": "India"
                    }
                ]
            },
            {
                "name": "ni_nyampinga",
                "description": "NI NYAMPINGA",
                "sites": [
                    {
                        "name": "ni_nyampinga_rwanda",
                        "description": "Rwanda"
                    }
                ]
            }
        ]
    }
]
