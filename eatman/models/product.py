# -*- coding: utf-8 -*-

from odoo import models, fields, api


class product(models.Model):
    
    _inherit = "product.template"
    
    product_cook = fields.Boolean(default=False,string="Produit cuisiné")
    sale_ok = fields.Boolean(default=False,string="Produit vendu")
    purchase_ok = fields.Boolean(default=False,string="Produit acheté")
    
    #Gestion des unités de mesure pour les différents process
    #inventaire
    #cuisine
    #vente
    #achat
    #unité pivot de référence pour les 
                                      
    unit_of_inventory_1 = fields.Many2one('uom.uom', 'unité d inventaire1')
    unit_of_inventory_2 = fields.Many2one('uom.uom', 'unité d inventaire2')
    unit_of_inventory_3 = fields.Many2one('uom.uom', 'unité d inventaire3')
    
    unit_of_reference = fields.Many2one('uom.uom', 'unité de référence')
    unit_of_cooking = fields.Many2one('uom.uom', 'unité de préparation')
    unit_of_sale = fields.Many2one('uom.uom', 'unité de vente')
    unit_of_purchase = fields.Many2one('uom.uom', "unité d'achat")
    
    #Conversion doit permettre de calculer facilement un ratio. Ex:
    #6 bouteilles = 1 pack
    #1 boite = 250 Grammes
    
    conversion_sale_source_unit = fields.Char(related='unit_of_sale.name', store=True)
    conversion_sale_target_unit = fields.Char(related='unit_of_reference.name', store=True)
    
    conversion_purchase_source_unit = fields.Char(related='unit_of_purchase.name', store=True)
    conversion_purchase_target_unit = fields.Char(related='unit_of_reference.name', store=True)
    
    
    conversion_cook_source_unit = fields.Char(related='unit_of_cooking.name', store=True)
    conversion_cook_target_unit = fields.Char(related='unit_of_reference.name', store=True)
    
    conversion_sale_source_quantity = fields.Float(digits="3")
    conversion_sale_target_quantity = fields.Float(digits="3")
    
    conversion_purchase_source_quantity = fields.Float(digits="3")
    conversion_purchase_target_quantity = fields.Float(digits="3")
    
    
    conversion_cook_source_quantity = fields.Float(digits="3")
    conversion_cook_target_quantity = fields.Float(digits="3")
    
    conversion_inventory1 = fields.Float(digits="3")
    conversion_inventory2 = fields.Float(digits="3")
    conversion_inventory3 = fields.Float(digits="3")
    
    ratio_sale = fields.Float(compute="_value_ratio_sale", store=True, digits="3")
    
    @api.depends('conversion_sale_source_quantity','conversion_sale_target_quantity')
    def _value_ratio_sale(self):
        for record in self:
            record.ratio_sale = float(record.conversion_sale_source_quantity) / float(record.conversion_sale_target_quantity)
    
    
    
    #ratio_supply = fields.Float(compute="_value_ratio_supply", store=True, digits="3")
    #ratio_cook = fields.Float(compute="_value_ratio_cook", store=True, digits="3")

     
    

    #     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
