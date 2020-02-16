# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

from dateutil.relativedelta import relativedelta


class renegociocaoCredito(models.Model):
     _name = 'renegociocao.credito'
     _description = 'Renegociação de Crédito'

     codigo = fields.Char(string="Codigo", equired=True, copy=False, readonly=True, index=True,
                          default=lambda self: _('New'))
     numero_op = fields.Char(string="Num OP", equired=True, copy=False, readonly=True, index=True,
                          default=lambda self: _('New'))
     documentos = fields.Char(string="Documento", default="Renegociação")
     num_docum = fields.Char(string="Num Documento", equired=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
     credito_id = fields.Many2one('credito.aprovado', string="Nome", required=True,  domain=[('estado', '=', '1'),  ('renegociado', '=', False),])
     data = fields.Date(string="Data", default=fields.Date.today)
     capital = fields.Float(string="Capital", related="credito_id.prestacao", store=True,)
     juros = fields.Float(string="Juros", related="credito_id.juros_quadro", store=True,)
     identificacao_proponente = fields.Many2one('pessoas', related="credito_id.identificacao_proponente", store=True, string="Pessoas", )
     total = fields.Float(string="Total", compute='calc_total')
     multa = fields.Float(string="Multa")
     outros = fields.Float(string="Outros")
     total_mont_negocio = fields.Float(string="Montante", compute='calc_total')
     num_prestacao = fields.Integer(string="Numero Prestacao", required=True, default=1)
     data_primer_prestacao = fields.Date(string="Data Primeira Prestação", default=fields.Date.today)
     procesando_desembolso_ids = fields.One2many('procesando.desembolso', 'renegociocao_credito_id')
     metudo_calculo = fields.Selection([('1', 'Degresivo'), ('2', 'Constante'), ('3', 'Simplis')], default="3")
     juros_quadro = fields.Float(string="Juros Calculado", compute='gerar', store=True)
     amotizacao = fields.Float(string="Amortização", compute='gerar', store=True)
     #prestacao = fields.Float(string="Prestação", compute='gerar', store=True)
     divida = fields.Float(string="Divida", compute='gerar', store=True)
     valor_em_div = fields.Float(string="Valor em Divida", related="credito_id.valor_em_div")
     prestacao = fields.Float(string="Prestacao", compute='gerar', store=True)
     desting_ata = fields.Boolean(string="Ata", default=True)
     nif_pessoa = fields.Char(string="NIF", related="identificacao_proponente.nif_pessoa", store=True)
     utilizador_id = fields.Many2one('res.users', string="Utilizador", default=lambda self: self.env.user)
     numer_prest = fields.Integer(string="Nº")
     control_presta = fields.Boolean(string="Atualizar")
     ata_id = fields.Integer(string="ID Ata", related="credito_id.ata_id", store=True)#para ajudar no procedimento de renegociacao

     def _comput_line(self, line):
         return {'displlay_type': line.displlay_type, 'state': 'draft', }

     @api.depends('capital', 'juros')
     def calc_total(self):
         for r in self:
             r.total = r.capital + r.juros
             r.total_mont_negocio = r.valor_em_div + r.multa

     @api.model
     def create(self, vals):
         vals['codigo'] = self.env['ir.sequence'].next_by_code('renegocio.codigo') or _('New')
         vals['num_docum'] = self.env['ir.sequence'].next_by_code('reneg.codigo.num') or _('New')
         vals['numero_op'] = self.env['ir.sequence'].next_by_code('op.num') or _('New')
         res = super(renegociocaoCredito, self).create(vals)

         return res

     #@api.multi
     #def write(self, vals):
     #    self.gerar_plan_desemb()
     #    res = super(renegociocaoCredito, self).write(vals)
     #    return res

     @api.one
    # @api.depends('num_prestacao', 'juros_quadro', 'total_mont_negocio', )
     def gerar(self):
         cont_prest = self.num_prestacao
         cont = 0

         self.ensure_one()
         j = self.outros / 100.0
         self.juros_quadro = self.total_mont_negocio * j
         self.amotizacao = round(self.total_mont_negocio / self.num_prestacao)
         self.prestacao = round(self.amotizacao + self.juros_quadro)
         self.divida = round(self.total_mont_negocio - self.amotizacao)
         anular = self.env["procesando.desembolso"].search([('identificacao_proponente', '=', self.identificacao_proponente.id)]).unlink()
         while cont_prest > 0:
             if cont == 0:
                 plano_obj_lina0 = self.env['procesando.desembolso']
                 plano_desemb = plano_obj_lina0.create({'numer_prest': 0, 'capital': self.total_mont_negocio,
                                                        'identificacao_proponente': self.identificacao_proponente.id,
                                                        'data_processado': self.data, 'renegociocao_credito_id': self.id, })

             # data_prest = date_after_month
             if cont == 1:
                 data_prest = self.data_primer_prestacao
                 plano_obj = self.env['procesando.desembolso']
                 plano_desemb = plano_obj.create({'prestacao_processado': self.prestacao,
                                                  'juros_outros': self.juros_quadro,
                                                  'numer_prest': cont, 'renegociocao_credito_id': self.id,
                                                  'identificacao_proponente': self.identificacao_proponente.id,
                                                  'amortizacao': self.amotizacao, 'capital': self.divida,
                                                  'data_processado': data_prest, })
             if cont > 1:
                 date_after_month = self.data_primer_prestacao + relativedelta(months=1 + cont - 2)
                 data_prest = date_after_month
                 plano_obj = self.env['procesando.desembolso'].search(
                     [('numer_prest', '=', cont - 1), ('identificacao_proponente', '=', self.identificacao_proponente.id)])
                 for rec in plano_obj:
                     if self.divida > 0:
                         self.divida = rec.capital - rec.amortizacao
                         if self.divida < 6 and self.divida != 0:  # aque resolve o problema de  1 escudo ....
                             self.amotizacao = rec.capital
                             self.divida = 0
                 plano_desemb = plano_obj.create({'prestacao_processado': self.prestacao,
                                                  'juros_outros': self.juros_quadro,
                                                  'numer_prest': cont, 'renegociocao_credito_id': self.id,
                                                  'identificacao_proponente': self.identificacao_proponente.id,
                                                  'amortizacao': self.amotizacao, 'capital': self.divida,
                                                  'data_processado': data_prest, })

             self.numer_prest = cont + 1
             if self.numer_prest == self.num_prestacao:
                 pass  # cont_prest += 1
             else:
                 cont_prest -= 1
             cont += 1
         return True

     @api.model
     def credito_aprovado(self):
         ata = self.env['acta.comite'].search([('id', '=', self.ata_id)])
         cred_aprov_obj = self.env['credito.aprovado']
         cred_apro = cred_aprov_obj.create({'valor': self.total_mont_negocio, 'numero_prestacao': self.num_prestacao,
                                            'por': ata.por,
                                            'identificacao_proponente': ata.identificacao_proponente.id,
                                            'juros': self.outros,
                                            'data': self.data, 'prestacao': self.prestacao,
                                            'juros_quadro': self.juros_quadro, 'ata_id': self.ata_id,
                                            'data_primeira': self.data_primer_prestacao,
                                            'periodo_carencia': ata.periodo_carencia, 'aprovado': ata.aprovado,
                                            'calcular_juro_periodo_carenc': ata.calcular_juro,
                                            'metudo_calculo': self.metudo_calculo})
         return cred_apro

     @api.one
     def gerar_plan_desemb(self): #para reg_docum
         ata = self.env['acta.comite'].search([('id', '=', self.ata_id)])
         self.ensure_one()
         renegoc_rec_doc = self.env["reg.docum"].search([('ata', '=', self.ata_id), ('estado', '!=', '3')])
         if renegoc_rec_doc:
             for a in renegoc_rec_doc:
                 a.renegociado = True
         renegoc_op = self.env["tesouraria.ordem.pagamento"].search([('ata', '=', self.ata_id)])
         if renegoc_op:
             for o in renegoc_op:
                 o.renegociado = True
         renegoc_cred_aprov = self.env["credito.aprovado"].search([('ata_id', '=', self.ata_id)])
         if renegoc_cred_aprov:
             for cp in renegoc_cred_aprov:
                 cp.renegociado = True
         renegoc_dt_op = self.env["detalhes.documento.op"].search([('ata', '=', self.ata_id)])
         if renegoc_dt_op:
             for dt in renegoc_dt_op:
                 dt.renegociado = True
         pessoa_ter = self.env['terceiro.terceiro'].search([('ata_id', '=', self.ata_id)])
         self.ensure_one()
         cont_prest = self.num_prestacao
         cont = 0

         self.ensure_one()
         j = self.outros / 100.0
         self.juros_quadro = self.total_mont_negocio * j
         self.amotizacao = round(self.total_mont_negocio / self.num_prestacao)
         self.prestacao = round(self.amotizacao + self.juros_quadro)
         self.divida = round(self.total_mont_negocio - self.amotizacao)
         self.valor_divida_total = round(self.prestacao * self.num_prestacao)
         ata.creat_op()
         ata.creat_det_op()
         self.credito_aprovado()
         cred_aprov_obj = self.env['credito.aprovado'].search(
             [('identificacao_proponente', '=', self.identificacao_proponente.id),  ('renegociado', '=', False), ('estado', '=', '1')])

         while cont_prest > 0:
             if cont == 0: #este e o recoord de OP (PRESTAÇÃO 0)
                 plano_obj_0 = self.env['reg.docum']
                 plano_desemb_0 = plano_obj_0.create({'numer_prest': 0, 'divida': self.total_mont_negocio,
                                                  'nome_terc': pessoa_ter.id,
                                                  'valor_desembolso': self.total_mont_negocio,
                                                  'desting_solict': self.desting_ata,
                                                  'prest_zerro': self.desting_ata,
                                                  'desting_ata': self.desting_ata,
                                                  'id_cred_aprov': cred_aprov_obj.id,
                                                  'total': self.total_mont_negocio,
                                                  'saldo_pagamento': self.total_mont_negocio,
                                                  'ata': self.ata_id,
                                                  #'saldo': self.prestacao,
                                                  'valorAsc': self.total_mont_negocio,
                                                  'submeter': self.desting_ata,
                                                  'agente': self.utilizador_id.id,
                                                  'cod_documento': self.numero_op,
                                                  'numero_credito': self.codigo,
                                                  'desting_doc_desp': self.desting_ata,
                                                  'data_documento': self.data_primer_prestacao})
             if cont == 1:
                 cod_doc = self.num_docum + '/' + str(cont)
                 data_prest = self.data_primer_prestacao
                 plano_obj_1 = self.env['reg.docum'].search([('numer_prest', '=', cont)])
                 plano_desemb_1 = plano_obj_1.create({'prestacao': self.prestacao, 'submeter': self.desting_ata,
                                                  'juro_jerado': self.juros_quadro, 'total': self.prestacao,
                                                  'valorAsc': self.prestacao, 'numer_prest': self.numer_prest,
                                                  'nome_terc': pessoa_ter.id,
                                                  'saldo': self.prestacao,
                                                  'valor_desembolso': self.total_mont_negocio,
                                                  'cod_documento': cod_doc,
                                                  'documentos': self.documentos,
                                                  'desting_ata': self.desting_ata,
                                                  'desting_doc_vend': self.desting_ata,
                                                  'desting_solict': self.desting_ata,
                                                  'numero_credito': self.codigo,
                                                  'aprovado': '1',
                                                  'ata': self.ata_id,
                                                  'agente': self.utilizador_id.id,
                                                  'id_cred_aprov': cred_aprov_obj.id,
                                                  'amortizacao': self.amotizacao, 'divida': self.total_mont_negocio,
                                                  'numeros_docum': self.codigo, 'data_documento': data_prest, })
             if cont > 1:
                 cod_doc = self.num_docum + '/' + str(cont)
                 date_after_month = self.data_primer_prestacao + relativedelta(months=1 + cont - 2)
                 data_prest = date_after_month
                 plano_obj_maior_1 = self.env['reg.docum'].search(
                     [('numer_prest', '=', cont - 1), ('nome_terc', '=', pessoa_ter.id)])
                 for rec in plano_obj_maior_1:
                     if self.divida > 0:
                         self.divida = rec.divida - rec.amortizacao
                         if self.divida < 6 and self.divida != 0:  # aque resolve o problema de  1 escudo ....
                             self.amotizacao = rec.divida
                             self.valor_divida_total += self.divida
                             self.divida = 0
                 plano_desemb_maior_1 = plano_obj_maior_1.create({'prestacao': self.prestacao, 'submeter': self.desting_ata,
                                          'juro_jerado': self.juros_quadro, 'total': self.prestacao,
                                          'valorAsc': self.prestacao, 'numer_prest': self.numer_prest,
                                          'nome_terc': pessoa_ter.id,
                                          'saldo': self.prestacao,
                                          'valor_desembolso': self.total_mont_negocio,
                                          'cod_documento': cod_doc,
                                          'documentos': self.documentos,
                                          'desting_ata': self.desting_ata,
                                          'desting_doc_vend': self.desting_ata,
                                          'desting_solict': self.desting_ata,
                                          'numero_credito': self.codigo,
                                          'aprovado': '1', 'ata': self.ata_id,
                                          'agente': self.utilizador_id.id,
                                          'id_cred_aprov': cred_aprov_obj.id,
                                          'amortizacao': self.amotizacao, 'divida': self.total_mont_negocio,
                                          'numeros_docum': self.codigo, 'data_documento': data_prest})

             self.numer_prest = cont + 1
             if self.numer_prest == self.num_prestacao:
                 pass
             else:
                 cont_prest -= 1
             cont += 1
             cred_aprov = self.env['credito.aprovado'].search(
                 [('ata_id', '=', self.ata_id), ('estado', '=', '1')])
             if cred_aprov:
                 for c in cred_aprov:
                     c.valor_em_div = self.valor_divida_total  # calcula a divida total do cliente
                     c.prestacao = self.prestacao
                     c.juros_quadro = self.juros_quadro

         #plano_des_obj = self.env['reg.docum'].search([('receb_solici', '=', True)])
         #for docu in plano_des_obj:
         #    if docu:
         #        docu.write({'receb_solici': False})
         #cred_aprov = self.env['credito.aprovado'].search(
         #    [('nif_pessoa', '=', self.nif_pessoa), ('estado', '=', '1')])
         #if cred_aprov:
         #    for c in cred_aprov:
         #        c.valor_em_div = self.valor_divida_total #calcula a divida total do cliente
         #        c.prestacao = self.prestacao
         #        c.juros_quadro = self.juros_quadro

         return True



class procesando(models.Model):
    _name = 'procesando.desembolso'
    #_rec_name = 'name'
    _description = 'Plano Reembolso Gerado'

    codigo = fields.Char(string="Codigo", equired=True, copy=False, readonly=True, index=True,
                         default=lambda self: _('New'))
    numer_prest = fields.Integer(string="Nº")
    renegociocao_credito_id = fields.Many2one('renegociocao.credito')
    data_processado = fields.Date(string="Data")
    data_documento = fields.Date(string="Data Documento")
    prestacao_processado = fields.Float(string="Prestação")
    juros_outros = fields.Float(string="Juros/Outros")
    amortizacao = fields.Float(string="Amortizacão")
    capital = fields.Float(string="Capital")
    credito_id = fields.Many2one('credito.aprovado', string="Credito")
    identificacao_proponente = fields.Many2one('pessoas', store=True, string="Pessoas", )

    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid'), ('cancel', 'Cancelled'), ],
                             string='Status', index=True, default='draft', track_visibility='onchange',
                             copy=False)
    displlay_type = fields.Selection([('line_section', 'section'), ('line_note', 'nota')], string='displlay')

    @api.model
    def create(self, vals):

        vals['codigo'] = self.env['ir.sequence'].next_by_code('desel.codigo.plan') or _('New')
        res = super(procesando, self).create(vals)
        return res