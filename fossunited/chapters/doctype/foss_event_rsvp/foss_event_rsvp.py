# Copyright (c) 2023, Frappe x FOSSUnited and contributors
# For license information, please see license.txt

import json

import frappe
from frappe.website.website_generator import WebsiteGenerator

from fossunited.fossunited.forms import create_submission


class FOSSEventRSVP(WebsiteGenerator):
    def before_save(self):
        self.set_route()
        self.enable_rsvp_tab()

    def on_update(self):
        if self.rsvp_count >= self.max_rsvp_count:
            self.is_published = 0

    def get_context(self, context):
        frappe.cache().set_value("linked_rsvp", self.name)

        context.event = frappe.get_doc(
            "FOSS Chapter Event", self.event
        )
        context.event_name = self.event_name
        context.event_date = context.event.event_start_date.strftime(
            "%B %d, %Y"
        )

        form_fields = [
            {
                "fieldname": "name1",
                "fieldtype": "Data",
                "label": "Full Name",
                "reqd": 1,
                "value": frappe.get_value(
                    "User", frappe.session.user, "full_name"
                ),
            },
            {
                "fieldname": "im_a",
                "fieldtype": "Select",
                "label": "I'm a",
                "description": "Select your current profession",
                "options": "\nStudent\nProfessional\nOther",
                "reqd": 1,
            },
        ]
        form_fields.extend(self.get_custom_questions())
        context.form_fields = form_fields

        context.already_rsvp = (
            True if self.check_if_already_rsvp() else False
        )
        context.submission_doctype = "FOSS Event RSVP Submission"
        if context.already_rsvp:
            context.submission = frappe.db.get_value(
                "FOSS Event RSVP Submission",
                {
                    "linked_rsvp": self.name,
                    "submitted_by": frappe.session.user,
                },
            )
            frappe.cache().set_value("submission", context.submission)

        context.no_cache = 1

    def set_route(self):
        event_route = frappe.db.get_value(
            "FOSS Chapter Event", self.event, "route"
        )
        self.route = f"{event_route}/rsvp"

    def enable_rsvp_tab(self):
        frappe.db.set_value(
            "FOSS Chapter Event", self.event, "show_rsvp", 1
        )

    def get_custom_questions(self):
        custom_questions = []
        for index, question in enumerate(
            self.custom_questions, start=1
        ):
            custom_questions.append(
                {
                    "fieldname": "custom_question_" + str(index),
                    "fieldtype": question.type,
                    "label": question.question,
                    "options": question.options,
                    "reqd": question.is_mandatory or 0,
                    "description": question.description,
                }
            )
        return custom_questions

    def check_if_already_rsvp(self):
        return frappe.db.exists(
            "FOSS Event RSVP Submission",
            {
                "linked_rsvp": self.name,
                "submitted_by": frappe.session.user,
            },
        )


@frappe.whitelist()
def create_rsvp(fields):
    fields_dict = {
        "doctype": "FOSS Event RSVP Submission",
        "linked_rsvp": frappe.cache().get_value("linked_rsvp"),
        "submitted_by": frappe.session.user,
    }
    fields_dict.update(json.loads(fields))
    return create_submission(fields_dict)
