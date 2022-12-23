from odoo import models, fields, api, _

class ServiceWizard(models.TransientModel):
    _name = 'service.service.wizard'
    _description = 'Service Wizard'

    service_id = fields.Many2one('service.service', string="Service ID")
    description = fields.Text(string="Description")

    # def action_confirm(self):
    #     active_id = self.env.context.get('active_id')
    #     service = self.env['service.service'].browse(active_id)
    #     if service:
    #         service.description = self.description

    # @api.model
    # def default_get(self, fields):
    #     res = super(ServiceWizard, self).default_get(fields)
    #     if self.env.context.get('active_id') and self.env.context.get('active_model') == 'service.service':
    #         service = self.env['service.service'].browse(self.env.context.get('active_id'))
    #         if service.exists():
    #             res.update({'description': service.email})
    #     return res
