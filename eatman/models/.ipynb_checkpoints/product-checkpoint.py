# -*- coding: utf-8 -*-

from odoo import models, fields, api


class product(models.Model):
    
    _inherit = "product.template"
    
    product_cook = fields.Boolean(default=False,string="Produit cuisiné")
    sale_ok = fields.Boolean(default=False,string="Produit vendu")
    purchase_ok = fields.Boolean(default=False,string="Produit acheté")
    
    unit_of_reference = fields.Many2one('uom.uom', 'unité de référence',help="Unité de référence")
    unit_of_cooking = fields.Many2one('uom.uom', 'unité de préparation',help="Unité de préparation")
    unit_of_sale = fields.Many2one('uom.uom', 'unité de vente',help="Unité de vente")
    unit_of_purchase = fields.Many2one('uom.uom', "unité d'achat" ,help="Unité d'achat")
                                      
    unit_of_inventory_1 = fields.Many2one('uom.uom', 'unité d inventaire1')
    unit_of_inventory_2 = fields.Many2one('uom.uom', 'unité d inventaire2')
    unit_of_inventory_3 = fields.Many2one('uom.uom', 'unité d inventaire3')
    
    conversion_sale = fields.Float(digits="3")
    conversion_supply= fields.Float(digits="3")
    conversion_cook= fields.Float(digits="3")
    conversion_inventory1 = fields.Float(digits="3")
    conversion_inventory2 = fields.Float(digits="3")
    conversion_inventory3 = fields.Float(digits="3")
    
    ratio_sale = fields.Float(digits="3")
    ratio_supply = fields.Float(digits="3")
    ratio_cook = fields.Float(digits="3")

    

    #     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
