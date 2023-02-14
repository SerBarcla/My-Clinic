{
    'name': 'MyClinic',
    'version': '1.0',
    'category': 'Health',
    'summary': 'Odoo app for managing a clinic',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/myclinic_views.xml',
        'views/prescription_views.xml',
        'views/configuration_views.xml',
        'views/patient_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
