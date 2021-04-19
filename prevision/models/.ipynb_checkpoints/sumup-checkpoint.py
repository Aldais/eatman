from odoo import models, fields, api


class sumup(models.Model):
    _name = 'prevision.sumup'
    _description = 'Intégration des ventes'

    name = fields.Char()
    date = fields.Date()
    state = fields.Selection(string='Status', selection=[
        ('brouillon', 'Brouillon'),
        ('confirmer', 'En cours'),
        ('terminer', 'Terminé')],
        copy=False, index=True, readonly=True, default = "brouillon")

    sumup_line_ids= fields.One2many('prevision.sumup.line', 'sumup')

    company_id = fields.Many2one(
        'res.company', 'Company', index=1)
    
    @api.model
    def automatic_company_assignement(self):
        self.company_id = self.env.user.company_id
        #self.description = self.env.user.company_id.name

    @api.model  
    def create(self, vals):
        record = super(sumup, self).create(vals)
        record.automatic_company_assignement()
        return record

    
    def sumup_line_assignement(self):
        for record in self:
            if (record.state == 'brouillon'):
                product_ids = self.env['product.template'].search([('company_id', '=', self.env.user.company_id.id),('sale_ok','=',True)])
                lines=[]
                record.state = 'confirmer'
                             
                for product in product_ids:
                    lines.append(self.env['prevision.sumup.line'].create({'product_sold': product.id, 'sumup': self.id}))
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class sumupLine(models.Model):
    _name = 'prevision.sumup.line'
    _description = 'Lignes de vente'

    name = fields.Char()
    sumup = fields.Many2one(
        'prevision.sumup', 'Fichier de vente',
        help="Fichier de vente")
    product_sold = fields.Many2one(
        'product.template', 'Produit vendu')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1)
        
    quantity_sold = fields.Float(digits=(3,3), string="quantité vendue")
    sale_uom = fields.Many2one('uom.uom','Unité de vente',readonly=True)
