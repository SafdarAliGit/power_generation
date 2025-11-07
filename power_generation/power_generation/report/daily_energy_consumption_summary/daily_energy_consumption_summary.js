frappe.query_reports["Daily Energy Consumption Summary"] = {
    "filters": [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.add_days(frappe.datetime.get_today(), -7)
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.get_today()
        },
        {
            fieldname: "utility",
            label: __("Utility"),
            fieldtype: "Select",
            options: "Gas\nWater\nElectricity",
            reqd: 0,
        }
    ]
};
