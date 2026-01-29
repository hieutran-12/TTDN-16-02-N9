# AI Chat Assistant Configuration

## Rule-Based Detector Configuration

# Confidence threshold (0.0 - 1.0)

# If rule confidence >= threshold: use rule-based handler

# If rule confidence < threshold: use LLM

RULE_CONFIDENCE_THRESHOLD = 0.7

# Intent detection patterns

INTENT_PATTERNS = {
'list_read': {
'keywords': ['danh sách', 'liệt kê', 'lấy', 'hiển thị', 'xem'],
'weight': 1.0,
},
'create': {
'keywords': ['tạo', 'thêm', 'new', 'add'],
'weight': 1.0,
},
'update': {
'keywords': ['cập nhật', 'sửa', 'thay đổi', 'edit'],
'weight': 1.0,
},
'delete': {
'keywords': ['xóa', 'delete', 'remove'],
'weight': 0.8, # Higher threshold for dangerous operations
},
'search': {
'keywords': ['tìm', 'search', 'lọc', 'filter'],
'weight': 1.0,
},
'statistics': {
'keywords': ['thống kê', 'tổng', 'cộng', 'sum', 'count'],
'weight': 1.0,
},
'navigation': {
'keywords': ['đi tới', 'mở', 'vào', 'navigate'],
'weight': 1.0,
},
}

## LLM Configuration

# Model details

LLM_MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
LLM_QUANTIZATION = "4bit" # 4bit or 8bit or none

# Generation parameters

LLM_MAX_TOKENS = 512
LLM_TEMPERATURE = 0.7
LLM_TOP_P = 0.95
LLM_DO_SAMPLE = True

# Device configuration

LLM_DEVICE = "cuda" # cuda or cpu (auto-fallback if GPU unavailable)
LLM_DEVICE_MAP = "auto" # auto or cpu or cuda

## Entity Extractor Configuration

ENTITY_PATTERNS = {
'amount': {
'enabled': True,
'units': ['đồng', 'vnd', 'triệu', 'tỷ', 'k'],
},
'date': {
'enabled': True,
'formats': ['dd/mm/yyyy', 'dd-mm-yyyy', 'ngày X tháng Y'],
},
'phone': {
'enabled': True,
'country_code': '+84', # Vietnam
},
'email': {
'enabled': True,
},
'id': {
'enabled': True,
'patterns': ['ID', 'mã', 'code'],
},
'name': {
'enabled': True,
},
'number': {
'enabled': True,
},
}

## Module Mappings

MODULES = {
'nhan_su': {
'display_name': 'Nhân sự',
'models': ['hr.employee', 'hr.department', 'hr.job', 'certificate'],
'keywords': ['nhân viên', 'phòng ban', 'chức vụ', 'chứng chỉ'],
'enabled': True,
},
'quan_ly_tai_san': {
'display_name': 'Quản lý tài sản',
'models': ['tai.san', 'loai.tai.san', 'vi.tri', 'khau.hao', 'bao.tri'],
'keywords': ['tài sản', 'loại tài sản', 'vị trí', 'khấu hao', 'bảo trì'],
'enabled': True,
},
'tai_chinh_ke_toan': {
'display_name': 'Tài chính kế toán',
'models': ['account.move', 'account.invoice', 'account.chart.template'],
'keywords': ['hóa đơn', 'phiếu', 'lương', 'chi phí', 'tài khoản'],
'enabled': True,
},
}

## Chat Widget Configuration

WIDGET_CONFIG = {
'position': 'bottom-right', # bottom-right, bottom-left, top-right, top-left
'width': '380px',
'height': '600px',
'theme': 'light', # light or dark
'auto_expand': False,
'show_on_load': True,
}

## Logging Configuration

LOGGING = {
'enabled': True,
'log_level': 'INFO', # DEBUG, INFO, WARNING, ERROR
'log_storage': 'database', # database or file
'max_log_retention': 90, # days
'log_entities': True,
'log_confidence': True,
'log_processing_time': True,
}

## API Configuration

API_CONFIG = {
'base_url': '/ai/chat',
'endpoints': {
'chat': '/ai/chat',
'stats': '/ai/chat/stats',
'history': '/ai/chat/history',
},
'timeout': 30, # seconds
'max_message_length': 1000,
'rate_limit': 100, # requests per minute
}

## Performance Tuning

PERFORMANCE = {
'rule_processor_timeout': 5, # seconds
'llm_processor_timeout': 30, # seconds
'cache_results': True,
'cache_ttl': 3600, # seconds
'batch_processing': False,
}

## Advanced Options

ADVANCED = {
'fallback_mode': 'generic', # generic, rule_only, llm_only
'enable_nlp_preprocessing': True,
'enable_entity_normalization': True,
'enable_response_validation': True,
'enable_context_tracking': False,
'debug_mode': False,
}

## Vietnamese Language Configuration

VIETNAMESE_CONFIG = {
'nlp_library': 'underthesea',
'segmentation': True,
'pos_tagging': True,
'named_entity_recognition': True,
'enable_diacritics_normalization': True,
}
