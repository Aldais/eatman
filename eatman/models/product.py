# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from datetime import datetime
class product(models.Model):
    
    _inherit = "product.template"    
    debug = fields.Char()
    unit_of_reference = fields.Many2one('uom.uom', 'Unité de référence')
    
    

    
#!!!!!!!!!!Gestion des allergènes###############################################################################################################
    allergene_ids= fields.Many2many('eatman.allergene', string="Liste des allergènes")

#!!!!!!!!!!Cooked product - information related##################################################################################################
    product_cook = fields.Boolean(default=False,string="Produit cuisiné")
    unit_of_cooking = fields.Many2one('uom.uom', 'Unité de préparation')
    conversion_cook_cook_unit = fields.Char(related='unit_of_cooking.name', string="Conversion unité preparation/reference", store=True)
    conversion_cook_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference preparation", store=True)
    conversion_cook_cook_quantity = fields.Float(digits=(3,3))
    conversion_cook_reference_quantity = fields.Float(digits=(3,3))
    
        #Check result of teh control of the reference unit and cooking unit
    reference_eq_cooking = fields.Boolean()
    
        #If product cooked, it should be linked to a receipe
    receipe_id= fields.One2many('eatman.receipe', 'product_cooked')
    
    @api.onchange('unit_of_cooking','unit_of_reference')
    def ochange_unit_of_cooking(self):
        if self.unit_of_cooking == self.unit_of_reference:
            self.conversion_cook_cook_quantity = 1
            self.conversion_cook_reference_quantity = 1
        else :
            self.conversion_cook_cook_quantity = 0
            self.conversion_cook_reference_quantity = 0
    
    
    #!!!!!!!!Sales management #########################################################################################################################
    sale_ok = fields.Boolean(default=False,string="Produit vendu")
    unit_of_sale = fields.Many2one('uom.uom', 'Unité de vente')
    reference_eq_sale = fields.Boolean()
    sale_ratio = fields.Float(digits=(10,10), string="Ratio de vente")
    
    conversion_sale_sale_unit = fields.Char(related='unit_of_sale.name', string="Conversion unité vente/reference", store=True)
    conversion_sale_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion  unité reference/vente", store=True)
    conversion_sale_sale_quantity = fields.Float(digits=(3,3))
    conversion_sale_reference_quantity = fields.Float(digits=(3,3))
    
    
    #!!!!!!!Stock Management ##################################################################################################################################
    stock_quantity = fields.Float(digits=(3,3), string ='Quantité en stock', store=True)
    
                ###Unit of measure for stock###
    unit_of_inventory_1 = fields.Many2one('uom.uom', "Unité d' inventaire 1")
    unit_of_inventory_2 = fields.Many2one('uom.uom', "Unité d' inventaire 2")
    unit_of_inventory_3 = fields.Many2one('uom.uom', "Unité d' inventaire 3")
    
                #####Stock information for conversion
    conversion_inventory1_inventory1_unit = fields.Char(related='unit_of_inventory_1.name', string="Conversion unité inventaire1/reference", store=True)
    conversion_inventory1_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference unité/inventaire1", store=True)
    conversion_inventory2_inventory2_unit = fields.Char(related='unit_of_inventory_2.name', string="Conversion unité inventaire2/reference", store=True)
    conversion_inventory2_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference unité/inventaire2", store=True)
    conversion_inventory3_inventory3_unit = fields.Char(related='unit_of_inventory_3.name', string="Conversion unité inventaire3/reference", store=True)
    conversion_inventory3_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference unité/inventaire3", store=True)
    conversion_inventory1_inventory1_quantity = fields.Float(digits=(3,3))
    conversion_inventory1_reference_quantity = fields.Float(digits=(3,3))
    conversion_inventory2_inventory2_quantity = fields.Float(digits=(3,3))
    conversion_inventory2_reference_quantity = fields.Float(digits=(3,3))
    conversion_inventory3_inventory3_quantity = fields.Float(digits=(3,3))
    conversion_inventory3_reference_quantity = fields.Float(digits=(3,3))
                ####Stock information for displaying conversion on view product
    reference_eq_inv1 = fields.Boolean()
    reference_eq_inv2 = fields.Boolean()
    reference_eq_inv3 = fields.Boolean()
    

#!!!!!Foodcost Information ##############################################################################################
    foodcost_unit_reference =fields.Char(related='unit_of_reference.name', string="foodcost unité reference", store=True)
    foodcost = fields.Float(digits=(3,3), string="foodcost")
    foodcost_text = fields.Char(compute="foodcost_text_compute", string="Foodcost")
    foodcost_date = fields.Date("Date du dernier calcul de foodcost")
    @api.depends('foodcost')
    def foodcost_text_compute(self):
        for record in self:
            record.foodcost_text = str(record.foodcost)+" € pour 1"+str(record.foodcost_unit_reference)


#!!!!!!Requirement for preparation slip##################################################################################
    requirement_ids= fields.One2many('eatman.requirement', "product_required", string="Liste des besoins")
    net_requirement = fields.Float(compute="requirement_net_calculation", store=True, digits=(3,3), string="Besoin net")
    
        #Gross requirement are expressed in reference UoM
    gross_requirement = fields.Float(compute="requirement_aggregation", store=True, digits=(3,3), string="Besoin Total")

    
    @api.depends('requirement_ids','conversion_cook_cook_quantity','conversion_cook_reference_quantity')
    def requirement_aggregation(self):
        for record in self:
            record.gross_requirement = 0
            for requirement in record.requirement_ids:
                record.gross_requirement += record.conversion_cook_to_reference(requirement.quantity_required)


                
  
    
    @api.depends('gross_requirement', 'stock_quantity')
    def requirement_net_calculation(self):
        for record in self:
            record.net_requirement = record.gross_requirement - record.stock_quantity
            if record.net_requirement <0:
                record.net_requirement = 0

    
#!!!!!!Requirement for purchasing##################################################################################
    supplier = fields.Many2one('res.partner', string='Fournisseur')
    purchase_requirement_ids= fields.One2many('eatman.requirement_purchase', "product_required", string="Liste des besoins achat")
    purchase_net_requirement = fields.Float(compute="requirement_net_calculation_purchase", store=True, digits=(3,3), string="Besoin net achat")
    
        #Gross requirement are expressed in reference UoM
    purchase_gross_requirement = fields.Float(compute="requirement_aggregation_purchase", store=True, digits=(3,3), string="Besoin total d'achat")

    @api.depends('purchase_requirement_ids','conversion_purchase_purchase_quantity')
    def requirement_aggregation_purchase(self):
        for record in self:
            record.purchase_gross_requirement = 0
            for requirement in record.purchase_requirement_ids:
                record.purchase_gross_requirement += record.conversion_purchase_reference(requirement.quantity_required)
                
  
    
    @api.depends('purchase_gross_requirement', 'stock_quantity')
    def requirement_net_calculation_purchase(self):
        for record in self:
            record.purchase_net_requirement = record.purchase_gross_requirement - record.stock_quantity
            if record.purchase_net_requirement <0:
                record.purchase_net_requirement = 0
    

    #!!!!!!!!!!!!Purchase information ######################################################################################################################
    purchase_ok = fields.Boolean(default=False,string="Produit acheté")
        #Information for purchase price
    unit_of_purchase = fields.Many2one('uom.uom', "Unité de prix d'achat")
    purchase_price = fields.Float(digits=(3,3), string="Prix d'achat")
    purchase_quantity = fields.Float(digits=(3,3), string="Quantité d'achat")
    
        #Information for purchase order
    unit_purchase_order = fields.Many2one('uom.uom', "Unité de commande d'achat")

    
    purchase_order_quantity = fields.Float(digits=(3,3), string="Quantité de commande")
    unit_purchase_pack = fields.Many2one('uom.uom', "Unité de colisage d'achat")
    purchase_order_quantity = fields.Float(digits=(3,3), string="Quantité de colisage")
    
        #information for purchase conversion display
        
    conversion_purchase_purchase_unit = fields.Char(related='unit_of_purchase.name', string="Conversion unité achat/reference", store=True)
    conversion_purchase_reference_unit = fields.Char(related='unit_of_reference.name', string="Conversion unité reference/achat", store=True)
    conversion_purchase_purchase_quantity = fields.Float(digits=(3,3))
    conversion_purchase_reference_quantity = fields.Float(digits=(3,3))
    

    
    #Conversion entre unité prix et unité purchase / unité purchase et unité colisage
    conv_purchase_price_purchase_unit = fields.Char(related='unit_of_purchase.name', string="Conversion unité prix achat/ unité de commande", store=True)
    conv_purchase_purchase_price_unit = fields.Char(related='unit_purchase_order.name', string="Conversion unité de commande/ unité de prix", store=True)
    conv_purchase_price_purchase_quantity = fields.Float(digits=(3,3))
    conv_purchase_purchase_price_quantity = fields.Float(digits=(3,3))

    conv_purchase_purchase_pack_unit = fields.Char(related='unit_purchase_order.name', string="Conversion unité de commande/ unité de colisage", store=True)
    conv_purchase_pack_purchase_unit = fields.Char(related='unit_purchase_pack.name', string="Conversion unité de colisage/ unité de commande", store=True)
    conv_purchase_purchase_pack_quantity = fields.Float(digits=(3,3))
    conv_purchase_pack_purchase_quantity = fields.Float(digits=(3,3))

    
    #Contrôle d'équivalence des unité à compléter

    
    reference_eq_purchase = fields.Boolean()
    purch_price_eq_order = fields.Boolean()
    purch_order_eq_pack = fields.Boolean()

    #Nous surcharcheons la gestion des unités. Par défaut l'unité de uom_id et uom_po_id sera égale à l'unité de référence
    @api.onchange('unit_of_reference')
    def purchase_uom_copy(self):
        self.uom_po_id = self.unit_of_reference.id
        self.uom_id = self.unit_of_reference.id
    

    @api.onchange('unit_of_purchase','unit_purchase_order','unit_purchase_pack')
    def unit_control_purchase(self):
        for record in self:
            if record.unit_of_purchase.id == record.unit_purchase_order.id:
                record.purch_price_eq_order = True
            else: 
                record.purch_price_eq_order = False
    
            if record.unit_purchase_order.id == record.unit_purchase_pack.id:
                record.purch_order_eq_pack = True
            else: 
                record.purch_order_eq_pack = False
    
    
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

        
    


    #Si l'unité de reference et l'unité de cookin sont égales alors on fait la conversion en auto         
    
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
    

    @api.onchange('unit_purchase_order','unit_purchase_pack')
    def ochange_unit_of_purchase_pack(self):

        if self.unit_purchase_order == self.unit_purchase_pack:
            self.conv_purchase_purchase_pack_quantity = 1
            self.conv_purchase_pack_purchase_quantity = 1
        else:
            self.conv_purchase_purchase_pack_quantity = 0
            self.conv_purchase_pack_purchase_quantity = 0
  
    @api.onchange('unit_purchase_order','unit_of_purchase')
    def ochange_unit_of_purchase_price(self):

        if self.unit_purchase_order == self.unit_of_purchase:
            self.conv_purchase_price_purchase_quantity = 1
            self.conv_purchase_purchase_price_quantity = 1
        else:
            self.conv_purchase_price_purchase_quantity = 0
            self.conv_purchase_purchase_price_quantity = 0


    
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
        self.foodcost_date = datetime.today()
        try:
            for record in self:
                foodcost_cook = 0
                quantity_cook = 0
                # dette technique: ajouter un contrôle sur le niveau pour s'assurer que l'on ne boucle pas
                #Si le produit est acheté alors le foodcost est calculé sur la base des données d'achats
                if record.purchase_ok:
                    if record.conversion_purchase_reference(record.purchase_quantity) >0:
                        record.foodcost = record.purchase_price/record.conversion_purchase_reference(record.purchase_quantity)
                        return record.foodcost
                #sinon une recette doit être associée et le foodcost est égale à la somme des foodcost de la recette réexprimé en unité de référence

                else:
                    for receipe_line in record.receipe_id.receipe_line_ids:
                        if receipe_line.product_ingredient.name != False:
                            quantity_cook = receipe_line.ingredient_quantity/((100-receipe_line.ingredient_lost_rate)/100)
                            receipe_line.product_ingredient.foodcost_calculation()
                            #on calcul le foodcost en unité de préparation:
                            foodcost_cook += receipe_line.product_ingredient.foodcost_cook_unit() * quantity_cook
                            record.debug += "Foodcost_calculation: "+receipe_line.product_ingredient.name 
                            record.debug +=": " +str(receipe_line.product_ingredient.foodcost_cook_unit())
                            record.debug +=" * "+ str(quantity_cook)
                            record.debug +=" = "+str(foodcost_cook)
                        else:
                            record.debug += "Foodcost_calculation: "+receipe_line.receipe.name +"Pas de produit dans une des lignes de recette"

                    #UIne fois le calcul du foodcost en unité de mesure de preparation a été réalisé on le transforme pour 1 unité de préparation puis pour une unité de référence
                    if record.receipe_id.receipe_quantity >0:
                        if self.conversion_cook_reference_quantity>0:
                            record.foodcost = foodcost_cook/record.receipe_id.receipe_quantity*self.conversion_cook_cook_quantity/self.conversion_cook_reference_quantity
                            return record.foodcost
        except (RuntimeError, TypeError, NameError, ValueError) as inst:
            self.debug = 'Erreur lors du foodcost'+inst.args[0]
        pass
        return 0

    def requirement_calculation(self, quantity, requirement_father):
        try:
            for record in self:
                self.env['eatman.requirement'].create({'product_required': record.id, 'quantity_required': quantity, 'requirement_father': requirement_father, 'company_id':record.company_id.id})

                if record.receipe_id != False:
                    for line in record.receipe_id.receipe_line_ids:
                        quantity_ingredient = quantity/record.receipe_id.receipe_quantity*line.ingredient_quantity/((100-line.ingredient_lost_rate)/100)
                        line.product_ingredient.requirement_calculation(quantity_ingredient, record.name)
        except (RuntimeError, TypeError, NameError, ValueError, ZeroDivisionError) as inst:
            self.debug = 'Erreur lors du requirement calculation'+inst.args[0]
        pass
        return 0
        
    def requirement_calculation_purchase(self, quantity, requirement_father):
        for record in self:

            self.env['eatman.requirement_purchase'].create(
                {'product_required': record.id, 
                 'quantity_required': quantity, 
                 'requirement_father': requirement_father, 
                 'company_id':record.company_id.id})

            if record.receipe_id != False:
                for line in record.receipe_id.receipe_line_ids:
                    quantity_ingredient = quantity/record.receipe_id.receipe_quantity*line.ingredient_quantity/((100-line.ingredient_lost_rate)/100)
                    line.product_ingredient.requirement_calculation_purchase(quantity_ingredient, record.name)
        return 0
                       ######### Fonction de Conversion #########
    
    
    def conversion_purchase_reference(self, quantity):
        if self.conversion_purchase_purchase_quantity >0:
            return quantity*self.conversion_purchase_reference_quantity/self.conversion_purchase_purchase_quantity
        return 0
     

    def conversion_sale_to_reference(self, quantity):

        if self.conversion_sale_sale_quantity >0:
            return quantity*self.conversion_sale_reference_quantity/self.conversion_sale_sale_quantity
        return 0
    

    def conversion_cook_to_reference(self, quantity):
        if self.conversion_cook_cook_quantity >0:
            #self.debug += "---conversion_cook_to_reference:" + str(quantity)+ " * " + str(self.conversion_cook_cook_quantity) + " / "+ str(self.conversion_cook_reference_quantity)+ " ---"
            return quantity*self.conversion_cook_reference_quantity/self.conversion_cook_cook_quantity
        return 0
    
    def conversion_reference_to_cook(self,quantity):
        if self.conversion_cook_reference_quantity >0:


            return quantity*self.conversion_cook_cook_quantity/self.conversion_cook_reference_quantity
        return 0

    def foodcost_cook_unit(self):
        foodcost_cook_unit = 0

        try:
            if self.conversion_cook_cook_quantity >0:
                 foodcost_cook_unit=  self.foodcost * self.conversion_cook_reference_quantity /self.conversion_cook_cook_quantity
            self.debug += "---foodcost_cook_unit:" +self.name+" "+str(self.foodcost)+ " * " + str(self.conversion_cook_reference_quantity) + " / "+ str(self.conversion_cook_cook_quantity)+ " = "+str(foodcost_cook_unit)+" ---"
        except (RuntimeError, TypeError, NameError, ValueError) as inst:
            self.debug = 'Erreur lors de la conversion de quantité'+inst.args[0]
            pass
        return foodcost_cook_unit

    
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
    
    def conversion_initial(self):
    
        product_ids = self.env['product.template'].sudo().search([('id','!=', False)])
    
        for product in product_ids:    
            if product.unit_of_sale == product.unit_of_reference:
                product.conversion_sale_sale_quantity = 1
                product.conversion_sale_reference_quantity = 1
                
            if product.unit_of_cooking == product.unit_of_reference:
                product.conversion_cook_cook_quantity = 1
                product.conversion_cook_reference_quantity = 1


            if product.unit_of_purchase == product.unit_of_reference:
                product.conversion_purchase_purchase_quantity = 1
                product.conversion_purchase_reference_quantity = 1


            if product.unit_of_inventory_1 == product.unit_of_reference:
                product.conversion_inventory1_inventory1_quantity = 1
                product.conversion_inventory1_reference_quantity = 1


            if product.unit_of_inventory_2 == product.unit_of_reference:
                product.conversion_inventory2_inventory2_quantity = 1
                product.conversion_inventory2_reference_quantity = 1


            if product.unit_of_inventory_3 == product.unit_of_reference:
                product.conversion_inventory3_inventory3_quantity = 1
                product.conversion_inventory3_reference_quantity = 1


            if product.unit_purchase_order == product.unit_purchase_pack:
                product.conv_purchase_purchase_pack_quantity = 1
                product.conv_purchase_pack_purchase_quantity = 1


            if product.unit_purchase_order == product.unit_of_purchase:
                product.conv_purchase_price_purchase_quantity = 1
                product.conv_purchase_purchase_price_quantity = 1