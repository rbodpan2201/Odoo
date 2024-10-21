from odoo import models, fields

class Presupuesto(models.Model):
    _name="presupuesto"
    _inherit="image.mixin"
    name=fields.Char(string='Nombre', require=True)
    description = fields.Text(string='Descripción')
    price = fields.Float(string='Precio', digit=(10,2))
    status = fields.Selection([
        ('draft' , 'Borrador'),
        ('confirmed' , 'Confirmado'),
        ('done' , 'Hecho')
    ],string='Estado',default='draft')
    is_active = fields.Boolean(string='Activo', default=True)
    start_date= fields.Date(string='Fecha de Inicio')
    persona_ventas = fields.Many2one(comodel_name="res.partner")
    genero_ids=fields.Many2many(comodel_name="clasificacion")