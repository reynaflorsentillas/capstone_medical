# -*- coding: utf-8 -*-
{
    'name': "medical_base",

    'summary': """
        Medical Base""",

    'description': """
        Base of Medical Solution.
        - Patient
        - Patient Family
        - Ethnic Group 
        - Health Professionals
        - Appointments
    """,

    'author': "Capstone Solutions Inc.",
    'website': "http://www.capstone.ph",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Medical',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/medical_security.xml',
        'data/ir_sequence_data.xml',
        'data/medical_specialty_data.xml',
        'data/medical_ethnic_group_data.xml',
        'data/medical_appointment_stage_data.xml',
        'views/res_partner_view.xml',
        'views/product_product_view.xml',
        'views/medical_specialty_view.xml',
        'views/medical_ethnic_group_view.xml',
        'views/medical_physician_view.xml',
        'views/medical_patient_family_view.xml',
        'views/medical_patient_view.xml',
        'views/medical_appointment_view.xml',
        'views/medical_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}