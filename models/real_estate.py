from odoo import fields, models, api

class RealEstate(models.Model):
    _name = 'real.estate'
    _description = 'Test model'

    active = fields.Boolean(default=True, invisble=True)
    name= fields.Char(required=True)
    state =fields.Selection(
        [
        ("new","New"), 
        ("received","Offer Received"),
        ("accepted","Offer Accepted"),
        ("sold","Sold"),
        ("cacelled","Cancelled"),
        ],
        required=True,
        default="new",        
        copy=False,
    )
    postcode= fields.Char()
    address = fields.Char()

    def _defualt_date(self):
        return fields.Date.today()
    
    owner_id = fields.Many2one('estate.owner') 
    description= fields.Char(string="description")
    date_available= fields.Date(default=_defualt_date)
    excepected_price = fields.Float()
    best_offer = fields.Float(compute='_compute_max_offer')    
    selling_price = fields.Float(readonly=True)
    living_area = fields.Integer(string="Living Area (sqm)")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [
         ("north","North"),
         ("south","South"),
         ("east","East"),
         ("west","West"),  
        ]
    )


    total_area = fields.Float(string='Total Area', compute='_compute_total_area')
    offers_ids= fields.One2many("offer","desired_estate_id") 


    @api.depends('living_area', 'garden_area')  
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area       
      
    @api.depends("offers_ids.amount")
    def _compute_max_offer(self):
        for rec in self:
            if rec.offers_ids:
                rec.best_offer = max(rec.offers_ids.mapped('amount'))
            else:
                rec.best_offer = 0.0   

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0
                record.garden_orientation= ''

    @api.onchange("date_available")  
    def _onchange_date_available(self):
        for record in self:
            if record.date_available < fields.Date.today():
                return{
                    "warning":{
                        "title": ("Warning"),
                        "message": ("date invalid")
                    }
                }        

    def sold_action(self):
        for record in self:
            record.state = "sold"
            record.selling_price = record.best_offer

