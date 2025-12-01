# Copyright (c) 2025, Safdar Ali and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DailyEnergyConsumption(Document):
	def on_submit(self):
		# Only create Stock Entry for Water plant floor
		if self.plant_floor != "Water":
			return

		# Get values from Single Doc "Daily Energy Consumption Settings"
		settings = frappe.get_single("Daily Energy Consumption Settings")

		# These come from single doctype
		item_code = settings.item
		from_warehouse = settings.from_warehouse

		if not item_code or not from_warehouse:
			frappe.throw("Item or From Warehouse not found in Daily Energy Consumption Settings.")

		# Create Stock Entry
		se = frappe.new_doc("Stock Entry")
		se.stock_entry_type = "Material Issue"
		se.from_warehouse = from_warehouse
		se.custom_daily_energy_consumption = self.name

		# Loop child table "daily_energy_consumption_item"
		for row in self.daily_energy_consumption_item:
			qty = row.cons  # field "cons" used as qty

			if not qty or qty <= 0:
				continue

			se.append("items", {
				"item_code": item_code,
				"qty": qty
			})

		if not se.items:
			frappe.throw("No valid items (qty > 0) found to create Stock Entry.")

		se.save(ignore_permissions=True)
		se.submit()
