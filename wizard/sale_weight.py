# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
import math


class ChangeSaleWeight(models.TransientModel):
	_name = 'sale.order.weight'
	_description = 'Sale set weight with weighing scale'

	orderline_id = fields.Many2one('sale.order.line', 'Sale Order Line', required=True)
	product_uom_qty = fields.Float(digits=(5, 2), required=True)
	# price_subtotal = fields.Monetary(string='Subtotal', readonly=True, store=True)

	@api.model
	def default_get(self,fields):
		res = super(ChangeSaleWeight, self).default_get(fields)

		if 'orderline_id' in fields and not res.get('orderline_id') and self._context.get('active_model') == 'sale.order.line' and self._context.get('active_id'):
			res['orderline_id'] = self._context['active_id']
		if 'product_uom_qty' in fields and not res.get('qty') and res.get('orderline_id'):
			res['product_uom_qty'] = self.env['sale.order.line'].browse(res.get['orderline_id']).product_qty
		# if 'price_subtotal' in fields and not res.get('price_subtotal') and res.get('orderline_id'):
		# 	res['price_subtotal'] = self.env['sale.order.line'].browse(res.get['orderline_id']).price_subtotal

	@api.multi
	def set_weight(self):
		for wizard in self:
			order = wizard.orderline_id
			order.write({'product_uom_qty': wizard.product_uom_qty, 'price_subtotal': wizard.price_subtotal})

	# @api.depends('product_uom_qty')
	# def _compute_amount(self):
	# 	line = self.env['sale.order.line']

