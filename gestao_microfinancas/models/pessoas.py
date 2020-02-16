# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class pessoal(models.Model):
     _name = 'pessoas'
     _description = 'Pessoal'
     _rec_name = 'name'

     codigo = fields.Char(string="Codigo", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
     name = fields.Char(string="Nome", required=True)
     alcunha = fields.Char(string="Alcunha")
     data_realiz = fields.Date(string="Data acta", default=fields.Date.today)

     nif = fields.Integer(string="NIF")# Para eliminar
     telefone_fixo = fields.Integer(string="Telefone Fixo")
     telemovel = fields.Integer(string="Telemovel")# Para eliminar

     nif_pessoa = fields.Char(string="NIF Pessoa", size=9, required=True,) # required=True,
     telefone_pessoa = fields.Char(string="Telefone Pessoa", required=True, size=7) # required=True,
     fixo_pessoa = fields.Char(string="Fax Pessoa", required=True, size=7)#required=True,

     tipo_documento = fields.Selection([('1', 'BI'), ('2', 'Passaporte'), ('3', 'CNI'), ('4', 'Outro')], default="1", string="Tipo Documento")
     numero_documento = fields.Char(string="Numero Documento")
     membro = fields.Boolean(string="Membro")
     sexo = fields.Selection([('False', 'Feminino'), ('True', 'Masculino')], default="False", string="Sexo")
     local_nascimento = fields.Char(string="Local Nascimento")
     data_nascimento = fields.Date(string="Data Nascimento")
     nacionalidade = fields.Char(string="Nacionalidade")
     nome_conjugue = fields.Char(string="Nome Conjugue")
     estado_civil = fields.Selection([('1', 'Solteiro(a)'), ('2', 'Casado(a)'), ('3', 'Viúvo(a)'), ('4', 'Divorciado(a)'), ('5', 'Outro')], default="1", string="Estado Civil")
     documento = fields.Char(string="Documento")
     endereco = fields.Char(string="Endereco")
     bairo_id = fields.Many2one('lugares.lugares', string="Bairo")
     concelho_id = fields.Many2one('concelho.concelho', related="bairo_id.concelho_id", tring="Concelho")
     freguesia_id = fields.Many2one('freguesia.freguesia', related="bairo_id.freguesia_id", tring="Freguesia")
     zona_id = fields.Many2one('zonas.zonas', related="bairo_id.zona_id", tring="Lugares")
     ilha_id = fields.Many2one('ilha', related="bairo_id.ilha_id", string="Ilha")

     vizinho = fields.Char(string="Vizinho")
     tipo_residencia = fields.Selection([('1', 'Própria'), ('2', 'Alugada'), ('3', 'Financiada'),
                                        ('4', 'De Familiares'), ('5', 'Outro')], string="Tipo Residencia")
     referencia = fields.Text(string="Referencia")
     no_agregado_familhar = fields.Char(string="Numero Familiares")
     n_filhos = fields.Char(string="Numero Filhos")
     escolaridade = fields.Selection([('1', 'Analfabeto'), ('2', 'Primária'), ('3', 'Secundária'), ('4', 'Profissional'), ('5', 'Superior')], string="Escolaridade")
     tempo = fields.Integer(string="Tempo Residencia")
     obs = fields.Text(string="Obs")
     tem_solicitacao = fields.Selection([('1', 'Sim'), ('2', 'Não')], string="Tem Documento", default='2')
     tem_pedido = fields.Selection([('1', 'Sim'), ('2', 'Não')], string="Tem Pedido", default='2')
     tem_despesas = fields.Boolean(string="Tem Despesas")
     fiador = fields.Selection([('1', 'Sim'), ('2', 'Não')], string="Fiador", default='2')
     mae = fields.Char(string="mãe", required=True)
     pai = fields.Char(string="Pai", required=True)
     fiador_id = fields.Many2one('fiador', string='Fiadores')
     utilizador_id = fields.Many2one('res.users', string="Utilizador", default=lambda self: self.env.user)
     socio = fields.Boolean(string="Socio")
     ata_id = fields.Integer(string="ID Ata")

     _sql_constraints = [('nif_pessoa_unique', 'unique(nif_pessoa)', 'Nif ja existe!')]

     dados_antigo = fields.Boolean(string="Dados Antigo")  # se True porque os dados são antigo

     @api.one
     @api.constrains('dados_antigo')
     def val_dados_antig(self):  # Verificar se o dados e antigo ou não
        if self.dados_antigo == True:
            pass
           #raise ValidationError(
           #    'Dados antigo, ha algumas informações que precisam ser modificado, contacta o adminstrador de sistema se consideras-te que é um erro ')

     @api.model
     def _get_next_cod(self):
          sequence = self.env['ir.sequence'].search([('code', '=', 'pessoa.codigo')])
          next = sequence.get_next_char(sequence.number_next_actual)
          return next

     @api.model
     def create(self, vals):
          vals['codigo'] = self.env['ir.sequence'].next_by_code('pessoa.codigo') or _('New')
          res = super(pessoal, self).create(vals)
          return res

     @api.multi
     @api.constrains('nif', 'telefone_fixo', 'numero_documento')
     def _check_size(self):
          nif = str(self.nif_pessoa)
          telef = str(self.telefone_pessoa)
          num = str(self.numero_documento)
          num_agreg = str(self.no_agregado_familhar)
          num_fil = str(self.n_filhos)
          temp = str(self.tempo)
          if (nif.isnumeric()) == True:
               if len(str(nif)) < 9:
                    raise ValidationError('O campo NIF recebe 9 dígitos!')
          else:
               raise ValidationError('O campo NIF tem que ser numerico e 9 dígitos!')

          if (telef.isnumeric()) == True:
               if len(str(telef)) < 7:
                    raise ValidationError('O campo Telefone recebe 7 dígitos!')
          else:
               raise ValidationError('O campo Telefone tem que ser numerico e 7 dígitos!')
          if (num.isnumeric()) == False:
             raise ValidationError('O campo Numero tem que ser numerico!')
          if (num_agreg.isnumeric()) == False:
             raise ValidationError('O campo Nº Agregado tem que ser numerico!')
          if (num_fil.isnumeric()) == False:
             raise ValidationError('O campo Nº Filho tem que ser numerico!')

          if (temp.isnumeric()) == False:
               raise ValidationError('O campo Tempo tem que ser numerico!')



