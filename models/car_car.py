# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xmlrpc.client

class CarCar(models.Model):
    _name = 'car.car'
    _description = 'Car'
    
    name                = fields.Char(string="Name")
    car_type_id         = fields.Many2one('car.type', string="Car Type")

    def xml_rpc_create_service(self):
        url_data = self.env['ir.config_parameter'].sudo().get_param('data_url')
        url_db = self.env['ir.config_parameter'].sudo().get_param('data_db')
        url_username = self.env['ir.config_parameter'].sudo().get_param('data_username')
        url_password = self.env['ir.config_parameter'].sudo().get_param('data_password')
        
        url = url_data
        db = url_db
        username = url_username
        password = url_password

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        
        model = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        create_service = model.execute_kw(db, uid, password, 'service.service', 'create', [{'partner_id': 7, 'car_id': 1, 'responsible_id': 2}])


class CarType(models.Model):
    _name = 'car.type'
    _description = 'Car Type'
    
    name                = fields.Char(string="Name")