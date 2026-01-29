# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json
import time

from ..ai_engine.hybrid import HybridEngine


class AIChatController(http.Controller):
    """API endpoints cho AI Chat Assistant"""

    @http.route('/ai/chat', type='http', auth='user', methods=['POST'], csrf=False)
    def chat_endpoint(self, **kwargs):
        """
        Endpoint chính để xử lý tin nhắn
        POST /ai/chat
        Payload: {
            "message": "Lấy danh sách nhân viên phòng IT",
            "module": "nhan_su"  # optional
        }
        """
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            user_message = data.get('message', '').strip()
            module_hint = data.get('module', None)
            
            if not user_message:
                return Response(
                    json.dumps({'success': False, 'error': 'Message is empty'}),
                    content_type='application/json'
                )
            
            # Khởi tạo Hybrid Engine
            start_time = time.time()
            hybrid_engine = HybridEngine(request.env)
            response_data = hybrid_engine.process_query(user_message, module_hint)
            processing_time = (time.time() - start_time) * 1000  # convert to ms
            
            # Lưu log
            request.env['ai_chat_assistant.chat_log'].create_log(
                message=user_message,
                response=response_data.get('response'),
                intent=response_data.get('intent'),
                method=response_data.get('method'),
                success=response_data.get('success', False),
                processing_time=processing_time,
                confidence_score=response_data.get('confidence_score', 0),
                extracted_entities=response_data.get('entities'),
                error_message=response_data.get('error'),
            )
            
            return Response(
                json.dumps({
                    'success': True,
                    'response': response_data.get('response'),
                    'intent': response_data.get('intent'),
                    'method': response_data.get('method'),
                    'confidence_score': response_data.get('confidence_score', 0),
                    'entities': response_data.get('entities', {}),
                    'processing_time_ms': round(processing_time, 2),
                }),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'success': False, 'error': str(e)}),
                content_type='application/json'
            )

    @http.route('/ai/chat/stats', type='http', auth='user', methods=['GET'], csrf=False)
    def get_statistics(self, days=7, **kwargs):
        """
        Lấy thống kê tương tác
        GET /ai/chat/stats?days=7
        """
        try:
            days = int(kwargs.get('days', 7))
            stats = request.env['ai_chat_assistant.chat_log'].get_statistics(days)
            
            return Response(
                json.dumps({'success': True, 'data': stats}),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'success': False, 'error': str(e)}),
                content_type='application/json'
            )

    @http.route('/ai/chat/history', type='http', auth='user', methods=['GET'], csrf=False)
    def get_chat_history(self, limit=10, **kwargs):
        """
        Lấy lịch sử chat
        GET /ai/chat/history?limit=10
        """
        try:
            limit = int(kwargs.get('limit', 10))
            user = request.env.user
            
            logs = request.env['ai_chat_assistant.chat_log'].search(
                [('user_id', '=', user.id)],
                order='create_date desc',
                limit=limit
            )
            
            history = []
            for log in logs:
                history.append({
                    'id': log.id,
                    'message': log.message,
                    'response': log.response,
                    'intent': log.intent,
                    'method': log.method,
                    'success': log.success,
                    'confidence_score': log.confidence_score,
                    'processing_time_ms': log.processing_time,
                    'create_date': log.create_date.isoformat(),
                })
            
            return Response(
                json.dumps({'success': True, 'data': history}),
                content_type='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps({'success': False, 'error': str(e)}),
                content_type='application/json'
            )
