frappe.query_reports["Daily Energy Consumption"] = {
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
            fieldname: "workstation",
            label: __("Workstation"),
            fieldtype: "Link",
            options: "Workstation",
            reqd: 0,
            get_query: function() {
                return {
                    filters: [
                        ["workstation_type", "=", "Energy"]
                    ]
                };
            }
        }
    ]
};
