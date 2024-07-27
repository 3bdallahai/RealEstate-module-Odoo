from odoo import fields, models, api, _

class PropertyType(models.Model):
    _name = 'property.type'
    _description ='types' 
    _sql_constrain = ("unique_type_name","UNIQUE(name)","type name should be unique")

    name = fields.Char(required=True)
    property_ids=fields.One2many("real.estate","type_id" ) 
    property_count = fields.Integer(compute="_compute_property_count")

    @api.depends('property_ids')
    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)

    def action_open_property_ids(self):
        return {
            "name": _("Related Properties"),
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "real.estate",
            "target": "current",
            "domain": [('type_id', '=', self.id)],
            "context": {'default_type_id': self.id}
        }        

