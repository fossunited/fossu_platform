# Copyright (c) 2024, Frappe x FOSSUnited and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class FOSSHackathonPartnerProject(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        about: DF.SmallText | None
        hackathon: DF.Link | None
        logo: DF.AttachImage | None
        poc_email: DF.Data | None
        project_name: DF.Data | None
        repo_link: DF.Data | None
    # end: auto-generated types
    pass
