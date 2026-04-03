// Copyright (c) 2026, Abhishek  and contributors
// For license information, please see license.txt


frappe.ui.form.on('Booking', {

    refresh: function(frm) {

        
        if (frm.fields_dict.from_date && frm.fields_dict.from_date.datepicker) {
            frm.fields_dict.from_date.datepicker.update({
                minDate: frappe.datetime.get_today()
            });
        }

        
        if (frm.fields_dict.to_date && frm.fields_dict.to_date.datepicker) {
            frm.fields_dict.to_date.datepicker.update({
                minDate: frappe.datetime.get_today()
            });
        }

        
        toggle_fields(frm);

        
        set_car_filter(frm);
    },

    validate: function(frm) {

        
        if (frm.doc.from_date && frm.doc.from_date < frappe.datetime.get_today()) {
            frappe.throw("From Date cannot be in the past");
        }

        
        if (frm.doc.to_date && frm.doc.from_date && frm.doc.to_date < frm.doc.from_date) {
            frappe.throw("To Date cannot be before From Date");
        }
    },

    
    calculation_type: function(frm) {
        toggle_fields(frm);
    }

});



function toggle_fields(frm) {

    
    if (frm.doc.calculation_type === "Per Day") {

        
        frm.set_df_property('price_per_km', 'hidden', 1);
        frm.set_value('price_per_km', 0);

        
        frm.set_df_property('distance', 'hidden', 1);
        frm.set_value('distance', 0);

    }

    
    else if (frm.doc.calculation_type === "Per KM") {

        
        frm.set_df_property('price_per_km', 'hidden', 0);

        
        frm.set_df_property('distance', 'hidden', 0);
    }
}



function set_car_filter(frm) {

    if (frm.fields_dict.cars && frm.fields_dict.cars.grid) {

        frm.fields_dict.cars.grid.get_field('car').get_query = function() {
            return {
                filters: {
                    available: 1
                }
            };
        };
    }
}