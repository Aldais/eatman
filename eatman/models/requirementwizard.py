from datetime import datetime
from odoo import models, fields, api

class requirementwizard(models.TransientModel):
    _name = 'eatman.requirementwizard'
    _description = 'Lancement calcul des besoins'

    test = fields.Float()
    
    def _default_name(self):
        value = "Date: "+str(datetime.now())
        return value

    name = fields.Char(default=lambda self: self._default_name())
    
    company_id = fields.Many2one(
        'res.company', 'Company', index=1)
    
    turnover = fields.Float(digits = (3,3), string="Chiffre d'affaire" )
    
    @api.model
    def automatic_company_assignement(self):
        self.company_id = self.env.user.company_id
        #self.description = self.env.user.company_id.name

    @api.model  
    def create(self, vals):
        record = super(requirementwizard, self).create(vals)
        record.automatic_company_assignement()
        return record
    
    status = fields.Selection([('1','En préparation'),
                                   ('2','Terminé'),
                                   ('3','Annulé'),
                                   ],string='Status', copy='False' ,default='1')
    #product_calculated = fields.Many2many(
    #    'product.template', 'Produit avec coût de revient calculé',
    #    help="Ingrédient de la recette")
   
    def requirement_delete(self):
        self.env['eatman.requirement'].sudo().search([('company_id','=', self.company_id.id)]).unlink()

    def requirement_total(self):
        self.requirement_delete()
        self.env['ir.config_parameter'].sudo().set_param('turnover',self.turnover)
        self.test =  self.env['ir.config_parameter'].sudo().get_param('turnover')
        
        product_ids = self.env['product.template'].sudo().search([('sale_ok', '=', True),('company_id','=', self.env.user.company_id.id)])
        for product in product_ids:
            sold_quantity = product.sale_ratio*self.turnover
            reference_quantity = product.conversion_sale_reference(sold_quantity)
            cook_quantity = product.conversion_reference_cook(reference_quantity)
            product.requirement_calculation(cook_quantity,"Prévision de vente")
        self.status = '2';
        preparation_slip_ids = self.env['eatman.preparationslip'].sudo().search([('id', '!=', False),('company_id','=', self.env.user.company_id.id)])
        for preparation_slip in preparation_slip_ids:
            preparation_slip.turnover = self.env['ir.config_parameter'].sudo().get_param('turnover')
