# -*- coding: utf-8 -*-
from odoo import models, fields, api
import feedparser
import logging
import datetime
import pytz
import requests
import limit

_logger = logging.getLogger(__name__)
#  _logger.erro()


class market_price(models.Model):
    _name = 'market.price'

    _defaults = {'name': lambda obj, cr, uid, context: obj.pool.get(
         'ir.sequence').get(cr, uid, 'reg_code_mp'), }

    @api.one
    @api.depends('price_ton', 'date')
    def _compute_mx(self):
        if self.date:
            self.usd = self.env['market.usd'].search(
                [("date", "=", self.date)], limit=1)
            self.price_mx = self.price_ton * self.usd.exchange_rate


    name = fields.Char()
    date = fields.Date(required=True, default=fields.Date.today)
    price_ton = fields.Float(required=True)
    price_mx = fields.Float(compute="_compute_mx", store=True)
    hour_create = fields.Char(compute="_compute_hour", store=True)

    @api.one
    @api.depends('price_ton', 'date')
    def _compute_hour(self):
        local = pytz.timezone("America/Chihuahua")
         # _logger.warning(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        utc = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
        local_hr = local.localize(utc, is_dst=None)
        utc_hr = local_hr.astimezone(pytz.utc)
        self.hour_create = utc_hr.strftime("%Y-%m-%d %I:%M %Z%z")[10:16]


    @api.multi
    def quandl(self):
        base = self.env['market.base'].search([], order='id DESC', limit=1)
        resp = requests.get(base['url_price_corn'])
        if resp.status_code != 200:
            _logger.error("Error to get price corn to quandl")
        response = resp.json()
        if response['dataset']['dataset_code'] == "CH2018":
            # if response['dataset']['newest_available_date'] ==
            # datetime.date.today():
            print (response['dataset']['newest_available_date'])
            base = self.env['market.base'].search([], order='id DESC', limit=1)
            self.price_ton = (response['dataset']['data'][0][6] * 0.3936825) + base['base']

    @api.model
    def quandl_auto(self):
        base = self.env['market.base'].search([], order='id DESC', limit=1)
        resp = requests.get(base['url_price_corn'])
        if resp.status_code != 200:
            _logger.error("Error to get price corn to quandl")
        response = resp.json()
        if response['dataset']['dataset_code'] == "CH2018":
            # if response['dataset']['newest_available_date'] ==
            # datetime.date.today():
            date = datetime.date.today()
            base = self.env['market.base'].search([], order='id DESC', limit=1)
            price_ton = (response['dataset']['data'][0][6] * 0.3936825) + base['base']
            tc = self.env['market.usd'].search(
                [("date", "=", date)], limit=1)
            pricemx = price_ton * tc.exchange_rate
            local = pytz.timezone("America/Chihuahua")
            utc = datetime.datetime.strptime(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
            local_hr = local.localize(utc, is_dst=None)
            utc_hr = local_hr.astimezone(pytz.utc)
            self.env['market.price'].create({
                                    'date': date,
                                    'price_ton': price_ton,
                                    'price_mx': pricemx,
                                    'hour_create': utc_hr.strftime("%Y-%m-%d %I:%M %Z%z")[10:16]})


class market_price_usd(models.Model):

    _name = 'market.usd'

    _defaults = {'name': lambda obj, cr, uid, context: obj.pool.get(
        'ir.sequence').get(cr, uid, 'reg_code_mu'), }

    name = fields.Char()

    date = fields.Date(required=True, default=fields.Date.today)
    exchange_rate = fields.Float()

    @api.one
    def banxico(self):
        rss_url = "http://www.banxico.org.mx/rsscb/rss?BMXC_canal=fix&BMXC_idioma=es"
        feeds = feedparser.parse(rss_url)
        for feed in feeds["items"]:
            title = feed["title"]
        self.exchange_rate = float(title[4:11])

    @api.model
    def banxico_auto(self):
        date = datetime.date.today()
        rss_url = "http://www.banxico.org.mx/rsscb/rss?BMXC_canal=fix&BMXC_idioma=es"
        feeds = feedparser.parse(rss_url)
        for feed in feeds["items"]:
            title = feed["title"]
        self.env['market.usd'].create({
                                'date': date,
                                'exchange_rate': float(title[4:11])
        })
        # _logger.info("ok")

    _sql_constraints = [
        ('date_unique',
        'UNIQUE(date)',
        "Solo se permite un tipo de cambio por dia"),
    ]


class market_price_base(models.Model):
    _name = 'market.base'

    _defaults = {'name': lambda obj, cr, uid, context: obj.pool.get(
        'ir.sequence').get(cr, uid, 'reg_code_mb'), }

    name = fields.Char()

    season = fields.Char(required=True)
    base = fields.Float(required=True, help="Currency USD")
    cost = fields.Float()
    price_min = fields.Float()
    url_price_corn = fields.Char(
        required=True, help="This url is from de page www.quandl.com that correspond to web service")
