from odoo import models, fields, api


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
            reference_quantity = product.conversion_sale_reference(sold_quantity)
            cook_quantity = product.conversion_reference_cook(reference_quantity)
            product.requirement_calculation_purchase(cook_quantity,"Prévision de vente")
        self.purchaseorderline_completion()
    
    
    #Au clic "proposition d'achat" ajouter les lignes de produit corresponsant avec l'unité de commande d'achat et l'unité de colisage
    def purchaseorderline_completion(self):
        product_ids = self.env['product.template'].sudo().search([('supplier','=', self.partner_id.id)])
        for product in product_ids:
            self.env['purchase.order.line'].create(
                {
                    'name': product.name,
                    'order_id': self.id,
                    'date_planned': self.date_order,
                    'product_qty': product.purchase_net_requirement,
                    'price_unit': 0.0,
                    'product_id': product.id,
                    'product_uom': product.unit_purchase_order.id,

                })
    
    
#class purchase 
    #ajouter les informations de colisage
    


