# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging


class product(models.Model):
    
    _inherit = "product.template"
    
    debug = fields.Char()
    product_cook = fields.Boolean(default=False,string="Produit cuisiné")
    sale_ok = fields.Boolean(default=False,string="Produit vendu")
    purchase_ok = fields.Boolean(default=False,string="Produit acheté")

    receipe_id= fields.One2many('eatman.receipe', 'product_cooked')


    #####Gestion des unités de mesure###########################################
    unit_of_inventory_1 = fields.Many2one('uom.uom', "Unité d' inventaire 1")
    unit_of_inventory_2 = fields.Many2one('uom.uom', "Unité d' inventaire 2")
    unit_of_inventory_3 = fields.Many2one('uom.uom', "Unité d' inventaire 3")
    
    unit_of_reference = fields.Many2one('uom.uom', 'Unité de référence')
    unit_of_cooking = fields.Many2one('uom.uom', 'Unité de préparation')
    unit_of_sale = fields.Many2one('uom.uom', 'Unité de vente')
    unit_of_purchase = fields.Many2one('uom.uom', "Unité d'achat")
    
    reference_eq_cooking = fields.Boolean()
    reference_eq_sale = fields.Boolean()
    reference_eq_purchase = fields.Boolean()
    reference_eq_inv1 = fields.Boolean()
    reference_eq_inv2 = fields.Boolean()
    reference_eq_inv3 = fields.Boolean()

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
    
    
    #Contrôle d'équivalence des unités
    @api.onchange('unit_of_reference', 'unit_of_cooking', 'unit_of_sale','unit_of_purchase','unit_of_inventory_1','unit_of_inventory_2','unit_of_inventory_3')
    def unit_control(self):
        for record in self:
            if record.unit_of_reference.id == record.unit_of_cooking.id:
                record.reference_eq_cooking = True
            else: 
                record.reference_eq_cooking = False

            if record.unit_of_reference == record.unit_of_sale:
                record.reference_eq_sale = True
            else: record.reference_eq_sale = False

            if record.unit_of_reference == record.unit_of_purchase:
                record.reference_eq_purchase = True
            else: record.reference_eq_purchase = False

            if record.unit_of_reference == record.unit_of_inventory_1:
                record.reference_eq_inv1 = True
            else: 
                record.reference_eq_inv1 = False

            if record.unit_of_reference == record.unit_of_inventory_2:
                record.reference_eq_inv2 = True
            else: 
                record.reference_eq_inv2 = False

            if record.unit_of_reference == record.unit_of_inventory_3:
                record.reference_eq_inv3 = True
            else: record.reference_eq_inv3 = False

        
    
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

    #Si l'unité de reference et l'unité de cookin sont égales alors on fait la conversion en auto         
    @api.onchange('unit_of_cooking','unit_of_reference')
    def ochange_unit_of_cooking(self):
        if self.unit_of_cooking == self.unit_of_reference:
            self.conversion_cook_cook_quantity = 1
            self.conversion_cook_reference_quantity = 1
        else :
            self.conversion_cook_cook_quantity = 0
            self.conversion_cook_reference_quantity = 0
    
    @api.onchange('unit_of_sale','unit_of_reference')
    def ochange_unit_of_sale(self):

        if self.unit_of_sale == self.unit_of_reference:
            self.conversion_sale_sale_quantity = 1
            self.conversion_sale_reference_quantity = 1
        else:
            self.conversion_sale_sale_quantity = 0
            self.conversion_sale_reference_quantity = 0
    
    @api.onchange('unit_of_purchase','unit_of_reference')
    def ochange_unit_of_purchase(self):

        if self.unit_of_purchase == self.unit_of_reference:
            self.conversion_purchase_purchase_quantity = 1
            self.conversion_purchase_reference_quantity = 1
        else:
            self.conversion_purchase_purchase_quantity = 0
            self.conversion_purchase_reference_quantity = 0
    
    @api.onchange('unit_of_inventory_1','unit_of_reference')
    def ochange_unit_of_inv1(self):
        if self.unit_of_inventory_1 == self.unit_of_reference:
            self.conversion_inventory1_inventory1_quantity = 1
            self.conversion_inventory1_reference_quantity = 1
        else:
            self.conversion_inventory1_inventory1_quantity = 0
            self.conversion_inventory1_reference_quantity = 0

            
    @api.onchange('unit_of_inventory_2','unit_of_reference')
    def ochange_unit_of_inv2g(self):
        if self.unit_of_inventory_2 == self.unit_of_reference:
            self.conversion_inventory2_inventory2_quantity = 1
            self.conversion_inventory2_reference_quantity = 1
        else:
            self.conversion_inventory2_inventory2_quantity = 0
            self.conversion_inventory2_reference_quantity = 0
    
    @api.onchange('unit_of_inventory_3','unit_of_reference')
    def ochange_unit_of_inv3(self):
        if self.unit_of_inventory_3 == self.unit_of_reference:
            self.conversion_inventory3_inventory3_quantity = 1
            self.conversion_inventory3_reference_quantity = 1
        else:
            self.conversion_inventory3_inventory3_quantity = 0
            self.conversion_inventory3_reference_quantity = 0
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

    def foodcost_cook_unit(self):
        self.debug += "---foodcost_cook_unit:" + str(self.foodcost)+ " * " + str(self.conversion_cook_reference_quantity) + " / "+ str(self.conversion_cook_cook_quantity)+ " ---"
        if self.conversion_cook_cook_quantity >0:       
             return self.foodcost * self.conversion_cook_reference_quantity /self.conversion_cook_cook_quantity
        return 0

    def foodcost_cook_reference(self, foodcost_cook,quantity_receipe):
        return foodcost_cook / quantity_receipe / self.conversion_cook_reference(quantity_receipe)
        
    


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
        self.debug = 1
        for record in self:
            foodcost_cook = 0
            quantity_cook = 0
            # dette technique: ajouter un contrôle sur le niveau pour s'assurer que l'on ne boucle pas
            #Si le produit est acheté alors le foodcost est calculé sur la base des données d'achats
            if record.purchase_ok:
                record.foodcost = record.purchase_price/record.conversion_purchase_reference(record.purchase_quantity)
                return record.foodcost
            #sinon une recette doit être associée et le foodcost est égale à la somme des foodcost de la recette réexprimé en unité de référence
            
            else:
                for receipe_line in record.receipe_id.receipe_line_ids:
                    quantity_cook = receipe_line.ingredient_quantity/((100-receipe_line.ingredient_lost_rate)/100)
                    receipe_line.product_ingredient.foodcost_calculation()
                    foodcost_cook += receipe_line.product_ingredient.foodcost_cook_unit() * quantity_cook
                    record.debug += receipe_line.product_ingredient.name +": " +str(receipe_line.product_ingredient.foodcost_cook_unit())+" * "+ str(quantity_cook)+" / "
                #UIne fois le calcul du foodcost en unité de mesure de preparation a été réalisé on le transforme pour 1 unité de préparation puis pour une unité de référence
                if record.receipe_id.receipe_quantity >0:
                    if record.conversion_cook_reference(record.receipe_id.receipe_quantity)>0:
                        record.foodcost = record.foodcost_cook_reference(foodcost_cook,record.receipe_id.receipe_quantity)
                        return record.foodcost
                return 0

    def requirement_calculation(self, quantity, requirement_father):
        for record in self:
            self.env['eatman.requirement'].create({'product_required': record.id, 'quantity_required': quantity, 'requirement_father': requirement_father, 'company_id':record.company_id.id})

            if record.receipe_id != False:
                for line in record.receipe_id.receipe_line_ids:
                    quantity_ingredient = quantity/record.receipe_id.receipe_quantity*line.ingredient_quantity/((100-line.ingredient_lost_rate)/100)
                    line.product_ingredient.requirement_calculation(quantity_ingredient, record.name)
            