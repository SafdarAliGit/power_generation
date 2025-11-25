import frappe

def execute(filters=None):
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    data = []
    columns = get_columns()

    # ----------------------------------------
    # 1) DAILY PRODUCTION SUMMARY
    # ----------------------------------------
    prod = frappe.db.sql("""
        SELECT 
            dpi.workstation,
            SUM(dpi.kg) AS total_kg
        FROM `tabDaily Production Item` dpi
        JOIN `tabDaily Production` dp ON dp.name = dpi.parent
        WHERE dp.docstatus = 1 
          AND dp.date BETWEEN %s AND %s
        GROUP BY dpi.workstation
        ORDER BY dpi.workstation
    """, (from_date, to_date), as_dict=True)

    total_production_kg = sum(r.total_kg for r in prod) if prod else 0

    data.append({"section": "Daily Production Summary"})
    data.extend(prod)
    data.append({"workstation": "Total Production", "total_kg": total_production_kg})

    # ----------------------------------------
    # 2) DAILY ENERGY CONSUMPTION
    # ----------------------------------------
    energy = frappe.db.sql("""
        SELECT 
            deci.workstation,
            deci.plant_floor,
            SUM(deci.amount) AS total_amount
        FROM `tabDaily Energy Consumption Item` deci
        JOIN `tabDaily Energy Consumption` dec_m ON dec_m.name = deci.parent
        WHERE dec_m.docstatus = 1
          AND dec_m.date BETWEEN %s AND %s
        GROUP BY deci.workstation, deci.plant_floor
        ORDER BY deci.workstation
    """, (from_date, to_date), as_dict=True)

    total_energy = sum(r.total_amount for r in energy) if energy else 0

    data.append({"section": "Daily Energy Consumption"})
    data.extend(energy)
    data.append({"workstation": "Total Energy", "total_amount": total_energy})

    # ----------------------------------------
    # 3) WATER CONSUMPTION (Stock Entry)
    # ----------------------------------------
    water = frappe.db.sql("""
        SELECT 
            sed.item_code AS workstation,
            SUM(sed.amount) AS total_amount,
            SUM(sed.qty) AS total_kg
        FROM `tabStock Entry Detail` sed
        JOIN `tabStock Entry` se ON se.name = sed.parent
        WHERE se.docstatus = 1
          AND sed.item_code = 'Water'
          AND se.stock_entry_type = 'Material Issue'
          AND se.posting_date BETWEEN %s AND %s
        GROUP BY sed.item_code
    """, (from_date, to_date), as_dict=True)

    total_water = sum(r.total_amount for r in water) if water else 0

    data.append({"section": "Water Consumption"})
    data.extend(water)
    data.append({"workstation": "Total Water Amount", "total_amount": total_water})

    # ----------------------------------------
    # 4) ACCOUNTS (GL Entry)
    # ----------------------------------------
    accounts = frappe.db.sql("""
        SELECT 
            gle.account,
            SUM(gle.debit) AS total_debit
        FROM `tabGL Entry` gle
        JOIN `tabAccount` acc ON acc.name = gle.account
        WHERE gle.is_cancelled = 0
          AND acc.parent_account = 'Manufacturing Expense - CT'
          AND gle.posting_date BETWEEN %s AND %s
        GROUP BY gle.account
        ORDER BY gle.account
    """, (from_date, to_date), as_dict=True)

    total_accounts = sum(r.total_debit for r in accounts) if accounts else 0

    data.append({"section": "Manufacturing Accounts"})
    data.extend(accounts)
    data.append({"workstation": "Total Accounts", "total_amount": total_accounts})

    # ----------------------------------------
    # 5) FINAL RATE CALCULATION
    # ----------------------------------------
    if total_production_kg > 0:
        final_rate = (total_energy + total_water + total_accounts) / total_production_kg
    else:
        final_rate = 0

    data.append({
        "section": "Final Costing",
        "rate": final_rate
    })

    return columns, data


# ---------------------------------------------------------
# COLUMNS
# ---------------------------------------------------------
def get_columns():
    return [
        {"label": "Section", "fieldname": "section", "fieldtype": "Data", "width": 200},
        {"label": "Workstation/Account", "fieldname": "workstation", "fieldtype": "Data", "width": 200},
        {"label": "Plant Type", "fieldname": "plant_floor", "fieldtype": "Data", "width": 120},
        {"label": "Qty", "fieldname": "total_kg", "fieldtype": "Float", "width": 150},
        {"label": "Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "width": 150}
    ]
