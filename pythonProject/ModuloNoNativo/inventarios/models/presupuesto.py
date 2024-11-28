import logging
from odoo import models, fields, api

_logger = logging.getLogger("Raul Bodas")

class Presupuesto(models.Model):
    _name="presupuesto"
    _inherit="image.mixin"
    name=fields.Char(string='Nombre', require=True)
    description = fields.Text(string='Descripción')
    unidades_producto = fields.Integer(string='Unidades del Producto', default=1)
    precio_unitario = fields.Float(string='Precio Unitario', digits=(10, 2), default=0.0)
    price = fields.Float(
        string='Precio Total',
        compute="_compute_price",
        store=True,
        digits=(10, 2),
    )
    status = fields.Selection([
        ('draft' , 'Borrador'),
        ('confirmed' , 'Confirmado'),
        ('done' , 'Hecho'),
    ],readonly=True, string='Estado', default='draft')
    is_active = fields.Boolean(string='Activo', default=True)
    start_date= fields.Date(string='Fecha de Inicio')
    puntuacion_vendedor_introducir = fields.Integer(string="Puntuacion_vendedor")
    puntuacion_vendedor = fields.Integer(string="Puntuacion", related="puntuacion_vendedor_introducir")
    persona_ventas = fields.Many2one(comodel_name="res.partner")
    genero_ids=fields.Many2many(comodel_name="clasificacion")
    detalles_venta = fields.Char(string="Detalles venta", required=True)
    Subir_archivo=fields.Binary(string="Archivo")
    nombre_archivo=fields.Char(string="Nombre del archivo")
    link=fields.Char(string="Url", widget="url")
    categoria_ventas = fields.Many2one(
        comodel_name="res.partner.category",
        string="Categoria contacto",
        default=lambda self: self.env["res.partner.category"].search([('name', '=', 'ventas')], limit=1)
    )

    @api.depends('unidades_producto', 'precio_unitario')
    def _compute_price(self):
        for record in self:
            record.price = record.unidades_producto * record.precio_unitario

    def confirmar_presupuesto(self):
        if self.status == "draft":
            self.status="confirmed"
            _logger.info(f"Presupuesto {self.name} confirmado")


    def terminar_presupuesto(self):
        if self.status == "confirmed":
            self.status="done"
