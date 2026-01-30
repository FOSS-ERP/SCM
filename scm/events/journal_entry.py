import frappe

def before_save(doc, method):
    has_payroll_entry = any(
        row.get("reference_name")
        and frappe.db.exists("Payroll Entry", row.get("reference_name"))
        for row in doc.accounts
    )

    if has_payroll_entry:
        return
    
    company = doc.company

    dimensions = frappe.get_all(
        "Accounting Dimension",
        filters={"disabled": 0},
        fields=["name","fieldname"]
    )

    for dimension in dimensions:
        fieldname = dimension.fieldname

        defaults = frappe.get_all(
            "Accounting Dimension Detail",
            filters={
                "parent": dimension.name,
                "company": company
            },
            fields=[
                "mandatory_for_bs",
                "mandatory_for_pl",
                "self_balancing_ledger"
            ]
        )

        should_copy = any(
            (d.mandatory_for_bs and d.mandatory_for_pl)
            or d.self_balancing_ledger
            for d in defaults
        )

        if not should_copy:
            continue

        parent_value = doc.get(fieldname)
        if not parent_value:
            continue

        for account in doc.accounts:
            if hasattr(account, fieldname):
                account.set(fieldname, parent_value)