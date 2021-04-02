# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging


class product(models.Model):
    
    _inherit = "product.template"
    
    product_cook = fields.Boolean(default=False,string="Produit cuisiné")
    sale_ok = fields.Boolean(default=False,string="Produit vendu")
    purchase_ok = fields.Boolean(default=False,string="Produit acheté")
    receipe_id= fields.One2many('eatman.receipe', 'product_cooked')

    #Gestion des unités de mesure pour les différents process
    #inventaire
    #cuisine
    #vente
    #achat
    #unité pivot de référence pour les 
                                      
    unit_of_inventory_1 = fields.Many2one('uom.uom', 'Unité d inventaire1')
    unit_of_inventory_2 = fields.Many2one('uom.uom', 'Unité d inventaire2')
    unit_of_inventory_3 = fields.Many2one('uom.uom', 'Unité d inventaire3')
    
    unit_of_reference = fields.Many2one('uom.uom', 'Unité de référence')
    unit_of_cooking = fields.Many2one('uom.uom', 'Unité de préparation')
    unit_of_sale = fields.Many2one('uom.uom', 'Unité de vente')
    unit_of_purchase = fields.Many2one('uom.uom', "Unité d'achat")
    
    #Conversion doit permettre de calculer facilement un ratio. Ex:
    #6 bouteilles = 1 pack
    #1 boite = 250 Grammes
    
    conversion_sale_sale_unit = fields.Char(related='unit_of_sale.name', string="Conversion unité vente/reference", store=True)
    conversion_sale_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion  unité reference/vente", store=True)
    
    conversion_purchase_purchase_unit = fields.Char(related='unit_of_purchase.name', string="Conversion unité achat/reference", store=True)
    conversion_purchase_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference/achat", store=True)
    
    
    conversion_cook_cook_unit = fields.Char(related='unit_of_cooking.name', string="Conversion unité preparation/reference", store=True)
    conversion_cook_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference preparation", store=True)
    
    conversion_sale_sale_quantity = fields.Float(digits=(3,3))
    conversion_sale_reference_quantity = fields.Float(digits=(3,3))
    
    conversion_purchase_purchase_quantity = fields.Float(digits=(3,3))
    conversion_purchase_reference_quantity = fields.Float(digits=(3,3))
    
    
    conversion_cook_cook_quantity = fields.Float(digits=(3,3))
    conversion_cook_reference_quantity = fields.Float(digits=(3,3))
    
    conversion_inventory1 = fields.Float(digits=(3,3))
    conversion_inventory2 = fields.Float(digits=(3,3))
    conversion_inventory3 = fields.Float(digits=(3,3))
    
    ratio_sale = fields.Float(compute="_value_ratio_sale", store=True, digits=(3,3))
    @api.depends('conversion_sale_sale_quantity','conversion_sale_reference_quantity')
    def _value_ratio_sale(self):
        for record in self:
            if (record.conversion_sale_reference_quantity >0):
                record.ratio_sale = float(record.conversion_sale_sale_quantity) / float(record.conversion_sale_reference_quantity)
    
    
    
    ratio_purchase = fields.Float(compute="_value_ratio_purchase", store=True, digits=(3,3))
    @api.depends('conversion_purchase_purchase_quantity','conversion_purchase_purchase_quantity')
    def _value_ratio_purchase(self):
        for record in self:
            if (record.conversion_purchase_reference_quantity >0):
                record.ratio_purchase = float(record.conversion_purchase_purchase_quantity) / float(record.conversion_purchase_reference_quantity)
                
    ratio_cook = fields.Float(compute="_value_ratio_cook", store=True, digits=(3,3))
    @api.depends('conversion_cook_cook_quantity','conversion_cook_reference_quantity')
    def _value_ratio_cook(self):
        for record in self:
            if (record.conversion_cook_reference_quantity >0):
                record.ratio_cook = float(record.conversion_cook_cook_quantity) / float(record.conversion_cook_reference_quantity)
     

    
    
    purchase_price = fields.Float(digits=(3,3), string="Prix d'achat")
    purchase_quantity = fields.Float(digits=(3,3), string="Quantité d'achat")
    purchase_rounding = fields.Float(digits=(3,3), string="Arrondi de commande")
    
    foodcost = fields.Float(digits=(3,3), string="Food cost")

    #     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

    def foodcost_total(self):
        self.foodcost_calculation()
    
    @api.model
    def foodcost_calculation(self):
        self.description = "OK4"
        foodcost_local = 0
        _logger = logging.getLogger(__name__)
        _logger.info('------------------------')
        # dette technique: ajouter un contrôle sur le niveau pour s'assurer que l'on ne boucle pas
        if self.purchase_ok:
            self.foodcost = self.purchase_price*self.ratio_purchase
            
            return self.foodcost
        else:
            for receipe_line in self.receipe_id.receipe_line_ids:
                foodcost_local += receipe_line.product_ingredient.foodcost_calculation()*receipe_line.ingredient_quantity
            self.foodcost = foodcost_local / self.receipe_id.receipe_quantity/self.ratio_cook
            return foodcost_local/self.receipe_id.receipe_quantity

#si produit acheté on retourne le prix d'achat exprimé en unité de préparation
    # return = purchase price/purchase_quantity * ratio_purchase * ratio_cook
#si recette associée : Récupérer la recette associée
    #Pour tous les ingrédient de la recette
        #foodcost_cook_unit += produit.foodcost()*ingredient_quantity

    #product[foodcost]=foodcost_cook_unit/receipe_quantity/ratio_cook 
    #return foodcost_cook_unit/receipe_quantity

#Convert_purchase_to_cook()

#Convert_cook_to_purchase()

#Convert_cook_to_reference()

#Convert_reference_to_cook()

#Convert_purchase_to_reference()

#Convert_reference_to_purchase()



