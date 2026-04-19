{
    'name': 'Gym Addon',
    'version': '17.0.3.0.0',
    'summary': 'Gestión de gimnasio',
    'description': 'Módulo para la gestión de actividades y abonados de un gimnasio.',
    'category': 'Services',
    'author': 'Formación Odoo',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/gym_activity_views.xml',
        'views/gym_schedule_views.xml',
    ],
    'installable': True,
    'application': True,
}
