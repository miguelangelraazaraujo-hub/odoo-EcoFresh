{
    'name': 'Gym Addon',
    'version': '17.0.1.0.0',
    'summary': 'Gestión de gimnasio',
    'description': 'Módulo para la gestión de actividades y abonados de un gimnasio.',
    'category': 'Services',
    'author': 'Formación Odoo',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/gym_activity_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}