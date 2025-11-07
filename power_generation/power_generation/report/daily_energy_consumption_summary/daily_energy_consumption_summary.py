import frappe

def execute(filters=None):
    filters = filters or {}
    
    workstations = frappe.db.get_all(
        "Daily Energy Consumption Item",
        distinct=True,
        pluck="workstation"
    )

    columns = get_columns(workstations)
    data = []

    # Base condition
    conditions = "de.docstatus = 1"
    
    # Apply filters if provided
    if filters.get("from_date"):
        conditions += " AND de.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND de.date <= %(to_date)s"
    if filters.get("utility"):
        conditions += " AND deci.utility = %(utility)s"

    # Query
    query = f"""
        SELECT
            de.date,
            deci.utility,
            deci.workstation,
            SUM(deci.amount) AS amount
        FROM
            `tabDaily Energy Consumption` de
        INNER JOIN
            `tabDaily Energy Consumption Item` deci ON deci.parent = de.name
        WHERE {conditions}
        GROUP BY de.date, deci.workstation,deci.utility
        ORDER BY de.date
    """

    raw_data = frappe.db.sql(query, filters, as_dict=True)

    # Pivot logic
    grouped_data = {}
    for row in raw_data:
        date = row.date
        workstation = row.workstation
        amount = int(round(float(row.amount or 0), 0))  # Rounded and converted to int

        if date not in grouped_data:
            grouped_data[date] = {ws: 0 for ws in workstations}
            grouped_data[date]["Total Amount"] = 0

        grouped_data[date][workstation] += amount
        grouped_data[date]["Total Amount"] += amount

    # Assemble final data rows
    for date in sorted(grouped_data.keys()):
        row = [date]
        for ws in workstations:
            row.append(grouped_data[date].get(ws, 0))
        row.append(grouped_data[date]["Total Amount"])
        data.append(row)

    return columns, data

def get_columns(workstations):
    columns = [{"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120}]
    
    for ws in workstations:
        columns.append({
            "label": ws,
            "fieldname": ws.lower().replace(" ", "_").replace("-", "_"),
            "fieldtype": "Currency",  # Changed from Float to Int
            "width": 120
        })
    
    columns.append({
        "label": "Total Amount",
        "fieldname": "total_amount",
        "fieldtype": "Currency",  # Changed from Float to Int
        "width": 130
    })
    
    return columns