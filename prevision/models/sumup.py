from odoo import models, fields, api


class sumup(models.Model):
    _name = 'prevision.sumup'
    _description = 'Intégration des ventes'

    name = fields.Char()
    date = fields.Date()

    sale_sumup_line_ids= fields.One2many('prevision.sale_sumup.line', 'sale_sumup')

    company_id = fields.Many2one(
        'res.company', 'Company', index=1)
    
    @api.model
    def automatic_company_assignement(self):
        self.company_id = self.env.user.company_id
        #self.description = self.env.user.company_id.name

    @api.model  
    def create(self, vals):
        record = super(receipe, self).create(vals)
        record.automatic_company_assignement()
        return record

#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class sale_sumupLine(models.Model):
    _name = 'prevision.sale_sumup.line'
    _description = 'Lignes de vente'

    name = fields.Char()
    sale_sumup = fields.Many2one(
        'prevision.sale_sumup', 'Fichier de vente',
        help="Fichier de vente")
    product_sold = fields.Many2one(
        'product.template', 'Produit vendu')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1)
        
    quantity_sold = fields.Float(digits=(3,3), string="quantité vendue")
    sale_uom = fields.Many2one('uom.uom',
    'Unité de vente', related='product_ingredient.unit_of_sale',
     readonly=True)
