from odoo import models, fields, api


class requirement(models.Model):
    _name = 'eatman.requirement'
    _description = 'Besoin'
    
    product_required = fields.Many2one('product.template', 'Produit demandé', help="Produit cuisiné")
    quantity_required = fields.Float(digits=(3,3), string="Quantité demandée")

    receipe_uom = fields.Many2one('uom.uom',
    'Unité de préparation', related='product_required.unit_of_cooking',
     readonly=True) 
