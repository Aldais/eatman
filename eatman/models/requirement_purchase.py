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


