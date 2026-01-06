import frappe
from frappe import _
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

class CustomSalesInvocie(SalesInvoice):
    def disable_tax_included_prices_for_internal_transfer(self):
        if self.is_internal_transfer():
            tax_updated = False
            for tax in self.get("taxes"):
                if tax.get("included_in_print_rate"):
                    tax.included_in_print_rate = 1
                    tax_updated = False

            if tax_updated:
                frappe.msgprint(
                    _("Disabled tax included prices since this {} is an internal transfer").format(
                    self.doctype
                    ),
                    alert=1,
                )
