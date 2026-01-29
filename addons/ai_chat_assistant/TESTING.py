#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Chat Assistant - Test Examples

This file demonstrates how to test the AI Chat Assistant module
"""

# Test examples for different query types

TEST_QUERIES = {
    'list_read': [
        "Danh sách nhân viên phòng IT",
        "Lấy danh sách tài sản",
        "Hiển thị tất cả hóa đơn",
        "Xem danh sách chứng chỉ",
    ],
    
    'search': [
        "Tìm nhân viên tên Nguyen",
        "Tìm kiếm hóa đơn số HD001",
        "Lọc tài sản loại máy tính",
        "Tìm chi phí từ 1 triệu đến 5 triệu",
    ],
    
    'statistics': [
        "Thống kê tổng số nhân viên",
        "Tính tổng giá trị tài sản",
        "Số lượng hóa đơn tháng 1",
        "Thống kê chi phí quý 4",
    ],
    
    'create': [
        "Tạo nhân viên mới tên Tuan",
        "Thêm tài sản mới giá 10 triệu",
        "Tạo hóa đơn 500 triệu",
        "Tạo bản ghi mới",
    ],
    
    'update': [
        "Cập nhật lương nhân viên ID 123",
        "Sửa vị trí tài sản ID 456",
        "Cập nhật trạng thái hóa đơn",
        "Thay đổi phòng ban nhân viên",
    ],
    
    'delete': [
        "Xóa nhân viên ID 789",
        "Xóa tài sản ID 321",
        "Xoá hóa đơn ID 654",
    ],
    
    'navigation': [
        "Đi tới module nhân sự",
        "Mở trang quản lý tài sản",
        "Vào danh sách kế toán",
    ],
    
    'mixed': [
        "Danh sách nhân viên phòng IT từ 2024",
        "Tìm kiếm tài sản giá từ 100 triệu đến 500 triệu",
        "Thống kê hóa đơn tháng 1 năm 2024",
        "Cập nhật lương nhân viên Nguyen Van A tăng 10%",
    ],
}

# Expected results for testing

EXPECTED_RESULTS = {
    'list_read': {
        'intent': 'list_read',
        'module': 'nhan_su',  # or quan_ly_tai_san, tai_chinh_ke_toan
        'success': True,
        'method': 'rule',  # Should be rule-based for simple queries
    },
    'search': {
        'intent': 'search',
        'success': True,
        'entities': {
            'names': ['Nguyen'],  # Example for names
            'numbers': [],  # For ranges
        },
    },
}

# API Testing Code

API_TEST_CODE = """
# Test with curl
curl -X POST http://localhost:8069/ai/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Danh sách nhân viên phòng IT"}'

# Test statistics
curl http://localhost:8069/ai/chat/stats?days=7

# Test chat history
curl http://localhost:8069/ai/chat/history?limit=10

# Python test
import requests
import json

url = "http://localhost:8069/ai/chat"
headers = {"Content-Type": "application/json"}
data = {"message": "Danh sách nhân viên phòng IT"}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
"""

# Unit test examples

UNIT_TEST_EXAMPLES = """
from odoo.tests import common

class TestAIChatAssistant(common.TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.env['ai.chat.log'].create({
            'user_id': self.env.uid,
            'message': 'Test message',
            'response': 'Test response',
            'intent': 'list_read',
            'method': 'rule',
            'success': True,
            'processing_time': 45.2,
            'confidence_score': 85.5,
        })
    
    def test_rule_detector(self):
        from ai_chat_assistant.ai_engine.rules import RuleDetector
        detector = RuleDetector()
        intent, conf = detector.detect_intent("Danh sách nhân viên")
        self.assertEqual(intent, 'list_read')
        self.assertGreater(conf, 0.7)
    
    def test_entity_extractor(self):
        from ai_chat_assistant.ai_engine.extractor import EntityExtractor
        extractor = EntityExtractor()
        entities = extractor.extract_all("Tìm tài sản giá 500 triệu")
        self.assertIn('amounts', entities)
        self.assertGreater(len(entities['amounts']), 0)
    
    def test_chat_log_creation(self):
        log = self.env['ai.chat.log'].create({
            'user_id': self.env.uid,
            'message': 'Test query',
            'response': 'Test response',
            'intent': 'search',
            'method': 'rule',
            'success': True,
        })
        self.assertTrue(log.id)
        self.assertEqual(log.user_id, self.env.user)
    
    def test_statistics(self):
        stats = self.env['ai.chat.log'].get_statistics(days=7)
        self.assertIn('total_interactions', stats)
        self.assertIn('success_rate', stats)
        self.assertGreater(stats['total_interactions'], 0)
"""

# Entity extraction test

ENTITY_EXTRACTION_TEST = """
Test cases for entity extraction:

Input: "Tìm tài sản ID 123 giá từ 100 triệu đến 500 triệu từ 2024-01-15"
Expected:
{
    'ids': ['123'],
    'amounts': [
        {'amount': '100', 'format': 'triệu'},
        {'amount': '500', 'format': 'triệu'},
    ],
    'dates': [
        {'original': '2024-01-15', 'format': 'yyyy-mm-dd'},
    ],
    'numbers': ['100', '500', '2024', '01', '15'],
    'filters': [
        {'filter': '100', 'type': 'range'},
        {'filter': '500', 'type': 'range'},
    ],
}

Input: "Nhân viên Nguyen Van A, email: abc@example.com, điện thoại: 0912345678"
Expected:
{
    'names': ['Nguyen Van A'],
    'emails': ['abc@example.com'],
    'phones': ['0912345678'],
}

Input: "Hóa đơn số 1000k tháng 12"
Expected:
{
    'amounts': [
        {'amount': '1000000', 'format': 'k (thousands)'},
    ],
    'numbers': ['1000', '12'],
}
"""

# Performance benchmarks

PERFORMANCE_BENCHMARKS = """
Expected performance metrics:

Rule-Based Processing:
- Intent detection: 2-5ms
- Entity extraction: 5-10ms
- Handler execution: 10-30ms
- Total: ~45ms average

LLM Processing (GPU):
- Model loading: ~2-3 seconds (first time)
- Tokenization: 10-20ms
- Generation: 100-300ms
- Decoding: 10-20ms
- Total: ~200-350ms average

LLM Processing (CPU):
- Similar but 3-5x slower
- Total: ~1-2 seconds

Success metrics:
- Rule-based success rate: 90-95%
- LLM success rate: 85-90%
- Overall success rate: 90%+
"""

if __name__ == '__main__':
    print("AI Chat Assistant - Test Examples")
    print("==================================")
    print("\nTest Query Examples:")
    for intent, queries in TEST_QUERIES.items():
        print(f"\n{intent.upper()}:")
        for query in queries:
            print(f"  - {query}")
    
    print("\n\nRun tests with:")
    print("  python -m pytest tests/")
    print("  or")
    print("  ./odoo-bin --test-enable -m ai_chat_assistant")
