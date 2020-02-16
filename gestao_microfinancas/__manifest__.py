# -*- coding: utf-8 -*-
{
    'name': "Gestão Microcrédito",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Cabosys",
    'website': "http://www.cabosys.cv",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Gestão microfinancas',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'parametros'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/pessoas.xml',
        'views/fiadores.xml',
        'views/grupos.xml',
        'views/solicitacao_credito.xml',
        'views/acta_comite_credito.xml',
        'views/renegociacao_credito.xml',
        'views/clientes.xml',
        'views/credito_aprovado.xml',
        'views/plano_desembolso.xml',
        'views/reports_plano_aplicacao.xml',
        'views/reports_fluxo_caixa_balanco.xml',
        'views/report_ficha_avalista.xml',
        'views/reports_contrato_emprestimo.xml',
        'views/report_plano_reembolso.xml',
        'views/reports_confissao_divida.xml',
        'security/grupo_microfinancas_security.xml',
        'views/report_solicitacao_credito.xml',
        'views/reports_ata_ficha_aprov.xml',

        'security/ir.model.access.csv',
        # 'static/css/report_plano_aplicacao.css',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
