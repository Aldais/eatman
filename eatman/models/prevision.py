from odoo import models, fields, api


class previsionwizard(models.Model):
    _name = 'eatman.previsionwizard'
    _description = 'Calcul des prévisions'

    name = fields.Char()
    turnover = fields.Float(digits=(3,3), string="Chiffre d'affaire prévisionnel")
    
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

    def _planning():
        for record in self:
            product_ids = self.env['product.template'].sudo().search([('sale_ok', '=', True),('company_id','=',self.env.user.company_id)])
            for product in product_ids:
                product.requirement_planning(record.turnover)
    
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

