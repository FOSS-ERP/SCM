# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import json

import frappe
from frappe import _, scrub
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
from frappe.database.schema import validate_column_name
from frappe.model import core_doctypes_list
from frappe.model.document import Document
from frappe.utils import cstr

from erpnext.accounts.doctype.repost_accounting_ledger.repost_accounting_ledger import (
	get_allowed_types_from_settings,
)


def get_accounting_dimensions(as_list=True, filters=None):
	if not filters:
		filters = {"disabled": 0}

	if frappe.flags.accounting_dimensions is None:
		frappe.flags.accounting_dimensions = frappe.get_all(
			"Accounting Dimension",
			fields=["label", "fieldname", "disabled", "document_type"],
			filters=filters,
		)

	if as_list:
		return [d.fieldname for d in frappe.flags.accounting_dimensions]
	else:
		return frappe.flags.accounting_dimensions

## Add accounting Dimention field
def make_dimension_in_accounting_doctypes(doc, doclist=None):
	# Force doclist to be only Journal Entry
	doclist = ["Journal Entry"]

	doc_count = len(get_accounting_dimensions())
	count = 0
	# repostable_doctypes = get_allowed_types_from_settings()

	for doctype in doclist:
		
		insert_after_field = "accounting_dimensions_section"

		df = {
			"fieldname": doc.fieldname,
			"label": doc.label,
			"fieldtype": "Link",
			"options": doc.document_type,
			"insert_after": insert_after_field,
			"owner": "Administrator",
			# "allow_on_submit": 1 if doctype in repostable_doctypes else 0,
		}

		meta = frappe.get_meta(doctype, cached=False)
		fieldnames = [d.fieldname for d in meta.get("fields")]

		if df["fieldname"] not in fieldnames:
			create_custom_field(doctype, df, ignore_validate=True)

		count += 1

		# frappe.publish_progress(count * 100 / len(doclist), title=_("Creating Dimensions..."))
		frappe.clear_cache(doctype=doctype)



def delete_accounting_dimension_from_journal_entry(doc, doclist=None):
	doclist = ["Journal Entry"]

	# Delete Custom Field
	frappe.db.sql(
		"""
		DELETE FROM `tabCustom Field`
		WHERE fieldname = %s
		AND dt = %s
		""",
		(doc.fieldname, "Journal Entry")
	)

	# Delete Property Setter
	frappe.db.sql(
		"""
		DELETE FROM `tabProperty Setter`
		WHERE field_name = %s
		AND doc_type = %s
		""",
		(doc.fieldname, "Journal Entry")
	)

	# Clear Cache
	frappe.clear_cache(doctype="Journal Entry")
