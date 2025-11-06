import frappe

def execute(filters=None):
    filters = filters or {}
    
    workstations = frappe.db.get_all(
        "Daily Production Item",
        distinct=True,
        pluck="workstation"
    )

    columns = get_columns(workstations)
    data = []

    # Base condition
    conditions = "dmp.docstatus = 1"
    
    # Apply filters if provided
    if filters.get("from_date"):
        conditions += " AND dmp.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND dmp.date <= %(to_date)s"

    # Query
    query = f"""
        SELECT
            dmp.date,
            dpi.workstation,
            SUM(dpi.kg) AS kg
        FROM
            `tabDaily Production` dmp
        INNER JOIN
            `tabDaily Production Item` dpi ON dpi.parent = dmp.name
        WHERE {conditions}
        GROUP BY dmp.date, dpi.workstation
        ORDER BY dmp.date
    """

    raw_data = frappe.db.sql(query, filters, as_dict=True)

    # Pivot logic
    grouped_data = {}
    for row in raw_data:
        date = row.date
        workstation = row.workstation
        kg = int(round(float(row.kg or 0), 0))  # Rounded and converted to int

        if date not in grouped_data:
            grouped_data[date] = {ws: 0 for ws in workstations}
            grouped_data[date]["Total KG"] = 0

        grouped_data[date][workstation] += kg
        grouped_data[date]["Total KG"] += kg

    # Assemble final data rows
    for date in sorted(grouped_data.keys()):
        row = [date]
        for ws in workstations:
            row.append(grouped_data[date].get(ws, 0))
        row.append(grouped_data[date]["Total KG"])
        data.append(row)

    return columns, data

def get_columns(workstations):
    columns = [{"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120}]
    
    for ws in workstations:
        columns.append({
            "label": ws,
            "fieldname": ws.lower().replace(" ", "_").replace("-", "_"),
            "fieldtype": "Int",  # Changed from Float to Int
            "width": 120
        })
    
    columns.append({
        "label": "Total KG",
        "fieldname": "total_kg",
        "fieldtype": "Int",  # Changed from Float to Int
        "width": 130
    })
    
    return columns