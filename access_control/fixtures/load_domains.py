# Domain hierarchy based on:
# https://praekelt.atlassian.net/wiki/spaces/GEM/pages/215515423/Roles+Permissions+Guidelines?preview=/55574535/118751390/Domain%20Hierarchy%20(5).png
DOMAIN_HIERARCHY = [
    {
        "name": "girl_effect_organisation",
        "description": "The top level of the organisation",
        "roles": {},
        "subdomains": [
            {
                "name": "springster",
                "description": "springster",
                "subdomains": [
                    {
                        "name": "a_markets",
                        "description": "A Markets",
                        "subdomains": [
                            {
                                "name": "philippines",
                                "description": "Philippines"
                            },
                            {
                                "name": "south_africa",
                                "description": "South Africa"
                            },
                            {
                                "name": "nigeria",
                                "description": "Nigeria"
                            }
                        ]
                    },
                    {
                        "name": "c_markets",
                        "description": "C Markets",
                        "subdomains": [
                            {
                                "name": "algeria",
                                "description": "Algeria"
                            },
                            {
                                "name": "angola",
                                "description": "Angola"
                            },
                            {
                                "name": "benin",
                                "description": "Benin"
                            },
                            {
                                "name": "cape_verde",
                                "description": "Cape Verde"
                            },
                            {
                                "name": "chad",
                                "description": "Chad"
                            },
                            {
                                "name": "congo",
                                "description": "DRC"
                            },
                            {
                                "name": "gabon",
                                "description": "Gabon"
                            },
                            {
                                "name": "ghana",
                                "description": "Ghana"
                            },
                            {
                                "name": "guinea",
                                "description": "Guinea"
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
                "description": "Global Management Portal",
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
