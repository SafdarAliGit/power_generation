// Copyright (c) 2025, Safdar Ali and contributors
// For license information, please see license.txt

frappe.ui.form.on("Daily Production", {
	refresh(frm) {
    frm.set_query("workstation","daily_production_item", function() {
            return {
                filters: {
                    "workstation_type": "Production"
                }
            }
        });
	},
});

frappe.ui.form.on("Daily Production Item", {
    rate: function(frm, cdt, cdn) {
        calc_amount_and_sum(frm, cdt, cdn);
    },
    kg: function(frm, cdt, cdn) {
        calc_amount_and_sum(frm, cdt, cdn);
    }
});

function calc_amount_and_sum(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    // Ensure numeric values
    const rate_value = (row.rate || 0);
    const kg_value   = (row.kg   || 0);

    // Compute amount for the row
    const amount_value = rate_value * kg_value;
    frappe.model.set_value(cdt, cdn, "amount", amount_value);

    // Sum totals for the parent document
    let total_amount = 0;
    let total_kg     = 0;

    (frm.doc.daily_production_item || []).forEach(function(r) {
        total_amount += (r.amount || 0);
        total_kg     += (r.kg     || 0);
    });

    frm.set_value("total_amount", total_amount);
    frm.set_value("total_kg", total_kg);

    // Optionally refresh fields if needed
    frm.refresh_field("daily_production_item");
    frm.refresh_field("total_amount");
    frm.refresh_field("total_kg");
}
