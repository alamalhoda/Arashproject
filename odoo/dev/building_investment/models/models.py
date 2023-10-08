import logging

import jdatetime
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


@api.model
def _default_project(self):
    # return self.env['building_investment.project'].search([('name', '=', 'Head/Branch')], limit=1).id
    return self.env['building_investment.project'].search([], limit=1).id
    # _logger.debug(self.env['building_investment.project'].search([('id', '=', 1)], limit=1))
    # return 1


class Investment(models.Model):
    _name = 'building_investment.investment'
    _description = 'Investment'

    INVESTMENT_TYPE = [("1", "واریز"), ("2", "سود"), ("3", "برداشت")]
    amount = fields.Float(string='مبلغ')
    investor_id = fields.Many2one('building_investment.investor', string='سرمایه گزار')
    date = fields.Date(string='تاریخ')
    date_shamsi = fields.Char(string='تاریخ شمسی', compute='_compute_date_shamsi')
    display_name = fields.Char(compute='_compute_display_name', store=True, string='Display Name')
    investment_type = fields.Selection(INVESTMENT_TYPE, string="نوع", default=INVESTMENT_TYPE[0][0])
    is_profie_calculated = fields.Boolean(string="محاسبه سود", default=False)
    project_id = fields.Many2one('building_investment.project', string='پروژه', default=_default_project)
    day_of_project = fields.Integer(string='روز پروژه', compute='_compute_day_of_project')

    @api.model
    def create(self, vals):
        _logger.debug("...........create model %s", "investment")
        return super().create(vals)

    @api.depends('date')
    def _compute_date_shamsi(self):
        # _logger.debug(self.date)
        for record in self:
            if record.date:
                record.date_shamsi = str(jdatetime.date.fromgregorian(date=record.date))
            else:
                record.date_shamsi = None

    @api.depends('date')
    def _compute_day_of_project(self):
        for record in self:
            if record.date:
                timedelta = record.project_id.date_end - record.date
                record.day_of_project = timedelta.days + 1
            else:
                record.day_of_project = None

    @api.depends('investor_id', 'date', 'amount')
    def _compute_display_name(self):
        for record in self:
            _logger.warning(f"{record.investor_id.display_name}")
            record.display_name = f"{record.investor_id.display_name} ({record.date}) ({record.amount})"

    @api.onchange('amount')
    def _onchange_amount_currency(self):
        # اینجا می‌توانید تغییرات مقادیر مرتبط را پس از تغییر مبلغ انجام دهید
        pass

    def invest(self):
        # اینجا می‌توانید عملیات لازم برای سرمایه‌گذاری را انجام دهید
        pass


class Investor(models.Model):
    # _inherit = 'res.partner'
    _name = 'building_investment.investor'
    _description = 'Investor'
    _rec_name = 'display_name'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='cascade')

    investments = fields.One2many('building_investment.investment', 'investor_id', string='Investments')
    display_name = fields.Char(compute='_compute_display_name', store=True, string='Display Name')

    @api.depends('partner_id')
    def _compute_display_name(self):
        for record in self:
            _logger.warning(f"{record.partner_id.name}")
            record.display_name = f"{record.partner_id.name}"


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
