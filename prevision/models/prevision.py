from odoo import models, fields, api


class prevision(models.Model):
    _name = 'prevision.prevision'
    _description = 'Prévision'

    name = fields.Char()
    product_planned = fields.Many2one('eatman.product', 'Produit planifié', help="Produit cuisiné")

    quanity_planned = fields.Float(digits=(3,3), string="quantité planifiée")
    
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

