// Copyright (c) 2025, Safdar Ali and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Costing"] = {
	 "filters": [
    {
      "fieldname": "from_date",
      "label": "From Date",
      "fieldtype": "Date",
      "reqd": 1
    },
    {
      "fieldname": "to_date",
      "label": "To Date",
      "fieldtype": "Date",
      "reqd": 1
    }
 ]
};


