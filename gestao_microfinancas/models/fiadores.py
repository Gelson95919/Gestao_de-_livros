# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class fiador(models.Model):
    _name = 'fiador'
    _rec_name = 'codigo'

    _description = 'Fiador'
    codigo = fields.Char(string="Codigo", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    numero = fields.Char(string="Codigo", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    pessoa_id = fields.Many2one('pessoas', string="Código")
    pessoa_fiador_id = fields.Many2one('pessoas', string="Nome", required=True)#
    name = fields.Char(string="Nome", related='pessoa_fiador_id.name')
    professao_id = fields.Many2one('profissoes.profissoes', string="Professoes", required=True)#
    lugar_trabalho = fields.Char(string="Lugar Trabalho", required=True)#
    telefone = fields.Char(string="Telefone", size=7, required=True)#
    vencimento = fields.Float(string="Vencimento", required=True)#
    residencia = fields.Char(string="Residência")
    avalista = fields.Many2one('avalista', string="Avalista")
    solicitacao_credito_id = fields.Many2one('solicitacao.credito')
    propornente_ids = fields.Many2many('pessoas',  domain="[('tem_solicitacao','!=','1')]", string='Lista de Proponente')
    utilizador_id = fields.Many2one('res.users', string="Utilizador", default=lambda self: self.env.user)

    dados_antigo = fields.Boolean(string="Dados Antigo")  # se True porque os dados são antigo

    @api.one
    @api.constrains('dados_antigo')
    def val_dados_antig(self):  # Verificar se o dados e antigo ou não
        if self.dados_antigo == True:
            pass
           #raise ValidationError(
           #    'Dados antigo, ha algumas informações que precisam ser modificado, contacta o adminstrador de sistema se consideras-te que é um erro ')

    @api.one
    @api.constrains('dados_antigo')
    def val_dados_antig(self):  # Verificar se o dados e antigo ou não
        if self.dados_antigo == True:
            pass
           #raise ValidationError(
           #    'Dados antigo, ha algumas informações que precisam ser modificado, contacta o adminstrador de sistema se consideras-te que é um erro ')

    @api.one
    @api.constrains('dados_antigo')
    def val_dados_antig(self):  # Verificar se o dados e antigo ou não
        if self.dados_antigo == True:
            pass
           #raise ValidationError(
           #    'Dados antigo, ha algumas informações que precisam ser modificado, contacta o adminstrador de sistema se consideras-te que é um erro ')

    @api.one
    @api.constrains('dados_antigo')
    def val_dados_antig(self):  # Verificar se o dados e antigo ou não
        if self.dados_antigo == True:
            pass
           #raise ValidationError(
           #    'Dados antigo, ha algumas informações que precisam ser modificado, contacta o adminstrador de sistema se consideras-te que é um erro ')

    @api.one
    @api.constrains('dados_antigo')
    def val_dados_antig(self):  # Verificar se o dados e antigo ou não
        if self.dados_antigo == True:
            pass
           #raise ValidationError(
           #    'Dados antigo, ha algumas informações que precisam ser modificado, contacta o adminstrador de sistema se consideras-te que é um erro ')

    @api.one
    @api.constrains('dados_antigo')
    def val_dados_antig(self):  # Verificar se o dados e antigo ou não
        if self.dados_antigo == True:
            pass
           #raise ValidationError(
           #    'Dados antigo, ha algumas informações que precisam ser modificado, contacta o adminstrador de sistema se consideras-te que é um erro ')


    @api.model
    def create(self, vals):
        vals['codigo'] = self.env['ir.sequence'].next_by_code('fiador.fiador.codigo') or _('New')
        vals['numero'] = self.env['ir.sequence'].next_by_code('fiador.fiador.numero') or _('New')
        res = super(fiador, self).create(vals)
        res.add_pess_com_fiador()
        return res

    def add_pess_com_fiador(self):
        add_fiador = self.env["pessoas"].search([('id', '=', self.pessoa_id.id)])
        if add_fiador:
            for av in add_fiador:
                av.write({'fiador': '1'})

    @api.multi
    @api.constrains('nif', 'telefone_fixo', 'numero_documento')
    def _check_size(self):

         telef = str(self.telefone)

         if (telef.isnumeric()) == True:
              if len(str(telef)) < 7:
                   raise ValidationError('O campo Telefone recebe 7 dígitos!')
         else:
              raise ValidationError('O campo Telefone tem que ser numerico e 7 dígitos!')




class avalista(models.Model):
    _name = 'avalista'
    _rec_name = 'codigo'
    _description = 'Avalista'
    codigo = fields.Char(string="Codigo", equired=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    name = fields.Char(string="Nome")

    @api.model
    def create(self, vals):
        vals['codigo'] = self.env['ir.sequence'].next_by_code('avalista') or _('New')
        res = super(avalista, self).create(vals)
        return res




