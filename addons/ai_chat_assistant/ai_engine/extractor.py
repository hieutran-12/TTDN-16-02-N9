# -*- coding: utf-8 -*-
import re
from typing import Dict, List
from datetime import datetime


class EntityExtractor:
    """
    Trích xuất các entity từ tin nhắn
    Hỗ trợ: số tiền, ID, email, điện thoại VN, ngày tháng, số tiền, tên người, bộ lọc
    """
    
    def __init__(self):
        self.patterns = {
            'numbers': r'\b\d+(?:\.\d+)?\b',
            'ids': r'\b(?:ID|id|mã|code)[\s:]*(\w+)\b',
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phones': r'(?:\+84|0)[0-9]{8,10}',  # VN phone format
            'dates': [
                r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',  # dd/mm/yyyy or dd-mm-yyyy
                r'ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})',  # ngày X tháng Y
                r'(\d{1,2})/(\d{1,2})',  # dd/mm
            ],
            'amounts': [
                r'(\d+(?:\.\d{3})*)\s*(?:đồng|vnd|triệu|tỷ)',
                r'(\d+)\s*(?:k|K)',  # k = 1000
            ],
            'names': r'(?:tên|name)\s*[:=]?\s*([A-Za-zÀ-ỿ\s]+)',
            'filters': [
                r'(?:từ|from)\s+(\d+)',
                r'(?:đến|to)\s+(\d+)',
                r'(?:lọc|filter)\s+([^,]+)',
            ]
        }
    
    def extract_all(self, message: str) -> Dict[str, List]:
        """
        Trích xuất tất cả các entity loại từ tin nhắn
        """
        return {
            'numbers': self.extract_numbers(message),
            'ids': self.extract_ids(message),
            'emails': self.extract_emails(message),
            'phones': self.extract_phones(message),
            'dates': self.extract_dates(message),
            'amounts': self.extract_amounts(message),
            'names': self.extract_names(message),
            'filters': self.extract_filters(message),
        }
    
    def extract_numbers(self, text: str) -> List[str]:
        """Trích xuất các số từ text"""
        matches = re.findall(self.patterns['numbers'], text)
        return list(set(matches))  # Remove duplicates
    
    def extract_ids(self, text: str) -> List[str]:
        """Trích xuất IDs/mã từ text"""
        matches = re.findall(self.patterns['ids'], text, re.IGNORECASE)
        return list(set(matches))
    
    def extract_emails(self, text: str) -> List[str]:
        """Trích xuất emails từ text"""
        matches = re.findall(self.patterns['emails'], text)
        return list(set(matches))
    
    def extract_phones(self, text: str) -> List[str]:
        """Trích xuất số điện thoại Việt Nam từ text"""
        matches = re.findall(self.patterns['phones'], text)
        return list(set(matches))
    
    def extract_dates(self, text: str) -> List[Dict]:
        """
        Trích xuất ngày tháng từ text
        Returns: list of dicts with 'original' và 'parsed' fields
        """
        dates = []
        text_lower = text.lower()
        
        # Format: dd/mm/yyyy or dd-mm-yyyy
        matches = re.findall(self.patterns['dates'][0], text)
        for match in matches:
            dates.append({'original': match, 'format': 'dd/mm/yyyy or dd-mm-yyyy'})
        
        # Format: ngày X tháng Y
        matches = re.findall(self.patterns['dates'][1], text_lower)
        for match in matches:
            dates.append({'original': f"ngày {match[0]} tháng {match[1]}", 'format': 'ngày X tháng Y'})
        
        return dates
    
    def extract_amounts(self, text: str) -> List[Dict]:
        """
        Trích xuất các số tiền từ text
        Hỗ trợ: VND, triệu, tỷ, k (nghìn)
        """
        amounts = []
        text_lower = text.lower()
        
        # Pattern 1: 1.000.000 đồng, 500 triệu, 2 tỷ
        matches = re.findall(self.patterns['amounts'][0], text, re.IGNORECASE)
        for match in matches:
            amounts.append({'amount': match, 'format': 'number + unit'})
        
        # Pattern 2: k (nghìn)
        matches = re.findall(self.patterns['amounts'][1], text, re.IGNORECASE)
        for match in matches:
            amounts.append({'amount': f"{match}000", 'format': 'k (thousands)'})
        
        return amounts
    
    def extract_names(self, text: str) -> List[str]:
        """Trích xuất tên người từ text"""
        matches = re.findall(self.patterns['names'], text, re.IGNORECASE)
        return [m.strip() for m in matches if m.strip()]
    
    def extract_filters(self, text: str) -> List[Dict]:
        """Trích xuất các bộ lọc từ text"""
        filters = []
        text_lower = text.lower()
        
        # From-To filters
        for pattern in self.patterns['filters'][:2]:
            matches = re.findall(pattern, text_lower)
            if matches:
                filters.extend([{'filter': m, 'type': 'range'} for m in matches])
        
        # Custom filters
        matches = re.findall(self.patterns['filters'][2], text_lower)
        filters.extend([{'filter': m, 'type': 'custom'} for m in matches])
        
        return filters
