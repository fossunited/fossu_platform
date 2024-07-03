# Copyright (c) 2023, Frappe x FOSSUnited and contributors
# For license information, please see license.txt

from datetime import datetime

import frappe
from frappe.website.website_generator import WebsiteGenerator

from fossunited.fossunited.utils import is_user_team_member

BASE_DATE = datetime.now().replace(
    hour=0, minute=0, second=0, microsecond=0
)


class FOSSChapterEvent(WebsiteGenerator):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        from fossunited.chapters.doctype.foss_chapter_event_member.foss_chapter_event_member import (
            FOSSChapterEventMember,
        )
        from fossunited.chapters.doctype.foss_event_community_partner.foss_event_community_partner import (
            FOSSEventCommunityPartner,
        )
        from fossunited.fossunited.doctype.foss_event_field.foss_event_field import (
            FOSSEventField,
        )
        from fossunited.fossunited.doctype.foss_event_schedule.foss_event_schedule import (
            FOSSEventSchedule,
        )
        from fossunited.fossunited.doctype.foss_event_sponsor.foss_event_sponsor import (
            FOSSEventSponsor,
        )
        from fossunited.ticketing.doctype.foss_ticket_tier.foss_ticket_tier import (
            FOSSTicketTier,
        )

        banner_image: DF.AttachImage | None
        chapter: DF.Link | None
        chapter_name: DF.Data | None
        community_partners: DF.Table[FOSSEventCommunityPartner]
        custom_fields: DF.Table[FOSSEventField]
        deck_link: DF.Data | None
        event_bio: DF.Data | None
        event_description: DF.TextEditor | None
        event_end_date: DF.Datetime | None
        event_location: DF.Data | None
        event_members: DF.Table[FOSSChapterEventMember]
        event_name: DF.Data
        event_permalink: DF.Data | None
        event_schedule: DF.Table[FOSSEventSchedule]
        event_start_date: DF.Datetime | None
        event_type: DF.Link | None
        external_event_url: DF.Data | None
        is_external_event: DF.Check
        is_paid_event: DF.Check
        is_published: DF.Check
        map_link: DF.Data | None
        must_attend: DF.Check
        paid_tshirts_available: DF.Check
        primary_button_label: DF.Data | None
        primary_button_url: DF.Data | None
        route: DF.Data | None
        secondary_button_label: DF.Data | None
        secondary_button_url: DF.Data | None
        show_cfp: DF.Check
        show_photos: DF.Check
        show_rsvp: DF.Check
        show_schedule: DF.Check
        show_speakers: DF.Check
        sponsor_list: DF.Table[FOSSEventSponsor]
        status: DF.Literal[
            "", "Draft", "Live", "Approved", "Concluded", "Cancelled"
        ]
        t_shirt_price: DF.Currency
        ticket_form_description: DF.MarkdownEditor | None
        tiers: DF.Table[FOSSTicketTier]
    # end: auto-generated types

    def before_insert(self):
        self.copy_team_members()

    def copy_team_members(self):
        if not self.chapter:
            return

        chapter_team_members = frappe.get_doc(
            "FOSS Chapter", self.chapter
        ).chapter_members

        for member in chapter_team_members:
            self.append(
                "event_members",
                {
                    "member": member.chapter_member,
                    "full_name": member.full_name,
                    "role": member.role,
                    "email": member.email,
                },
            )

    def before_save(self):
        if self.has_value_changed("status"):
            self.update_published_status()
        self.set_route()

    def update_published_status(self):
        if self.status == "Draft" or self.status == "Cancelled":
            self.is_published = 0
            return

        if self.status == "Live" or self.status == "Approved":
            self.is_published = 1
            return

        if self.status == "Concluded":
            self.is_published = 1
            self.handle_concluded_event()

    def handle_concluded_event(self):
        event_permalink = self.event_permalink
        self.event_permalink = f"{event_permalink}-archive-{frappe.generate_hash(length=8)}"

    def set_route(self):
        if self.is_external_event:
            return
        self.route = f"events/{self.event_permalink}"

    def get_context(self, context):
        context.chapter = frappe.get_doc("FOSS Chapter", self.chapter)
        context.nav_items = self.get_navbar_items()
        context.sponsors_dict = self.get_sponsors()
        context.volunteers = self.get_volunteers()
        context.speakers = self.get_speakers()
        context.rsvp_status_block = self.get_rsvp_status_block()
        context.cfp_status_block = self.get_cfp_status_block()
        context.user_cfp_submissions = self.get_user_cfp_submissions()
        context.recent_cfp_submissions = (
            self.get_recent_cfp_submissions()
        )
        context.schedule_dict = self.get_schedule_dict()
        context.no_cache = 1

    def get_navbar_items(self):
        navbar_items = [
            "event_information",
            "speakers",
            "rsvp",
            "talk_proposal",
            "schedule",
        ]

        if is_user_team_member(self.chapter, frappe.session.user):
            return navbar_items

        if not self.show_speakers:
            navbar_items.remove("speakers")
        if not self.show_rsvp or self.paid_event:
            navbar_items.remove("rsvp")
        if not self.show_cfp:
            navbar_items.remove("talk_proposal")
        if not self.show_schedule:
            navbar_items.remove("schedule")

        return navbar_items

    def get_sponsors(self):
        sponsors_dict = {}
        for sponsor in self.sponsor_list:
            if sponsor.sponsorship_tier not in sponsors_dict:
                sponsors_dict[sponsor.sponsorship_tier] = []
            sponsors_dict[sponsor.sponsorship_tier].append(sponsor)
        return sponsors_dict

    def get_volunteers(self):
        members = []
        for member in self.event_members:
            profile = frappe.get_doc(
                "FOSS User Profile", member.member
            ).as_dict()
            members.append(
                {
                    "full_name": member.full_name,
                    "role": member.role or "Volunteer",
                    "profile_picture": profile.profile_photo
                    if profile.profile_photo
                    else "/assets/fossunited/images/defaults/user_profile_image.png",
                    "route": profile.route,
                }
            )
        return members

    def get_speakers(self):
        speaker_cfps = frappe.get_all(
            "FOSS Event CFP Submission",
            filters={
                "event": self.name,
                "status": "Approved",
            },
            fields=["talk_title", "submitted_by", "picture_url"],
        )
        speakers = []
        for cfp in speaker_cfps:
            print(cfp)
            user = frappe.get_doc(
                "FOSS User Profile", {"email": cfp.submitted_by}
            )
            speakers.append(
                {
                    "full_name": user.full_name,
                    "talk_title": cfp.talk_title,
                    "profile_picture": cfp.picture_url
                    or user.profile_photo
                    or "/assets/fossunited/images/defaults/user_profile_image.png",
                    "route": user.route,
                }
            )

        return speakers

    def get_rsvp_status_block(self):
        rsvp_status_block = {}
        rsvp_status_block["doctype"] = "FOSS Event RSVP"
        rsvp_status_block["block_for"] = "rsvp"

        if frappe.db.exists("FOSS Event RSVP", {"event": self.name}):
            rsvp_form = frappe.get_doc(
                "FOSS Event RSVP", {"event": self.name}
            )
            rsvp_status_block |= {
                "form_route": rsvp_form.route,
                "has_doc": True,
                "block_heading": "RSVP Form is Live!",
                "docname": rsvp_form.name,
                "is_published": rsvp_form.is_published,
                "is_unpublished": not rsvp_form.is_published,
            }
            if is_user_team_member(self.chapter, frappe.session.user):
                rsvp_status_block |= {
                    "is_team_member": True,
                    "form_edit": True,
                    "is_published": rsvp_form.is_published,
                    "is_unpublished": not rsvp_form.is_published,
                }
            else:
                rsvp_status_block["is_team_member"] = False
                if frappe.db.exists(
                    "FOSS Event RSVP Submission",
                    {
                        "linked_rsvp": rsvp_form.name,
                        "submitted_by": frappe.session.user,
                    },
                ):
                    submission = frappe.get_doc(
                        "FOSS Event RSVP Submission",
                        {
                            "linked_rsvp": rsvp_form.name,
                            "submitted_by": frappe.session.user,
                        },
                    )
                    rsvp_status_block |= {
                        "has_submitted": True,
                        "block_heading": "You have RSVP'd",
                        "submission": submission.name,
                        "edit_submission": True,
                    }
                else:
                    rsvp_status_block["show_primary_cta"] = True
                    rsvp_status_block[
                        "primary_cta"
                    ] = "RSVP for the event"

            if not rsvp_form.is_published:
                rsvp_status_block[
                    "block_heading"
                ] = "RSVP Form is Unpublished!"
        else:
            rsvp_status_block["has_doc"] = False
            rsvp_status_block[
                "block_heading"
            ] = "RSVP Form is not live yet!"
            if is_user_team_member(self.chapter, frappe.session.user):
                rsvp_status_block[
                    "block_heading"
                ] = "Create RSVP for the event"
                rsvp_status_block["is_team_member"] = True
                rsvp_status_block["create_form"] = True
            else:
                rsvp_status_block["is_team_member"] = False
                rsvp_status_block["show_primary_cta"] = False
        return rsvp_status_block

    def get_cfp_status_block(self):
        cfp_status_block = {}
        cfp_status_block["doctype"] = "FOSS Event CFP"
        cfp_status_block["block_for"] = "cfp"

        if frappe.db.exists("FOSS Event CFP", {"event": self.name}):
            cfp_form = frappe.get_doc(
                "FOSS Event CFP", {"event": self.name}
            )
            cfp_status_block |= {
                "form_route": cfp_form.route,
                "has_doc": True,
                "block_heading": "Call for Proposal (CFP) Form is Live!",
                "docname": cfp_form.name,
                "deadline": cfp_form.deadline.strftime(
                    "%d %B, %Y  %I:%M %p"
                )
                if cfp_form.deadline
                else None,
                "is_published": cfp_form.is_published,
                "is_unpublished": not cfp_form.is_published,
            }
            if is_user_team_member(self.chapter, frappe.session.user):
                cfp_status_block |= {
                    "is_team_member": True,
                    "form_edit": True,
                    "is_published": cfp_form.is_published,
                    "is_unpublished": not cfp_form.is_published,
                }
            else:
                cfp_status_block["is_team_member"] = False
                if frappe.db.exists(
                    "FOSS Event CFP Submission",
                    {
                        "linked_cfp": cfp_form.name,
                        "submitted_by": frappe.session.user,
                    },
                ):
                    submission = frappe.get_doc(
                        "FOSS Event CFP Submission",
                        {
                            "linked_cfp": cfp_form.name,
                            "submitted_by": frappe.session.user,
                        },
                    )
                    cfp_status_block |= {
                        "has_submitted": True,
                        "block_heading": "You have submitted a talk",
                        "submission": submission.name,
                    }

                cfp_status_block["show_primary_cta"] = True
                cfp_status_block[
                    "primary_cta"
                ] = "Submit a talk proposal"

            if not cfp_form.is_published:
                cfp_status_block[
                    "block_heading"
                ] = "Talk Proposal Form is Unpublished!"
        else:
            cfp_status_block["has_doc"] = False
            cfp_status_block[
                "block_heading"
            ] = "Talk Proposal Form is not live yet!"
            if is_user_team_member(self.chapter, frappe.session.user):
                cfp_status_block[
                    "block_heading"
                ] = "Create Call for Proposal (CFP) for the event"
                cfp_status_block["is_team_member"] = True
                cfp_status_block["create_form"] = True
            else:
                cfp_status_block["is_team_member"] = False
                cfp_status_block["show_primary_cta"] = False
        return cfp_status_block

    def get_user_cfp_submissions(self):
        submissions = frappe.get_all(
            "FOSS Event CFP Submission",
            filters={
                "event": self.name,
                "submitted_by": frappe.session.user,
            },
            fields=[
                "name",
                "route",
                "talk_title",
                "status",
            ],
        )
        return submissions or []

    def get_recent_cfp_submissions(self):
        submissions = frappe.get_all(
            "FOSS Event CFP Submission",
            filters={"event": self.name},
            fields=[
                "name",
                "route",
                "talk_title",
                "submitted_by",
                "picture_url",
                "status",
            ],
            order_by="creation desc",
            limit=6,
        )
        for submission in submissions:
            if submission.status == "Approved":
                user = frappe.get_doc(
                    "FOSS User Profile",
                    {"email": submission.submitted_by},
                )
                submission["user_route"] = user.route
                submission["full_name"] = user.full_name
                submission["profile_picture"] = (
                    submission.picture_url
                    or user.profile_photo
                    or "/assets/fossunited/images/defaults/user_profile_image.png"
                )
        return submissions or []

    def get_schedule_dict(self):
        schedule_dict = {}
        for schedule in self.event_schedule:
            date = schedule.scheduled_date.strftime("%-d %B")
            if date not in schedule_dict:
                schedule_dict[date] = []
            get_speakers(schedule)
            schedule.start_time = BASE_DATE + schedule.start_time
            schedule.end_time = BASE_DATE + schedule.end_time
            schedule_dict[date].append(schedule)

        schedule_dict["days"] = list(schedule_dict.keys())
        return schedule_dict


def get_speakers(schedule):
    if not schedule.linked_cfp:
        schedule.no_speaker = True
        return

    cfp = frappe.get_doc(
        "FOSS Event CFP Submission", schedule.linked_cfp
    )
    user = frappe.get_doc(
        "FOSS User Profile", {"email": cfp.submitted_by}
    )
    schedule.cfp_route = cfp.route
    schedule.speaker_route = user.route
    schedule.speaker_full_name = user.full_name
    schedule.speaker_designation_company = (
        cfp.designation + " at " + cfp.organization
    )
