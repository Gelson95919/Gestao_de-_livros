# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class solicitacaoCredito(models.Model):
    _name = 'solicitacao.credito'
    _description = 'Solicitação de Crédito'
    _rec_name = 'name_client'

    codigo = fields.Char(string="Codigo", required=True, copy=False, readonly=True, index=True,
                         default=lambda self: self._get_next_cod(), store=True, )
    origem = fields.Selection([('1', 'Palestra'), ('2', 'Porta-a-porta'), ('3', 'Rádio'), ('4', 'Divulgação Móvel'),
                               ('5', 'Indicação outro Cliente'), ('6', 'Cartazes'), ('7', 'Eventos'), ('8', 'Outros')],
                              default='1',  required=True)
    data = fields.Date(string="Data", required=True, default=fields.Date.today)
    date_start = fields.Date(string="Data Primeira", default=fields.Date.today)

    identificacao_proponente = fields.Many2one('pessoas', string="Pessoas", required=True, domain=[('tem_pedido', '=', '2')])

    # Dados proponente
    nif = fields.Integer('NIF', store=True)  # para eliminar
    telefone_fixo = fields.Integer(string="Telefone Fixo", related="identificacao_proponente.telefone_fixo",
                                   store=True)  # para eliminar
    telefone = fields.Integer(string="Telefone Fixo")  # para eliminar
    telemovel = fields.Integer(string="Telemovel", related="identificacao_proponente.telemovel",
                               store=True)  # para eliminar

    nif_pessoa = fields.Char(string="NIF", related="identificacao_proponente.nif_pessoa", store=True)
    telefone_pessoa = fields.Char(string="Telefone Negocio", required=True, store=True)
    fixo_pessoa = fields.Char(string="Fax", related="identificacao_proponente.fixo_pessoa", store=True)

    numero_documento = fields.Char(string="Numero Documento", related="identificacao_proponente.numero_documento",
                                   store=True)
    name_client = fields.Char(string="Nome", related="identificacao_proponente.name", store=True)
    cod_client = fields.Char(string="Codigo Pessoa", related="identificacao_proponente.codigo", store=True)
    alcunha = fields.Char(string="Alcunha", related="identificacao_proponente.alcunha", store=True)
    sexo = fields.Selection([('True', 'Feminino'), ('False', 'Masculino')], string="Sexo",
                            related="identificacao_proponente.sexo", store=True)
    local_nascimento = fields.Char(string="Local Nascimento", related="identificacao_proponente.local_nascimento",
                                   store=True)
    data_nascimento = fields.Date(string="Data Nascimento", related="identificacao_proponente.data_nascimento",
                                  store=True)
    nacionalidade = fields.Char(string="Nacionalidade", related="identificacao_proponente.nacionalidade", store=True)
    nome_conjugue = fields.Char(string="Nome Conjugue", related="identificacao_proponente.nome_conjugue", store=True)
    estado_civil = fields.Selection(
        [('1', 'Solteiro(a)'), ('2', 'Casado(a)'), ('3', 'Viúvo(a)'), ('4', 'Divorciado(a)'), ('5', 'Outro')],
        default="1", string="Estado", related="identificacao_proponente.estado_civil", store=True)
    documento = fields.Char(string="Documento", related="identificacao_proponente.documento", store=True)
    endereco_prop = fields.Char(string="Endereco", related="identificacao_proponente.endereco", store=True)
    bairo_id = fields.Many2one('lugares.lugares', string="Bairo", required=True, store=True)
    name_bairo = fields.Char(string="Nome", related="bairo_id.name", )
    concelho_id = fields.Many2one('concelho.concelho', related="bairo_id.concelho_id", tring="Concelho")
    name_concelho = fields.Char(string="Nome", related="concelho_id.name", )
    freguesia_id = fields.Many2one('freguesia.freguesia', related="bairo_id.freguesia_id", tring="Freguesia")
    zona_id = fields.Many2one('zonas.zonas', related="bairo_id.zona_id", tring="Lugares")
    ilha_id = fields.Many2one('ilha', related="bairo_id.ilha_id", string="Ilha")
    name_ilha = fields.Char(string="Nome", related="ilha_id.name", )
    vizinho = fields.Char(string="Vizinho", related="identificacao_proponente.vizinho", store=True)
    tipo_residencia = fields.Selection([('1', 'Própria'), ('2', 'Alugadqa'), ('3', 'Financiada'),
                                        ('4', 'De Familiares'), ('5', 'Outro')], string="Tipo",
                                       related="identificacao_proponente.tipo_residencia", store=True)
    referencia = fields.Text(string="Referencia", related="identificacao_proponente.referencia", store=True)
    no_agregado_familhar = fields.Char(string="Numero Familiares",
                                       related="identificacao_proponente.no_agregado_familhar", store=True)
    n_filhos = fields.Char(string="Numero Filhos", related="identificacao_proponente.n_filhos", store=True)
    escolaridade = fields.Selection(
        [('1', 'Analfabeto'), ('2', 'Primária'), ('3', 'Secundária'),
         ('4', 'Proficional'), ('5', 'Superior')], string="Escolaridade",
        related="identificacao_proponente.escolaridade", store=True)
    tempo = fields.Integer(string="Tempo residencia", related="identificacao_proponente.tempo", store=True)

    ropornente = fields.Char(string="Propornente", related="identificacao_proponente.name", store=True)
    valor_solicitado = fields.Float(string="Valor Solicitado", required=True)#
    valor_escrita = fields.Char(string="Valor Escrita")
    prestacao_pagar = fields.Float(string="Prestacao que pode Pagar", required=True)
    numero_prestacoes = fields.Integer(string="Numero Prestacoes", default=1.00, required=True)
    por = fields.Selection([('ao_ano', 'ao Ano'), ('ao_mes', 'ao mês')], default="ao_ano")
    documentos = fields.Char(string="Documento", default="Solicitação")
    finalidade = fields.Selection(
        [('1', 'Iniciar Negócio'), ('2', 'Reforçar'), ('3', 'Ampliar')],
        default='1', required=True)
    actividade = fields.Char(string="Actividade", required=True)
    aplicacao = fields.Selection(
        [('1', 'Fundo de Maneio'), ('2', 'Inventario Fixo'), ('3', 'Misto'),
         ('4', 'Outro')], default='1', required=True)
    aplica = fields.Char(string="Aplicac")
    outro_aplica = fields.Char(string="Aplicac")
    nome = fields.Char(string="Nome", required=True)
    inicio = fields.Selection([('1', '6 Mess a 1 ano'), ('2', '1 ano  a 3 ano'), ('3', '> 3 ano')], string="Duração",
                              required=True)#
    endereco = fields.Char(string="Endereco", required=True)#

    tipo_grupo = fields.Selection([('1', 'Individual'), ('2', 'Empresário'), ('3', 'Grupo')], default='1',
                                  required=True)#
    nome_grupo = fields.Many2one('grupo', string="Nome Grupo")
    lista_group = fields.One2many('membro', 'solicitacao_id', required=True)#
    primeir_vez = fields.Selection([('1', 'Sim'), ('2', 'Não')], default='1', required=True)#
    local_trabalho = fields.Selection(
        [('1', 'Próprio'), ('2', 'Alugado'), ('3', 'Financiado'), ('4', 'Cedido'),
         ('5', 'Outros')], default='1', required=True)#
    especifica_outro_loc_trab = fields.Char(string='Especifica Outros Local Trabalho')
    setor = fields.Selection([('1', 'Comércio'), ('2', 'Serviço'), ('3', 'Produção'), ('4', 'Agricultura'),
                              ('5', 'Pesca'), ('6', 'Pequena Industria e Transf'), ('7', 'Pecuária'),
                              ('8', 'Agropecuária'), ('9', 'Consumo'), ('10', 'Melhoria habitacional'),
                              ('11', 'Outros')], default='1', required=True)#
    especifica_outro_setor = fields.Char(string='Especifica Outros')
    area = fields.Selection([('1', 'Urbano'), ('2', 'Sub Urbano'), ('3', 'Rural'), ('0', ' ')], default="1", required=True)#
    estrotura_fisica = fields.Selection(
        [('1', 'Móvel'), ('2', 'Na Feria'), ('3', 'Ponto Comercial'), ('4', 'Casa'), ('5', 'Ponto Fixo')], default='1',
         required=True)#
    tipo_controle = fields.Selection(
        [('1', 'Estoque'), ('2', 'Livro Caixa'), ('3', 'Faz de Cabeça'), ('4', 'Nenhum')],
        default='1', required=True)#
    cond_imovel = fields.Selection([('1', 'Própio'), ('2', 'Alugado'), ('3', 'Outros')], default='1', required=True)#
    num_pessoa_negoc = fields.Char(string="Numero de pessoas no negocio",)  #
    familiar = fields.Char(string="Familiar", required=True)#
    nao_familiar = fields.Char(string="Nao Familia", required=True)#
    num_pess_dep_negoc = fields.Char(string="Numero de pessoas dependem do negocio", required=True)#
    renda_familiar = fields.Char(string="Renda Familiar", required=True)#
    participou_capacitacao = fields.Selection([('True', 'Sim'), ('False', 'Não')], default="True")
    qual = fields.Char(string="Qual?")
    plano_aplicacao_ids = fields.One2many('plano.aplicacao', 'solicitacao_credito_id', required=True)#
    valor_total = fields.Float(string="Valor Total Itens", compute='compute_val_tot', store=True)
    declarar_bens = fields.Boolean(string="Declaracao de Bens")
    declaracoes_bens_ids = fields.One2many('declaracoes.bens', 'solicitacao_credito_id')
    declarar_fianca = fields.Boolean(string="Declaracao de Financas")
    declaracoes_fiancas_ids = fields.One2many('declaracoes.fiancas', 'solicitacao_credito_id')
    grupos_ids = fields.One2many('grupo', 'solicitacao_credito_id')
    tempo_moradia_na_comunidade = fields.Selection([('1', 'Acima de 2 Anos'), (
        '2', 'Acima de 1 ano e menos de 2 anos'), ('3', 'Abaixo de 1 ano')], default="2", required=True)#
    conhece_actividade = fields.Selection([('1', 'Conhece muito bem sua actividade'),
                                           ('2', 'Conhece regularmente sua actividade'),
                                           ('3', 'Conhece pouco sua actividade')],
                                          default="2", required=True)#
    tempo_negocio = fields.Selection([('1', 'Acima de 2 Anos'),
                                      ('2', 'Acima de 1 ano e menos de 2 anos'),
                                      ('3', 'Abaixo de 1 ano')],
                                     default="2", required=True)#
    organizacao_negocio = fields.Selection(
        [('1', 'Muito organizado'), ('2', 'Organizado regular'),
         ('3', 'Pouco organizado')], default="2", required=True)#
    local_negocio_fixos = fields.Selection(
        [('1', 'O negócio é fixo, o ponto é próprio, fora de casa'), ('2', 'Fixo e na casa'),
         ('3', 'Ambulante')], default="2", required=True)#
    tranparencia_na_informacao = fields.Selection(
        [('1', 'Total transparência em conceder informações'),
         ('2', 'Mediana Transparência'),
         ('3', 'Dificuldade para obter informações')], default="2", required=True)#
    tamanho_negocio = fields.Selection(
        [('1', 'Acumulação ampliada'), ('2', 'Acumulação Simples'),
         ('3', 'Subsistência')], default="2", required=True)#
    ref_vizin_sobr_client = fields.Selection([('1', 'Boas'), ('2', 'Regulares'), ('3', 'Más')],
                                             default="2", required=True)#
    consult_catastral = fields.Selection([('1', 'Excelente histórico de pagamento'),
                                          ('2', 'Regular histórico (atraso, mas pagou)'),
                                          ('3', 'Sem histórico (primaria solicitação)'),
                                          ('4', 'Histórico negativo de pagamento')],
                                         default="2", required=True)#
    situacao_na_esfera_familiar = fields.Selection(
        [('1', 'Não apresenta problemas em família'),
         ('2', 'Algum problema em familia'),
         ('3', 'Com muitos problemas em familia')], default="2", required=True)#
    imprissao_do_agente_sob_cliente = fields.Selection(
        [('1', 'Excelente impressão'), ('2', 'Boa impressão'),
         ('3', 'Regular impressão'), ('4', 'Péssima impressão')],
        default="2", required=True)#

    utilizador_id = fields.Many2one('res.users', string="Utilizador", default=lambda self: self.env.user)
    nome_util = fields.Char(tring="Utilizador", related='utilizador_id.name')
    agente = fields.Many2one('res.users', string="Agente", compute='valid_utilizador')
    nome_agente = fields.Char(tring="Agente", compute='valid_utilizador')
    util_agent = fields.Boolean(string="Utilizador Agente", compute='valid_utilizador')
    info_adicion = fields.Text(string="Informacoes Adicionais")
    submeter = fields.Boolean(string="Submeter")
    desting_doc_quo = fields.Boolean(string="Documento/Quotas", default=True)
    nmuero_prefix = fields.Char(string="Quota", reequired=True, copy=False, readonly=True, index=True,
                                default=lambda self: _('New'))
    plano_desemboso_id = fields.Many2one('plano.desembolso')  # chavi de microcredito
    acta_ou_solici = fields.Boolean(string="Solicitação ou Acta", default=True)
    aceitado = fields.Boolean(string=" Aceitado")  # Quando a solicitação foi aprovado tornase tru
    periodicidade = fields.Selection(
        [('1', 'Semanal'), ('2', 'Quinzenal'), ('3', 'Mensal'), ('4', 'Trimestral'), ('5', 'Anual'),
         ('6', 'Semestral'), ('outros;', 'Outros')], default="3", required=True)#
    juros = fields.Float(string="Juros", default=10.00, store=True, readonly=True)
    numer_prest = fields.Integer(string="Nº")
    metudo_calculo = fields.Selection([('degresivo', 'Degresivo'), ('constante', 'Constante'), ('simplis', 'Simples')],
                                      default="simplis")
    aprovado = fields.Selection([('True', 'Sim'), ('False', 'Não')], default='False', string=" Aprovado")
    estado = fields.Selection([('0', 'Pendente'), ('1', 'Submetido'), ('2', 'Rejeitado'), ('4', 'Em andamento'), ('9', 'Anulado'), ('3', 'Aprovado'), ('6', 'Fechado')], index=True,
                               track_visibility='onchange', default='0',
                              readonly=True, copy=False)#
    pont_qualif = fields.Float(string="Ponto de Qualificação", compute="calculat", store=True)
    nqualificacao = fields.Integer('Num Qualificação', compute="calculat", store=True)

    tipo = fields.Selection([('1', 'Proponho'), ('2', 'Não Proponho')], default="2", string="Aprovado gestor")
    valor_gestor = fields.Float(string="Valor Agente")
    valor_prestacao = fields.Float(string="Valor Prestacao Agente")
    prazo = fields.Integer(string="Prazo")
    periodicidade_agent = fields.Selection(
        [('1', 'Semanal'), ('2', 'Quinzenal'), ('3', 'Mensal'), ('4', 'Trimestral'),
         ('5', 'Anual'), ('6', 'Outros')], default="3")
    parecer = fields.Text(string="Parecer")

    receitas_operacionais = fields.Float(string="Receitas Operacionais")
    custo_operacional = fields.Float(string="Custo Operacional")
    capacidade_pagamento = fields.Float(string="Lucro Operacional")
    # Sobre Relatorio
    tem_fluxo = fields.Boolean(string="Tem Fluxo de Caixa")
    titulo_report = fields.Char(string="Titulo Relatorio")
    fluxo_caixa_ids = fields.One2many('fluxo.caixa', 'solicitacao_id', string="Fluxo de caixa", store=True, copy=True,
                                      index=True)  # capt report
    balanco_ids = fields.One2many('balanco', 'solicitacao_id', string="Balanço", store=True, copy=True,
                                  index=True)  # capt report
    tp_prop = fields.Char(string="Tipo Proponho", compute='add_val_x', store=True)
    tp_no_prop = fields.Char(string="Tipo no Proponho", compute='add_val_x', store=True)
    per_simana = fields.Char(string="Periodicidade simanal", compute='add_val_x', store=True)
    per_quinzenal = fields.Char(string="Periodicidade quinzenal", compute='add_val_x', store=True)
    per_mensal = fields.Char(string="Periodicidade mensal", compute='add_val_x', store=True)
    tem_balanco = fields.Boolean(string="Balanco Feito")
    ata = fields.Integer(string="ID Ata")
    inic = fields.Char(string="INICio Ativ")

    dados_antigo = fields.Boolean(string="Dados Antigo") #se True porque os dados são antigo

    @api.one
    @api.constrains('dados_antigo')
    def val_dados_antig(self):  # Verificar se o dados e antigo ou não
        if self.dados_antigo == True:
            pass
        # raise ValidationError(
        #    'Dados antigo, ha algumas informações que precisam ser modificado, contacta o adminstrador de sistema se consideras-te que é um erro ')

    #primeiraves = fields.Selection([('1', 'Primeira vez'), ('2', 'Segunda vez')], compute='primeira_vez', store=True)

    @api.multi
    @api.constrains('valor_solicitado')
    def _check_size(self):
       num_pess_nego = str(self.num_pessoa_negoc)
       famil = str(self.familiar)
       not_famil = str(self.nao_familiar)
       n_pess_dep_ner = str(self.num_pess_dep_negoc)
       rend_famil = str(self.renda_familiar)


       #if (num_pess_nego.isnumeric()) == False:
       #     raise ValidationError('O campo Nº Pess.Trab.Negoc tem que ser numerico!')
       if (famil.isnumeric()) == False:
           raise ValidationError('O campo Familiar tem que ser numerico!')
       if (not_famil.isnumeric()) == False:
           raise ValidationError('O campo não Familiar tem que ser numerico!')
       if (n_pess_dep_ner.isnumeric()) == False:
           raise ValidationError('O campo Nº Pess.Dep.Negoc tem que ser numerico!')
       if (rend_famil.isnumeric()) == False:
            raise ValidationError('O campo Renda Familiar tem que ser numerico!')

    @api.model
    def create(self, vals):
        vals['codigo'] = self.env['ir.sequence'].next_by_code('solicitacaoCredito.codigo') or _('New')
        vals['nmuero_prefix'] = self.env['ir.sequence'].next_by_code('quota.quota') or _('New')
        res = super(solicitacaoCredito, self).create(vals)
        res.val_pess()
        res.gerar()

        return res

    @api.model
    def _get_next_cod(self):
        sequence = self.env['ir.sequence'].search([('code', '=', 'solicitacaoCredito.codigo')])
        next = sequence.get_next_char(sequence.number_next_actual)
        return next

    @api.model
    def val_pess(self):
        pessoa = self.env['pessoas'].search([('id', '=', self.identificacao_proponente.id)])
        pessoa.write({'tem_pedido': '1'})

    @api.multi
    def write(self, vals):
        self.atual_flux()
        self.assoc_flux_caixa()

        """self.atual_flux()
        valor = {}
        if 'prestacao' in vals: valor['prestacao'] = vals['prestacao']
        if 'juros_quadro' in vals: valor['juro_jerado'] = vals['juros_quadro']
        if 'prestacao' in vals: valor['total'] = vals['prestacao']
        if 'prestacao' in vals: valor['valorAsc'] = vals['prestacao']
        if 'identificacao_proponente' in vals: valor['nome_terc'] = vals['identificacao_proponente']
        if 'amotizacao' in vals: valor['amortizacao'] = vals['amotizacao']
        if 'divida' in vals: valor['divida'] = vals['divida']
        if 'data_documento' in vals: valor['data'] = vals['data_documento']

        campo_prest = self.env['reg.docum'].search([('numeros_docum', '=', self.codigo)])
        campo_prest.write(valor)"""
        obg = super(solicitacaoCredito, self).write(vals)

        return obg

    def _comput_line(self, line):
        return {'displlay_type': line.displlay_type, 'state': 'draft', }

    @api.multi
    @api.onchange('nome_grupo')
    def _onchange_reg_docum_receb_ids(self):
        menb = self.env['membro'].search([('grupo_id', '=', self.nome_grupo.id)])
        list_of_menb = []
        for line in menb:
            data = self._comput_line(line)
            data.update({'nome': line.nome, 'codigo': line.codigo, })
            list_of_menb.append((1, line.id, data))
        return {'value': {"lista_group": list_of_menb}}

    @api.multi
    def s(self):
        self.env["plano.financiamento"].search([('nome_terc', '=', self.identificacao_proponente.id)]).unlink()
        ac = self.env['ir.model.data'].xmlid_to_res_id('gestao_microfinancas.plano_desembolso_form',
                                                       raise_if_not_found=True)
        # sql = "DELETE FROM reg_docum WHERE submeter = False AND desting_solict = True AND aprovado = 'nao'"
        # self.env.cr.execute(sql)
        valor_solicitado = False
        numero_prestacoes = False
        periodicidade = False
        identificacao_proponente = False
        codigo = False
        juros = False
        acta_ou_solici = False
        aprovado = False
        for o in self:
            valor_solicitado = o.valor_solicitado
            numero_prestacoes = o.numero_prestacoes
            identificacao_proponente = o.identificacao_proponente
            codigo = o.codigo
            acta_ou_solici = o.acta_ou_solici
            periodicidade = o.periodicidade
            juros = o.juros
            aprovado = o.aprovado
        result = {
            'name': 'Plano de Desembolso',
            'view_type': 'form',
            'res_model': 'plano.desembolso',
            'view_id': ac,
            'context': {'default_valor': valor_solicitado, 'default_numero_prestacao': numero_prestacoes,
                        'default_identificacao_proponente': identificacao_proponente.id,
                        'default_codigo': codigo, 'default_aprovadp': aprovado, 'default_juros': juros,
                        'default_solici': acta_ou_solici, 'default_periodicidade': periodicidade},
            'type': 'ir.actions.act_window',
            'target': 'new',
            'view_mode': 'form'
        }
        self.gerar()
        return result

    @api.one
    @api.depends('plano_aplicacao_ids.total')
    def compute_val_tot(self):
        self.valor_total = sum(line.total for line in self.plano_aplicacao_ids)

    @api.onchange('valor_total')
    def tchek_val_tot(self):
        if self.valor_total > self.valor_solicitado:
            warning = {
                'title': _('Atenção!'),
                'message': _('A somma dos valores tem que ser igual ao montante solicitado no pedido de credito.'),
            }

            return {'warning': warning}

    @api.one
    @api.depends('numero_prestacoes', 'juros_quadro', 'valor_solicitado', )
    def gerar(self):

        self.ensure_one()
        juros = 10.0
        cont_prest = self.numero_prestacoes
        cont = 0
        j = juros / 100.0
        self.juros_quadro = self.valor_solicitado * j
        self.amotizacao = round(self.valor_solicitado / self.numero_prestacoes)
        self.prestacao = round(self.amotizacao + self.juros_quadro)
        self.divida = round(self.valor_solicitado - self.amotizacao)

        while cont_prest > 0:
            if cont == 0:
                plano_obj_lina0 = self.env['plano.financiamento']
                plano_desemb = plano_obj_lina0.create({'numer_prest': 0, 'divida': self.valor_solicitado,
                                                       'nome_terc': self.identificacao_proponente.id,
                                                       'desting_solict': self.desting_doc_quo,
                                                       'data_documento': self.data, })

            # data_prest = date_after_month
            if cont == 1:
                data_prest = self.date_start
                plano_obj = self.env['plano.financiamento']
                plano_desemb = plano_obj.create({'prestacao': self.prestacao,
                                                 'juro_jerado': self.juros_quadro, 'total': self.prestacao,
                                                 'numer_prest': self.numer_prest,
                                                 'nome_terc': self.identificacao_proponente.id,

                                                 'desting_solict': self.desting_doc_quo,
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
                plano_desemb = plano_obj.create({'prestacao': self.prestacao,
                                                 'juro_jerado': self.juros_quadro, 'total': self.prestacao,
                                                 'numer_prest': self.numer_prest,
                                                 'nome_terc': self.identificacao_proponente.id,
                                                 'desting_solict': self.desting_doc_quo,
                                                 'amortizacao': self.amotizacao, 'divida': self.divida,
                                                 'data_documento': data_prest, })

            self.numer_prest = cont + 1
            if self.numer_prest == self.numero_prestacoes:
                pass  # cont_prest += 1
            else:
                cont_prest -= 1
            cont += 1
        return True

    def assoc_flux_caixa(self):#e balanco
        fluxo_caixa_men = self.env['fluxo.caixa'].search([('ropornente_id', '=', self.identificacao_proponente.id)])
        if fluxo_caixa_men:
            for flux in fluxo_caixa_men:
                flux.solicitacao_id = self.id

        balanc = self.env['balanco'].search([('ropornente_id', '=', self.identificacao_proponente.id)])
        if balanc:
            for bl in balanc:
                bl.solicitacao_id = self.id

    # Apaga o fluxo de caixa que foi
    @api.multi
    def atual_flux(self):
        if self.aprovado == 'False':
            flux_caixa = self.env['fluxo.caixa'].search(
                [('ropornente_id', '=', self.identificacao_proponente.id), ('atl_flux', '=', True)])
            if flux_caixa:
                flux_caixa = self.env['fluxo.caixa'].search(
                    [('ropornente_id', '=', self.identificacao_proponente.id), ('atl_flux', '=', False)]).unlink()

            balanc = self.env['balanco'].search(
                [('ropornente_id', '=', self.identificacao_proponente.id), ('atl_bal', '=', True)])
            if balanc:
                bal = self.env['balanco'].search(
                    [('ropornente_id', '=', self.identificacao_proponente.id), ('atl_bal', '=', False)]).unlink()

    # ---------Abre o formulario fluxo de caixa-------------------------------
    @api.multi
    def fluxo_caixa_mensal(self):
        # id = False
        nqualificacao = False
        identificacao_proponente = False

        receitas_operacionais = False
        custo_operacional = False
        outras_receitas_nao_op = False
        custo_mercadoria = False
        outras_despesas_nao_op = False
        pagamento_pessoal = False
        paga_trasnp_fret_carg = False
        outra_presta_lojas_cas_saud = False
        taxas_aluguer_imposto = False
        desponibilidade_liquida = False
        lucro_operacional = False
        capacidade_pagamento = False
        ropornente_id = False
        id = False
        fluxo = self.env['fluxo.caixa'].search([('aprovado', '=', self.aprovado), ('ropornente_id', '=', self.identificacao_proponente.id), ('solicitacao_id', '=', self.id)])#, ('aprovado', '=', self.aprovado)
        ac = self.env['ir.model.data'].xmlid_to_res_id('gestao_microfinancas.fluxo_caixa_form', raise_if_not_found=True)
        if fluxo:
            for dad in fluxo:
                # id = dad.id
                identificacao_proponente = dad.ropornente_id
                receitas_operacionais = dad.receitas_operacionais
                custo_operacional = dad.custo_operacional
                outras_receitas_nao_op = dad.outras_receitas_nao_op
                custo_mercadoria = dad.custo_mercadoria
                outras_despesas_nao_op = dad.outras_despesas_nao_op
                pagamento_pessoal = dad.pagamento_pessoal
                paga_trasnp_fret_carg = dad.paga_trasnp_fret_carg
                outra_presta_lojas_cas_saud = dad.outra_presta_lojas_cas_saud
                agua_luz_telef = dad.agua_luz_telef
                taxas_aluguer_imposto = dad.taxas_aluguer_imposto
                desponibilidade_liquida = dad.desponibilidade_liquida
                outros_custos = dad.outros_custos
                lucro_operacional = dad.lucro_operacional
                capacidade_pagamento = dad.capacidade_pagamento
                nqualificacao = dad.nqualificacao
                ropornente_id = dad.ropornente_id
                #id = dad.solicitacao_id

            result = {
                'name': 'Fluxo de Caxa',
                'view_type': 'form',
                'res_model': 'fluxo.caixa',
                'view_id': ac,
                'context': {  # 'default_solicitacao_id': id,
                    'default_nqualificacao': nqualificacao,
                    'default_ropornente_id': identificacao_proponente.id,
                    'default_receitas_operacionais': receitas_operacionais,
                    'default_custo_operacional': custo_operacional,
                    'default_outras_receitas_nao_op': outras_receitas_nao_op,
                    'default_custo_mercadoria': custo_mercadoria,
                    'default_outras_despesas_nao_op': outras_despesas_nao_op,
                    'default_pagamento_pessoal': pagamento_pessoal,
                    'default_paga_trasnp_fret_carg': paga_trasnp_fret_carg,
                    'default_outra_presta_lojas_cas_saud': outra_presta_lojas_cas_saud,
                    'default_agua_luz_telef': agua_luz_telef,
                    'default_taxas_aluguer_imposto': taxas_aluguer_imposto,
                    'default_desponibilidade_liquida': desponibilidade_liquida,
                    'default_outros_custos': outros_custos,
                    'default_atl_flux': self.desting_doc_quo,
                    'default_capacidade_pagamento': capacidade_pagamento,
                    'default_lucro_operacional': lucro_operacional, },
                    #'default_solicitacao_id': id,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'view_mode': 'form'
            }
            return result

        else:
            for o in self:
                nqualificacao = o.nqualificacao
                identificacao_proponente = o.identificacao_proponente
            result = {
                'name': 'Fluxo de Caxa',
                'view_type': 'form',
                'res_model': 'fluxo.caixa',
                'view_id': ac,
                'context': {'default_nqualificacao': nqualificacao,'default_solicitacao_id': id,
                            'default_ropornente_id': identificacao_proponente.id},

                'type': 'ir.actions.act_window',
                'target': 'new',
                'view_mode': 'form'
            }

            return result

    # ---------Abre o formulario balanco--------------------------------------
    def balanco(self):
        activo_circular = False
        passivo_circular = False
        caixa_banco_poupancas = False
        contas_receb_terceiro = False
        estoques = False
        financiamento_emprestimo = False
        outros = False
        imoveis = False
        fornecidores = False
        imobilizado = False
        maquina_equipamentos = False
        adiantamento_cliente = False
        outros_passivo = False
        moveis_utencilios = False
        passivo_longo_prazo = False
        veiculos = False
        financiamento_longo_prazo = False
        outros_imobil = False
        patrimonio_liquido = False
        acdtivo_familia = False
        activo_total = False
        passivo_total = False
        identificacao_proponente = False
        id = False
        balan = self.env['balanco'].search([('aprovado', '=', self.aprovado), ('ropornente_id', '=', self.identificacao_proponente.id), ('solicitacao_id', '=', self.id)])#, ('ropornente_id', '=', self.identificacao_proponente.id), ('solicitacao_id', '=', self.id)
        ac = self.env['ir.model.data'].xmlid_to_res_id('gestao_microfinancas.balanco_form', raise_if_not_found=True)
        if balan:
            for b in balan:
                activo_circular = b.activo_circular
                passivo_circular = b.passivo_circular
                caixa_banco_poupancas = b.caixa_banco_poupancas
                contas_receb_terceiro = b.contas_receb_terceiro
                estoques = b.estoques
                financiamento_emprestimo = b.financiamento_emprestimo
                outros = b.outros
                imobilizado = b.imobilizado
                imoveis = b.imoveis
                fornecidores = b.fornecidores
                maquina_equipamentos = b.maquina_equipamentos
                adiantamento_cliente = b.adiantamento_cliente
                outros_passivo = b.outros_passivo
                moveis_utencilios = b.moveis_utencilios
                passivo_longo_prazo = b.passivo_longo_prazo
                veiculos = b.veiculos
                financiamento_longo_prazo = b.financiamento_longo_prazo
                outros_imobil = b.outros_imobil
                patrimonio_liquido = b.patrimonio_liquido
                acdtivo_familia = b.acdtivo_familia
                activo_total = b.activo_total
                passivo_total = b.passivo_total
                identificacao_proponente = b.ropornente_id
                id = b.solicitacao_id

            result = {
                'name': ('Balanço'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'balanco',
                'view_id': ac,
                'context': {'default_ropornente_id': identificacao_proponente.id,
                            'default_activo_circular': activo_circular,
                            'default_passivo_circular': passivo_circular,
                            'default_caixa_banco_poupancas': caixa_banco_poupancas,
                            'default_contas_receb_terceiro': contas_receb_terceiro,
                            'default_estoques': estoques,
                            'default_financiamento_emprestimo': financiamento_emprestimo,
                            'default_outros': outros,
                            'default_imobilizado': imobilizado,
                            'default_imoveis': imoveis,
                            'default_fornecidores': fornecidores,
                            'default_maquina_equipamentos': maquina_equipamentos,
                            'default_adiantamento_cliente': adiantamento_cliente,
                            'default_outros_passivo': outros_passivo,
                            'default_moveis_utencilios': moveis_utencilios,
                            'default_passivo_longo_prazo': passivo_longo_prazo,
                            'default_veiculos': veiculos,
                            'default_financiamento_longo_prazo': financiamento_longo_prazo,
                            'default_outros_imobil': outros_imobil,
                            'default_patrimonio_liquido': patrimonio_liquido,
                            'default_acdtivo_familia': acdtivo_familia,
                            'default_atl_bal': self.desting_doc_quo,
                            'default_activo_total': activo_total,
                            'default_passivo_total': passivo_total,
                            'default_solicitacao_id': id,
                            },
                'type': 'ir.actions.act_window',
                'target': 'new'}
            return result
        else:
            for o in self:
                identificacao_proponente = o.identificacao_proponente
            result = {
                'name': ('Balanço'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'balanco',
                'view_id': ac,
                'context': {'default_ropornente_id': identificacao_proponente.id, 'default_solicitacao_id': id},
                'type': 'ir.actions.act_window',
                'target': 'new'}
            return result

    # ---------Abre o formulario compor vemda--------------------------------
    def comportamento_das_vendas(self):
        identificacao_proponente = False
        id = False
        ac = self.env['ir.model.data'].xmlid_to_res_id('gestao_microfinancas.vendas_form', raise_if_not_found=True)
        for o in self:
            id = o.id
            identificacao_proponente = o.identificacao_proponente
        result = {
            'name': ('Vendas'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'vendas',
            'view_id': ac,
            'context': {'default_solicitacao_id': id, 'default_ropornente_id': identificacao_proponente.id},
            'type': 'ir.actions.act_window',
            'target': 'new'}
        return result

    # ---------Calcula a pontuação--------------------------------
    @api.model
    @api.onchange('tempo_moradia_na_comunidade', 'tempo_negocio', 'local_negocio_fixos', 'tamanho_negocio',
                  'consult_catastral', 'ref_vizin_sobr_client',
                  'situacao_na_esfera_familiar', 'imprissao_do_agente_sob_cliente', 'conhece_actividade',
                  'organizacao_negocio', 'tranparencia_na_informacao')
    def calculat(self):
        num_pont = 0
        if self.tempo_moradia_na_comunidade == '1':
            num_pont += 5
            self.pont_qualif = num_pont
        elif self.tempo_moradia_na_comunidade == '2':
            num_pont += 2
            self.pont_qualif = num_pont
        elif self.tempo_moradia_na_comunidade == '3':
            num_pont += 0
            self.pont_qualif = num_pont

        if self.tempo_negocio == '1':
            num_pont += 5
            self.pont_qualif = num_pont
        elif self.tempo_negocio == '2':
            num_pont += 2
            self.pont_qualif = num_pont
        elif self.tempo_negocio == '3':
            num_pont += 0
            self.pont_qualif = num_pont

        if self.local_negocio_fixos == '1':
            num_pont += 5
            self.pont_qualif = num_pont
        elif self.local_negocio_fixos == '2':
            num_pont += 2
            self.pont_qualif = num_pont
        elif self.local_negocio_fixos == '3':
            num_pont += 1
            self.pont_qualif = num_pont

        if self.tamanho_negocio == '1':
            num_pont += 5
            self.pont_qualif = num_pont
        elif self.tamanho_negocio == '2':
            num_pont += 2
            self.pont_qualif = num_pont
        elif self.tamanho_negocio == '3':
            num_pont += 1
            self.pont_qualif = num_pont

        if self.consult_catastral == '1':
            num_pont += 5
            self.pont_qualif = num_pont
        elif self.consult_catastral == '2':
            num_pont += 1
            self.pont_qualif = num_pont
        elif self.consult_catastral == '3':
            num_pont += 0
            self.pont_qualif = num_pont
        elif self.consult_catastral == '4':
            num_pont += -30
            self.ok = num_pont

        if self.ref_vizin_sobr_client == '1':
            num_pont += 5
            self.pont_qualif = num_pont
        elif self.ref_vizin_sobr_client == '2':
            num_pont += 2
            self.pont_qualif = num_pont
        elif self.ref_vizin_sobr_client == '3':
            num_pont += 0
            self.pont_qualif = num_pont

        if self.situacao_na_esfera_familiar == '1':
            num_pont += 5
            self.pont_qualif = num_pont
        elif self.situacao_na_esfera_familiar == '2':
            num_pont += 1
            self.pont_qualif = num_pont
        elif self.situacao_na_esfera_familiar == '3':
            num_pont += 0
            self.pont_qualif = num_pont

        if self.imprissao_do_agente_sob_cliente == '1':
            num_pont += 5
            self.pont_qualif = num_pont
        elif self.imprissao_do_agente_sob_cliente == '2':
            num_pont += 2
            self.pont_qualif = num_pont
        elif self.imprissao_do_agente_sob_cliente == '3':
            num_pont += 1
            self.pont_qualif = num_pont
        elif self.imprissao_do_agente_sob_cliente == '4':
            num_pont += 0
            self.pont_qualif = num_pont

        if self.conhece_actividade == '1':
            num_pont += 5
            self.pont_qualif = num_pont
        elif self.conhece_actividade == '2':
            num_pont += 2
            self.pont_qualif = num_pont
        elif self.conhece_actividade == '3':
            num_pont += 0
            self.pont_qualif = num_pont

        if self.organizacao_negocio == '1':
            num_pont += 5
            self.pont_qualif = num_pont
        elif self.organizacao_negocio == '2':
            num_pont += 2
            self.pont_qualif = num_pont
        elif self.organizacao_negocio == '3':
            num_pont += 1
            self.pont_qualif = num_pont

        if self.tranparencia_na_informacao == '1':
            num_pont += 5
            self.pont_qualif = num_pont
        elif self.tranparencia_na_informacao == '2':
            num_pont += 1
            self.pont_qualif = num_pont
        elif self.tranparencia_na_informacao == '3':
            num_pont += 0
            self.pont_qualif = num_pont
        if self.pont_qualif >= 27:
            self.nqualificacao = 70
        elif self.pont_qualif >= 23 and self.pont_qualif <= 26:
            self.nqualificacao = 60
        elif self.pont_qualif >= 20 and self.pont_qualif <= 22:
            self.nqualificacao = 50
        elif self.pont_qualif >= 16 and self.pont_qualif <= 19:
            self.nqualificacao = 30
        else:
            self.nqualificacao = 0

    # ---------Atribui o valor X para os valores escolhidos--------
    @api.onchange('tipo', 'periodicidade_agent')
    @api.depends('tipo')
    def add_val_x(self):
        if self.tipo == "1":
            self.tp_prop = 'X'
            self.tp_no_prop = " "

        else:
            self.tp_prop = " "
            self.tp_no_prop = 'X'

        if self.periodicidade_agent == '1':
            self.per_simana = 'X'
            self.per_quinzenal = ''
            self.per_mensal = ''

        elif self.periodicidade_agent == '2':
            self.per_simana = ''
            self.per_quinzenal = 'X'
            self.per_mensal = ''

        elif self.periodicidade_agent == '3':
            self.per_simana = ''
            self.per_quinzenal = ''
            self.per_mensal = 'X'


    @api.onchange('utilizador_id')
    def valid_utilizador(self):
        util = self.env['agentes.agentes'].search([('operador', '=', self.utilizador_id.id)])
        if util:
            self.util_agent = True
            # self.nome_agente = util.name
            # self.agente = util.id

    @api.onchange('submeter')
    def on_change_state(self):
        # for record in self:
        if self.submeter == True:
            self.estado = '1'
        else:
            self.estado = '0'


class planAplicacao(models.Model):
    _name = 'plano.aplicacao'
    _rec_name = 'item'
    _description = 'Plano Aplicação'
    data_realiz = fields.Date(string="Data acta", default=fields.Date.today)

    item = fields.Char(string="Item")
    unidade_id = fields.Many2one('unimedida.unimedida', string="Unidade Medida")
    name_unid = fields.Char(string="Nome Unidade", related='unidade_id.name')
    preco_unit = fields.Float(string="Preço Unitário")
    quantidade = fields.Float(string="Quantidade")
    total = fields.Float(string="Total", compute='calc_preco_tot')
    verif = fields.Float(string="Verif")
    solicitacao_credito_id = fields.Many2one('solicitacao.credito')

    @api.one
    @api.depends('preco_unit', 'quantidade')
    def calc_preco_tot(self):
        for line in self:
            line.total = line.preco_unit * line.quantidade


class declaracoesBens(models.Model):
    _name = 'declaracoes.bens'
    _rec_name = 'item'
    _description = 'Declarações de Bens'
    data_realiz = fields.Date(string="Data acta", default=fields.Date.today)

    item = fields.Char(string="Item")
    valor = fields.Float(string="Valor")
    solicitacao_credito_id = fields.Many2one('solicitacao.credito')


class declaracoesFiancas(models.Model):
    _name = 'declaracoes.fiancas'
    # _rec_name = 'name'
    _description = 'Declarações de Fiança'
    data_realiz = fields.Date(string="Data acta", default=fields.Date.today)

    fiador_id = fields.Many2one('fiador', string="Código Fiador")
    solicitacao_credito_id = fields.Many2one('solicitacao.credito', string="Código Pedido")
    nome = fields.Many2one('pessoas', string="Nome", related="fiador_id.pessoa_id")

    numero = fields.Char(string="Numero", related="fiador_id.numero")
    codigo = fields.Char(string="Codigo", related="fiador_id.codigo")
    pessoa_id = fields.Many2one('pessoas', string="Código", related="fiador_id.pessoa_id")
    name = fields.Char(string="Nome", related='fiador_id.name')
    lugar_trabalho = fields.Char(string="Lugar Trabalho", related='fiador_id.lugar_trabalho')
    telefone = fields.Char(string="Telefone", size=7, related='fiador_id.telefone')
    vencimento = fields.Float(string="Vencimento", related='fiador_id.vencimento')
    residencia = fields.Char(string="Residência",  related='fiador_id.residencia')


class fluxoCaixa(models.Model):
    _name = 'fluxo.caixa'
    # _rec_name = 'name'
    _description = 'Fluxo de Caixa'
    data_realiz = fields.Date(string="Data", default=fields.Date.today)

    receitas_operacionais = fields.Float(string="Receitas Operacionais")
    custo_operacional = fields.Float(string="Custo Operacional", compute='calc_flux')
    outras_receitas_nao_op = fields.Float(string="Outras Receitas")
    custo_mercadoria = fields.Float(string="Custo Mercadoria")
    outras_despesas_nao_op = fields.Float(string="Outras despesas")
    pagamento_pessoal = fields.Float(string="Pagamento pessoal")
    paga_trasnp_fret_carg = fields.Float(string="Pagar transporte fret")
    outra_presta_lojas_cas_saud = fields.Float(string="outras prestacao")
    agua_luz_telef = fields.Float(string="Água, luz e telefone")
    taxas_aluguer_imposto = fields.Float(string="Taxa alug impost")
    desponibilidade_liquida = fields.Float(string="Disponibilidade Liquida", compute='calc_flux')
    outros_custos = fields.Float(string="Outros Custos")
    lucro_operacional = fields.Float(string="Lucro Operacional", compute='calc_flux')
    capacidade_pagamento = fields.Float(string="Capacidade Operacional", )
    nqualificacao = fields.Integer(string="Qualificação")
    ropornente_id = fields.Many2one('pessoas', string="Pessoas", )
    atl_flux = fields.Boolean(string="Actualiza Fluxo")
    solicitacao_id = fields.Many2one('solicitacao.credito', string="Solicitação")
    fluxo_caixa_feito = fields.Boolean(string="Fluxo feito", default=True)
    aprovado = fields.Selection([('True', 'Sim'), ('False', 'Não')], store=True, default = 'False')

    sid_pedido1 = fields.Integer(string='Id Pedido1')
    data_balam = fields.Char(string="Data Balancete")

    @api.multi
    def complet_solic(self):
        solic = self.env['solicitacao.credito'].search([('identificacao_proponente', '=', self.ropornente_id.id)])
        if solic:
            for rec in solic:
                rec.receitas_operacionais = self.receitas_operacionais
                rec.custo_operacional = self.custo_operacional
                rec.capacidade_pagamento = self.capacidade_pagamento
                rec.tem_fluxo = True

    @api.model
    def create(self, vals):

        res = super(fluxoCaixa, self).create(vals)
        res.complet_solic()
        return res

    @api.one
    @api.depends('desponibilidade_liquida', 'nqualificacao', 'receitas_operacionais', 'outras_receitas_nao_op',
                 'custo_mercadoria', 'outras_despesas_nao_op', 'pagamento_pessoal', 'paga_trasnp_fret_carg',
                 'outra_presta_lojas_cas_saud', 'agua_luz_telef', 'taxas_aluguer_imposto', 'outros_custos')
    def calc_flux(self):
        self.custo_operacional = round(
            self.custo_mercadoria + self.pagamento_pessoal + self.paga_trasnp_fret_carg + self.agua_luz_telef + self.taxas_aluguer_imposto + self.outros_custos)
        self.lucro_operacional = round(self.receitas_operacionais - self.custo_operacional)
        self.desponibilidade_liquida = round(
            self.lucro_operacional + self.outras_receitas_nao_op - self.outras_despesas_nao_op - self.outra_presta_lojas_cas_saud)
        self.capacidade_pagamento = round(self.desponibilidade_liquida * (self.nqualificacao / 100))


class balanco(models.Model):
    _name = 'balanco'
    # _rec_name = 'name'
    _description = 'Balanço'
    data_realiz = fields.Date(string="Data Balanco", default=fields.Date.today)

    activo_circular = fields.Float(string="Activo Curicular", compute='calc_balanc')
    passivo_circular = fields.Float(string="Passivo Curicular", compute='calc_balanc')
    caixa_banco_poupancas = fields.Float(string="Caixas bancos poupancas")
    contas_receb_terceiro = fields.Float(string="Contas a receber de Terceiro")
    estoques = fields.Float(string="Estaoques")
    financiamento_emprestimo = fields.Float(string="Financiamento de empréstimo")
    outros = fields.Float(string="Outros")
    imobilizado = fields.Float(string="Imobilizado", compute='calc_balanc')
    imoveis = fields.Float(string="Imoveis")
    fornecidores = fields.Float(string="Fornecidores")
    maquina_equipamentos = fields.Float(string="Maquinas e equipamentos")
    adiantamento_cliente = fields.Float(string="Adiantamento de Clientes")
    outros_passivo = fields.Float(string="Outros Passiv")
    moveis_utencilios = fields.Float(string="Móveis e utensílios")
    passivo_longo_prazo = fields.Float(string="PASSIVO DE LONGO PRAZO", compute='calc_balanc')
    veiculos = fields.Float(string="Veículos")
    financiamento_longo_prazo = fields.Float(string="Financiamento de longo prazo")
    outros_imobil = fields.Float(string="Outros Imov")
    patrimonio_liquido = fields.Float(string="PATRIMONIO LIQUIDO")
    acdtivo_familia = fields.Float(string="Activo da familia (terreno...)")
    activo_total = fields.Float(string="ATIVO TOTAL", compute='calc_balanc')
    passivo_total = fields.Float(string="PASSIVO TOTAL", compute='calc_balanc')
    ropornente_id = fields.Many2one('pessoas', string="Pessoas", )
    atl_bal = fields.Boolean(string="Actualiza Fluxo")
    solicitacao_id = fields.Many2one('solicitacao.credito', string="Solicitação")
    balanco_feito = fields.Boolean(string="Balanco Feito")
    aprovado = fields.Selection([('True', 'Sim'), ('False', 'Não')], store=True, default = 'False')

    id_pedido = fields.Char(string='Id Pedido')
    sid_pedido1 = fields.Integer(string='Id Pedido1')
    data_balam = fields.Char(string="Data Balancete")

    @api.multi
    def complet_solic(self):
        solic = self.env['solicitacao.credito'].search([('identificacao_proponente', '=', self.ropornente_id.id)])
        if solic:
            for rec in solic:
                rec.tem_balanco = True

    @api.model
    def create(self, vals):

        res = super(balanco, self).create(vals)
        res.complet_solic()
        return res

    @api.one
    @api.depends('caixa_banco_poupancas', 'contas_receb_terceiro', 'estoques', 'outros', 'imoveis',
                 'maquina_equipamentos',
                 'moveis_utencilios', 'veiculos', 'outros_imobil', 'acdtivo_familia', 'activo_circular', 'imobilizado',
                 'passivo_circular', 'financiamento_emprestimo', 'fornecidores', 'passivo_longo_prazo',
                 'outros_passivo', 'financiamento_longo_prazo', 'patrimonio_liquido')
    def calc_balanc(self):
        self.activo_circular = round(
            self.caixa_banco_poupancas + self.contas_receb_terceiro + self.estoques + self.outros)
        self.imobilizado = round(
            self.imoveis + self.maquina_equipamentos + self.moveis_utencilios + self.veiculos + self.outros_imobil)
        self.activo_total = round(self.activo_circular + self.imobilizado)
        self.passivo_circular = round(
            self.financiamento_emprestimo + self.fornecidores + self.adiantamento_cliente + self.outros_passivo)
        self.passivo_longo_prazo = round(self.financiamento_longo_prazo)
        self.patrimonio_liquido = round(self.activo_total)
        self.passivo_total = round(self.passivo_circular + self.passivo_longo_prazo + self.patrimonio_liquido)


class vendas(models.Model):  # Comportamento das vendas
    _name = 'vendas'
    # _rec_name = 'name'
    _description = 'Comportamento das Vendas'
    data_realiz = fields.Date(string="Data acta", default=fields.Date.today)

    # Boas
    jan_b = fields.Boolean()
    control_b = fields.Boolean(default="True")  # campo utilizado para controlo
    fev_b = fields.Boolean()
    mar_b = fields.Boolean()
    abr_b = fields.Boolean()
    mai_b = fields.Boolean()
    jun_b = fields.Boolean()
    jul_b = fields.Boolean()
    ago_b = fields.Boolean()
    set_b = fields.Boolean()
    out_b = fields.Boolean()
    nov_b = fields.Boolean()
    dez_b = fields.Boolean()

    # Regulares
    jan_r = fields.Boolean()
    fev_r = fields.Boolean()
    mar_r = fields.Boolean()
    abr_r = fields.Boolean()
    mai_r = fields.Boolean()
    jun_r = fields.Boolean()
    jul_r = fields.Boolean()
    ago_r = fields.Boolean()
    set_r = fields.Boolean()
    out_r = fields.Boolean()
    nov_r = fields.Boolean()
    dez_r = fields.Boolean()

    # pessimas
    jan_p = fields.Boolean()
    fev_p = fields.Boolean()
    mar_p = fields.Boolean()
    abr_p = fields.Boolean()
    mai_p = fields.Boolean()
    jun_p = fields.Boolean()
    jul_p = fields.Boolean()
    ago_p = fields.Boolean()
    set_p = fields.Boolean()
    out_p = fields.Boolean()
    nov_p = fields.Boolean()
    dez_p = fields.Boolean()
    ropornente_id = fields.Many2one('pessoas', string="Pessoas", )
    solicitacao_id = fields.Many2one('solicitacao.credito', string="Solicitação")



