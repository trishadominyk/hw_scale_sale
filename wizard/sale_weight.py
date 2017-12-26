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

	@api.model
	def default_get(self,fields):
		res = super(ChangeSaleWeight, self).default_get(fields)
		if 'orderline_id' in fields and not res.get('orderline_id') and self._context.get('active_model') == 'sale.order.line' and self._context.get('active_id'):
			res['orderline_id'] = self._context['active_id']
		if 'weight' in fields and not res.get('weight') and res.get('orderline_id'):
			res['weight'] = self.env['sale.order.line'].browse(res.get('orderline_id')).weight
		if 'product_uom_qty' in fields and not res.get('product_uom_qty') and res.get('orderline_id'):
			res['product_uom_qty'] = self.env['sale.order.line'].browse(res.get('orderline_id')).product_uom_qty
		if 'price_subtotal' in fields and not res.get('price_subtotal') and res.get('orderline_id'):
			res['price_subtotal'] = self.env['sale.order.line'].browse(res.get('orderline_id')).price_subtotal

		return res

	@api.multi
	def set_weight(self):
		for wizard in self:
			order = wizard.orderline_id
			product = self.env['sale.order.line'].browse(wizard.orderline_id).id.product_id

			weight = self.env['product.template'].browse(product).id.weight
			qty = wizard.weight/weight

			order.write({
				'product_uom_qty': qty,
				'weight': wizard.weight
			})
		return {}

	@api.depends('weight','product_uom_qty')
	def _update_price(self):
		for line in self:
			price = line.orderline_id.price_unit * (1 - (line.orderline_id.discount or 0.0) / 100.0)
			taxes = line.orderline_id.tax_id.compute_all(price, line.orderline_id.order_id.currency_id, line.product_uom_qty, product=line.orderline_id.product_id, partner=line.orderline_id.order_id.partner_shipping_id)

			line.update({
				'price_subtotal': taxes['total_excluded']
			})

	@api.depends('weight','product_uom_qty')
	def compute_qty(self):
		for line in self:
			weight = self.env['product.template'].browse(line.orderline_id.product_id).id.weight
			total_weight = line.weight
			qty = total_weight/weight

			line.update({
				'product_uom_qty': qty
			})

	orderline_id = fields.Many2one('sale.order.line', string='Description', required=True, readonly=True)
	weight = fields.Float(digits=(5, 2), string='Weight', required=True)
	product_uom_qty = fields.Float(compute='compute_qty', string='Quantity', readonly=True, store=True)
	price_subtotal = fields.Float(compute='_update_price', string='Subtotal', readonly=True, store=True)
