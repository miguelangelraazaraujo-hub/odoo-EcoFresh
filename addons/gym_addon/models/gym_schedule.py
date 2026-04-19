from odoo import models, fields


class GymSchedule(models.Model):
    _name = 'gym.schedule'
    _description = 'Horario semanal de actividades'
    _order = 'day_of_week, time_start'

    # Many2one → cada horario pertenece a UNA actividad
    activity_id = fields.Many2one(
        comodel_name='gym.activity',
        string='Actividad',
        required=True,
        ondelete='cascade',
    )
    day_of_week = fields.Selection(
        selection=[
            ('0', 'Lunes'),
            ('1', 'Martes'),
            ('2', 'Miércoles'),
            ('3', 'Jueves'),
            ('4', 'Viernes'),
            ('5', 'Sábado'),
            ('6', 'Domingo'),
        ],
        string='Día de la semana',
        required=True,
    )
    time_start = fields.Float(
        string='Hora de inicio',
        required=True,
    )
    time_end = fields.Float(
        string='Hora de fin',
        required=True,
    )
    instructor = fields.Char(
        string='Monitor/a',
    )
