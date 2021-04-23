from datetime import datetime
from odoo import models, fields, api

class previsionwizard(models.TransientModel):
    _name = 'eatman.previsionwizard'
    _description = 'Lancement des prévision'

    def _default_name(self):
        value = "Date: "+str(datetime.now())
        return value

    name = fields.Char(default=lambda self: self._default_name())
    
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
    
    status = fields.Selection([('1','En préparation'),
                                   ('2','Terminé'),
                                   ('3','Annulé'),
                                   ],string='Status', copy='False' ,default='1')
    #product_calculated = fields.Many2many(
    #    'product.template', 'Produit avec coût de revient calculé',
    #    help="Ingrédient de la recette")
   
    def foodcost_total(self):
        produit_ids = self.env['product.template'].sudo().search([('product_cook', '=', True),('company_id','=', self.env.user.company_id)])
        for produit in produit_ids:
            produit.foodcost_calculation()
        self.status = '2';
     #   product_calculated = produit_ids
