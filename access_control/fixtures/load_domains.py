# Domain hierarchy based on:
# https://praekelt.atlassian.net/wiki/spaces/GEM/pages/215515423/Roles+Permissions+Guidelines?preview=/55574535/118751390/Domain%20Hierarchy%20(5).png
ROLES = [
    "role_delegator",
    "governance_admin",
    "governance_viewer",
    "data_admin",
    "data_editor",
    "data_viewer",
    "content_admin",
    "content_editor",
    "content_viewer"
]

DOMAIN_HIERARCHY = [
    {
        "name": "girl_effect_organisation",
        "description": "The top level of the organisation",
        "roles": ["tech_admin"],
        "subdomains": [
            {
                "name": "springster",
                "description": "springster",
                "roles": ROLES,
                "subdomains": [
                    {
                        "name": "a_markets",
                        "description": "A Markets",
                        "roles": ROLES,
                        "subdomains": [
                            {
                                "name": "philippines",
                                "description": "Philippines",
                                "roles": ROLES
                            },
                            {
                                "name": "south_africa",
                                "description": "South Africa",
                                "roles": ROLES
                            },
                            {
                                "name": "nigeria",
                                "description": "Nigeria",
                                "roles": ROLES
                            }
                        ]
                    },
                    {
                        "name": "c_markets",
                        "description": "C Markets",
                        "roles": ROLES,
                        "subdomains": [
                            {
                                "name": "algeria",
                                "description": "Algeria",
                                "roles": ROLES
                            },
                            {
                                "name": "angola",
                                "description": "Angola",
                                "roles": ROLES
                            },
                            {
                                "name": "benin",
                                "description": "Benin",
                                "roles": ROLES
                            },
                            {
                                "name": "cape_verde",
                                "description": "Cape Verde",
                                "roles": ROLES
                            },
                            {
                                "name": "chad",
                                "description": "Chad",
                                "roles": ROLES
                            },
                            {
                                "name": "congo",
                                "description": "DRC",
                                "roles": ROLES
                            },
                            {
                                "name": "gabon",
                                "description": "Gabon",
                                "roles": ROLES
                            },
                            {
                                "name": "ghana",
                                "description": "Ghana",
                                "roles": ROLES
                            },
                            {
                                "name": "guinea",
                                "description": "Guinea",
                                "roles": ROLES
                            },
                        ]
                    }
                ]
            },
            {
                "name": "ge_corporate",
                "description": "GE Corporate Site"
            },
            {
                "name": "tega",
                "description": "TEGA",
                "subdomains": [
                    {
                        "name": "tega_nigeria",
                        "Description": "Nigeria"
                    },
                    {
                        "name": "tega_malawi",
                        "Description": "Malawi"
                    },
                    {
                        "name": "tega_rwanda",
                        "Description": "Rwanda"
                    },
                    {
                        "name": "tega_idia",
                        "Description": "India"
                    },
                    {
                        "name": "tega_usa",
                        "Description": "United States of America"
                    },
                    {
                        "name": "tega_bangladesh",
                        "Description": "bangladesh"
                    },
                ]
            },
            {
                "name": "girl_connect",
                "description": "Girl Connect"
            },
            {
                "name": "yegna",
                "description": "YEGNA",
                "subdomains": [
                    {
                        "name": "yegna_ethiopia",
                        "description": "Ethiopia"
                    }
                ]
            },
            {
                "name": "zathu",
                "description": "ZATHU",
                "subdomains": [
                    {
                        "name": "zathu_malawi",
                        "description": "Malawi"
                    }
                ]
            },
            {
                "name": "india",
                "description": "India (Brand TBC)",
                "subdomains": [
                    {
                        "name": "india_india",
                        "description": "India"
                    }
                ]
            },
            {
                "name": "ni_nyampinga",
                "description": "NI NYAMPINGA",
                "subdomains": [
                    {
                        "name": "ni_nyampinga_rwanda",
                        "description": "Rwanda"
                    }
                ]
            },
            {
                "name": "gmp",
                "description": "Global Management Portal"
            },
            {
                "name": "impact_dash",
                "description": "Impact Dashboard"
            },
            {
                "name": "event_log",
                "description": "Event Log"
            }
        ]
    }
]
