# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ServiceService(models.Model):
    _name = 'service.service'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Service Order'
    
    @api.model
    def create(self, values):
        record = super(ServiceService, self).create(values)
        record['name'] = self.env['ir.sequence'].next_by_code('service.service.sequence') or 'New'
        return record

    @api.model
    def subtotal_report(self):
        for rec in self:
            total = 0.0
            for line in rec.service_line_ids:
                total += line.price_subtotal
        
        return total

    name                = fields.Char(string="Name")
    # active              = fields.Boolean(string="Active", default=True)

    #customer
    customer_id         = fields.Many2one('res.partner', string="Customer", required=True, default=1)
    phone               = fields.Char(string="Phone")
    email               = fields.Char(string="Email", default="Email Default")

    #responsible
    is_mandatory        = fields.Boolean(string="Mandatory?")
    responsible_id      = fields.Many2one('res.users',string="Responsible")

    description         = fields.Text(string="Description")
    state               = fields.Selection([('draft','Draft'),
                                            ('in_progress','In Progress'),
                                            ('done','Done')], default='draft', string="State", tracking=True)

    service_line_ids    = fields.One2many('service.order.line', 'service_id', string="Service Line")

    
    def button_in_progress(self):
        print("Current State", self.state, type(self.state))

        self.state = 'in_progress'
        
        print("New State", self.state, type(self.state))
        self.is_mandatory = True
        self.description = "Running function from API Create"

        
    @api.onchange('customer_id')
    def onchange_customer(self):
        for i in self:
            if i.customer_id:
                i.phone = "+62-8123-3244-2321"
                i.email = "oncahnge.email@gmail.com"

    def function_server_action(self):
        for i in self:
            i.is_mandatory = True
            i.description = "Server Action and Scheduler Success"

    @api.model
    def scheduler_function(self):
        service = self.env["service.service"].search([('is_mandatory', '=', False)])
        for serv in service:
            serv.function_server_action()

    def open_wizard(self):
        return {
                'name': _('Wizard'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'service.service.wizard',
                'target': 'new',
                'context': {
                    'default_service_id': self.ids[0],
                    }
            }


class ServiceOrderLine(models.Model):
    _name = 'service.order.line'
    _description = 'Service Order Line'

    service_id      = fields.Many2one('service.service', string="Service ID")
    name            = fields.Char(string="Name")

    car_id          = fields.Many2one('car.car', string="Car")
    car_type_id     = fields.Many2one('car.type', string="Car Type")
    quantity        = fields.Float(string="Qty")
    price_unit      = fields.Float(string="Price Unit")
    price_subtotal  = fields.Float(string="Subtotal", compute='depends_quantity', store=True)

    @api.depends('quantity', 'price_unit')
    def depends_quantity(self):
        for i in self:
            if i.quantity:
                i.price_subtotal = i.quantity * i.price_unit
            else:
                i.price_subtotal = 0

    @api.onchange('car_id')
    def onchange_car_id(self):
        for i in self:
            if i.car_id:
                i.car_type_id = i.car_id.car_type_id.id
                i.name = i.car_id.name


class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    service_id  = fields.Many2one('service.service', string="Service No")
    description = fields.Char(string="Description")

    def button_inherit_function(self):
        for i in self:
            i.description = "Sukses Hit Function"


    def action_confirm(self):
        res = super(InheritSaleOrder, self).action_confirm()
        self.service_id = 5
        self.button_inherit_function()

        return res