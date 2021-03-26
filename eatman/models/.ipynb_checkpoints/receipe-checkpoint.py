from odoo import models, fields, api


class receipe(models.Model):
    _name = 'eatman.receipe'
    _description = 'Mes recettes'

    name = fields.Char()
    product_cooked = fields.Many2one('product.template', 'Produit cuisiné', help="Produit cuisiné")
    receipe_quantity = fields.Float(digits="3", string="quantité de la recette")
    receipe_uom = fields.Many2one('uom.uom',
    'Unité de préparation', related='product_cooked.unit_of_cooking',
     readonly=True) 
    receipe_line_ids= fields.One2many('eatman.receipe.line', 'receipe')


#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class receipeLine(models.Model):
    _name = 'eatman.receipe.line'
    _description = 'Lignes de recettes'

    name = fields.Char()
    receipe = fields.Many2one(
        'eatman.receipe', 'Recette',
        help="Recette associé")
    product_ingredient = fields.Many2one(
        'product.template', 'Ingrédient',
        help="Ingrédient de la recette")
    ingredient_quantity = fields.Float(digits="3", string="quantité de la recette")
    ingredient_uom = fields.Many2one('uom.uom',
    'Unité de préparation', related='product_ingredient.unit_of_cooking',
     readonly=True)
    ingredient_lost_rate =fields.Float(digits="3", string="Perte en %")