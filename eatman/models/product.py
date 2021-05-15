# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging


class product(models.Model):
    
    _inherit = "product.template"
    
    product_cook = fields.Boolean(default=False,string="Produit cuisiné")
    sale_ok = fields.Boolean(default=False,string="Produit vendu")
    purchase_ok = fields.Boolean(default=False,string="Produit acheté")

    receipe_id= fields.One2many('eatman.receipe', 'product_cooked')


    #####Gestion des unités de mesure###########################################
    unit_of_inventory_1 = fields.Many2one('uom.uom', 'Unité d inventaire1')
    unit_of_inventory_2 = fields.Many2one('uom.uom', 'Unité d inventaire2')
    unit_of_inventory_3 = fields.Many2one('uom.uom', 'Unité d inventaire3')
    
    unit_of_reference = fields.Many2one('uom.uom', 'Unité de référence')
    unit_of_cooking = fields.Many2one('uom.uom', 'Unité de préparation')
    unit_of_sale = fields.Many2one('uom.uom', 'Unité de vente')
    unit_of_purchase = fields.Many2one('uom.uom', "Unité d'achat")
    
    #####Gestion des stocks#####################################################
    
    #Stock quantity are expressed in refernce UoM
    stock_quantity = fields.Float(digits=(3,3), string ='Quantité en stock', store=True)


    conversion_sale_sale_unit = fields.Char(related='unit_of_sale.name', string="Conversion unité vente/reference", store=True)
    conversion_sale_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion  unité reference/vente", store=True)
    
    conversion_purchase_purchase_unit = fields.Char(related='unit_of_purchase.name', string="Conversion unité achat/reference", store=True)
    conversion_purchase_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference/achat", store=True)
    
    
    conversion_cook_cook_unit = fields.Char(related='unit_of_cooking.name', string="Conversion unité preparation/reference", store=True)
    conversion_cook_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference preparation", store=True)
    
    conversion_inventory1_inventory1_unit = fields.Char(related='unit_of_inventory_1.name', string="Conversion unité inventaire1/reference", store=True)
    conversion_inventory1_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference unité/inventaire1", store=True)
    conversion_inventory2_inventory2_unit = fields.Char(related='unit_of_inventory_2.name', string="Conversion unité inventaire2/reference", store=True)
    conversion_inventory2_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference unité/inventaire2", store=True)
    conversion_inventory3_inventory3_unit = fields.Char(related='unit_of_inventory_3.name', string="Conversion unité inventaire3/reference", store=True)
    conversion_inventory3_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference unité/inventaire3", store=True)
    
    
    conversion_sale_sale_quantity = fields.Float(digits=(3,3))
    conversion_sale_reference_quantity = fields.Float(digits=(3,3))
    
    conversion_purchase_purchase_quantity = fields.Float(digits=(3,3))
    conversion_purchase_reference_quantity = fields.Float(digits=(3,3))
    
    conversion_cook_cook_quantity = fields.Float(digits=(3,3))
    conversion_cook_reference_quantity = fields.Float(digits=(3,3))
    
    
    conversion_inventory1_inventory1_quantity = fields.Float(digits=(3,3))
    conversion_inventory1_reference_quantity = fields.Float(digits=(3,3))
    conversion_inventory2_inventory2_quantity = fields.Float(digits=(3,3))
    conversion_inventory2_reference_quantity = fields.Float(digits=(3,3))
    conversion_inventory3_inventory3_quantity = fields.Float(digits=(3,3))
    conversion_inventory3_reference_quantity = fields.Float(digits=(3,3))
    
    foodcost_unit_reference =fields.Char(related='unit_of_reference.name', string="foodcost unité reference", store=True)
    
    purchase_price = fields.Float(digits=(3,3), string="Prix d'achat")
    purchase_quantity = fields.Float(digits=(3,3), string="Quantité d'achat")
    purchase_rounding = fields.Float(digits=(3,3), string="Arrondi de commande")
    
    foodcost = fields.Float(digits=(3,3), string="foodcost")
    
    sale_ratio = fields.Float(digits=(3,3), string="Ratio de vente")
    
    
    requirement_ids= fields.One2many('eatman.requirement', "product_required", string="Liste des besoins")
    
    #Gross requirement are expressed in reference UoM
    gross_requirement = fields.Float(compute="requirement_aggregation", store=True, digits=(3,3), string="Besoin Total")
    gross_requirement_cooking_unit = fields.Float(compute="requirement_aggregation", store=True, digits=(3,3), string="Besoin unité de préparation")
    
    @api.depends('requirement_ids')
    def requirement_aggregation(self):
        for record in self:
            record.gross_requirement = 0
            record.gross_requirement_cooking_unit = 0
            for requirement in record.requirement_ids:
                record.gross_requirement += record.conversion_cook_reference(requirement.quantity_required)
                record.gross_requirement_cooking_unit += requirement.quantity_required
                
    net_requirement = fields.Float(compute="requirement_net_calculation", store=True, digits=(3,3), string="Besoin net")
    @api.depends('gross_requirement', 'stock_quantity')
    def requirement_net_calculation(self):
        for record in self:
            record.net_requirement = record.gross_requirement - record.stock_quantity
            if record.net_requirement <0:
                record.net_requirement = 0

    ######### Fonction de Conversion #########
    
    def conversion_inventory1_reference(self, quantity):
        if self.conversion_inventory1_inventory1_quantity >0:
            return quantity*self.conversion_inventory1_reference_quantity/self.conversion_inventory1_inventory1_quantity
        return 0
    
    def conversion_inventory2_reference(self, quantity):
        if self.conversion_inventory2_inventory2_quantity >0:
            return quantity*self.conversion_inventory2_reference_quantity/self.conversion_inventory2_inventory2_quantity
        return 0
    
    def conversion_inventory3_reference(self, quantity):
        if self.conversion_inventory3_inventory3_quantity >0:
            return quantity*self.conversion_inventory3_reference_quantity/self.conversion_inventory3_inventory3_quantity
        return 0
    
    def conversion_purchase_reference(self, quantity):
        if self.conversion_purchase_purchase_quantity >0:
            return quantity*self.conversion_purchase_reference_quantity/self.conversion_purchase_purchase_quantity
        return 0
     
    def conversion_sale_reference(self, quantity):
        if self.conversion_sale_sale_quantity >0:
            return quantity*self.conversion_sale_reference_quantity/self.conversion_sale_sale_quantity
        return 0
    
    def conversion_cook_reference(self, quantity):
        if self.conversion_cook_cook_quantity >0:
            return quantity*self.conversion_cook_reference_quantity/self.conversion_cook_cook_quantity
        return 0
    
    def conversion_reference_cook(self,quantity):
        if self.conversion_cook_reference_quantity >0:
            return quantity*self.conversion_cook_cook_quantity/self.conversion_cook_reference_quantity
        return 0

    



############################################################Function##############################################################
    
    #Assign automaticcaly the  company of the user connected to the product
    @api.model
    def automatic_company_assignement(self):
        self.company_id = self.env.user.company_id
        #self.description = self.env.user.company_id.name

    #Override of the function create in order to automatically assigne the default company of the user as company of the product.
    @api.model
    def create(self, vals):
        record = super(product, self).create(vals)
        record.automatic_company_assignement()
        return record
    
    #For a given product calculate his food cost based on purchase price and receipe
    def foodcost_calculation(self):
        for record in self:
            foodcost_local = 0
            # dette technique: ajouter un contrôle sur le niveau pour s'assurer que l'on ne boucle pas
            if record.purchase_ok:
                record.foodcost = record.purchase_price/record.purchase_quantity/record.conversion_purchase_reference(1)
                return record.foodcost
            else:
                for receipe_line in record.receipe_id.receipe_line_ids:
                    foodcost_local += receipe_line.product_ingredient.foodcost_calculation()*receipe_line.ingredient_quantity/((100-receipe_line.ingredient_lost_rate)/100)
                if record.receipe_id.receipe_quantity >0:
                    if record.conversion_cook_reference(record.receipe_id.receipe_quantity)>0:
                        record.foodcost = foodcost_local / record.conversion_cook_reference(record.receipe_id.receipe_quantity)
                        return foodcost_local/record.receipe_id.receipe_quantity


    def requirement_calculation(self, quantity, requirement_father):
        for record in self:
            self.env['eatman.requirement'].create({'product_required': record.id, 'quantity_required': quantity, 'requirement_father': requirement_father, 'company_id':record.company_id.id})

            if record.receipe_id != False:
                for line in record.receipe_id.receipe_line_ids:
                    quantity_ingredient = quantity/record.receipe_id.receipe_quantity*line.ingredient_quantity/((100-line.ingredient_lost_rate)/100)
                    line.product_ingredient.requirement_calculation(quantity_ingredient, record.name)
            