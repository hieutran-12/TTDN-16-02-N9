# -*- coding: utf-8 -*-
import re
import json
from typing import Dict, List, Tuple


class RuleDetector:
    """
    Rule-based detector cho 70% các truy vấn đơn giản
    Sử dụng regex + keyword matching
    """
    
    # Intent patterns
    INTENT_PATTERNS = {
        'list_read': [
            r'danh\s*sách|liệt\s*kê|lấy|hiển\s*thị|xem|show|list',
            r'nhân\s*viên|phòng\s*ban|tài\s*sản|hóa\s*đơn|chứng\s*chỉ',
        ],
        'create': [
            r'tạo|thêm|tạo\s*mới|new|add|insert',
            r'nhân\s*viên|phòng\s*ban|tài\s*sản|hóa\s*đơn',
        ],
        'update': [
            r'cập\s*nhật|sửa|thay\s*đổi|update|edit|modify',
            r'nhân\s*viên|phòng\s*ban|tài\s*sản|hóa\s*đơn',
        ],
        'delete': [
            r'xóa|delete|remove|xóa\s*bỏ',
            r'nhân\s*viên|phòng\s*ban|tài\s*sản|hóa\s*đơn',
        ],
        'search': [
            r'tìm|search|tìm\s*kiếm|lọc|filter',
            r'nhân\s*viên|phòng\s*ban|tài\s*sản|hóa\s*đơn|chứng\s*chỉ',
        ],
        'statistics': [
            r'thống\s*kê|tổng|cộng|sum|count|total',
            r'lương|chi\s*phí|tài\s*sản|hóa\s*đơn',
        ],
        'navigation': [
            r'đi\s*tới|mở|vào|go\s*to|open|navigate',
            r'nhân\s*viên|phòng\s*ban|tài\s*sản|hóa\s*đơn',
        ],
    }
    
    # Module mappings - Vietnamese to Odoo model names
    MODULE_MAPPINGS = {
        'nhan_su': {
            'keywords': [
                'nhân\s*viên|employee|nv', 
                'phòng\s*ban|department|pb', 
                'chức\s*vụ|position|cv',
                'chứng\s*chỉ|certificate|cc',
                'công\s*tác|job|work',
            ],
            'models': ['hr.employee', 'hr.department', 'hr.job', 'certificate'],
        },
        'quan_ly_tai_san': {
            'keywords': [
                'tài\s*sản|asset|ts',
                'loại\s*tài\s*sản|asset\s*type|lts',
                'vị\s*trí|location|vt',
                'khấu\s*hao|depreciation|kh',
                'bảo\s*trì|maintenance|bt',
            ],
            'models': ['tai.san', 'loai.tai.san', 'vi.tri', 'khau.hao'],
        },
        'tai_chinh_ke_toan': {
            'keywords': [
                'hóa\s*đơn|invoice|hd',
                'phiếu|voucher|receipt|pk',
                'lương|salary|payroll',
                'chi\s*phí|expense|cp',
                'tài\s*khoản|account|tk',
            ],
            'models': ['account.move', 'account.invoice', 'hr.payroll'],
        },
    }
    
    def __init__(self):
        self.confidence_threshold = 0.7
    
    def detect_intent(self, message: str) -> Tuple[str, float]:
        """
        Phát hiện intent từ tin nhắn
        Returns: (intent, confidence)
        """
        message_lower = message.lower()
        max_confidence = 0
        detected_intent = 'unknown'
        
        for intent, patterns in self.INTENT_PATTERNS.items():
            pattern_matches = 0
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    pattern_matches += 1
            
            if pattern_matches > 0:
                confidence = min(1.0, pattern_matches / len(patterns))
                if confidence > max_confidence:
                    max_confidence = confidence
                    detected_intent = intent
        
        return detected_intent, max_confidence
    
    def detect_module(self, message: str) -> Tuple[str, float]:
        """
        Phát hiện module nào bị liên quan
        Returns: (module_name, confidence)
        """
        message_lower = message.lower()
        max_confidence = 0
        detected_module = None
        
        for module_name, config in self.MODULE_MAPPINGS.items():
            matched_keywords = 0
            for keyword in config['keywords']:
                if re.search(keyword, message_lower):
                    matched_keywords += 1
            
            if matched_keywords > 0:
                confidence = matched_keywords / len(config['keywords'])
                if confidence > max_confidence:
                    max_confidence = confidence
                    detected_module = module_name
        
        return detected_module or 'general', max_confidence
    
    def extract_entities(self, message: str) -> Dict:
        """
        Trích xuất entities từ tin nhắn
        """
        from .extractor import EntityExtractor
        extractor = EntityExtractor()
        return extractor.extract_all(message)
    
    def process_query(self, message: str, module_hint: str = None) -> Dict:
        """
        Xử lý truy vấn dựa trên rule
        """
        intent, intent_conf = self.detect_intent(message)
        module, module_conf = self.detect_module(message)
        entities = self.extract_entities(message)
        
        # Override module nếu có hint
        if module_hint:
            module = module_hint
        
        # Tính overall confidence
        overall_confidence = (intent_conf + module_conf) / 2
        
        return {
            'intent': intent,
            'module': module,
            'entities': entities,
            'confidence_score': min(100, overall_confidence * 100),
            'can_use_rule': overall_confidence >= self.confidence_threshold,
        }
