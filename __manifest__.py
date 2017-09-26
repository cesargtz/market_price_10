# -*- coding: utf-8 -*-
{
    'name': "market_price",


    'description': """
        adds the price of the corn with the current value of the market
    """,

    'author': "Yecora",
    'website': "yecora.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        'security/market_access.xml',
        'security/ir.model.access.csv',
        'views/market_price.xml',
        'views/market_usd.xml',
        'views/market_base.xml',
        'views/automated_price.xml',
        
        #'templates.xml',
    ],

}
