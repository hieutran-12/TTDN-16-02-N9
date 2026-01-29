# -*- coding: utf-8 -*-
from odoo import api, fields, models
import json
from datetime import datetime


class AIChatLog(models.Model):
    """Model để lưu lịch sử tương tác với AI Chat Assistant"""
    _name = 'ai_chat_assistant.chat_log'
    _description = 'AI Chat Log'
    _order = 'create_date desc'

    user_id = fields.Many2one('res.users', string='Người dùng', required=True, readonly=True)
    message = fields.Text(string='Tin nhắn từ người dùng', required=True, readonly=True)
    response = fields.Text(string='Phản hồi từ AI', readonly=True)
    intent = fields.Char(string='Intent (Ý định)', size=100, readonly=True)
    method = fields.Selection([
        ('rule', 'Rule-Based Detector'),
        ('llm', 'LLM Detector'),
        ('fallback', 'Fallback Response'),
    ], string='Phương pháp xử lý', readonly=True)
    success = fields.Boolean(string='Thành công', readonly=True, default=False)
    error_message = fields.Text(string='Thông báo lỗi', readonly=True)
    processing_time = fields.Float(string='Thời gian xử lý (ms)', readonly=True)
    confidence_score = fields.Float(string='Độ tin cậy (%)', readonly=True)
    extracted_entities = fields.Text(string='Entities trích xuất', readonly=True)  # JSON format
    
    @api.model
    def create_log(self, message, response, intent, method, success, 
                   processing_time, confidence_score, extracted_entities=None, error_message=None):
        """
        Tạo log entry
        """
        return self.create({
            'user_id': self.env.uid,
            'message': message,
            'response': response,
            'intent': intent,
            'method': method,
            'success': success,
            'processing_time': processing_time,
            'confidence_score': confidence_score,
            'extracted_entities': json.dumps(extracted_entities or {}),
            'error_message': error_message,
        })

    @api.model
    def get_statistics(self, days=7):
        """
        Lấy thống kê tương tác trong N ngày gần đây
        """
        from datetime import datetime, timedelta
        start_date = datetime.now() - timedelta(days=days)
        
        logs = self.search([('create_date', '>=', start_date)])
        
        total = len(logs)
        successful = len(logs.filtered('success'))
        rule_based = len(logs.filtered(lambda x: x.method == 'rule'))
        llm_based = len(logs.filtered(lambda x: x.method == 'llm'))
        fallback = len(logs.filtered(lambda x: x.method == 'fallback'))
        
        avg_confidence = sum(logs.mapped('confidence_score')) / total if total > 0 else 0
        avg_time = sum(logs.mapped('processing_time')) / total if total > 0 else 0
        
        return {
            'total_interactions': total,
            'successful_interactions': successful,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'rule_based_count': rule_based,
            'llm_based_count': llm_based,
            'fallback_count': fallback,
            'avg_confidence_score': round(avg_confidence, 2),
            'avg_processing_time': round(avg_time, 2),
        }
