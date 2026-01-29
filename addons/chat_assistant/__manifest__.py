{
    'name': 'Chat Assistant AI',
    'version': '15.0.1.0.0',
    'category': 'Productivity',
    'summary': 'AI-powered chat assistant for Odoo navigation',
    'description': """
        Chat Assistant
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['web', 'base'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'chat_assistant/static/src/js/chat.js',
            'chat_assistant/static/src/css/chat.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}