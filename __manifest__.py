# -*- coding: utf-8 -*-
{
    'name': "market_price",


    'description': """
        adds the price of the corn with the current value of the market
    """,

    'author': "pelek",

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
        'views/market_free.xml',
        'views/automated_price.xml',

        #'templates.xml',
    ],

}
