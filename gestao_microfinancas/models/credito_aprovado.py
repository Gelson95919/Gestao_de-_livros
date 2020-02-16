# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class creditoAprovado(models.Model):
    _name = 'credito.aprovado'
    _description = 'Credito Aprovado'
    _rec_name = 'identificacao_proponente'
    codigo = fields.Char(string="Codigo", equired=True, copy=False, readonly=True, index=True,
                         default=lambda self: _('New'))
    id_credito = fields.Many2one('acta.comite', string="ID Credito")
    id_cliente = fields.Many2one('clientes', string="ID Cliente")
    valor = fields.Float(string="Valor")
    numero_prestacao = fields.Integer(string="Numero prestacao")
    juros = fields.Float(string="Juros")#related="id_credito.juros"
    por = fields.Selection([('1', 'ao Ano'), ('2', 'ao mês')], default="1")
    periodicidade = fields.Selection([('1', 'Semanal'), ('2', 'Quinzenal'), ('3', 'Mensal'), ('4', 'Trimestral'), ('5', 'Anual'), ('6', 'Outros')], default="1")
    periodquant = fields.Integer(string=" ")
    data = fields.Date(string="Data",)# default=fields.Date.today
    data_primeira = fields.Date(string="Data Primeira")# default=fields.Date.today,
    periodo_carencia = fields.Integer(string="Período Carência")
    calcular_juro_periodo_carenc = fields.Boolean(string="Calcular juros no periodo de Carência")
    metudo_calculo = fields.Selection([('1', 'Degresivo'), ('2', 'Constante'), ('3', 'Simples')], default="3")
    identificacao_proponente = fields.Many2one('pessoas', string="Pessoas")#, required=True
    nif = fields.Integer(string="Nif", related="identificacao_proponente.nif") #para remover

    nif_pessoa = fields.Char(string="NIF Pessoa",  size=9, related="identificacao_proponente.nif_pessoa")#required=True,
    reg_docum_ids_desenb = fields.One2many('reg.docum', 'id_cred_aprov', string="Prestação", store=True,
                                           copy=True)
    aprovado = fields.Selection([('True', 'Sim'), ('False', 'Não')])
    estado = fields.Selection([('1', 'Aberto'), ('2', 'Fechado')], default="1")
    vedre = fields.Selection([('1', 'Recebido Completo')], default="1")
    azul = fields.Selection([('1', 'Em Andamento')], default="1")
    vermelho = fields.Selection([('1', ' Não Recebido')], default="1")

    valor_em_div = fields.Float(string="Valor em Divida", store =True)
    prestacao = fields.Float(string="Prestação", store =True)
    juros_quadro = fields.Float(string="Juros calculado", store=True)
    anulado = fields.Boolean(string="Anulado")
    ata_id = fields.Integer(string="ID Ata")
    vd = fields.Selection([('1', ' Valor em divida')], default="1")#label de valor em divida
    renegociado = fields.Boolean(string="Renegociado")
    utilizador_id = fields.Many2one('res.users', string="Utilizador", default=lambda self: self.env.user)

    DOCUMOP = fields.Char()
    IDCREDITO = fields.Char()
    DOCUMOP_moved0 = fields.Char()
    cod_op = fields.Integer()

    dados_antigo = fields.Boolean(string="Dados Antigo")  # se True porque os dados são antigo

    @api.one
    @api.constrains('dados_antigo')
    def val_dados_antig(self):  # Verificar se o dados e antigo ou não
        if self.dados_antigo == True:
            pass
        # raise ValidationError(
        #    'Dados antigo, ha algumas informações que precisam ser modificado, contacta o adminstrador de sistema se consideras-te que é um erro ')

    #def mod_codop(self):
   #    terc = self.env['credito.aprovado'].search([('vd', '=', '1')])
   #    for c in terc:
   #        c.cod_op = c.DOCUMOP

    def mod_cred(self):
        ata = self.env['acta.comite'].search([('control_op', '=', True)])
        for c in ata:
            cred_apro = self.env['credito.aprovado'].search([('IDCREDITO', '=', c.id_credito)])
            for d in cred_apro:
                d.data = c.date_start
                d.data_primeira = c.data_desembolso
                d.periodicidade = c.periodicidade
                d.juros = c.juros



    @api.model
    def create(self, vals):
        vals['codigo'] = self.env['ir.sequence'].next_by_code('desel.codigo') or _('New')
        res = super(creditoAprovado, self).create(vals)

        return res
    def _comput_line(self, line):
         return {'displlay_type': line.displlay_type, 'state': 'draft', }







