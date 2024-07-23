from odoo import models, fields

class EstateOwner(models.Model):
    _name = 'estate.owner'
    _description = 'Estate Owner'

    name = fields.Char(string='owner_Name')
    phone_number = fields.Char(string='Phone Number')
    address = fields.Text(string='Address')
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], string='Status')
    wealth= fields.Float()
    estate_ids = fields.One2many('real.estate', 'owner_id')
    

