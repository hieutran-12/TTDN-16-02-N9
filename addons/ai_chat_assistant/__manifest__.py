# -*- coding: utf-8 -*-
{
    'name': "AI Chat Assistant",

    'summary': "AI Assistant cho Odoo (Rule-based + LLM)",

    'description': """
        Trợ lý AI cho Odoo 15:
        - NLP tiếng Việt
        - Rule-based + LLM
        - Chat widget backend
        - Phân tích nghiệp vụ
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Tools',
    'version': '1.0',

    'depends': [
        'base',
        'web',
    ],

    'data': [
        'data/module_mappings.xml',
        'security/ir.model.access.csv',
        'views/chat_log.xml',
        'views/menu.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'ai_chat_assistant/static/src/css/chat_widget.css',
            'ai_chat_assistant/static/src/js/chat_widget.js',
            'ai_chat_assistant/static/src/xml/chat_widget.xml',
        ],
    },

    'external_dependencies': {
        'python': ['underthesea'],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
}
