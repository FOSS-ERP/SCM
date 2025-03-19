import frappe

def validate(self, method):
    ad_list = frappe.db.sql("""
                    SELECT 
                        ad.name,
                        ad.fieldname
                    FROM `tabAccounting Dimension` AS ad
                    LEFT JOIN `tabAccounting Dimension Detail` AS adc ON adc.parent = ad.name
                    WHERE adc.self_balancing_ledger = '1'
                    GROUP BY ad.name, ad.fieldname
                """, as_dict=1)

    # ad_list = frappe.db.get_list("Accounting Dimension", {"disabled" : 0, }, ["name", "fieldname"])
    label_map = {}
    for row in ad_list:
        label_map[row.fieldname] = row.name
    available_field = []
    table_value = []  
    ad_error = []
    if self.voucher_type in ["Sales Invoice", "Purchase Invoice"]:
        doc_ = frappe.get_doc(self.voucher_type, self.voucher_no)
        meta = frappe.get_meta(self.voucher_type)
        for row in ad_list:
            if meta.has_field(row.get("fieldname")):
                available_field.append(row.fieldname)
                
        for row in available_field:
            main_form_ad = doc_.get(row)
            fieldname = row
            if self.voucher_type in ["Sales Invoice", "Purchase Invoice"]:
                for d in doc_.items:
                    table_value.append(d.get(fieldname))
                table_value = list(set(table_value))
                if len(table_value) >  1:
                    ad_error.append(label_map.get(row))
                if len(table_value) == 1 and table_value[0] != main_form_ad:
                    ad_error.append(label_map.get(row))
                table_value =[]
        

    available_field = []
    table_value = []  
    if self.voucher_type == "Journal Entry":
        doc_ = frappe.get_doc(self.voucher_type, self.voucher_no)
        meta = frappe.get_meta("Journal Entry Account")
        for row in ad_list:
            if meta.has_field(row.get("fieldname")):
                available_field.append(row.fieldname)
        
        for row in available_field:
            for d in doc_.accounts:
                table_value.append(d.get(row))
            table_value = list(set(table_value))
            
            if len(table_value) >  1:
                ad_error.append(label_map.get(row))
            table_value =[]
            
    if ad_error:
        frappe.throw(f"Accounting Dimension <b>{', '.join(ad_error)}</b> should be same in table")
