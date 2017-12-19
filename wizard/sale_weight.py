# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
import math

# class SaleWeightLine(models.Model):
# 	_inherit = 'sale.order.line'


class ChangeSaleWeight(models.TransientModel):
	_name = 'sale.order.weight'
	_description = 'Sale set weight with weighing scale'

	orderline_id = fields.Many2one('sale.order.line', string='Description', required=True, readonly=True)
	weight = fields.Float(digits=(5, 2), string='Weight', required=True)
	price_subtotal = fields.Float(string='Subtotal', readonly=True, store=True)

	@api.model
	def default_get(self,fields):
		res = super(ChangeSaleWeight, self).default_get(fields)
		if 'orderline_id' in fields and not res.get('orderline_id') and self._context.get('active_model') == 'sale.order.line' and self._context.get('active_id'):
			res['orderline_id'] = self._context['active_id']
		if 'weight' in fields and not res.get('weight') and res.get('orderline_id'):
			res['weight'] = self.env['sale.order.line'].browse(res.get('orderline_id')).weight
		if 'price_subtotal' in fields and not res.get('price_subtotal') and res.get('orderline_id'):
			res['price_subtotal'] = self.env['sale.order.line'].browse(res.get('orderline_id')).price_subtotal

		return res

	@api.multi
	def set_weight(self):
		for wizard in self:
			order = wizard.orderline_id
			order.write({'weight': wizard.weight})
		return {}

	@api.multi
	# @api.depends('weight','price_subtotal')
	def _update_price(self):
		for line in self:
			print line
			for product in self.env['sale.order.line'].search([('id','=',line.orderline_id)]):
				print product
				price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
				taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.weight, product=line.product_id, partner=line.order_id.partner_shipping_id)
				
				line.update({'price_subtotal': taxes['total_excluded']})

