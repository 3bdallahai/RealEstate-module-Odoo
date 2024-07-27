from odoo import api, fields, models, _
from datetime import timedelta
from odoo.exceptions import UserError

class Offer(models.Model):
    _name = 'offer'
    _description = 'Offer'
    _sql_constraints = [
        ("amount_positive","CHECK(amount>0)","excepected price should be positive"),   
                        ]
    _order="amount desc"


    amount =fields.Float(required=True)
    create_date=fields.Date(required=True, default=fields.Datetime.now)
    desired_estate_id = fields.Many2one("real.estate")
    validity =fields.Integer(required=True, default= 7)
    deadline_date   = fields.Date(compute="_compute_deadline_date"  )
    status = fields.Selection([("accepted", "accepted"),("rejected", "rejected")])

    @api.depends('create_date', 'validity')
    def _compute_deadline_date(self):
        for record in self:
            if record.create_date and record.validity is not None:
                create_date = fields.Date.from_string(record.create_date)
                record.deadline_date = create_date + timedelta(days=record.validity)

    def accept_action(self):
        self.ensure_one()
        if "accepted" in self.desired_estate_id.offers_ids.mapped('status'):
            raise UserError("property already sold")
        self.status= "accepted"
        self.desired_estate_id.state = "sold"
        self.desired_estate_id.selling_price= self.amount             

               
    def refuse_action(self):
        self.ensure_one()
        self.status= "rejected"

    @api.model
    def create(self, vals):
        # Create the offer record
        offer = super(Offer, self).create(vals)
        # Update the property state to 'received'
        if offer.desired_estate_id:
            offer.desired_estate_id.state = 'received'

        return offer    

 