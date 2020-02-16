# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class grupo(models.Model):
     _name = 'grupo'
     _description = 'Grupo'

     codigo = fields.Char(string="Codigo", equired=True, copy=False, readonly=True, index=True,
                          default=lambda self: _('New'))
     name = fields.Char(string="Nome")
     lista_group = fields.One2many('membro', 'grupo_id')
     solicitacao_credito_id = fields.Many2one('solicitacao.credito')
     _sql_constraints = [('name_unique', 'unique(name)', 'Nome ja existe!')]
     utilizador_id = fields.Many2one('res.users', string="Utilizador", default=lambda self: self.env.user)
     @api.model
     def create(self, vals):
         vals['codigo'] = self.env['ir.sequence'].next_by_code('grupo.codigo') or _('New')
         res = super(grupo, self).create(vals)
         return res



class membro(models.Model):
    _name = 'membro'
    #_rec_name = 'name'
    _description = 'Membro'

    cliente = fields.Many2one('pessoas', string="Cliente")
    coordenador = fields.Boolean(string="Coordenador")
    grupo_id = fields.Many2one('grupo')
    nome = fields.Char(string="Nome", related='cliente.name')
    codigo = fields.Char(string="Código", related='cliente.codigo')
    displlay_type = fields.Selection([('line_section', 'section'), ('line_note', 'nota')], string='displlay')
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid'), ('cancel', 'Cancelled'), ],
                             string='Status', index=True, readonly=True, default='draft', track_visibility='onchange',)

    solicitacao_id = fields.Many2one('solicitacao.credito', string="Solicitação")