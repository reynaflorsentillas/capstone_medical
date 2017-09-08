# -*- coding: utf-8 -*-
{
    'name': "Medical Website",

    'summary': """
        Website module of medical""",

    'description': """
        - Allow website visitors to submit appointment through a form
    """,

    'author': "Capstone Solutions Inc.",
    'website': "http://www.capstone.ph",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Medical',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_form'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/website_data.xml',
        'views/medical_appointment_online_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}