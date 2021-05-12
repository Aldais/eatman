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
    turnover = fields.Float(string = "Chiffre d'affaire concerné")
    text = fields.Text(string ='Indication')
    product_ids= fields.Many2many('product.template')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1)
    
        #Assign automaticcaly the  company of the user connected to the product
    @api.model
    def automatic_company_assignement(self):
        self.company_id = self.env.user.company_id
        #self.description = self.env.user.company_id.name

    #Override of the function create in order to automatically assigne the default company of the user as company of the product.
    @api.model
    def create(self, vals):
        record = super(preparationslip, self).create(vals)
        record.automatic_company_assignement()
        return record
    
    


