from datetime import datetime
from odoo import models, fields, api

class foodcostwizard(models.TransientModel):
    _name = 'eatman.foodcostwizard'
    _description = 'Calcul global du cout de revient'

    def _default_name(self):
        value = "Date: "+str(datetime.now())
        return value

    name = fields.Char(default=lambda self: self._default_name())
    
    status = fields.Selection([('1','En préparation'),
                                   ('2','Terminé'),
                                   ('3','Annulé'),
                                   ],string='Status', copy='False' ,default='1')
    #product_calculated = fields.Many2many(
    #    'product.template', 'Produit avec coût de revient calculé',
    #    help="Ingrédient de la recette")
   
    def foodcost_total(self):
        produit_ids = self.env['product.template'].sudo().search([('purchase_ok', '=', True)])
        for produit in produit_ids:
            produit.foodcost_calculation()
        self.status = '2';
        
        produit_ids = self.env['product.template'].sudo().search([('sale_ok', '=', True)])
        for produit in produit_ids:
            produit.foodcost_calculation()
        self.status = '2';
     #   product_calculated = produit_ids
