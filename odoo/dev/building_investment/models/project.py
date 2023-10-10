import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _name = "building_investment.project"
    _description = "Project"

    name = fields.Char(string="نام")
    date_land_sale = fields.Date(string="تاریخ خرید زمین")
    date_start = fields.Date(string="تاربخ شروع")
    date_end = fields.Date(string="تاریخ پایان")
    infrastructure = fields.Integer(string="زیربنا")
    infrastructure_pure = fields.Integer(string="زیربنای خالس")
    infrastructure_total = fields.Integer(string="زیربنای کل")
    daily_profit = fields.Float(string="سود روزانه")
