// Copyright (c) 2025, Safdar Ali and contributors
// For license information, please see license.txt

frappe.ui.form.on("Daily Energy Consumption", {
	refresh(frm) {
        frm.set_query("workstation","daily_energy_consumption_item", function() {
            return {
                filters: {
                    "workstation_type": "Energy"
                }
            }
        });
	},
});

frappe.ui.form.on("Daily Energy Consumption Item", {
    start_reading: function(frm, cdt, cdn) {
        recalc_row_and_totals(frm, cdt, cdn);
    },
    end_reading: function(frm, cdt, cdn) {
        recalc_row_and_totals(frm, cdt, cdn);
    }
});

function recalc_row_and_totals(frm, cdt, cdn) {
    let row = locals[cdt][cdn];

    // ensure numeric values
    const start_reading = (row.start_reading || 0);
    const end_reading   = (row.end_reading   || 0);
    const form_value    = (row.form          || 0);
    const rate_value    = (row.rate          || 0);

    // compute difference
    const diff_value = end_reading - start_reading;
    frappe.model.set_value(cdt, cdn, "diff", diff_value);

    // compute consumption = form * diff
    const cons_value = form_value * diff_value;
    frappe.model.set_value(cdt, cdn, "cons", cons_value);

    // compute amount = cons * rate
    const amount_value = cons_value * rate_value;
    frappe.model.set_value(cdt, cdn, "amount", amount_value);

    // compute total amount across all rows in child table
    let total_amt = 0;
    (frm.doc.daily_energy_consumption_item || []).forEach(function(r) {
        // r.amount could be undefined; ensure numeric
        total_amt += (r.amount || 0);
    });

    frm.set_value("total_amount", total_amt);
    // optionally refresh parent field
    frm.refresh_field("total_amount");
}
