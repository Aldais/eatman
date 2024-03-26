# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class ApiDevelopment(http.Controller):
    @http.route('/get_fp', auth='none', type = "http", csrf=False, methods=['GET'])
    def get_fp(self, **kw):
        
        fp_ids = http.request.env['eatman.preparationslip'].sudo().search([])
        output = [{
                    'NAME': fp.name,
                    'NB_PROD': len(fp.product_ids)
                    #'DATE': fp.date,
                    #'TEXT':fp.text,
        } for fp in fp_ids]

        # Convert the list of dictionaries to JSON
        response = http.Response(
            json.dumps(output, default=str),
            content_type='application/json;charset=utf-8')
        #response.status = 200  # OK
        return response
    
    @http.route('/put_ca', type='json', auth='none')
    def post_ca(self,**kw):
        requirement_wiz = http.request.env['eatman.requirementwizard']  # Access the model object
        vals = {
            'turnover': kw.get("ca_value"),
        }
        new_wizard = requirement_wiz.create(vals)
        new_wizard.requirement_total()
        response_data = {
                    "message": "Vos feuilles de préparation sont prêtes",
            }
        return response_data