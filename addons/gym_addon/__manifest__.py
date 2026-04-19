{
    'name': 'Gym Addon',
    'version': '17.0.4.0.0',
    'summary': 'Gestión de gimnasio',
    'description': 'Módulo para la gestión de actividades y abonados de un gimnasio.',
    'category': 'Services',
    'author': 'Formación Odoo',
    'depends': ['base', 'portal', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/gym_activity_views.xml',
        'views/gym_schedule_views.xml',
        'templates/portal_schedule.xml',
    ],
    'installable': True,
    'application': True,
}
