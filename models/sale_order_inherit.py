# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SOLineWeight(models.Model):
	_inherit = 'sale.order.line'

	total_weight = fields.Float(digits=(6, 2), string='Total Weight', default=1.00)

