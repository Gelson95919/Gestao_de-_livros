# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class clientes(models.Model):
     _name = 'clientes'
     _description = 'Clientes'

     codigo_cliente = fields.Char(string="Codigo Cliente", equired=True, copy=False, readonly=True, index=True,
                          default=lambda self: _('New'))
     name = fields.Char(string="Nome")
     nome_terc = fields.Many2one('pessoas', string="Pessoa")
     name_prop = fields.Char(string="Nome", related="nome_terc.name")

     nif_pessoa = fields.Char(string="NIF", size=9, related="nome_terc.nif_pessoa")#, required=True
     telefone_pessoa = fields.Char(string="Telefone", size=7, related="nome_terc.telefone_pessoa")#, required=True
     fixo_pessoa = fields.Char(string="Fax", size=7, related="nome_terc.fixo_pessoa")#, required=True
     tem_solicitacao = fields.Selection([('1', 'Sim'), ('2', 'Não')], string="Tem Documento", store=True, default='1')
     desting_doc_quo = fields.Boolean(string="Documento/Quotas", default=True)
     endereco = fields.Char(string="Endereco", related="nome_terc.endereco", store=True)
     id_pess = fields.Integer(string="IdPessoa")
     anulado = fields.Boolean(string="Anulado")
     ata_id = fields.Integer(string="ID Ata")
     estado = fields.Selection([('1', 'Aberto'), ('2', 'Fechado')], default="2")
     utilizador_id = fields.Many2one('res.users', string="Utilizador", default=lambda self: self.env.user)
     numero_conta =fields.Char(string="NUMERO CONTA")

     dados_antigo = fields.Boolean(string="Dados Antigo")  # se True porque os dados são antigo

     @api.one
     @api.constrains('dados_antigo')
     def val_dados_antig(self):  # Verificar se o dados e antigo ou não
          if self.dados_antigo == True:
               raise ValidationError(
                    'Dados antigo, ha algumas informações que precisam ser modificado, Contacta o adminstrador de sistema se consideraste que é um erro ')

     @api.model
     def create(self, vals):
          vals['codigo_cliente'] = self.env['ir.sequence'].next_by_code('clientes.codigo') or _('New')
          res = super(clientes, self).create(vals)
          res.cria_terc()
          return res

     def cria_terc(self):
          reval_terc = self.env["terceiro.terceiro"].search([('codigo', '=', '000')])
          for reval in reval_terc:
               reval.write({'receb_pess': True})

          # ----------------------add tercero com rubrica C-------------------------------------------------------------
          pessoa_ter = self.env['terceiro.terceiro']
          pessoa_ter.create(
               {'name': self.name_prop, 'nif_pessoa': self.nif_pessoa, 'fixo_pessoa': self.fixo_pessoa, 'telefone_pessoa': self.telefone_pessoa,
                'fornecedores': self.desting_doc_quo, 'pessoa': self.desting_doc_quo,
                'receb_pess': self.desting_doc_quo,  'street': self.endereco, 'ata_id': self.ata_id,
                'tem_solicitacao': self.tem_solicitacao,  'tem_despesas': self.desting_doc_quo, 'clientes': self.desting_doc_quo,
                'codigo': self.codigo_cliente})
