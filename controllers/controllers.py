# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import http, _, exceptions

class ServiceService(http.Controller):
    @http.route('/get_service_data', auth='public', type='json', method='GET')
    def get_service_data(self):
        service_obj = request.env["service.service"].search([])
        service_data = []
        for serv in service_obj:
            vals = {
                'id': serv.id,
                'service_name': serv.name,
                'customer_id': serv.customer_id.id,
                'customer_name': serv.customer_id.name,
            }
            service_data.append(vals)
        data = {'status': 200, 
                'response': service_data,
                'message': 'Success'}
        return data

    
    @http.route('/create_service_data', auth='public', type='json', method='POST')
    def create_service_service_data(self, **rec):
        customer_obj = http.request.env['res.partner'].sudo()

        if rec['customerId']:
            search_customer = customer_obj.search(['&', '|', ('id', '=', rec['customerId']), 
                                                             ('name', '=', rec['customerName']), 
                                                             ('phone', '=', rec['phone'])])
            print("Search Customer", search_customer, type(search_customer))

            if search_customer:
                customer_id = search_customer.id
            else:
                message = _('Customer ID "%s" Not Found' %(rec['customerId']))
                return {'status': 404, 
                        'status': 'Not Found',
                        'message': message}
        else:
            message = _('Customer ID Required')
            return {'status': 404, 
                        'status': 'Not Found',
                        'message': message}

        service_line = rec['line']
        service_obj = request.env['service.service'].sudo()
        if rec['customerId']:
            vals = {'customer_id': customer_id,
                    'responsible_id': rec['responsibleId']}
            
            new_data = service_obj.sudo().create(vals)

            for line in service_line:
                service_line_obj = request.env['service.order.line'].sudo()
                
                vals_line = {'service_id': new_data.id,
                             'car_id': line['carId']}
                
                new_line = service_line_obj.sudo().create(vals_line)

            new_data.button_in_progress()
            data = {'status': 200, 
                    'service_id': new_data.id,
                    'service_name': new_data.name,
                    'message': 'Success'}
        return data

    
    @http.route('/update_service_data', auth='public', type='json', method='POST')
    def update_service_service_data(self, **kwargs):
        service_obj = http.request.env['service.service'].sudo()
        search_service = service_obj.search([('id', '=', kwargs['serviceId'])])

        if search_service:
            vals = {'email': kwargs['email'],
                    'description': kwargs['description']}

            search_service.sudo().write(vals)
            
            data = {'status': 200, 
                    'service_id': search_service.id,
                    'service_name': search_service.name,
                    'message': 'Success Updated'}
        else:
            search_service.sudo().create(vals)
            data = {'status': 400, 
                    'service_id': 'Not Found',
                    'service_name': 'Not Found',
                    'message': 'Failed Update'}
        
        return data

    @http.route('/delete_service_data', auth='public', type='json', method='POST')
    def delete_service_data(self, **kwargs):
        service_obj = http.request.env['service.service'].sudo()
        search_service = service_obj.search([('id', '=', kwargs['serviceId'])])

        if search_service:
            search_service.sudo().unlink()
            data = {'status': 200, 
                    'service_id': search_service.id,
                    'message': 'Success Deleted'}
        else:
            data = {'status': 400, 
                    'service_id': 'Not Found',
                    'message': 'Failed Deleted'}
        return data


    
