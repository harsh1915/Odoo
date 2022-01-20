from email.policy import default
from odoo import models,fields,api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _rec_name = 'property_id'

    price = fields.Float()
    status = fields.Selection([
        ("accepted","Accepted"),
        ("refused","Refused")
        ])

    partner_id = fields.Many2one("res.partner")
    property_id = fields.Many2one("estate.property")

    def action_accepted(self):
        for record in self:
            record.status = "accepted"

    def action_refused(self):
        for record in self:
            record.status= "refused"

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char()

class  EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Estate Property Type"

    name = fields.Char()

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    
    
    name = fields.Char(default = "Unkhown",required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default = lambda self: fields.Datetime.now(), copy= False)
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(copy= False, readonly = True)
    bedrooms = fields.Integer(default= 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
    	("north", "North"),
    	("south", "South"),
    	("east", "East"),
    	("west", "West")
    	])
    active = fields.Boolean(default=True)
    image = fields.Image()
    property_type_id = fields.Many2one("estate.property.type")
    salesman_id = fields.Many2one("res.users")
    buyer_id = fields.Many2one("res.partner")
    property_tag_id = fields.Many2many("estate.property.tag")
    property_offer_id = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_area", inverse="_inverse_area")
    best_price = fields.Float(compute="_compute_best_price")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline")
    offer_state=fields.Selection([
        ("new", "New"),
        ("sold", "Sold"),
        ("cancel", "Canceled")
    ])


    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area=1000
                record.garden_orientation="north"
            else:
                record.garden_area=0
                record.garden_orientation=None


    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.date_availability, days=record.validity)


    def _inverse_area(self):
        for record in self:
            record.living_area = record.garden_area = record.total_area/2

    @api.depends("property_offer_id.price")
    def _compute_best_price(self):
        for record in self:
            max_price=0
            for offer in record.property_offer_id:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_price = max_price

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def action_sold(self):
        for record in self:
            record.offer_state="sold"

    def action_cancel(self):
        for record in self:
            record.offer_state="cancel"