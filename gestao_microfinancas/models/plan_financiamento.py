# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class planFinanc(models.Model):
     _name = 'plano.financiamento'
     _description = 'Plano Financiamento'

     codigo = fields.Char(string="Codigo", equired=True, copy=False, readonly=True, index=True,
                          default=lambda self: _('New'))
     codigo_desemb = fields.Char(string="Codigo", copy=False, readonly=True, index=True,)
     prestacao = fields.Float('Prestação')
     #submeter = fields.Boolean('submeter')
     juro_jerado = fields.Float('Juros')
     total = fields.Float('total')
     #valorAsc = fields.Float('')
     numer_prest = fields.Integer(string="Nº")
     nome_terc = fields.Many2one('pessoas', string="Terceiro")
     #desting_doc_vend = fields.Boolean(string="Documento/Venda")
     #documentos = fields.Char(string="Documento")
     amortizacao = fields.Float(string="Amortização")
     divida = fields.Float(string="Divida", store=True)
     #numeros_docum = fields.Char(string="Numero/Docum")
     data_documento = fields.Date(string="Data")
     plano_desembolso_id = fields.Many2one('plano.desembolso', index=True, store=True)
     ata_id = fields.Many2one('acta.comite')
     displlay_type = fields.Selection([('line_section', 'section'), ('line_note', 'nota')], string='displlay')
     state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid'), ('cancel', 'Cancelled'), ],
                              string='Status', index=True, readonly=True, default='draft', track_visibility='onchange',
                              copy=False)
     desting_solict = fields.Boolean(string="Solicitação")


     @api.model
     def create(self, vals):
          vals['codigo'] = self.env['ir.sequence'].next_by_code('fiador.fiador.codigo') or _('New')
          res = super(planFinanc, self).create(vals)
          return res



