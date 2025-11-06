import frappe

def execute(filters=None):
    filters = filters or {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {"label": "Start Reading", "fieldname": "start_reading", "fieldtype": "Float", "width": 120},
        {"label": "End Reading", "fieldname": "end_reading", "fieldtype": "Float", "width": 120},
        {"label": "Difference", "fieldname": "diff", "fieldtype": "Float", "width": 100},
        {"label": "Form", "fieldname": "form", "fieldtype": "Data", "width": 100},
        {"label": "Consumption", "fieldname": "cons", "fieldtype": "Float", "width": 120},
        {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
    ]


def get_conditions(filters):
    conditions = "1=1"
    if filters.get("workstation"):
        conditions += " AND dei.workstation = %(workstation)s"
    if filters.get("from_date"):
        conditions += " AND main.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND main.date <= %(to_date)s"
    return conditions


def get_data(filters):
    conditions = get_conditions(filters)

    query = f"""
        SELECT
            main.date,
            dei.start_reading,
            dei.end_reading,
            dei.diff,
            dei.form,
            dei.cons,
            dei.rate,
            dei.amount
        FROM
            `tabDaily Energy Consumption` AS main
        JOIN
            `tabDaily Energy Consumption Item` AS dei
            ON dei.parent = main.name
        WHERE
			main.docstatus = 1 AND
            {conditions}
        ORDER BY
            main.date ASC
    """

    data = frappe.db.sql(query, filters, as_dict=True)
    return data
