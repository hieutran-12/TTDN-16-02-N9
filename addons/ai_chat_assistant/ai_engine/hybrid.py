# -*- coding: utf-8 -*-
import logging
import json
from typing import Dict

from .rules import RuleDetector
from .llm import LLMDetector

_logger = logging.getLogger(__name__)


class HybridEngine:
    """
    Kiến trúc Hybrid Engine:
    - Rule-based (70%): Xử lý nhanh cho truy vấn đơn giản
    - LLM (30%): Xử lý chính xác cho truy vấn phức tạp
    - Fallback: Hỗ trợ khi cả 2 đều không hoạt động
    """
    
    def __init__(self, env):
        """
        Khởi tạo Hybrid Engine
        env: Odoo environment để truy cập models
        """
        self.env = env
        self.rule_detector = RuleDetector()
        self.llm_detector = None  # Disable LLM để tránh lỗi dependencies
        self.rule_threshold = 0.5  # Threshold thấp để rule-based xử lý hầu hết queries
        self.use_llm = False  # Set to True để enable LLM khi đã cài đủ dependencies
        
        # Import handlers
        from .handlers.navigation_handler import NavigationHandler
        from .handlers.data_handler import DataHandler
        from .handlers.query_handler import QueryHandler
        
        self.navigation_handler = NavigationHandler(env)
        self.data_handler = DataHandler(env)
        self.query_handler = QueryHandler(env)
    
    def process_query(self, message: str, module_hint: str = None) -> Dict:
        """
        Xử lý truy vấn toàn diện
        
        Flow:
        1. Rule Detector → Luôn sử dụng rule-based (LLM disabled)
        2. Fallback → Trả lời mặc định nếu rule không rõ
        
        Returns: Dict chứa response và metadata
        """
        try:
            # Bước 1: Rule-based detection (ALWAYS)
            _logger.info(f"Processing query: {message}")
            rule_result = self.rule_detector.process_query(message, module_hint)
            
            intent = rule_result['intent']
            module = rule_result['module']
            entities = rule_result['entities']
            confidence = rule_result['confidence_score']
            
            # Sử dụng rule-based detector (LLM disabled)
            _logger.info(f"Using rule-based detector (confidence: {confidence}%)")
            response_data = self._handle_rule_based(
                intent, module, entities, message
            )
            response_data['method'] = 'rule'
            response_data['confidence_score'] = confidence
            return response_data
        
        except Exception as e:
            _logger.error(f"Error processing query: {str(e)}")
            return self._fallback_response(message, str(e))
    
    def _handle_rule_based(self, intent: str, module: str, entities: Dict, 
                          message: str) -> Dict:
        """
        Xử lý bằng rule-based + handlers
        """
        try:
            response = ""
            success = False
            
            # Route đến handler tương ứng
            if intent == 'navigation':
                response = self.navigation_handler.handle(message, module, entities)
                success = True
            
            elif intent in ['list_read', 'search']:
                response = self.query_handler.handle_query(intent, module, entities)
                success = True
            
            elif intent == 'create':
                response = self.data_handler.handle_create(module, entities)
                success = True
            
            elif intent == 'update':
                response = self.data_handler.handle_update(module, entities)
                success = True
            
            elif intent == 'delete':
                response = self.data_handler.handle_delete(module, entities)
                success = True
            
            elif intent == 'statistics':
                response = self.query_handler.handle_statistics(module, entities)
                success = True
            
            else:
                response = f"Không nhận ra ý định: {intent}. Vui lòng rõ ràng hơn."
                success = False
            
            return {
                'intent': intent,
                'module': module,
                'response': response,
                'success': success,
                'entities': entities,
            }
        
        except Exception as e:
            _logger.error(f"Rule-based handling error: {str(e)}")
            return {
                'intent': intent,
                'module': module,
                'response': f"Lỗi xử lý: {str(e)}",
                'success': False,
                'error': str(e),
                'entities': entities,
            }
    
    def _handle_llm_based(self, message: str, rule_result: Dict) -> Dict:
        """
        Xử lý bằng LLM detector
        """
        try:
            # Prepare context from rule detector
            context = {
                'suspected_intent': rule_result['intent'],
                'suspected_module': rule_result['module'],
                'entities': rule_result['entities'],
            }
            
            # Process with LLM
            llm_response, llm_confidence = self.llm_detector.process_query(message, context)
            
            # Try to execute based on LLM output
            # (In real scenario, you'd parse LLM output and execute handlers)
            
            return {
                'intent': rule_result.get('intent', 'unknown'),
                'module': rule_result.get('module', 'general'),
                'response': llm_response,
                'success': True,
                'entities': rule_result.get('entities', {}),
                'confidence_score': llm_confidence * 100,
            }
        
        except Exception as e:
            _logger.error(f"LLM-based handling error: {str(e)}")
            return self._fallback_response(message, str(e))
    
    def _fallback_response(self, message: str, error: str = None) -> Dict:
        """
        Trả lời fallback khi cả rule và LLM đều không hoạt động
        """
        responses = [
            "Xin lỗi, tôi không hiểu yêu cầu của bạn. Vui lòng rõ ràng hơn.",
            "Có thể bạn muốn: lấy danh sách, tạo bản ghi mới, tìm kiếm, hoặc xem thống kê?",
            "Tôi hiểu được các lệnh liên quan đến: Nhân sự, Tài sản, Tài chính. Vui lòng chỉ định rõ.",
        ]
        
        fallback_message = responses[hash(message) % len(responses)]
        
        return {
            'intent': 'unknown',
            'module': 'general',
            'response': fallback_message,
            'success': False,
            'method': 'fallback',
            'error': error,
            'confidence_score': 0,
        }
