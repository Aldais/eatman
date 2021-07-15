from odoo import models, fields, api

import math



class requirementPurchase(models.Model):
    _name = 'eatman.requirement_purchase'
    _description = "Besoin d'achat"
    
    product_required = fields.Many2one('product.template', 'produit demandé', help="Produit cuisiné")
    quantity_required = fields.Float(digits=(3,3), string="Quantité demandée")
    requirement_father = fields.Char(string = "Besoin amont")
    receipe_uom = fields.Many2one('uom.uom','Unité de préparation', related='product_required.unit_of_cooking',readonly=True)


    
    company_id = fields.Many2one(
        'res.company', 'Company', index=1)
    
    
class purchase(models.Model):
    _inherit = "purchase.order"
    
    turnover = fields.Float(digits=(3,3), string="Chiffre d'affaire potentiel")
    
    
    def requirement_delete(self):
        self.env['eatman.requirement_purchase'].sudo().search([('company_id','=', self.company_id.id)]).unlink()


    
    #ajouter action qui calcul les besoin pour les produits et pour un CA défini
    
    def requirement_total(self):
        self.requirement_delete()
        
        product_ids = self.env['product.template'].sudo().search([('sale_ok', '=', True),('company_id','=', self.env.user.company_id.id)])
        for product in product_ids:
            sold_quantity = product.sale_ratio*self.turnover
            reference_quantity = product.conversion_sale_to_reference(sold_quantity)
            cook_quantity = product.conversion_reference_to_cook(reference_quantity)
            product.requirement_calculation_purchase(cook_quantity,"Prévision de vente")
        self.purchaseorderline_completion()
    
    
    #Au clic "proposition d'achat" ajouter les lignes de produit corresponsant avec l'unité de commande d'achat et l'unité de colisage
    def purchaseorderline_completion(self):
        product_ids = self.env['product.template'].sudo().search([('supplier','=', self.partner_id.id)])
        for product in product_ids:
            
            if product.purchase_net_requirement >0:
                #le pruchase_net_requirement est exprimé en unité de référence afin de permettre la soustraction des stocks
                #il est donc nécessaire de transformé cette valeur en unité d'achat
                #La ligne de commande d'achat va utilisé 3 unité: 
                #L'unité de uom_po_id qui est nécessaire dans odoo
                #L'unité d'achat qui provient de la fiche article
                #L'unité de colisage qui provient de la fiche article
                #L'unité de prix d'achat qui provient de l'unité d'achat
                quantity_price_unit =  product.purchase_net_requirement * product.conversion_purchase_purchase_quantity / product.conversion_purchase_reference_quantity
                
                quantity_po_unit = quantity_price_unit * product.conv_purchase_purchase_price_quantity / product.conv_purchase_price_purchase_quantity
                price_po_unit = product.purchase_price / product.purchase_quantity * product.conversion_purchase_purchase_quantity / product.conversion_purchase_reference_quantity
                
                quantity_pack_unit = quantity_po_unit*product.conv_purchase_pack_purchase_quantity/product.conv_purchase_purchase_pack_quantity
                quantity_pack_unit_round = math.ceil(quantity_pack_unit)
                
                quantity_po_unit_round = quantity_pack_unit_round / product.conv_purchase_pack_purchase_quantity * product.conv_purchase_purchase_pack_quantity
                
                quantity_price_unit_round = quantity_po_unit_round / product.conv_purchase_purchase_price_quantity * product.conv_purchase_price_purchase_quantity
                
                quantity_reference_unit_round = quantity_price_unit_round  * product.conversion_purchase_reference_quantity / product.conversion_purchase_purchase_quantity
                

                
                quantity_price_unit_round
                
                self.env['purchase.order.line'].create(
                    {
                        'name': str(quantity_po_unit_round)+" x "+product.unit_purchase_order.name+" du produit: "+product.name+" soit "+str(quantity_pack_unit_round)+" x "+product.unit_purchase_pack.name,
                        'order_id': self.id,
                        'date_planned': self.date_order,
                        #product_qty est exprimé en unité de référence car limitation de Odoo. 
                        #L'unité d'achat doit être identique dans la commande. 
                        #Nous avons surcharger la fiche article pour que uom_po_id soit égal à unit_of_reference
                        #Le montant de la commande étant calculé sur product_qty * price_unit. Nous devons définir l'arrondi
                        #de commande en unité d'achat en fonction de l'unité de packing
                        'product_qty': quantity_reference_unit_round,
                        'product_uom': product.uom_po_id.id,
                        'price_unit': price_po_unit,
                        'product_id': product.id,
                        'pack_quantity':quantity_pack_unit,
                        'pack_quantity_roundup':quantity_pack_unit_round,
                        'pack_unit':product.unit_purchase_pack.id,
                        'price_quantity':quantity_price_unit,
                        'price_uom':product.unit_of_purchase.id,
                        'po_quantity':quantity_po_unit,
                        'po_unit':product.unit_purchase_order.id,
                        'po_quantity_roundup': quantity_po_unit_round
                    })
    
    
class purchaseLine(models.Model):
    _inherit = "purchase.order.line"
    price_uom = fields.Many2one('uom.uom', "Unité de prix d'achat")
    price_quantity = fields.Float(digits=(3,3), string="Quantité unité de prix")
    
    po_unit = fields.Many2one('uom.uom', "Unité de commande d'achat")
    po_quantity_roundup = fields.Float(digits=(3,3), string="Quantité unité de commande(arrondi)")
    po_quantity = fields.Float(digits=(3,3), string="Quantité unité de commande")
    
    pack_quantity = fields.Float(digits=(3,3), string="Quantité en unité de colisage")
    pack_quantity_roundup= fields.Float(digits=(3,3), string="Quantité en unité de colisage(arrondi)")
    pack_unit = fields.Many2one('uom.uom', "Unité de colisage d'achat")
    
        #fonction qui recalcul les unités et le prix lorsque le produit est renseigné
    @api.onchange('product_id')
    def ochange_product_id(self):
        self.price_uom = self.product_id.unit_of_purchase.id
        self.pack_unit = self.product_id.unit_purchase_pack.id
        self.po_unit = self.product_id.unit_purchase_order.id

