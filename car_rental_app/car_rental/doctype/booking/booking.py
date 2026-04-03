# Copyright (c) 2026, Abhishek  and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import throw
from datetime import datetime


class Booking(Document):

    def validate(self):
        self.calculate_amount()
        self.check_double_booking()

    def calculate_amount(self):

        total = 0  

        
        for row in self.cars:

           
            if self.calculation_type == "Per Day":

                if self.from_date and self.to_date and row.car:

                    from_date = datetime.strptime(str(self.from_date), "%Y-%m-%d")
                    to_date = datetime.strptime(str(self.to_date), "%Y-%m-%d")

                    days = (to_date - from_date).days + 1

                    price = frappe.db.get_value("Car", row.car, "price_per_day")

                    if price:
                        total += days * price   

                    
                    if row.driver_required == "Yes" and row.driver_charge:
                        total += days * row.driver_charge


            
            elif self.calculation_type == "Per KM":

                if self.distance and row.price_per_km:

                    total += self.distance * row.price_per_km

                    
                    if row.driver_required == "Yes" and row.driver_charge:
                        total += row.driver_charge


        self.total_amount = total


    def check_double_booking(self):

        if self.calculation_type == "Per Day":

            for row in self.cars:

                if row.car and self.from_date and self.to_date:

                    existing = frappe.db.sql("""
                        SELECT name FROM `tabBooking`
                        WHERE name != %s
                        AND docstatus < 2
                        AND EXISTS (
                            SELECT 1 FROM `tabBooking Item`
                            WHERE parent = `tabBooking`.name
                            AND car = %s
                        )
                        AND (
                            (%s BETWEEN from_date AND to_date)
                            OR
                            (%s BETWEEN from_date AND to_date)
                            OR
                            (from_date BETWEEN %s AND %s)
                        )
                    """, (
                        self.name or "",
                        row.car,
                        self.from_date,
                        self.to_date,
                        self.from_date,
                        self.to_date
                    ))

                    if existing:
                        throw(f"Car {row.car} already booked for selected dates")       