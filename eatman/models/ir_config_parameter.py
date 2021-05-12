
from odoo import models, fields, api

import logging


class ResConfigParameter(models.Model):
    
    _inherit = "ir.config_parameter"
    turnover = fields.Float(string = "Chiffre d'affaire")