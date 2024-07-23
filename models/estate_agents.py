from odoo import fields, models


class Agents(models.Model):
    _name = 'agents'
    _description = 'Agents'


    name=fields.Char(required=True)
    age=fields.Integer()
    rating=fields.Selection(
        [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5')
        ]
    )