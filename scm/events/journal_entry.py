import frappe

def validate(doc, method):
    has_payroll_entry = False
    for row in doc.accounts:
        if row.get("reference_name") and frappe.db.exists("Payroll Entry", row.get("reference_name")):
            has_payroll_entry = True

    if not has_payroll_entry:
        for account in doc.accounts:
            account.section_80_g = doc.section_80_g
            account.business_unit = doc.business_unit
            account.fc_compliance = doc.fc_compliance
            account.geographical_location = doc.geographical_location