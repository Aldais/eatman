from odoo import models, fields, api


class requirement(models.Model):
    _name = 'eatman.requirement'
    _description = 'Besoin'
    
    product_required = fields.Many2one('product.template', 'produit demandé', help="Produit cuisiné")
    quantity_required = fields.Float(digits=(3,3), string="Quantité demandée")
    requirement_father = fields.Char(string = "Besoin amont")
    receipe_uom = fields.Many2one('uom.uom','Unité de préparation', related='product_required.unit_of_cooking',readonly=True)
    company_id = fields.Many2one(
        'res.company', 'Company', index=1)

class preparationslip(models.Model):
    _name = 'eatman.preparationslip'
    _description = 'Feuille de preparation'
    
    name = fields.Char()
    date = fields.Date()
    
    text = fields.Text(string ='Indication')
    product_ids= fields.Many2many('product.template')
    
    

#class preparationslipline(models.Model):
#    _name = 'eatman.preparationslip.line'
#    _description = 'Besoin de preparation'
    
#    preparationslip = fields.Many2one('eatman.preparationslip', 'Feuille de préparation')
#    product_cooked = fields.Many2one('product.template', 'produit', help="Produit cuisiné")
#    quantity_cooked = fields.Float(string = "Quantité" )
#    unit_cooked = fields.Many2one('uom.uom','Unité de préparation', related='product_cooked.unit_of_cooking',readonly=True)
#    quantity_inventory = fields.Float(string = "Quantité en inventaire")
#    unit_inventory = fields.Many2one('uom.uom','Unité de stock', related='product_cooked.unit_of_reference',readonly=True)

    
    