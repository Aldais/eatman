# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class ApiDevelopment(http.Controller):
    @http.route('/get_fp', auth='none', type = "http", csrf=False, methods=['GET'])
    def get_fps(self, **kw):
        
        fp_ids = http.request.env['eatman.preparationslip'].sudo().search([])
        output = [{
                    'ID': fp.id,
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
    
# A FINIR

    @http.route('/get_fiche', auth='none', type = "json", csrf=False, methods=['POST'])
    def get_fiche_prepa(self, **kw):
        fiche_prepa_id = kw.get("fiche_prepa")
        fp_ids = http.request.env['eatman.preparationslip'].sudo().search([('id','=',fiche_prepa_id)])
        output = [{
            'NAME': fp.name,
            'PRODUCTS_IDS': [{
                'PRODUCT':product.name,
                'QTE':str(product.net_requirement_cooking)+" "+product.unit_of_cooking.name
            } for product in fp.product_ids]
        } for fp in fp_ids]

        return output
    #Envoyer le CA dans Odoo et lancer le calcul de besoin
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
    
    #Récupérer la liste des produits
    @http.route('/get_product', auth='none', type = "http", csrf=False, methods=['GET'])
    def get_product(self, **kw):
        
        product_ids = http.request.env['product.template'].sudo().search([('sale_ok','=',True)])
        output = [{
                    'ID': product.id,
                    'NAME': product.name,
                    'FOODCOST': product.foodcost,
                    'PRIX': product.price_ttc,
                    'RATIO': product.foodcost_ratio
        } for product in product_ids]

        # Convert the list of dictionaries to JSON
        response = http.Response(
            json.dumps(output, default=str),
            content_type='application/json;charset=utf-8')
        #response.status = 200  # OK
        return response
    
        #Récupérer la liste des produits
    @http.route('/get_product_stock', auth='none', type = "http", csrf=False, methods=['GET'])
    def get_product(self, **kw):
        
        product_ids = http.request.env['product.template'].sudo().search(['&',('sale_ok','=',False),('product_cook','=',True)])
        output = [{
                    'ID': product.id,
                    'NAME': product.name,
        } for product in product_ids]

        # Convert the list of dictionaries to JSON
        response = http.Response(
            json.dumps(output, default=str),
            content_type='application/json;charset=utf-8')
        #response.status = 200  # OK
        return response