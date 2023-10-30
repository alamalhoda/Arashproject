import datetime
import logging

import jdatetime
from odoo import models, fields, api
from odoo.modules import module

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
    _order = 'date desc, investor_id, investment_type'

    INVESTMENT_TYPE = [("1", "واریز"), ("2", "سود"), ("3", "برداشت")]
    amount = fields.Float(string='مبلغ', digits=(16, 0))
    investor_id = fields.Many2one('building_investment.investor', string='سرمایه گزار')
    date = fields.Date(string='تاریخ', required=True)
    date_shamsi = fields.Char(string='تاریخ شمسی', compute='_compute_date_shamsi', store=True)
    date_shamsi_year = fields.Char(string='تاریخ شمسی-سال', compute='_compute_date_shamsi_year', store=True)
    date_shamsi_year_month = fields.Char(string='تاریخ شمسی-سال-ماه', compute='_compute_date_shamsi_year_month',
                                         store=True)
    display_name = fields.Char(compute='_compute_display_name', store=True, string='Display Name')
    investment_type = fields.Selection(INVESTMENT_TYPE, string="نوع", default=INVESTMENT_TYPE[0][0])
    is_profie_calculated = fields.Boolean(string="محاسبه سود", default=False)
    calculat_profite = fields.Boolean(string="آیا سود محاسبه شود؟", default=True)
    project_id = fields.Many2one('building_investment.project', string='پروژه', default=_default_project)
    day_of_project = fields.Integer(string='روز پروژه', compute='_compute_day_of_project')
    convert = fields.Boolean(string='convert', default=False)  # کانورت اطلاعات از فایل اکسل

    @api.model
    def create(self, vals):
        _logger.debug("...........create model %s", "investment")
        # هنگام کانورت اطلاعات از فایل اکسل تاریخ شمسی به میلادی تبدیل و ذخیره میگردد
        if vals.get('convert') and vals.get('date_shamsi'):
            shamsi_date = vals.get('date_shamsi').split('/')
            shamsi_date_year = int(shamsi_date[0])
            shamsi_date_month = int(shamsi_date[1])
            shamsi_date_day = int(shamsi_date[2])

            gregorian_date = jdatetime.jalali.JalaliToGregorian(shamsi_date_year, shamsi_date_month, shamsi_date_day)
            gregorian_date = datetime.date(gregorian_date.gyear, gregorian_date.gmonth, gregorian_date.gday)
            vals['date'] = gregorian_date
        # هنگام ایجاد اگر تاریخ شمسی نداشت ایجاد میکند
        if vals.get('date') and not vals.get('date_shamsi'):
            gregorian_date = vals.get('date')
            shamsi_date = jdatetime.date.fromgregorian(date=gregorian_date).strftime("%Y/%m/%d")
            vals['date_shamsi'] = shamsi_date
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

    @api.depends('date', 'project_id.date_end')
    def _compute_day_of_project(self):
        for record in self:
            if record.date and record.project_id.date_end:
                timedelta = record.project_id.date_end - record.date
                record.day_of_project = timedelta.days + 1
            else:
                record.day_of_project = None

    @api.depends('date')
    def _compute_date_shamsi(self):
        for record in self:
            gregorian_date = record.date
            record.date_shamsi = jdatetime.date.fromgregorian(date=gregorian_date).strftime("%Y/%m/%d")

    @api.depends('date')
    def _compute_date_shamsi_year(self):
        for record in self:
            gregorian_date = record.date
            sh = jdatetime.date.fromgregorian(date=gregorian_date)
            record.date_shamsi_year = sh.year

    @api.depends('date')
    def _compute_date_shamsi_year_month(self):
        for record in self:
            try:
                gregorian_date = record.date
                sh = jdatetime.date.fromgregorian(date=gregorian_date)
                record.date_shamsi_year_month = f"{sh.year}-{sh.month:02}({sh.j_months_fa[sh.month - 1]})"
            except Exception as e:
                _logger.debug(f"........_compute_date_shamsi_year_month {record.id} ----- {e}")

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
        _logger.debug(".........invest ................")
        print(self.amount)
        pass

    def _compute_profite(self):
        days = self.day_of_project
        profite_per_day = self.project_id.daily_profit
        # محاسبه سود بر اساس روز پروژه و مبلغ و درصد سود روزانه
        calculated_profite = self.amount * days * profite_per_day
        return calculated_profite

    def _create_profite(self):
        # ایجاد رکورد سود
        new_profite = self.env['building_investment.investment'].create({
            'amount': self._compute_profite(),
            'investor_id': self.investor_id.id,  # به .id توجه شود
            'date': self.date,
            'investment_type': "2"  # سود
        })
        _logger.debug(f"........._create_profite for : {self.display_name} ................")
        return new_profite

    def compute_profite_action(self):
        new_profite = self._create_profite()
        _logger.debug(f"......................دکمه محاسبه سود................................")
        # self.env.notify_info("سود created")
        # self._notify_info("طود created")
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'ذخیره سود',
                'message': f"سود برای '{new_profite.investor_id.display_name}' به مبلغ '{new_profite.amount}' ایجاد شد.",
                'sticky': True,
                'buttons': [
                    {'text': 'Ok', 'icon': 'fa-check'},
                    {'text': 'Cancel', 'icon': 'fa-close'},
                ]
            }
        }

    def action_calculate_profit(self):
        """
        دکمه محاسبه سود در لیست سرمایه گزاری ها برای محاسبه سود چند رکورد با هم
        :return:
        """
        selected_records = self.env.context.get('active_ids', [])  # دریافت رکوردهای انتخاب شده
        for record in self.env['building_investment.investment'].browse(selected_records):
            # calculate profit 
            # record.profit = ... 
            # record.write()
            record._create_profite()
            _logger.debug(f"--------------------------------{record}")

        return {'type': 'ir.actions.act_window_close'}


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
    sum_of_investments = fields.Float(compute='_compute_sum_of_investments', store=True, digits=(16, 0),
                                      string="موجودی کل")
    sum_of_variz = fields.Float(compute='_compute_sum_of_variz', store=True, digits=(16, 0), string="مجموع واریز")
    sum_of_profite = fields.Float(compute='_compute_sum_of_profite', store=True, digits=(16, 0), string="مجموع سود")
    sum_of_bardasht = fields.Float(compute='_compute_sum_of_bardasht', store=True, digits=(16, 0),
                                   string="مجموع برداشت")
    sum_of_variz_bardasht = fields.Float(compute='_compute_sum_of_variz_bardasht', store=False, digits=(16, 0),
                                         string="واریز + برداشت")

    @api.depends('name', 'family')
    def _compute_display_name(self):
        for record in self:
            # _logger.warning(f"{record.partner_id.name}")
            record.display_name = f"{record.name} {record.family}"

    @api.depends('investments')
    def _compute_sum_of_investments(self):
        for record in self:
            record.sum_of_investments = sum(investment.amount for investment in record.investments)

    @api.depends('investments')
    def _compute_sum_of_variz(self):
        for record in self:
            record.sum_of_variz = sum(
                investment.amount for investment in record.investments if investment.investment_type == "1")

    @api.depends('investments')
    def _compute_sum_of_profite(self):
        for record in self:
            record.sum_of_profite = sum(
                investment.amount for investment in record.investments if investment.investment_type == "2")

    @api.depends('investments')
    def _compute_sum_of_bardasht(self):
        for record in self:
            record.sum_of_bardasht = sum(
                investment.amount for investment in record.investments if investment.investment_type == "3")

    def _compute_sum_of_variz_bardasht(self):
        for record in self:
            record.sum_of_variz_bardasht = sum(
                investment.amount for investment in record.investments if investment.investment_type != "2")

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
            'sel_groups_1_9_10': 9,
            # این مقدار به مدل res.users می گوید که کاربر جدید باید به گروه group_portal_user اضافه شود
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