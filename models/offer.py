from odoo import api, fields, models, _
from datetime import timedelta
from odoo.exceptions import UserError

class Offer(models.Model):
    _name = 'offer'
    _description = 'Offer'


    amount =fields.Float(required=True)
    create_date=fields.Date(required=True)
    desired_estate_id = fields.Many2one("real.estate")
    validity =fields.Integer(required=True)
    deadline_date   = fields.Date(compute="_compute_deadline_date"  )
    status = fields.Selection([("accepted", "accepted"),("rejected", "rejected")])

    @api.depends('create_date', 'validity')
    def _compute_deadline_date(self):
        for record in self:
            if record.create_date:
                create_date = fields.Date.from_string(record.create_date)
                record.deadline_date = create_date + timedelta(days=record.validity)

    def accept_action(self):
        self.ensure_one()
        if "accepted" in self.desired_estate_id.offers_ids.mapped('status'):
            raise UserError("property already sold")
        self.status= "accepted"
        self.desired_estate_id.state = "sold"
        self.desired_estate_id.selling_price= self.amount             

               
