# -*- coding	: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from datetime import date
from datetime import timedelta

class stock_move(osv.osv):
    _name = 'stock.move'
    _inherit = 'stock.move'


    def _check_location_id(self, cr, uid, ids, context=None):

        stock_moves = self.browse(cr, uid, ids, context=context)
        for stock_move in stock_moves:
		for user in stock_move.location_id.user_ids:
			if user.id == uid:
				return True
        return False

    def _get_date_from_str(self,parm_string=None):
	
	if not parm_string:
		return False
	
	year = int(parm_string[:4])
	month = int(parm_string[5:7])
	day = int(parm_string[8:11])

	return date(year,month,day)

    def _check_date(self, cr, uid, ids, context=None):

	now = date.today()
        stock_moves = self.browse(cr, uid, ids, context=context)
        for stock_move in stock_moves:
		if now > self._get_date_from_str(stock_move.date):
			return False

        return True

    def _check_date_expected(self, cr, uid, ids, context=None):

	now = date.today()

        stock_moves = self.browse(cr, uid, ids, context=context)
        for stock_move in stock_moves:
		if now > self._get_date_from_str(stock_move.date_expected):
			return False
	return True


    _constraints = [
        (_check_date, 'Fecha de movimiento no puede ser anterior a hoy', ['date']),
        (_check_date_expected, 'Fecha de movimiento esperado no puede ser anterior a hoy', ['date_expected']),
        (_check_location_id, 'El usuario no se encuentra habilitado para trabajar con el deposito seleccionado', ['location_id']),
    ]


stock_move()


class stock_location(osv.osv):
    _inherit = 'stock.location'
    _name = 'stock.location'

    _columns = {
	'user_ids':
	   fields.many2many(
	    'res.users',
	    'stock_location_user_rel',
	    'location_id',
	    'user_id',
	    'User'),
	}

stock_location()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
