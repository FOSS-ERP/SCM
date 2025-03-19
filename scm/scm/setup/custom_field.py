import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup_custom_fields():
    """Setup custom fields for Referral Practitioner Integration"""
    custom_fields = {
        "Accounting Dimension Detail": [
            {
                "fieldname" : "self_balancing_ledger",
                "label" : "Self Balancing Ledger",
                "fieldtype" : "Check",
                "insert_after": "mandatory_for_pl",
                "no_copy":1,
                "in_list_view": 1,

            }
        ]
    }
    
    create_custom_fields(custom_fields)
    