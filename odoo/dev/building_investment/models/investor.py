import datetime
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
    date = fields.Date(string='تاریخ', required=True)
    date_shamsi = fields.Char(string='تاریخ شمسی')
    display_name = fields.Char(compute='_compute_display_name', store=True, string='Display Name')
    investment_type = fields.Selection(INVESTMENT_TYPE, string="نوع", default=INVESTMENT_TYPE[0][0])
    is_profie_calculated = fields.Boolean(string="محاسبه سود", default=False)
    project_id = fields.Many2one('building_investment.project', string='پروژه', default=_default_project)
    day_of_project = fields.Integer(string='روز پروژه', compute='_compute_day_of_project')
    convert = fields.Boolean(string='convert', default=False) # کانورت اطلاعات از فایل اکسل
    @api.model
    def create(self, vals):
        _logger.debug("...........create model %s", "investment")
        #هنگام کانورت اطلاعات از فایل اکسل تاریخ شمسی به میلادی تبدیل و ذخیره میگردد
        if vals.get('convert') and vals.get('date_shamsi'):
            shamsi_date = vals.get('date_shamsi').split('/')
            shamsi_date_year = int(shamsi_date[0])
            shamsi_date_month = int(shamsi_date[1])
            shamsi_date_day = int(shamsi_date[2])

            gregorian_date = jdatetime.jalali.JalaliToGregorian(shamsi_date_year, shamsi_date_month, shamsi_date_day)
            gregorian_date = datetime.date(gregorian_date.gyear, gregorian_date.gmonth, gregorian_date.gday)
            vals['date'] = gregorian_date
            _logger.debug("...........create Investment %s ............", gregorian_date)
        return super().create(vals)

    # @api.depends('date')
    # def _compute_date_shamsi(self):
    #     # _logger.debug(self.date)
    #     for record in self:
    #         # if record.date:
    #         #     record.date_shamsi = str(jdatetime.date.fromgregorian(date=record.date))
    #         # else:
    #         #     record.date_shamsi = None
    #         record.date_shamsi = None

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

    user_id = fields.Many2one('res.users', string='کاربر', required=True, ondelete='restrict')
    user_name = fields.Char(string='نام کاربری', required=True)
    name = fields.Char(string='نام', required=True)
    family = fields.Char(string='نام خانوادگی', required=True)
    code_meli = fields.Char(string='کدملی')
    tel = fields.Char(string='تلفن')
    mobile1 = fields.Char(string='موبایل۱')
    mobile2 = fields.Char(string='موبایل۲')
    email = fields.Char(string='ایمیل')
    address = fields.Char(string='آدرس')
    investments = fields.One2many('building_investment.investment', 'investor_id', string='Investments')
    display_name = fields.Char(compute='_compute_display_name', store=True, string='Display Name')
    sum_of_investments = fields.Integer(compute='_compute_sum_of_investments', store=True)

    @api.depends('name', 'family')
    def _compute_display_name(self):
        for record in self:
            # _logger.warning(f"{record.partner_id.name}")
            record.display_name = f"{record.name}  {record.family}"

    @api.depends('investments')
    def _compute_sum_of_investments(self):
        for record in self:
            record.sum_of_investments = sum(investment.amount for investment in record.investments)

    def _create_user(self, name: str, user_name: str):
        """
         ایجاد یک کاربر جدید
        از نوع پرتال

        Args:
            name (str): نام کاربر
            user_name (str): نام کاربری

        Returns:
            کاربر جدید
        """
        return self.env['res.users'].create({
            'name': name,
            'login': user_name,
            'sel_groups_1_9_10': 9,  # این مقدار به مدل res.users می گوید که کاربر جدید باید به گروه group_portal_user اضافه شود
        })

    @api.model
    def create(self, vals):
        if not vals.get('user_id'):
            name = vals.get('name')
            family = vals.get('family')
            user_name = vals.get('user_name')

            existing_user = self.env['res.users'].search([('login', '=', user_name)], limit=1)
            if not existing_user:
                user = self._create_user(name + ' ' + family, user_name)
                vals['user_id'] = user.id
        return super(Investor, self).create(vals)
