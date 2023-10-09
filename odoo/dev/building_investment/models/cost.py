import logging
from odoo import api, models, fields

_logger = logging.getLogger(__name__)


class CostType(models.Model):
    _name = "building_investment.costtype"
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(string="نام")
    parent_id = fields.Many2one('building_investment.costtype', string='پدر', index=True)
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('building_investment.costtype', inverse_name='parent_id', string='فرزندان')
