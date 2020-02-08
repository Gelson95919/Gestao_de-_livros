from odoo import models, fields, exceptions, _

class LibraryBook(models.Model):
    _name = 'library.book'
    _rec_name = 'name'
    _description = 'Gestão de Lifros'

    name = fields.Char(string="Nome")
    descricao = fields.Text(string="Descrição")

