from odoo import models, fields, api


class inventory(models.Model):
    _name = 'eatman.inventory'
    _description = 'Inventaire'

    name = fields.Char(default="inventaire")
    date = fields.Date()
    note = fields.Text()
    state = fields.Selection(string='Status', selection=[
        ('brouillon', 'Brouillon'),
        ('confirmer', 'En cours'),
        ('terminer', 'Terminé')],
        copy=False, index=True, readonly=True, default = "brouillon")
    inventory_line_ids= fields.One2many('eatman.inventory.line', 'inventory')
    
    
    @api.model
    def _automatic_company_assignement(self):
        return self.env.user.company_id
    
    company_id = fields.Many2one('res.company', 'Company', index=1, default=_automatic_company_assignement)
    
    def inventory_line_assignement(self):
        for record in self:
            if (record.state == 'brouillon'):
                product_ids = self.env['product.template'].search([('company_id', '=', self.env.user.company_id.id)])
                lines=[]
                record.state = 'confirmer'
                             
                for product in product_ids:
                    lines.append(self.env['eatman.inventory.line'].create({'product_inventory': product.id, 'inventory': self.id}))

    
    def validate_inventory(self):
        for record in self:
            record.state = "terminer"
            for line in record.inventory_line_ids:
                line.product_inventory.stock_quantity = line.product_quantity_reference_uom

 #   @api.model  
 #   def create(self, vals):
 #       record = super(inventory, self).create(vals)
 #       record.automatic_company_assignement()
 #       return record

#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class inventoryLine(models.Model):
    _name = 'eatman.inventory.line'
    _description = "inventaire produit"
    
    name = fields.Char()
    product_inventory = fields.Many2one('product.template', 'Produit', help="Produit inventorié")
    product_quantity1 = fields.Float(digits=(3,3), string="quantité en stock1")
    inventory_uom1 = fields.Many2one('uom.uom',"Unité d'inventaire 1", related='product_inventory.unit_of_inventory_1',readonly=True)
    product_quantity2 = fields.Float(digits=(3,3), string="quantité en stock2")
    inventory_uom2 = fields.Many2one('uom.uom',"Unité d'inventaire 2", related='product_inventory.unit_of_inventory_2',readonly=True)
    product_quantity3 = fields.Float(digits=(3,3), string="quantité en stock3")
    inventory_uom3 = fields.Many2one('uom.uom',"Unité d'inventaire 3", related='product_inventory.unit_of_inventory_3',readonly=True)
    inventory= fields.Many2one('eatman.inventory', 'inventory',help="Recette associé")
    company_id = fields.Many2one('res.company', 'Company', related='inventory.company_id')
    
    product_quantity_reference_uom  = fields.Float(compute="_compute_stock_quantity", store=True, digits=(3,3))
    
    @api.depends('product_quantity1','product_quantity2','product_quantity3')
    def _compute_stock_quantity(self):
        for record in self:
            record.product_quantity_reference_uom = 0
            product_local = self.env["product.template"].search([('id', '=', record.product_inventory.id)])
            if record.product_quantity1 != False:
                record.product_quantity_reference_uom += product_local.conversion_inventory1_reference(record.product_quantity1)
            if record.product_quantity2 != False:
                record.product_quantity_reference_uom += product_local.conversion_inventory2_reference(record.product_quantity2)
            if record.product_quantity3 != False:
                record.product_quantity_reference_uom += product_local.conversion_inventory3_reference(record.product_quantity3)
    