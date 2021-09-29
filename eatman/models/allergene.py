from odoo import models, fields, api

class allergene(models.Model):
    _name = 'eatman.allergene'
    _description = "Gestion des allergènes"
    
    name = fields.Char(string = "Description")
    decret = fields.Char(string = "Decret")
