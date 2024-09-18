app_name = "fossunited"
app_title = "FOSSUnited Platform"
app_publisher = "Frappe x FOSSUnited"
app_description = "FOSS to organize events and to facilitate the community engagement"
app_email = "developers@fossunited.org"
app_license = "AGPL-3.0"

export_python_type_annotations = True

fixtures = ["State", "City", "FOSS Event Type"]

# Includes in <head>
# ------------------

# include js, css files in header of web template
web_include_css = ["/assets/fossunited/css/custom.css"]
web_include_js = ["website.bundle.js"]

# Jinja
# -----

# Add all simple route bench rules here
website_route_rules = [
    {
        "from_route": "/dashboard/<path:app_path>",
        "to_route": "dashboard",
    },
    {
        "from_route": "/events/<event>/cfp/new",
        "to_route": "/cfp/create/new",
    },
    {
        "from_route": "/events/<event>/rsvp/new",
        "to_route": "/rsvp/create/new",
    },
    {
        "from_route": "/events/<event_permalink>/schedule",
        "to_route": "/schedule",
    },
    {
        "from_route": "/events/<event_permalink>/cfp/<submission>/edit",
        "to_route": "/cfp/submission/edit",
    },
    {
        "from_route": "/events/<event_permalink>/rsvp/<submission>/edit",
        "to_route": "/rsvp/submission/edit",
    },
    {
        "from_route": "/<foss_user>/edit-profile",
        "to_route": "/foss_profile/edit",
    },
    {
        "from_route": "/create-foss-profile",
        "to_route": "/foss_profile/create",
    },
    {
        "from_route": "/events/<event_permalink>/book-conference-ticket",
        "to_route": "/book-conference-ticket",
    },
    {
        "from_route": "/events/<event_permalink>/cfp/all",
        "to_route": "/cfp/all",
    },
    {
        "from_route": "/hack/<permalink>/projects/all",
        "to_route": "/hackathon/projects",
    },
]

# add methods and filters to jinja environment
jinja = {
    "methods": [
        "fossunited.fossunited.utils.make_badge",
        "fossunited.fossunited.utils.get_doc_likes",
        "fossunited.fossunited.utils.get_user_socials",
        "fossunited.fossunited.utils.get_user_editable_doctype_fields",
        "fossunited.fossunited.utils.get_signup_optin_checks",
        "fossunited.fossunited.utils.get_grouped_events",
    ],
    "filters": [
        "fossunited.fossunited.utils.make_badge",
        "fossunited.fossunited.utils.get_profile_image",
    ],
}


signup_form_template = "fossunited.plugins.show_custom_signup"

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "User": {
        "after_insert": [
            "fossunited.fossunited.user_utils.set_unique_username",
            "fossunited.fossunited.user_utils.create_profile_on_user_create",
        ],
    },
    "Razorpay Payment": {
        "on_update": [
            "fossunited.ticketing.doctype.foss_event_ticket.foss_event_ticket.handle_payment_on_update"
        ],
        "before_insert": [
            "fossunited.ticketing.doctype.foss_event_ticket.foss_event_ticket.validate_payment_before_insert"
        ],
    },
}
