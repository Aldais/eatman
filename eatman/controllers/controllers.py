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
                    #'DATE': fp.date,
                    #'TEXT':fp.text,
        } for fp in fp_ids]

        # Convert the list of dictionaries to JSON
        response = http.Response(
            json.dumps(output, default=str),
            content_type='application/json;charset=utf-8')
        #response.status = 200  # OK
        return response