# -*- coding: utf-8 -*-
import json
import logging
from typing import Dict, Tuple
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

_logger = logging.getLogger(__name__)


class LLMDetector:
    """
    LLM-based detector cho 30% truy vấn phức tạp
    Sử dụng Qwen2.5-3B-Instruct với 4-bit quantization cho RTX 3050 4GB
    """
    
    def __init__(self):
        self.model_name = "Qwen/Qwen2.5-3B-Instruct"
        self.model = None
        self.tokenizer = None
        self.device = "cuda"  # Sẽ tự động fallback nếu GPU không khả dụng
        self._load_model()
    
    def _load_model(self):
        """
        Tải model Qwen2.5-3B với 4-bit quantization
        4-bit quantization cho phép chạy trên RTX 3050 4GB
        """
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
            
            # Check GPU availability
            if not torch.cuda.is_available():
                _logger.warning("GPU not available, using CPU for LLM")
                self.device = "cpu"
                self._load_model_cpu()
                return
            
            # 4-bit quantization configuration
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
            
            _logger.info(f"Loading {self.model_name} with 4-bit quantization...")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
            )
            
            _logger.info(f"{self.model_name} loaded successfully")
            
        except Exception as e:
            _logger.error(f"Failed to load LLM: {str(e)}")
            _logger.info("Falling back to CPU or rule-based processing")
            self._load_model_cpu()
    
    def _load_model_cpu(self):
        """
        Fallback: Tải model trên CPU (chậm hơn nhưng luôn hoạt động)
        """
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            _logger.info(f"Loading {self.model_name} on CPU (slow mode)...")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                device_map="cpu",
                trust_remote_code=True,
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
            )
            
            self.device = "cpu"
            _logger.info(f"{self.model_name} loaded on CPU")
            
        except Exception as e:
            _logger.error(f"Failed to load model on CPU: {str(e)}")
            self.model = None
    
    def process_query(self, message: str, context: Dict = None) -> Tuple[str, float]:
        """
        Xử lý truy vấn bằng LLM
        Returns: (response, confidence_score)
        """
        if self.model is None:
            return "Không thể xử lý truy vấn này. Vui lòng thử lại.", 0.0
        
        try:
            # Xây dựng prompt
            prompt = self._build_prompt(message, context)
            
            # Generate response
            response = self._generate_response(prompt)
            
            # Parse response để lấy intent, entities
            parsed = self._parse_response(response)
            
            return parsed['response'], parsed.get('confidence', 0.8)
            
        except Exception as e:
            _logger.error(f"LLM processing error: {str(e)}")
            return f"Lỗi xử lý: {str(e)}", 0.0
    
    def _build_prompt(self, message: str, context: Dict = None) -> str:
        """
        Xây dựng prompt cho LLM
        """
        system_prompt = """Bạn là một trợ lý AI thông minh cho hệ thống Odoo ERP của công ty.
Nhiệm vụ của bạn là:
1. Phân tích yêu cầu của người dùng bằng tiếng Việt
2. Xác định intent (lấy dữ liệu, tạo, cập nhật, xóa, tìm kiếm, thống kê)
3. Xác định module liên quan: nhan_su, quan_ly_tai_san, tai_chinh_ke_toan
4. Trích xuất entities quan trọng (số tiền, ID, ngày tháng, tên, bộ lọc)
5. Trả lời bằng JSON có định dạng:
{
    "intent": "...",
    "module": "...",
    "entities": {...},
    "response": "...",
    "confidence": 0.0-1.0
}"""
        
        user_message = f"Yêu cầu: {message}"
        
        if context:
            user_message += f"\nNgữ cảnh: {json.dumps(context, ensure_ascii=False)}"
        
        return f"{system_prompt}\n\n{user_message}"
    
    def _generate_response(self, prompt: str) -> str:
        """
        Sinh response từ LLM
        """
        import torch
        
        # Tokenize input
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.95,
                do_sample=True,
            )
        
        # Decode
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the assistant's part
        if "Yêu cầu:" in response:
            response = response.split("Yêu cầu:")[-1].strip()
        
        return response
    
    def _parse_response(self, response: str) -> Dict:
        """
        Parse response từ LLM (assuming JSON format)
        """
        try:
            # Tìm JSON trong response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                parsed = json.loads(json_str)
                return {
                    'intent': parsed.get('intent', 'unknown'),
                    'module': parsed.get('module', 'general'),
                    'entities': parsed.get('entities', {}),
                    'response': parsed.get('response', response),
                    'confidence': parsed.get('confidence', 0.8),
                }
        except Exception as e:
            _logger.warning(f"Failed to parse LLM response as JSON: {str(e)}")
        
        # Fallback: return raw response
        return {
            'intent': 'unknown',
            'module': 'general',
            'entities': {},
            'response': response,
            'confidence': 0.6,
        }
