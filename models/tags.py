from odoo import fields, models

class Tags(models.Model):
    _name ="tags"
    _description = "property tags"
    _sql_constraints = [
        ("unique_tag_name","UNIQUE(name)","Tag name should be unique")
    ]

    name = fields.Char(string="Tag Name", required=True)
    color =fields.Char()