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
        'name': fields.char('Name', size=32, readonly=True),
        'url': fields.char('URL', size=128, required=True),
        'printer_ids': fields.one2many(
            'pywebdriver.printer', 'server_id', 'Printer IDs'),
        'state': fields.selection([
            ('disconnected', 'Disconnected'),
            ('connected', 'Connected')],
            'State', readonly=True),
    }

    _defaults = {
        'name': '/',
    }

    def create(self, cr, uid, vals, context=None):
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool['ir.sequence'].next_by_code(
                cr, uid, 'pywebdriver.server', context=context)
        return super(PywebdriverServer, self).create(
            cr, uid, vals, context=context)

    def update_state_server(self, cr, uid, urls, context=None):
        server_ids = self.search(cr, uid, [
            ('url', 'not in', urls.values()),
        ], context=context)
        for server_id in server_ids:
            self.write(cr, uid, server_id, {
                'state': 'disconnected',
            }, context=context)
        return True

    def update_list_server(self, cr, uid, url, printer_data, context=None):
        server_ids = self.search(cr, uid, [('url', '=', url)], context=context)
        if server_ids:
            assert len(server_ids) == 1, 'Only one ID'
            server_id = server_ids[0]
        else:
            server_id = self.create(cr, uid, {
                'url': url,
                'state': 'connected',
            }, context=context)
        for printer in printer_data.items():
            name = printer[0]
            for key, value in printer[1].items():
                if key == 'device-uri':
                    code = value
            printer_ids = self.pool['pywebdriver.printer'].search(cr, uid, [
                ('name', '=', name),
                ('server_id', '=', server_id),
            ], context=context)
            if not printer_ids:
                self.pool['pywebdriver.printer'].create(cr, uid, {
                    'name': name,
                    'code': code,
                    'server_id': server_id,
                    'state': 'connected',
                }, context=context)

        return True


class PywebdriverPrinter(orm.Model):
    _name = 'pywebdriver.printer'

    _columns = {
        'name': fields.char('Name', required=True),
        'code': fields.char('Code'),
        'server_id': fields.many2one('pywebdriver.server', 'Server'),
    }

