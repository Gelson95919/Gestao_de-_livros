# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class planoDesembolso(models.Model):
    _name = 'plano.desembolso'
    _description = 'Plano Desembolso'
    _rec_name = 'codigo'
    # codigo = fields.Char(string="Codigo", equired=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    codigo = fields.Char(string="Codigo", equired=True, copy=False, readonly=True, index=True,
                         default=lambda self: _('New'))
    valor = fields.Float(string="Valor",  equired=True)
    numero_prestacao = fields.Float(string="Numero prestacao", store=True)
    juros = fields.Float(string="Juros", store=True, readonly=False)  # , compute="add_percent"
    por = fields.Selection([('1', 'ao Ano'), ('2', 'ao mês')], default="2")
    periodicidade = fields.Selection(
        [('1', 'Semanal'), ('2', 'Quinzenal'), ('3', 'Mensal'), ('4', 'Trimestral'), ('5', 'Semestral'),
         ('6;', 'Anual'), ('7;', 'Outros')], default="3")
    periodquant = fields.Integer(string=" ")
    data = fields.Date(string="Data", default=fields.Date.today)
    date_start = fields.Date(string="Data Primeira", default=fields.Date.today)
    date_end = fields.Date(string="Data Fim", default=fields.Date.today)
    duree_mois = fields.Char(string="Duração", default=1)

    periodo_carencia = fields.Integer(string="Período Carência")
    calcular_juro_periodo_carenc = fields.Boolean(string="Calcular juros no periodo de Carência")
    metudo_calculo = fields.Selection([('degresivo', 'Degresivo'), ('constante', 'Constante'), ('simplis', 'Simples')],
                                      default="simplis")
    # plano_gerado_ds = fields.One2many('plano.gerado.desembolso', 'plano_desembolso_id')
    # prestacao_ids = fields.One2many('prestacao', 'plano_desembolso_id', string="Prestação", store=True,
    # copy=True)
    plano_financiamento_ids = fields.One2many('plano.financiamento', 'plano_desembolso_id',
                                              string="Plano Financiamento", store=True,
                                              copy=True)
    solisit_ids = fields.One2many('solicitacao.credito', 'plano_desemboso_id', string="Reg Docum", store=True,
                                  copy=True)
    identificacao_proponente = fields.Many2one('pessoas', string="Pessoas",
                                               domain="[('tipo','=','pessoa')]", )
    identificacao = fields.Many2one('terceiro.terceiro', string="Pessoas", domain="[('tipo','=','pessoa')]", )

    """prestacao = fields.Float(string="Prestação", compute='gerar', store=True)
    amotizacao = fields.Float(string="Amortização", compute='gerar', store=True)"""
    juros_quadro = fields.Float(string="Juro calculado", compute='gerar', store=True)
    numer_prest_ger = fields.Integer(string="Nº", store=True)
    control_presta = fields.Boolean(string="Atualizar", store=True)
    documentos = fields.Char(string="Documento", default="Solicitação")
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid'), ('cancel', 'Cancelled'), ],
                             string='Status', index=True, default='draft', track_visibility='onchange',
                             copy=False)
    submeter = fields.Boolean(string="Submeter", default=True)
    desting_doc_quo = fields.Boolean(string="Documento/Quotas", default=True)
    divida = fields.Float(string="Dividas", compute="gerar", store=True)
    solici = fields.Boolean(string="Solicitação")
    ata = fields.Boolean(string="Ata")
    num_incr = fields.Integer(string="Control data Periodicidade", compute="addperiodc", readonly=False)
    plande = fields.Boolean(string="Plano Desembolso", default=True)
    aprovado = fields.Selection([('sim', 'Sim'), ('nao', 'Não')])
    vervalor_total = fields.Float(string="Valor total", compute="_compute_val_tot", store=True)

    dados_antigo = fields.Boolean(string="Dados Antigo")  # se True porque os dados são antigo

    @api.one
    @api.constrains('dados_antigo')
    def val_dados_antig(self):  # Verificar se o dados e antigo ou não
        if self.dados_antigo == True:
            pass
        # raise ValidationError(
        #    'Dados antigo, ha algumas informações que precisam ser modificado, contacta o adminstrador de sistema se consideras-te que é um erro ')

    # prestacao = fields.Float(string="Prestação", compute="gerar", store=True)
    # num_incr = fields.Integer(string="Incrimenta mes", default=0)

    @api.depends('plano_financiamento_ids.amortizacao')
    def _compute_val_tot(self):
        for rec in self:
            self.vervalor_total = sum(line.amortizacao for line in rec.plano_financiamento_ids)

    @api.model
    def create(self, vals):
        self.linc_plan_financ()
        vals['codigo'] = self.env['ir.sequence'].next_by_code('desel.codigo.plan') or _('New')
        res = super(planoDesembolso, self).create(vals)
        return res
    #@api.constrains('id')
    def linc_plan_financ(self):
        pl = self.env["plano.financiamento"].search([('nome_terc', '=', self.identificacao_proponente.id)])
        if pl:
            for p in pl:
                p.plano_desembolso_id = self.id

    # @api.model
    # def create(self, vals):
    # vals['codigo'] = self.env['ir.sequence'].next_by_code('desel.codigo') or _('New')
    #    res = super(planoDesembolso, self).create(vals)
    #    return res
    @api.model
    # @api.onchange('por')
    def add_percent(self):
        if self.por == '1':  # ao Ano
            if self.periodicidade == '1':
                self.juros = (self.juros / 365) * 7

            elif self.periodicidade == '2':
                self.juros = (self.juros / 365) * 15

            elif self.periodicidade == '3':
                self.juros = (self.juros / 12)

            elif self.periodicidade == '4':
                self.juros = (self.juros / 12) * 3
        elif self.por == '2':  # Ao Mes
            if self.periodicidade == '1':
                self.juros = (self.juros / 30) * 7

            elif self.periodicidade == '2':
                self.juros = (self.juros / 30) * 15

            elif self.periodicidade == '4':
                self.juros = self.juros * 3

            elif self.periodicidade == '5':
                self.juros = self.juros * 12

    @api.model
    @api.onchange('periodicidade')
    def addperiodc(self):
        if self.periodicidade == '1':
            self.num_incr = 7  # semanal
        elif self.periodicidade == '2':
            self.num_incr = 15  # Quinzenal
        elif self.periodicidade == '3':
            self.num_incr = 1  # Mensal
        elif self.periodicidade == '4':
            self.num_incr = 3  # Tri mestral
        elif self.periodicidade == '5':
            self.num_incr = 6  # semestral
        elif self.periodicidade == '6':
            self.num_incr = 1  # Anual
        else:
            self.num_incr = 1

    @api.multi
    @api.depends('valor', 'numero_prestacao', 'juros', 'date_start', 'data', 'juros_quadro', 'periodicidade',
                 'num_incr')
    def gerar(self):
        self.ensure_one()
        self.add_percent()
        # self.addperiodc()
        if self.numero_prestacao < 1:
            warning = {
                'title': _('Atenção!'),
                'message': _('ERRO! Numéro de quotas deve ser maior a zero (0).'),
            }
            return {'warning': warning}

        if self.periodo_carencia >= self.numero_prestacao:
            warning = {
                'title': _('Atenção!'),
                'message': _('ERRO! Numéro de período de carencia tem que ser menor ao numero de prestações.'),
            }
            return {'warning': warning}

        if self.metudo_calculo == 'simplis':
            # J = C * i * t
            j = self.juros / 100.0
            self.juros_quadro = self.valor * j * 1

            # J = M - C, onde M = C (1+i)^t
        # if self.metudo_calculo == 'constante':
        #    j = self.juros / 100.0

        cont_prest = self.numero_prestacao
        self.amotizacao = round(self.valor / self.numero_prestacao)
        self.prestacao = round(self.amotizacao + self.juros_quadro)
        self.divida = round(self.valor - self.amotizacao)
        cont = 0

        if self.solici == True:#na Solicitacao
            solic = self.env['solicitacao.credito'].search(
                [('identificacao_proponente', '=', self.identificacao_proponente.id), ])
        if self.ata == True:
            solic = self.env['acta.comite'].search(
                [('identificacao_proponente', '=', self.identificacao_proponente.id), ])
            for s in solic:
                if self.valor != s.valor_solicitado or self.metudo_calculo != s.metudo_calculo or self.valor != 0 or self.numero_prestacao != s.numero_prestacoes or self.date_start != s.date_start:
                    self.env["plano.financiamento"].search([('nome_terc', '=', self.identificacao_proponente.id)]).unlink()
                    self.env["plano.financiamento"].search(
                        [('numer_prest', '=', 0), ('nome_terc', '=', self.identificacao_proponente.id)]).unlink()
                    # sql = "DELETE FROM reg_docum WHERE submeter = False"
                    # self.env.cr.execute(sql)
                    # cont_prest = self.numero_prestacao
                    while cont_prest > 0:
                        if cont == 0:
                            plano_obj_lina0 = self.env['plano.financiamento']
                            plano_desemb = plano_obj_lina0.create({'numer_prest': 0, 'divida': self.valor,
                                                                   'nome_terc': self.identificacao_proponente.id,
                                                                   'codigo_desemb': self.codigo, 'plano_desembolso_id': self.id,
                                                                   'data_documento': self.data})  # 'data_documento': self.data,
                        elif cont == 1:
                            if self.metudo_calculo == 'constante':
                                self.juros_quadro = self.valor * self.juros
                                # self.amotizacao = self.prestacao - self.juros
                            data_prest = self.date_start
                            plano_obj = self.env['plano.financiamento']
                            plano_desemb = plano_obj.create({'prestacao': self.prestacao,
                                                             'juro_jerado': self.juros_quadro, 'total': self.prestacao,
                                                             'numer_prest': self.numer_prest, 'plano_desembolso_id': self.id,
                                                             'nome_terc': self.identificacao_proponente.id,
                                                             'amortizacao': self.amotizacao, 'divida': self.divida,
                                                             'desting_solict': self.desting_doc_quo,
                                                             'codigo_desemb': self.codigo,
                                                             'data_documento': data_prest})
                        elif cont > 1 and self.divida > 0:
                            # if self.periodicidade == 4:
                            # elif self.periodicidade == 3:
                            #    date_after_month = self.date_start + relativedelta(months=1 + cont - 2)

                            caldivid = self.env['plano.financiamento'].search(
                                [('numer_prest', '=', cont - 1), ('nome_terc', '=', self.identificacao_proponente.id)])
                            for rec in caldivid:
                                if self.divida > 0:
                                    self.divida = rec.divida - rec.amortizacao
                                    if self.divida < 6 and self.divida != 0: #aque resolve o problema de  1 escudo ....
                                        self.amotizacao = rec.divida
                                        self.prestacao += self.divida
                                        self.divida = 0

                                    if self.metudo_calculo == 'constante':
                                        self.juros_quadro = rec.divida * self.juros
                                        # self.amotizacao = rec.prestacao - rec.juro_jerado
                                        # self.divida = rec.divida - rec.amortizacao

                                    if self.divida < 0:
                                        self.divida = 0
                            if self.numero_prestacao > 6:
                                if self.divida >= 0 and cont > 1:
                                    # date_after_month = self.date_start + relativedelta(months=self.num_incr + cont - 2)
                                    if self.periodicidade == '4':
                                        date_after_month = self.date_start + relativedelta(months=self.num_incr + cont - 2)
                                    elif self.periodicidade == '1':
                                        date_after_month = self.date_start + relativedelta(days=self.num_incr + cont - 2)
                                    elif self.periodicidade == '2':
                                        date_after_month = self.date_start + relativedelta(days=self.num_incr + cont - 2)
                                    elif self.periodicidade == '3':
                                        date_after_month = self.date_start + relativedelta(months=1 + cont - 2)
                                    elif self.periodicidade == '5':
                                        date_after_month = self.date_start + relativedelta(months=self.num_incr + cont - 2)
                                    else:
                                        date_after_month = self.date_start + relativedelta(years=self.num_incr + cont - 2)
                                    data_prest = date_after_month
                                    plano_desemb = caldivid.create({'prestacao': self.prestacao,
                                                                    'juro_jerado': self.juros_quadro, 'total': self.prestacao,
                                                                    'numer_prest': self.numer_prest,
                                                                    'nome_terc': self.identificacao_proponente.id,
                                                                    'codigo_desemb': self.codigo,
                                                                    'desting_solict': self.desting_doc_quo,
                                                                    'plano_desembolso_id': self.id,
                                                                    'amortizacao': self.amotizacao, 'divida': self.divida,
                                                                    'data_documento': data_prest})  # , 'data_documento': data_prest
                                else:
                                    break
                            else:
                                if self.divida >= 0 and cont > 1:
                                    if self.periodicidade == '4':
                                        date_after_month = self.date_start + relativedelta(months=self.num_incr + cont - 2)
                                    elif self.periodicidade == '1':
                                        date_after_month = self.date_start + relativedelta(days=self.num_incr + cont - 2)
                                    elif self.periodicidade == '2':
                                        date_after_month = self.date_start + relativedelta(days=self.num_incr + cont - 2)
                                    elif self.periodicidade == '3':
                                        date_after_month = self.date_start + relativedelta(months=1 + cont - 2)
                                    elif self.periodicidade == '5':
                                        date_after_month = self.date_start + relativedelta(months=self.num_incr + cont - 2)
                                    else:
                                        date_after_month = self.date_start + relativedelta(years=self.num_incr + cont - 2)
                                    data_prest = date_after_month
                                    plano_desemb = caldivid.create({'prestacao': self.prestacao,
                                                                    'juro_jerado': self.juros_quadro, 'total': self.prestacao,
                                                                    'numer_prest': self.numer_prest,
                                                                    'nome_terc': self.identificacao_proponente.id,
                                                                    'codigo_desemb': self.codigo,
                                                                    'desting_solict': self.desting_doc_quo,
                                                                    # 'plande': self.plande, #'periodicidade': self.periodicidade,
                                                                    'plano_desembolso_id': self.id,
                                                                    'amortizacao': self.amotizacao, 'divida': self.divida,
                                                                    'data_documento': data_prest})  # , 'data_documento': data_prest

                        self.numer_prest = cont + 1
                        if self.numer_prest == self.numero_prestacao:
                            cont += 1
                            if self.periodicidade == '4':
                                self.num_incr += 3 - 1
                            elif self.periodicidade == '1':
                                self.num_incr += 7 - 1
                            elif self.periodicidade == '2':
                                self.num_incr += 15 - 1
                            elif self.periodicidade == '5':
                                self.num_incr += 6 - 1
                            elif self.periodicidade == '6':
                                self.num_incr += 1

                        else:
                            cont_prest -= 1
                            cont += 1
                            if self.periodicidade == '4':
                                if cont > 2:
                                    self.num_incr += 3 - 1
                            elif self.periodicidade == '1':
                                if cont > 2:
                                    self.num_incr += 7 - 1
                            elif self.periodicidade == '2':
                                if cont > 2:
                                    self.num_incr += 15 - 1
                            elif self.periodicidade == '5':
                                if cont > 2:
                                    self.num_incr += 6 - 1
                            elif self.periodicidade == '6':
                                if cont > 2:
                                    self.num_incr += 1

                    if self.numer_prest != 1:
                        if self.numero_prestacao != 1:
                            sql = "DELETE FROM plano_financiamento WHERE divida < amortizacao AND numer_prest = 1"
                            self.env.cr.execute(sql)
                        if self.numero_prestacao != 2:
                            sqls = "DELETE FROM plano_financiamento WHERE divida < amortizacao AND numer_prest = 2"
                            self.env.cr.execute(sqls)

                    prest = {"type": "ir.actions.do_nothing"}
                    return prest
        else:
            pass

        plano_link = self.env['plano.financiamento'].search([('codigo_desemb', '=', self.codigo), ('nome_terc', '=', self.identificacao_proponente.id)])
        for p in plano_link:
            p.plano_desembolso_id = self.id

    def _comput_line(self, line):
        return {'displlay_type': line.displlay_type, 'state': 'draft', }

    @api.model
    @api.onchange('control_presta', )
    def select_presta(self):

        if self.control_presta == True or self.control_presta == False:

            select_pres = self.env['plano.financiamento'].search([('nome_terc', '=', self.identificacao_proponente.id)])
            list_of_docum = []
            for line in select_pres:
                data = self._comput_line(line)
                data.update({'data_documento': line.data_documento, 'prestacao': line.prestacao,
                             'juro_jerado': line.juro_jerado, 'amortizacao': line.amortizacao, 'divida': line.divida})
                list_of_docum.append((1, line.id, data))
            # if self.solici == True:
            #   return {'value': {"prestacao_ids": list_of_docum}}
            # if self.ata == True:

            return {'value': {"plano_financiamento_ids": list_of_docum}}
