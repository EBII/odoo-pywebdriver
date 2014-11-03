# -*- encoding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2014 AKRETION (http://www.akretion.com)
#   @author Chafique DELLI
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
from openerp.osv import fields, orm


class PywebdriverServer(orm.Model):
    _name = 'pywebdriver.server'

    _columns = {
        'name': fields.char('Name', required=True),
        'url': fields.char('URL', size=128),
        'printer_ids': fields.one2many('pywebdriver.printer', 'server_id', 'Printers'),
    }


class PywebdriverPrinter(orm.Model):
    _name = 'pywebdriver.printer'

    _columns = {
        'name': fields.char('Name', required=True),
        'code': fields.char('Code'),
        'server_id': fields.many2one('pywebdriver.server', 'Server')

    }


