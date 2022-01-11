from odoo import models,fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate_Property"
    
    
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
    	("North", "North"),
    	("South", "South"),
    	("East", "East"),
    	("West", "West")
    	])
    active = fields.Boolean(default=True)