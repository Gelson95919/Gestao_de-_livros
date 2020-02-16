# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class acta(models.Model):
    _name = 'acta.comite'
    _rec_name = 'pedido_id'
    _description = 'Acta'
    codigo = fields.Char(string="Codigo", required=True, copy=False, readonly=True, index=True,
                         default=lambda self: self._get_next_cod(), store=True, )  # default=lambda self: _('New')
    numero_ata = fields.Char(string="Numero", index=True, default=lambda self: _('New'))
    codigo_cliente = fields.Char(string="Codigo", equired=True, copy=False, readonly=True, index=True,
                                 default=lambda self: _('New'))
    documentos = fields.Char(string="Documento", default="Acta")
    data_acta = fields.Date(string="Data acta", default=fields.Date.today)
    pedido_id = fields.Many2one('solicitacao.credito', string="Pedido",
                                domain=[('aprovado', '!=', '1'), ('submeter', '=', True), ('estado', '!=', '4')],required=True)#
    codigo_credito = fields.Char(string="Codigo Cred", related="pedido_id.codigo", store=True)
    id_pess = fields.Integer(string="ID Pessoa", related="pedido_id.id", )
    data_pedido = fields.Date(string="Data Pedido", related="pedido_id.data", store=True)
    ilha_cliente = fields.Char(string="Ilha/Cidade", related="pedido_id.name_ilha", store=True)
    telefone = fields.Integer(string="Telefone", related="pedido_id.telefone")
    agente = fields.Many2one(string="Comite", related="pedido_id.agente", store=True)
    name_agente = fields.Char(tring="Nome Agente", related='agente.name')
    proponente = fields.Char(string="Proponente", related="pedido_id.ropornente", store=True)
    identificacao_proponente = fields.Many2one('pessoas', related="pedido_id.identificacao_proponente", store=True,
                                               string="Pessoas", )
    valor_escrita = fields.Char(string="Valor Escrita", related="pedido_id.aplica", store=True,)
    estado_civil = fields.Selection(
        [('1', 'Solteiro(a)'), ('2', 'Casado(a)'), ('3', 'Viúvo(a)'), ('4', 'Divorciado(a)'), ('5', 'Outro')],
         string="Estado", related="identificacao_proponente.estado_civil", store=True,)
    freguesia_id = fields.Many2one('freguesia.freguesia', related="identificacao_proponente.freguesia_id", tring="Freguesia")
    nome_freguesia = fields.Char(string="Nome", related="freguesia_id.name")
    concelho_id = fields.Many2one('concelho.concelho', related="identificacao_proponente.concelho_id", tring="Concelho")
    nome_concelho = fields.Char(string="Nome", related="concelho_id.name")
    endereco_prop = fields.Char(string="Endereco", related="identificacao_proponente.endereco", store=True)
    name = fields.Char(string="Nome", related="identificacao_proponente.name")



    nif = fields.Integer(string="Nif", related="pedido_id.nif")#para remover
    telefone_fixo = fields.Integer(string="Telefone Fixo", related="pedido_id.telefone_fixo", store=True)#para remover
    telemovel = fields.Integer(string="Telemovel", related="pedido_id.telefone", store=True)#para remover

    nif_pessoa = fields.Char(string="NIF", related="pedido_id.nif_pessoa", store=True)
    telefone_pessoa = fields.Char(string="Telefone", related="pedido_id.telefone_pessoa", store=True)
    fixo_pessoa = fields.Char(string="Fax", related="pedido_id.fixo_pessoa", store=True)

    atraso_anterior = fields.Selection([('True', 'Sim'), ('False', 'Não')], default="False", string="Atraso Anterior",)
    avaliacao_qualitativa = fields.Float(string="Avaliacap qualitativa")

    nome_cliente = fields.Many2one(string="Nome", related="pedido_id.identificacao_proponente", store=True)
    tipo_negocio = fields.Char(string="Tipo Negocio", related="pedido_id.nome", store=True)
    receita_operacionais = fields.Float(string="Receita Operacionais", related="pedido_id.receitas_operacionais",
                                         store=True)

    numero_credito = fields.Char(string="Numero", index=True, related="pedido_id.codigo", store=True, )
    custos_opracionais = fields.Float(string="Custo Operacionais", related="pedido_id.custo_operacional", store=True)
    capacidade_pacto = fields.Float(string="Capacidade de Pacto", related="pedido_id.capacidade_pagamento", store=True)
    informacoes_cadastrais = fields.Float(string="Informacoes Cadastrais")
    valor_credito_anterior = fields.Float(string="Valor Credito Anterior")
    valor_solicitado = fields.Float(string="Valor Solicitado", related="pedido_id.valor_solicitado", store=True)
    prestacao_solicitada = fields.Float(string="Prestacao Solicitada", related="pedido_id.prestacao_pagar", store=True)
    valor_sugerido = fields.Float(string="Valor Sugirido", related="pedido_id.valor_gestor", store=True)
    prestacao_sugerido = fields.Float(string="Prestacao Sugirido", related="pedido_id.valor_prestacao", store=True)
    # flux_id = fields.Many2one('fluxo.caixa', string="Pessoas",  related="pedido_id.prestacao_pagar",)

    por = fields.Selection([('1', 'aoano'), ('2', 'ao mês')], default="2", string="Tipo cal jur mes/ano")
    aprovado = fields.Selection([('True', 'Sim'), ('False', 'Não')], string="Aprovado")
    numero = fields.Char(string="Numero", copy=False, default=lambda self: self._get_next_cod(), store=True, )
    valor_total = fields.Integer(string="Valor Total", store=True, readonly=False)
    valor_total_desen = fields.Float(string="Valor Total Desembolso", store=True, compute='gerar_plan_desemb',)
    numero_prestacoes = fields.Integer(string="Numero Prestacao", related="pedido_id.numero_prestacoes", store=True,
                                       readonly=False)
    periodicidade = fields.Selection(
        [('1', 'Semanal'), ('2', 'Quinzenal'), ('3', 'Mensal'), ('4', 'Trimestral'), ('5', 'Anual'), ('0', 'Outros')])
    mes = fields.Integer(string="Mes")
    data_desembolso = fields.Date(string="Data Desembolso", default=fields.Date.today)
    date_start = fields.Date(string="Primeira Prestação", default=fields.Date.today)
    periodo_carencia = fields.Char(string="Períodos de Carência")
    calcular_juro = fields.Boolean(string="Calcular juros no Períodos Carência")
    valor = fields.Float(string="Valor Comicao")#nao vale porque e do tipo Char

    valor_comicao = fields.Float(string="Valor Comicao")
    valor_percentual = fields.Boolean(string="Tchek Box %")
    financiamento_taxa = fields.Selection([('1', 'Sim'), ('2', 'Não')], default="2")
    gerar_conta_popanc = fields.Boolean(string="Gerar Conta Popanca")
    montante = fields.Float(string="Montante")
    fundo_id = fields.Many2one('fundos.fundos', string="Fundo")
    obs = fields.Text(string="OBS")
    comite_list_ids = fields.One2many('comite.credito', 'acta_id', string="Lista Comite")
    desting_ata = fields.Boolean(string="Ata", default=True)
    submeter = fields.Boolean(string="Submeter", default=True)
    acta_ou_solici = fields.Boolean(string="Acta ou Solicitação", default=True)
    desting_doc_quo = fields.Boolean(string="Documento/Quotas", default=True)
    juros = fields.Float(string="Juros/Taxa", store=True,)# default=10
    metudo_calculo = fields.Selection([('1', 'Degresivo'), ('2', 'Constante'), ('3', 'Simples')],
                                      default="3")
    fecha_abre = fields.Selection([('True', 'Fechado'), ('False', 'Aberto')], default='False', string='Fecho')

    # OPS
    documentos_op = fields.Char(string="Documento", default="Tesouraria/OP")
    control_op = fields.Boolean(default=True)  # controlar os OP
    numero_op = fields.Char(string='Numero', store=True, copy=True, readonly=False,
                            default=lambda self: _('New'))  # numero com prefix
    tot_op = fields.Float(string="Total OP", compute="calcula_tot_op", store=True)

    tipo = fields.Selection([('1', 'Proponho'), ('2', 'Não Proponho')], default="2")
    valor_gestor = fields.Float(string="Valor", related="pedido_id.valor_gestor", store=True, readonly=False)

    valor_prestacao = fields.Float(string="Valor Prestacao", related="pedido_id.prestacao_pagar", store=True,)
    prazo = fields.Integer(string="Prazo", related="pedido_id.numero_prestacoes", store=True,)
    periodicidade_agent = fields.Selection(
        [('1', 'Semanal'), ('2', 'Quinzenal'), ('3', 'Mensal'), ('4', 'Trimestral'),
         ('5', 'Anual'), ('6', 'Outros')], default="3")
    parecer = fields.Text(string="Parecer")
    anulado = fields.Boolean(string="Anulado")
    reg_doc_ids = fields.One2many('reg.docum', 'ata_id',
                                              string="Plano Financiamento", store=True,
                                              copy=True, index=True)#capt report

    # Metudo de Texte para os campos chec no relatorios
    atrazo_sim = fields.Char(string="Atrazo", compute='atrib', store =True)
    atrazo_nao = fields.Char(string="Atrazo", compute='atrib', store =True)
    juros_quadro = fields.Float(string="Juros calculado", compute="gerar_plan_desemb", store=True)
    amotizacao = fields.Float(string="Amortização calculado", compute="gerar_plan_desemb", store=True)
    val_cont_pop_e_vomicao = fields.Float(string="Calcular os  valores", compute="cal_val_com", store=True) #esse campo serve para calcular os valores da comição e de conta poupança caso exister
    estado = fields.Selection([('1', 'Pendente'), ('2', 'Submetido'), ('3', 'Aberto'), ('4', 'Fechado')], default="1",
                              index=True, track_visibility='onchange', copy=False)
    submeter_comite = fields.Boolean(string="Submeter Comite")
    prestacao = fields.Float(string="Prestação", compute='gerar_plan_desemb', store =True)
    valor_divida_total = fields.Float(string="Valor em Divida", compute='gerar_plan_desemb', store =True)
    renegociado = fields.Boolean(string="Renegociado")

    id_credito = fields.Char(string="IDCREDITO")

    dados_antigo = fields.Boolean(string="Dados Antigo")  # se True porque os dados são antigo
    reg_docum_ids_desenb = fields.One2many('reg.docum', 'id_cred_aprov', string="Prestação", store=True,
                                           copy=True)#reg_doc_ids devia ficar esse campo pelo facto de não ter o ata_id no reg_docum coloquei o campo reg_docum_ids_desenb
    setor = fields.Selection([('1', 'Comércio'), ('2', 'Serviço'), ('3', 'Produção'), ('4', 'Agricultura'),
                              ('5', 'Pesca'), ('6', 'Pequena Industria e Transf'), ('7', 'Pecuária'),
                              ('8', 'Agropecuária'), ('9', 'Consumo'), ('10', 'Melhoria habitacional'),
                              ('11', 'Outros')], related="pedido_id.setor", required=True)
    nome_agente = fields.Char(tring="Agente", related="pedido_id.nome_agente")
    prazo_agente = fields.Integer(string="Prazo", related="pedido_id.prazo")
    parecer_agente = fields.Text(string="Parecer", related="pedido_id.parecer")
    valor_agente= fields.Float(string="Valor Agente", related="pedido_id.valor_gestor")




    @api.one
    @api.constrains('dados_antigo')
    def val_dados_antig(self):  # Verificar se o dados e antigo ou não
        if self.dados_antigo == True:
            pass
           #raise ValidationError(
           #    'Dados antigo, ha algumas informações que precisam ser modificado, contacta o adminstrador de sistema se consideras-te que é um erro ')

    def compor_op(self):
        ata = self.env['acta.comite'].search([('id', '>=', 1)])
        #atac = self.env['acta.comite'].search([('juros', '=', 75)])
        #ataca = self.env['acta.comite'].search([('juros', '=', 17)])
        for c in ata:
            c.valor_comicao = c.valor

        #for a in atac:
        #    a.juros = 0.75

        #for b in ataca:
        #    b.juros = 1.7


    """@api.onchange('atraso_anterior')
    @api.depends('atraso_anterior')
    def atrib (self):
        if self.atraso_anterior == "1":
            self.atrazo_sim = "X"
        else:
            self.atrazo_sim = " "
        if self.atraso_anterior == "2":
            self.atrazo_nao = "X"                  
        else:
            self.atrazo_nao = " "  """




    @api.model
    def _get_next_cod(self):
        sequence = self.env['ir.sequence'].search([('code', '=', 'ata.codigo')])
        # num_sequenc = self.env['ir.sequence'].search([('code', '=', 'ata.numero')])
        next = sequence.get_next_char(sequence.number_next_actual)
        # next_num = num_sequenc.get_next_char(num_sequenc.number_next_actual)
        return next

    @api.model
    def create(self, vals):
        vals['codigo'] = self.env['ir.sequence'].next_by_code('ata.codigo') or _('New')
        vals['numero'] = self.env['ir.sequence'].next_by_code('ata.numero') or _('New')
        vals['numero_ata'] = self.env['ir.sequence'].next_by_code('acta.codigo.num') or _('New')
        # vals['name'] = str(vals['name']) + str(self.name)
        vals['numero_op'] = self.env['ir.sequence'].next_by_code('op.micro.num') or _('New')
        vals['codigo_cliente'] = self.env['ir.sequence'].next_by_code('sequ.clientes.codigo') or _('New')
        res = super(acta, self).create(vals)
        # self.remo_docum_allter()
        res.submet_ata() #decomentar depois de import
        return res
    #===============decomentar depois de import================================================
    @api.multi
    def write(self, vals):

        val = {}
        valor = {}
        if 'numero_ata' in vals: val['numeros_docum'] = vals['numero_ata']
        if 'codigo' in vals: val['id_documento'] = vals['codigo']
        if 'pedido_id' in vals: val['pedido_id'] = vals['pedido_id']
        if 'valor_total' in vals: val['total'] = vals['valor_total']
        if 'valor_total' in vals: val['valorAsc'] = vals['valor_total']
        if 'data_pedido' in vals: val['data_documento'] = vals['data_pedido']
        if 'aprovado' in vals: val['aprovado'] = vals['aprovado']
        if 'taxa' in vals: val['juros'] = vals['taxa']
        if 'por' in vals: val['por'] = vals['por']
        campo = self.env['reg.docum'].search(
            [('nome_terc', '=', self.identificacao_proponente.id), ('desting_ata', '=', self.desting_doc_quo)])
        campo.write(val)
        if self.aprovado == 'True':
            selict = self.env['solicitacao.credito'].search(
                [('identificacao_proponente', '=', self.identificacao_proponente.id), ('estado', '=', '1')])
            selict.write({'estado': '3'})

        """if 'valor_total' in vals: valor['valor'] = vals['valor_total']
        if 'prazo_prestacao' in vals: valor['numero_prestacao'] = vals['prazo_prestacao']
        if 'por' in vals: valor['por'] = vals['por']
        if 'data_desembolso' in vals: valor['data'] = vals['data_desembolso']
        if 'primeira_prestacao' in vals: valor['data_primeira'] = vals['primeira_prestacao']
        if 'periodo_carencia' in vals: valor['periodo_carencia'] = vals['periodo_carencia']
        if 'calcular_juro' in vals: valor['calcular_juro_periodo_carenc'] = vals['calcular_juro']
        if 'calculo' in vals: valor['metudo_calculo'] = vals['calculo']
        campo_desem = self.env['credito.aprovado'].search(
            [('codigo', '=', self.codigo)])
        campo_desem.write(valor)"""
        obg = super(acta, self).write(vals)
        return obg
    #===========================================================================================================

    @api.constrains('date_start')
    def val_data(self):
        if self.date_start == self.data_desembolso:
           raise ValidationError('Data de Desembolsos igual a data de primeira prestação')

    def submet_ata(self):
        selict = self.env['solicitacao.credito'].search(
            [('identificacao_proponente', '=', self.identificacao_proponente.id), ('estado', '=', '0')])
        selict.write({'estado': '1'})
        if self.aprovado == 'True':
            selict = self.env['solicitacao.credito'].search(
                [('identificacao_proponente', '=', self.identificacao_proponente.id), ('estado', '=', '1')])
            selict.write({'estado': '3'})

    # ----------------------fechar ata -------------------------------------------------------------
    def fechar(self):
        reval_terc = self.env["terceiro.terceiro"].search([('codigo', '=', '000')])
        for reval in reval_terc:
            reval.write({'receb_pess': False})
        #reg_obj_fech = self.env['reg.docum'].search([('nif', '=', self.nif), ('desting_ata', '=', True), ('docPag', '=', False), ('cobrado', '=', False)]).unlink()
        self.write({'fecha_abre': 'True'})
        self.write({'estado': '4'})
        clien = self.env['clientes'].search([('nome_terc', '=', self.identificacao_proponente.id)])
        if not clien:
           self.create_cliente()

        self.credito_aprovado()
        #self.my_action()

        #solic = self.env['solicitacao.credito'].search([('identificacao_proponente', '=', self.identificacao_proponente.id), ('aprovado', '=', '2'), ('estado', '=', '2')])
        #solic.write({'aprovado': self.aprovado})

        flx_caix = self.env['fluxo.caixa'].search([('ropornente_id', '=', self.identificacao_proponente.id)])
        flx_caix.write({'aprovado': self.aprovado})

        bal = self.env['balanco'].search([('ropornente_id', '=', self.identificacao_proponente.id)])
        bal.write({'aprovado': self.aprovado})

        self.creat_op()
        pessoa = self.env['pessoas'].search(
            [('id', '=', self.identificacao_proponente.id), ('tem_solicitacao', '=', '2'), ('tem_pedido', '=', '2')])
        pessoa.write({'tem_solicitacao': '1'})
        pessoa.write({'tem_pedido': '1'})
        pessoa.write({'ata_id': self.id})

        # ----------------------Aque prepara reg docum para receber as solicitações -----------------------------------
        self.creat_det_op()
        self.gerar_plan_desemb()

        # --------------------------tratar cliente e terceiro-------------------------------------------
        reval_terc = self.env["terceiro.terceiro"].search([('codigo', '=', '000')])
        for reval in reval_terc:
            reval.write({'receb_pess': True})

        pessoa_terc = self.env['terceiro.terceiro'].search([('ata_id', '=', clien.ata_id), ('tem_fatur', '=', False), ('tem_pedido', '=', '2')])
        if pessoa_terc:
            for p in pessoa_terc:
                p.tem_fatur = True
                p.write({'tem_pedido': '1'})
                p.write({'tem_solicitacao': '1'})


        pessoa_terc_forn = self.env['terceiro.terceiro'].search([('ata_id', '=', self.id), ('tem_despesas', '=', False)])
        for p in pessoa_terc_forn:
            p.tem_despesas = True
        if self.aprovado == 'True':
            selict = self.env['solicitacao.credito'].search(
                [('identificacao_proponente', '=', self.identificacao_proponente.id), ('aprovado', '=', self.aprovado), ('estado', '=', '3')])
            selict.write({'estado': '6'})
        prest_gerad = self.env['reg.docum'].search([('ata', '=', self.id)])
        if prest_gerad:
            for pr in prest_gerad:
                pr.ata_id = self.id
        return {
            "type": "ir.actions.act_window",
            "res_model": "acta.comite",
            "views": [[False, "form"]],
            "res_id": self.id,
            "target": "main",
            "context": {'show_message': True},
        }

    # -------------------------------------------------------------------------------------------------
    # Abrir Ata
    @api.one
    def abrir(self):#E preciso Analizar a função de abrir ata alguns duvidas
        self.write({'estado': '3'})
        self.write({'fecha_abre': '1'})
        pessoa_ter = self.env['terceiro.terceiro'].search([('ata_id', '=', self.id)])
        pode_abrir = self.env["reg.docum"].search(
            [('nome_terc', '=', pessoa_ter.id), ('cobrado', '=', True), ('ata', '=', self.id), ('desting_ata', '=', True)])
        if pode_abrir:
            raise ValidationError('Cliente ja tem algumas prestações pagas')
        else:
             self.iliminar()



    # ---------------------------------------------------------------------------------------------------------------
    @api.one
    def iliminar(self):#Anula apenas os registros que foi feito apartir de ata
        self.write({'fecha_abre': '1'})
        pessoa_ter = self.env['terceiro.terceiro'].search([('ata_id', '=', self.id)])
        pode_anular = self.env["reg.docum"].search([('nome_terc', '=', pessoa_ter.id), ('cobrado', '=', False), ('ata', '=', self.id)])
        if pode_anular:
            anular = self.env["reg.docum"].search([('nome_terc', '=', pessoa_ter.id), ('estado', '=', '1'), ('ata', '=', self.id)]).unlink()
            docum_op = self.env['tesouraria.ordem.pagamento'].search([('fornecedor_id', '=', pessoa_ter.id), ('estado', '=','1'), ('ata', '=', self.id)]).unlink()
            docum_op = self.env['detalhes.documento.op'].search([('teso_ordem_pagamento_id', '=', self.id)]).unlink()
            solic = self.env['solicitacao.credito'].search([('identificacao_proponente', '=', self.identificacao_proponente.id), ('aprovado', '=', '1')])
            solic.write({'aprovado': '2'})
            cred_aprov_obj = self.env['credito.aprovado'].search([('identificacao_proponente', '=', self.identificacao_proponente.id), ('estado', '=','1'), ('ata_id', '=', self.id)]).unlink()
            clien = self.env['clientes'].search([('nome_terc', '=', self.identificacao_proponente.id), ('ata_id', '=', self.id), ('estado', '=','1')])
            if clien:
                clien.unlink()
        else:
            raise ValidationError('O cliente ja tem algumas documentos pagas')

    #def anlar(self):
    #    self.anulado = True
    #    cred_aprov_obj = self.env['credito.aprovado'].search([('identificacao_proponente', '=', self.identificacao_proponente.id)])
    #    if cred_aprov_obj:
    #        for cr in cred_aprov_obj:
    #            cr.anulado = True
    # -------------------------------------------------------------------------------------------------
    def _comput_line(self, line):
        return {'displlay_type': line.displlay_type, 'state': 'draft'}

    # --------------------------add Cred aprovado--------------------------------------------------------
    @api.model
    def credito_aprovado(self):
        if self.aprovado == 'True':
            cred_aprov_obj = self.env['credito.aprovado']
            cred_apro = cred_aprov_obj.create({'valor': self.valor_total, 'numero_prestacao': self.numero_prestacoes,
                'por': self.por, 'identificacao_proponente': self.identificacao_proponente.id, 'juros': self.juros,
                'data': self.data_desembolso, 'prestacao': self.prestacao, 'juros_quadro': self.juros_quadro, 'ata_id': self.id,
                'data_primeira': self.date_start, 'periodo_carencia': self.periodo_carencia, 'aprovado': self.aprovado,
                'calcular_juro_periodo_carenc': self.calcular_juro, 'metudo_calculo': self.metudo_calculo})
            return cred_apro

    # ---------------------------------remov doc não aprov---------------------------------------------------
    def remo_docum_allter(self):
        self.env["reg.docum"].search(
            [('nome_terc', '=', self.identificacao_proponente.id), ('aprovado', '=', 'nao')]).unlink()
        # sql = "DELETE FROM reg_docum WHERE submeter = False AND desting_ata =True"
        # self.env.cr.execute(sql)

    # --------------------------fazer um plano financiamento--------------------------------------------------
    def plano_financiamento(self):
        if self.aprovado == 'True':
            plan = self.env["plano.financiamento"].search(
                [('nome_terc', '=', self.identificacao_proponente.id)]).unlink()
            ac = self.env['ir.model.data'].xmlid_to_res_id('gestao_microfinancas.plano_desembolso_form', raise_if_not_found=True)
            self.remo_docum_allter()
            valor_total = False
            numero_prestacoes = False
            identificacao_proponente = False
            codigo = False
            aprovado = False
            date_start = False
            acta_ou_solici = False
            juros = False
            for o in self:
                valor_total = o.valor_total
                numero_prestacoes = o.numero_prestacoes
                identificacao_proponente = o.identificacao_proponente
                codigo = o.codigo
                date_start = o.date_start
                acta_ou_solici = o.acta_ou_solici
                juros = o.juros
                aprovado = o.aprovado
            result = {
                'name': 'Plano de Desembolso',
                'view_type': 'form',
                'res_model': 'plano.desembolso',
                'view_id': ac,
                'context': {'default_valor': valor_total, 'default_numero_prestacao': numero_prestacoes,
                            'default_identificacao_proponente': identificacao_proponente.id, 'default_codigo': codigo,
                            'default_ata': acta_ou_solici, 'default_juros': juros, 'default_aprovadp': aprovado,
                            'default_date_start': date_start, },
                'type': 'ir.actions.act_window',
                'target': 'new',
                'view_mode': 'form'
            }

            self.gerar_plan_financiamento()
            return result
        else:
            raise ValidationError('Para isso, as atas devem ser aprovadas')

    # -------------------------gerar plano desembolso no reg docum---------------------------------------------
    @api.one
    #@api.depends('numero_prestacoes', 'juros_quadro', 'valor_total', )
    def gerar_plan_desemb(self): #para reg_docum
        pessoa_ter = self.env['terceiro.terceiro'].search([('ata_id', '=', self.id)])
        self.ensure_one()
        cont_prest = self.numero_prestacoes
        cont = 0
        j = self.juros / 100.0
        self.juros_quadro = self.valor_total * j
        self.amotizacao = round(self.valor_total / self.numero_prestacoes)
        self.prestacao = round(self.amotizacao + self.juros_quadro)
        self.divida = round(self.valor_total - self.amotizacao)
        self.valor_divida_total = round(self.prestacao * self.numero_prestacoes)
        if self.financiamento_taxa == 1:
            if self.gerar_conta_popanc == True:
                self.valor_total_desen = self.valor - self.montante
            else:
                self.valor_total_desen = self.prestacao
        else:
            self.valor_total_desen = self.prestacao
        cred_aprov_obj = self.env['credito.aprovado'].search(
            [('identificacao_proponente', '=', self.identificacao_proponente.id), ('estado', '=', '1')])
        # for rec in cred_aprov_obj:
        # cred_aprov_id = rec.id

        while cont_prest > 0:
            if cont == 0: #este e o recoord de OP (PRESTAÇÃO 0)
                plano_obj_0 = self.env['reg.docum']
                plano_desemb_0 = plano_obj_0.create({'numer_prest': 0, 'divida': self.valor_total_desen,
                                                 'nome_terc': pessoa_ter.id,
                                                 'valor_desembolso': self.valor_total_desen,
                                                 'desting_solict': self.desting_doc_quo,
                                                 'prest_zerro': self.desting_doc_quo,
                                                 'desting_ata': self.desting_doc_quo,
                                                 'id_cred_aprov': cred_aprov_obj.id,
                                                 'total': self.valor_total_desen,
                                                 'ata': self.id,
                                                 'saldo_pagamento': self.valor_total_desen,
                                                 #'saldo': self.prestacao,
                                                 'valorAsc': self.valor_total_desen,
                                                 'submeter': self.submeter,
                                                 'agente': self.agente.id,
                                                 'cod_documento': self.numero_op,
                                                 'numero_credito': self.numero_credito,
                                                 'desting_doc_desp': self.desting_doc_quo,
                                                 'numeros_docum': self.codigo,
                                                 'data_documento': self.data_pedido})
            if cont == 1:
                cod_doc = self.numero_ata + '/' + str(cont)
                data_prest = self.date_start
                plano_obj_1 = self.env['reg.docum'].search([('numer_prest', '=', cont)])
                plano_desemb_1 = plano_obj_1.create({'prestacao': self.valor_total_desen, 'submeter': self.submeter,
                                                 'juro_jerado': self.juros_quadro, 'total': self.valor_total_desen,
                                                 'valorAsc': self.valor_total_desen, 'numer_prest': self.numer_prest,
                                                 'nome_terc': pessoa_ter.id,
                                                 'saldo': self.valor_total_desen,
                                                 'valor_desembolso': self.valor_total_desen,
                                                 'ata': self.id,
                                                 'cod_documento': cod_doc,
                                                 'documentos': self.documentos,
                                                 'desting_ata': self.desting_doc_quo,
                                                 'desting_doc_vend': self.desting_doc_quo,
                                                 'desting_solict': self.desting_doc_quo,
                                                 'numero_credito': self.numero_credito,
                                                 'aprovado': self.aprovado,
                                                 'agente': self.agente.id,
                                                 'id_cred_aprov': cred_aprov_obj.id,
                                                 'amortizacao': self.amotizacao, 'divida': self.divida,
                                                 'numeros_docum': self.codigo, 'data_documento': data_prest, })
            if cont > 1:
                cod_doc = self.numero_ata + '/' + str(cont)
                date_after_month = self.date_start + relativedelta(months=1 + cont - 2)
                data_prest = date_after_month
                plano_obj_maior_1 = self.env['reg.docum'].search(
                    [('numer_prest', '=', cont - 1), ('nome_terc', '=', pessoa_ter.id)])
                for rec in plano_obj_maior_1:
                    if self.divida > 0:
                        self.divida = rec.divida - rec.amortizacao
                        if self.divida < 6 and self.divida != 0:  # aque resolve o problema de  1 escudo ....
                            self.amotizacao = rec.divida
                            self.valor_total_desen += self.divida
                            self.valor_divida_total +=self.divida
                            self.divida = 0
                        plano_desemb_maior_1 = plano_obj_maior_1.create({'prestacao': self.valor_total_desen, 'submeter': self.submeter,
                                                         'juro_jerado': self.juros_quadro, 'total': self.valor_total_desen,
                                                         'valorAsc': self.valor_total_desen, 'numer_prest': self.numer_prest,
                                                         'nome_terc': pessoa_ter.id,
                                                         'saldo': self.valor_total_desen,
                                                         'ata': self.id,
                                                         'cod_documento': cod_doc,
                                                         'valor_desembolso': self.valor_total_desen,
                                                         'documentos': self.documentos,
                                                         'desting_ata': self.desting_doc_quo,
                                                         'aprovado': self.aprovado,
                                                         'agente': self.agente.id,
                                                         'numero_credito': self.numero_credito,
                                                         'id_cred_aprov': cred_aprov_obj.id,
                                                         'desting_doc_vend': self.desting_doc_quo,
                                                         'desting_solict': self.desting_doc_quo,
                                                         'amortizacao': self.amotizacao, 'divida': self.divida,
                                                         'numeros_docum': self.codigo, 'data_documento': data_prest, })

            self.numer_prest = cont + 1
            if self.numer_prest == self.numero_prestacoes:
                pass
            else:
                cont_prest -= 1
            cont += 1

        plano_des_obj = self.env['reg.docum'].search([('receb_solici', '=', True)])
        for docu in plano_des_obj:
            if docu:
                docu.write({'receb_solici': False})
        cred_aprov = self.env['credito.aprovado'].search(
            [('ata_id', '=', self.id), ('estado', '=', '1')])
        if cred_aprov:
            for c in cred_aprov:
                c.valor_em_div = self.valor_divida_total #calcula a divida total do cliente
                c.prestacao = self.valor_total_desen
                c.juros_quadro = self.juros_quadro
        return True

    # -----------------------criar cliente------------------------------------------------------------------
    def create_cliente(self):
            clien = self.env['clientes']
            cliente = clien.create({'codigo_cliente': self.codigo_cliente, 'id_pess': self.id_pess, 'ata_id': self.id,
                                    'nome_terc': self.identificacao_proponente.id, 'name': self.name})
            return cliente



    # --------------------------plano fin-----------------------------------------------------------------------
    @api.one
    @api.depends('numero_prestacoes', 'juros_quadro', 'valor_total', )
    def gerar_plan_financiamento(self):
        pessoa_ter = self.env['pessoas'].search([('id', '=', self.identificacao_proponente.id)])
        self.ensure_one()

        cont_prest = self.numero_prestacoes
        cont = 0
        j = self.juros / 100.0
        self.juros_quadro = self.valor_total * j
        self.amotizacao = round(self.valor_total / self.numero_prestacoes)
        self.prestacao = round(self.amotizacao + self.juros_quadro)
        self.divida = round(self.valor_total - self.amotizacao)
        while cont_prest > 0:
            if cont == 0:
                plano_obj_lina0 = self.env['plano.financiamento']
                plano_desemb = plano_obj_lina0.create({'numer_prest': 0, 'divida': self.valor_total,
                                                       'nome_terc': self.identificacao_proponente.id,
                                                       'desting_solict': self.desting_doc_quo,
                                                       'data_documento': self.data_pedido, })

            if cont == 1:
                data_prest = self.date_start
                plano_obj = self.env['plano.financiamento'].search(
                    [('numer_prest', '=', cont), ('nome_terc', '=', self.identificacao_proponente.id)])
                plano_desemb = plano_obj.create({'prestacao': self.prestacao,
                                                 'juro_jerado': self.juros_quadro, 'total': self.prestacao,
                                                 'numer_prest': self.numer_prest,
                                                 'desting_solict': self.acta_ou_solici,
                                                 'nome_terc': pessoa_ter.id,
                                                 'amortizacao': self.amotizacao, 'divida': self.divida,
                                                 'data_documento': data_prest, })
            if cont > 1:
                date_after_month = self.date_start + relativedelta(months=1 + cont - 2)
                data_prest = date_after_month
                plano_obj = self.env['plano.financiamento'].search(
                    [('numer_prest', '=', cont - 1), ('nome_terc', '=', self.identificacao_proponente.id)])
                for rec in plano_obj:
                    if self.divida > 0:
                        self.divida = rec.divida - rec.amortizacao
                        if self.divida < 6 and self.divida != 0:  # aque resolve o problema de  1 escudo ....
                            self.amotizacao = rec.divida
                            self.divida = 0
                        plano_desemb = plano_obj.create({'prestacao': self.prestacao,
                                                   'juro_jerado': self.juros_quadro, 'total': self.prestacao,
                                                   'numer_prest': self.numer_prest,
                                                   'desting_solict': self.acta_ou_solici,
                                                   'nome_terc': pessoa_ter.id,
                                                   'amortizacao': self.amotizacao, 'divida': self.divida,
                                                   'data_documento': data_prest, })

            self.numer_prest = cont + 1
            if self.numer_prest == self.numero_prestacoes:
                pass
            else:
                cont_prest -= 1
            cont += 1
        return True

    # -------------Criar ordem pagamento---------------------------------------------------------------------
    def creat_op(self):
        pessoa_ter = self.env['terceiro.terceiro'].search([('ata_id', '=', self.id)])
        obs = 'Pelo Desembolso do Emprestimo Nº ' + self.codigo
        # self.detales = obs
        docum_op = self.env['tesouraria.ordem.pagamento']
        for p in pessoa_ter:
            doc_op = docum_op.create({'fornecedor_id': p.id, 'sem_cta_cte': self.desting_doc_quo, 'op_solic': self.desting_doc_quo,
                 'valor_total': self.valor_total, 'detalhes_ordem': obs, 'montante': self.tot_op, 'ata': self.id})#, 'nif_pessoa': self.nif_pessoa

    # ----------------------calcula o valor total de op----------------------------------------------------------
    #====================decomentar depois de import==========================================================
    @api.one
    @api.depends('valor_total', 'montante')
    def calcula_tot_op(self):
        if self.gerar_conta_popanc == True:
            self.tot_op = self.valor_total + self.montante
        else:
            self.tot_op = self.valor_total
   #======================================================================================================
    # ----------------------gerar detalhes ordem pagamento ------------------------------------------------------
    #==================decomentar depois de import=================================================================
    @api.depends('valor_total')
    def cal_val_com(self):
        for rec in self:
            rec.val_cont_pop_e_vomicao = rec.valor_total

    #==========================================================================================================
    def creat_det_op(self):
        # self.val_cont_pop_e_vomicao = self.valor_total
        det_op = self.env['tesouraria.ordem.pagamento'].search([('ata', '=', self.id)])

        if self.financiamento_taxa == '2':  #Não
            if self.gerar_conta_popanc == True:
                param = self.env['parametros.parametros'].search([('variavel', '=', 'codDesembolso')])
                cod_comp = self.env['compras.compras'].search([('codigo', '=', param.valor)])
                if not cod_comp:
                    raise ValidationError('Verifica a configuração de sistema! Contacte o administrador de sistema se considera que isso e um erro.')
                else:
                    #self.val_cont_pop_e_vomicao =self.valor_total - self.montante
                    for item in range(2):
                        if item == 0:
                            obs = 'Desembolso Credito Nº ' + self.codigo
                            docum_op = self.env['detalhes.documento.op']
                            for p in det_op:
                                doc_op = docum_op.create(
                                    {'codigo_id': cod_comp.id, 'descrecao': obs, 'codigo_cliente': self.codigo_cliente,
                                     'valor': self.val_cont_pop_e_vomicao,  'ata': self.id,
                                     'teso_ordem_pagamento_id': p.id, })  # 'ordem_pagamento_id': self.id
                        if item == 1:
                            param_pop = self.env['parametros.parametros'].search([('variavel', '=', 'codPoupanca')])
                            cod_comp_pop = self.env['compras.compras'].search([('codigo', '=', param_pop.valor)])
                            obss = 'Poupança Credito Nº ' + self.codigo
                            docum_ops = self.env['detalhes.documento.op']
                            for p in det_op:
                                docu_op = docum_ops.create(
                                    {'codigo_id': cod_comp_pop.id, 'descrecao': obss, 'codigo_cliente': self.codigo_cliente,
                                     'valor': self.montante, 'ata': self.id,
                                     'teso_ordem_pagamento_id': p.id, })  # 'ordem_pagamento_id': self.id
                        item += 1
            else:
                param_desem = self.env['parametros.parametros'].search([('variavel', '=', 'codDesembolso')])
                cod_comp_desem = self.env['compras.compras'].search([('codigo', '=', param_desem.valor)])
                if not cod_comp_desem:
                    raise ValidationError('Verifica a configuração de sistema! Contacte o administrador de sistema se considera que isso e um erro.')
                else:
                    obs = 'Desembolso Credito Nº ' + self.codigo
                    docum_op = self.env['detalhes.documento.op']
                    for p in det_op:
                        doc_op = docum_op.create({'codigo_id': cod_comp_desem.id, 'descrecao': obs, 'codigo_cliente': self.codigo_cliente,
                                                  'valor': self.valor_total, 'ata': self.id,
                                                  'teso_ordem_pagamento_id': p.id, })
        else:   #Sim
            #self.val_cont_pop_e_vomicao = self.valor_total
            if self.gerar_conta_popanc == True:

                #self.val_cont_pop_e_vomicao = self.valor_total - self.montante - self.valor_comicao
                param_com = self.env['parametros.parametros'].search([('variavel', '=', 'codComicao')])
                cod_comp_com = self.env['compras.compras'].search([('codigo', '=', param_com.valor)])
                if not cod_comp_com:
                    raise ValidationError('Verifica a configuração de sistema! Contacte o administrador de sistema se considera que isso e um erro.')
                else:

                    param_desem = self.env['parametros.parametros'].search([('variavel', '=', 'codDesembolso')])
                    cod_comp_desem = self.env['compras.compras'].search([('codigo', '=', param_desem.valor)])
                    if not cod_comp_desem:
                        raise ValidationError(
                            'Verifica a configuração de sistema! Contacte o administrador de sistema se considera que isso e um erro.')
                    else:
                        obs = 'Desembolso Credito Nº ' + self.codigo
                        docum_op = self.env['detalhes.documento.op']
                        for p in det_op:
                            doc_op = docum_op.create(
                                {'codigo_id': cod_comp_desem.id, 'descrecao': obs,
                                 'codigo_cliente': self.codigo_cliente,
                                 'valor': self.valor_total, 'ata': self.id,
                                 'teso_ordem_pagamento_id': p.id, })

                    for item in range(2):
                        if item == 0:
                            obs = 'Comição Credito Nº ' + self.codigo
                            docum_op = self.env['detalhes.documento.op']
                            for p in det_op:
                                doc_op = docum_op.create(
                                    {'codigo_id': cod_comp_com.id, 'descrecao': obs, 'codigo_cliente': self.codigo_cliente,
                                     'valor': self.valor_comicao, 'ata': self.id,
                                     'teso_ordem_pagamento_id': p.id, })
                        if item == 1:
                            param_po = self.env['parametros.parametros'].search([('variavel', '=', 'codPoupanca')])
                            cod_comp_po = self.env['compras.compras'].search([('codigo', '=', param_po.valor)])
                            obs = 'Poupança Credito Nº ' + self.codigo
                            docum_op = self.env['detalhes.documento.op']
                            doc_op = docum_op.create(
                                {'codigo_id': cod_comp_po.id, 'descrecao': obs, 'codigo_cliente': self.codigo_cliente,
                                 'valor': self.montante, 'ata': self.id,
                                 'teso_ordem_pagamento_id': det_op.id, })
                        item += 1

            else:
                param_c = self.env['parametros.parametros'].search([('variavel', '=', 'codComicao')])
                cod_comp_c = self.env['compras.compras'].search([('codigo', '=', param_c.valor)])
                if not cod_comp_c:
                    raise ValidationError('Verifica a configuração de sistema! Contacte o administrador de sistema se considera que isso e um erro.')
                else:
                    #self.val_cont_pop_e_vomicao = self.valor_total - self.valor_comicao
                    obs = 'Comição Credito Nº ' + self.codigo
                    docum_op = self.env['detalhes.documento.op']
                    for p in det_op:
                        doc_op = docum_op.create({'codigo_id': cod_comp_c.id, 'descrecao': obs, 'codigo_cliente': self.codigo_cliente,
                                                  'valor': self.valor, 'ata': self.id,
                                                  'teso_ordem_pagamento_id': p.id, })  # 'ordem_pagamento_id': self.id

    """ Descomentar depois de importacao"""

    @api.onchange('valor_gestor')
    def advaltot(self):
        self.valor_total = self.valor_gestor

    @api.onchange('submeter_comite')
    def on_change_state_sub(self):
        for record in self:
            if record.submeter_comite == True:
                record.estado = '2'
                record.numero_prestacoes = record.prazo
            else:
                record.estado = '1'

    @api.onchange('aprovado')
    def on_change_state_abert(self):
        for record in self:
            if record.aprovado == 'True':
                record.estado = '3'
            else:
                record.estado = '2'
        solic = self.env['solicitacao.credito'].search(
            [('identificacao_proponente', '=', self.identificacao_proponente.id), ('aprovado', '=', 'False')])
        for s in solic:
            s.estado = '3'

    @api.onchange('submeter_comite', 'tipo')
    def on_change_state_subm(self):
        for record in self:
            if record.tipo == '2':
                record.submeter_comite = False

            if record.submeter_comite == True:
                record.estado = '2'
            else:
                record.estado = '1'


    @api.constrains('submeter_comite')
    def on_change_state_subm(self):
        for record in self:
            if record.submeter_comite == True:
                record.estado = '2'
            else:
                record.estado = '1'

    #@api.onchange('gerar_conta_popanc')
    #def calc_mot_popam(self):
    #    j = 10
    #    self.montante = self.valor_total * (j/100)

    #@api.multi  # ADICIONA ALERTA
    #def my_action(self):

