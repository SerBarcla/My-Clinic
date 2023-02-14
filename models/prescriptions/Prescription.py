from odoo import models, fields, api

class Prescription(models.Model):
    _name = 'myclinic.prescription'
    _description = 'Prescription'
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient = fields.Many2one('res.partner', string='Patient', domain=[('is_patient','=',True)], required=True, ondelete='cascade')
    doctor = fields.Many2one('res.users', string='Doctor', default=lambda self: self.env.user, required=True)
    prescription_line = fields.One2many('myclinic.prescription.line', 'prescription_id', string='Prescription Lines')
    prescription_date = fields.Datetime(string='Prescription Date', default=fields.Datetime.now)
    stage = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('cancelled', 'Cancelled')], string='Stage', default='draft', required=True)
    user_type = fields.Selection([('internal', 'Internal'), ('admin', 'Admin')], string='User Type', compute='_compute_user_type', store=True)

    # Automated name format
    def name_get(self):
        result = []
        for record in self:
            pr_no = self.env['ir.sequence'].next_by_code('myclinic.prescription.sequence')
            name = f"Pres{pr_no}"
            result.append((record.id, name))
        return result
    
    @api.depends('stage')
    def _compute_user_type(self):
        for record in self:
            if record.stage == 'draft':
                record.user_type = 'internal'
            else:
                record.user_type = 'admin'
