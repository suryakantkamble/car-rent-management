# Copyright (c) 2026, Abhishek  and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import throw

class Customer(Document):

    def validate(self):
        self.validate_mobile_no()

    def validate_mobile_no(self):

        
        if not self.phone:
            return

       
        mobile = str(self.phone).strip()

        
        if not mobile.isdigit():
            throw("Mobile number must contain only digits")

       
        if len(mobile) != 10:
            throw("Mobile number must be exactly 10 digits")

        
        if mobile == mobile[0] * 10:
            throw("Invalid mobile number (cannot be all same digits)")

        
        if mobile[0] not in ["6", "7", "8", "9"]:
            throw("Mobile number must start with 6, 7, 8, or 9")