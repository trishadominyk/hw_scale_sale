# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplateWeight(models.Model):
	_inherit = 'product.template'

	weight_uom = fields.Many2one('product.uom', string='Weight Unit of Measure')