from odoo import models, fields, api


class inventory(models.Model):
    _name = 'eatman.inventory'
    _description = 'Inventaire'

    name = fields.Char()
    date = fields.Date()
    inventory_line_ids= fields.One2many('eatman.inventory.line', 'inventory')
    
    company_id = fields.Many2one(
        'res.company', 'Company', index=1)
    
    @api.model
    def automatic_company_assignement(self):
        self.company_id = self.env.user.company_id
        #self.description = self.env.user.company_id.name

    @api.model  
    def create(self, vals):
        record = super(inventory, self).create(vals)
        record.automatic_company_assignement()
        return record

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
    inventory_uom1 = fields.Many2one('uom.uom',
    "Unité d'inventaire 1", related='product_inventory.unit_of_inventory_1',
     readonly=True)
    product_quantity2 = fields.Float(digits=(3,3), string="quantité en stock2")
    inventory_uom2 = fields.Many2one('uom.uom',
    "Unité d'inventaire 2", related='product_inventory.unit_of_inventory_2',
     readonly=True)
    product_quantity3 = fields.Float(digits=(3,3), string="quantité en stock3")
    inventory_uom3 = fields.Many2one('uom.uom',
    "Unité d'inventaire 3", related='product_inventory.unit_of_inventory_3',
     readonly=True)
    inventory= fields.Many2one(
        'eatman.inventory', 'inventory',
        help="Recette associé")
    company_id = fields.Many2one(
        'res.company', 'Company', related='inventory.company_id')


