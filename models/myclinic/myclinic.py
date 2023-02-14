from odoo import api, fields, models, _


class MyClinic(models.Model):
    _name = 'myclinic.myclinic'
    _description = 'MyClinic'
    _order = 'id desc'
    
    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient = fields.Many2one('res.partner', string='Patient', domain=[('is_patient','=',True)], required=True, ondelete='cascade')
    medical_aid_scheme = fields.Char(string='Medical Aid Scheme')
    scheme_code = fields.Char(string='Scheme Code')
    age = fields.Integer(string='Age')
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Sex')
    blood_pressure = fields.Char(string='Blood Pressure')
    temperature = fields.Float(string='Temperature')
    spo2 = fields.Float(string='SPO2')
    pulse = fields.Float(string='Pulse')
    blood_sugar = fields.Float(string='Blood Sugar')
    height = fields.Float(string='Height (cm)')
    mass = fields.Float(string='Mass (kg)')
    bmi = fields.Float(string='BMI', compute='_compute_bmi')
    complaint = fields.Text(string='Complaint')
    diagnosis = fields.Text(string='Diagnosis')
    icd_diagnosis = fields.Many2one('myclinic.icd', string='ICD Diagnosis')
    treatment = fields.Text(string='Treatment')
    prescription = fields.Many2many('myclinic.prescription', string='Prescription')
    stage = fields.Selection([('arrival', 'Arrival'), ('screening', 'Screening'), ('waiting_room', 'Waiting Room'), ('consultation', 'Consultation'), ('done', 'Done'), ('cancelled', 'Cancelled')], string='Stage', default='arrival', required=True)
    user_type = fields.Selection([('internal', 'Internal'), ('admin', 'Admin')], string='User Type', compute='_compute_user_type', store=True)
    
    #convert to product
     @api.model
    def create(self, vals):
        record = super(MyClinic, self).create(vals)
        product = self.env['product.product'].create({
            'name': record.name
        })
        record.product_id = product.id
        return record

    # Automated name in format "PRNo:yymm0####"
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            pr_no = self.env['ir.sequence'].next_by_code('myclinic.prno.sequence')
            vals['name'] = f"PRNo:{pr_no}"
        return super(MyClinic, self).create(vals)

    @api.depends('mass', 'height')
    def _compute_bmi(self):
        for record in self:
            if record.mass and record.height:
                record.bmi = (record.mass / (record.height / 100) ** 2)
            else:
                record.bmi = 0
    
    @api.depends('stage')
    def _compute_user_type(self):
        for record in self:
            if record.stage in ('arrival', 'screening', 'waiting_room'):
                record.user_type = 'internal'
            else:
                record.user_type = 'admin'
