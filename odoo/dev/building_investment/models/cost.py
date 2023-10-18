import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class CostType(models.Model):
    _name = "building_investment.costtype"
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(string="نام")
    parent_id = fields.Many2one('building_investment.costtype', string='پدر', index=True)
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('building_investment.costtype', inverse_name='parent_id', string='فرزندان')
    cost_ids = fields.Many2one('building_investment.cost')



class Cost(models.Model):
    _name = "building_investment.cost"
    _description = "هزینه ها"

    name = fields.Char(string="عنوان")
    date = fields.Date(string="تاریخ")
    costtype_id = fields.One2many('building_investment.costtype', inverse_name="cost_ids",string="مرکز هزینه")
    amount = fields.Float(string="مبلغ")