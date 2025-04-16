frappe.ui.form.on('Journal Entry', {
    company: function(frm) {
        // Ensure the 'company' field is filled before proceeding
        if (!frm.doc.company) return;

        // Fetch all Accounting Dimensions
        frappe.db.get_list('Accounting Dimension', {
            fields: ['name'],
        }).then(dimensions => {
            dimensions.forEach(dim => {
                // Fetch Accounting Dimension Details for the current company and parent dimension
                frappe.db.get_list('Accounting Dimension Detail', {
                    filters: { company: frm.doc.company, parent: dim.name },
                    fields: ['self_balancing_ledger'],
                    parent_doctype: "Accounting Dimension"
                }).then(child_records => {

                    // Check if any record has 'self_balancing_ledger' set to 0
                    var is_editable = child_records.some(rec => rec.self_balancing_ledger === 0);
                    var fieldname = dim.name.toLowerCase(); // Convert dimension name to lowercase

                    // Determine if the field should be read-only or editable
                    var read_only = is_editable ? 0 : 1;
                    
                    // var custom_fieldname = fieldname;
                    var custom_fieldname = fieldname;
                    console.log(custom_fieldname);
                    
                    if(read_only) { 
                        frm.set_df_property(custom_fieldname, 'read_only', 0);
                    } else {
                        frm.set_df_property(custom_fieldname, 'read_only', 1);
                    }
                    
                    console.log("Setting field:", fieldname, "Read-Only:", read_only);

                    // Ensure the field exists in the 'accounts' child table before applying the property
                    if (frm.fields_dict["accounts"]?.grid?.get_field(fieldname)) {
                        frm.fields_dict["accounts"].grid.update_docfield_property(fieldname, "read_only", read_only);
                        frm.refresh_field("accounts"); // Refresh the 'accounts' child table to reflect changes
                    }
                });
            });
        });
    },
    //// Set location in child table.....
    location: function(frm) {
        if (frm.doc.location) {
            frm.doc.accounts.forEach(row => {
                frappe.model.set_value(row.doctype, row.name, 'location', frm.doc.location);
            });
        }
    },

    //// Set fc_compliance in child table.....
    fc_compliance: function(frm) {
        if (frm.doc.fc_compliance) {
            frm.doc.accounts.forEach(row => {
                frappe.model.set_value(row.doctype, row.name, 'fc_compliance', frm.doc.fc_compliance);
            });
        }
    }

});
