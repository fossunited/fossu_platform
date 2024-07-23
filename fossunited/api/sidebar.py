import frappe


@frappe.whitelist(allow_guest=True)
def get_sidebar_items():
    sidebar_items = [
        {
            "parent_label": "Profile",
            "items": [
                {
                    "label": "My Profile",
                    "route": "/me",
                }
            ],
        },
        {
            "parent_label": "Hackathons",
            "items": [
                {
                    "label": "Hackathons",
                    "route": "/my-hackathons",
                },
            ],
        },
    ]

    if user_is_chapter_member():
        sidebar_items.append(
            {
                "parent_label": "Organizer Dashboard",
                "items": [
                    {
                        "label": "Manage Chapter",
                        "route": "/chapter",
                    },
                ],
            }
        )

    if user_is_localhost_organizer():
        sidebar_items[1]["items"].append(
            {
                "label": "Manage Localhost",
                "route": "/localhost",
            }
        )

    return sidebar_items


def user_is_chapter_member(user: str = frappe.session.user):
    return bool(
        frappe.db.exists(
            "Has Role",
            {"role": "Chapter Team Member", "parent": user},
        )
    )


def user_is_localhost_organizer(user: str = frappe.session.user):
    return bool(
        frappe.db.exists(
            "Has Role",
            {"role": "Localhost Organizer", "parent": user},
        )
    )
