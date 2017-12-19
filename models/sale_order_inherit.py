# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SOLineWeight(models.Model):
	_inherit = 'sale.order.line'

	@api.depends('product_uom_qty')
	def _compute_weight(self):
		# total weight formula = qty * weight
		for line in self:
			if line.product_id:
				weight = self.env['product.template'].browse(line.product_id).id.weight
				qty = line.product_uom_qty
				total_weight = weight*qty

				line.update({
					'weight': total_weight
				})

	@api.depends('weight')
	def _compute_uom_qty(self):
		# quantity formula = total weight / weight
		for line in self:
			weight = self.env['product.template'].browse(line.product_id).id.weight
			total_weight = line.weight
			qty = total_weight/weight

			line.update({
				'product_uom_qty': qty
			})

	@api.model
	def create(self,values):
		onchange_fields = ['name', 'price_unit', 'product_uom', 'tax_id', 'weight', 'weigh_type']
		if values.get('order_id') and values.get('product_id') and any(f not in values for f in onchange_fields):
			line = self.new(values)
			line.product_id_change()
			for field in onchange_fields:
				if field not in values:
					values[field] = line._fields[field].convert_to_write(line[field], line)
		line = super(SOLineWeight, self).create(values)
		if line.state == 'sale':
			line._action_procurement_create()
			msg = _("Extra line with %s ") % (line.product_id.display_name,)
			line.order_id.message_post(body=msg)

		return line

	weight = fields.Float(compute='_compute_weight', digits=(6, 2), string='Total Weight', default=1.0)
	weigh_type = fields.Selection([('0', 'Net Weight'), ('1', 'Gross Weight')], default='0', help="Determinant for method of weighing", string='Weigh Type')

