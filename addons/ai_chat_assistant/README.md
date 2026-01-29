# AI Chat Assistant Module

Trợ lý AI thông minh cho hệ thống Odoo ERP với kiến trúc hybrid (Rule-based 70% + LLM 30%)

## Tính năng chính

### 1. Kiến trúc Hybrid

- **Rule-Based Detector (70%)**: Xử lý nhanh cho các truy vấn đơn giản
  - Phát hiện intent: lấy danh sách, tạo, cập nhật, xóa, tìm kiếm, thống kê, điều hướng
  - Phát hiện module: nhan_su, quan_ly_tai_san, tai_chinh_ke_toan
  - Trích xuất entities
  - Confidence threshold: 0.7

- **LLM Detector (30%)**: Xử lý phức tạp bằng Qwen2.5-3B
  - Model: Qwen2.5-3B-Instruct
  - Lượng tử hóa 4-bit cho RTX 3050 4GB
  - Fallback CPU support

### 2. Xử lý Entity

Hỗ trợ trích xuất các loại dữ liệu:

- **Số tiền**: VND, triệu, tỷ, k (nghìn)
- **ID/Mã**: ID nhân viên, tài sản, hóa đơn
- **Email**: Format email chuẩn
- **Điện thoại**: Định dạng Việt Nam (+84, 0)
- **Ngày tháng**: dd/mm/yyyy, ngày X tháng Y
- **Tên**: Tên người
- **Bộ lọc**: Khoảng từ-đến, custom filters

### 3. Đa Module

Tích hợp với các module chính:

- **nhan_su**: Nhân viên, phòng ban, chức vụ, chứng chỉ
- **quan_ly_tai_san**: Tài sản, loại, vị trí, khấu hao, bảo trì
- **tai_chinh_ke_toan**: Hóa đơn, lương, chi phí, tài khoản

### 4. Logging & Analytics

- Lưu lịch sử tất cả tương tác
- Thống kê: tổng số, tỷ lệ thành công, phương pháp, độ tin cậy
- Lọc theo thời gian, người dùng

### 5. Chat Widget

- Chat widget tích hợp vào backend
- Giao diện thân thiện, responsive
- Lịch sử chat, minimize/maximize
- Loading indicators, status messages

## Kiến trúc File

```
ai_chat_assistant/
├── __manifest__.py          # Cấu hình module
├── __init__.py              # Init files
├── models/
│   ├── __init__.py
│   └── chat_log.py         # Model logging
├── controllers/
│   ├── __init__.py
│   └── main.py             # API endpoints
├── ai_engine/
│   ├── __init__.py
│   ├── rules.py            # Rule-based detector
│   ├── extractor.py        # Entity extractor
│   ├── llm.py              # LLM detector
│   ├── hybrid.py           # Hybrid engine
│   └── handlers/
│       ├── __init__.py
│       ├── navigation_handler.py
│       ├── data_handler.py
│       └── query_handler.py
├── views/
│   ├── actions.xml
│   ├── assets.xml
│   ├── chat_log.xml
│   └── menu.xml
├── security/
│   └── ir.model.access.csv
├── data/
│   └── module_mappings.xml
└── static/
    └── src/
        ├── css/
        │   └── chat_widget.css
        ├── js/
        │   └── chat_widget.js
        └── xml/
            └── chat_widget.xml
```

## API Endpoints

### POST /ai/chat

Xử lý tin nhắn từ người dùng

**Request:**

```json
{
  "message": "Danh sách nhân viên phòng IT",
  "module": "nhan_su" // optional
}
```

**Response:**

```json
{
    "success": true,
    "response": "Danh sách nhân viên...",
    "intent": "list_read",
    "method": "rule",
    "confidence_score": 85.5,
    "entities": {...},
    "processing_time_ms": 45.2
}
```

### GET /ai/chat/stats

Lấy thống kê tương tác

**Query params:**

- `days`: Số ngày (mặc định 7)

**Response:**

```json
{
  "success": true,
  "data": {
    "total_interactions": 150,
    "successful_interactions": 145,
    "success_rate": 96.67,
    "rule_based_count": 105,
    "llm_based_count": 40,
    "fallback_count": 5,
    "avg_confidence_score": 87.3,
    "avg_processing_time": 52.4
  }
}
```

### GET /ai/chat/history

Lấy lịch sử chat của người dùng

**Query params:**

- `limit`: Số bản ghi (mặc định 10)

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "id": 123,
      "message": "Lấy danh sách nhân viên",
      "response": "Danh sách nhân viên...",
      "intent": "list_read",
      "method": "rule",
      "success": true,
      "confidence_score": 85.5,
      "processing_time_ms": 45.2,
      "create_date": "2024-01-15T10:30:00"
    }
  ]
}
```

## Cài đặt & Sử dụng

### 1. Cài đặt Dependencies

```bash
pip install transformers torch bitsandbytes numpy underthesea
```

### 2. Kích hoạt Module

```bash
# Trong Odoo CLI
./odoo-bin -u ai_chat_assistant -d database_name
```

### 3. Sử dụng Chat Widget

Widget sẽ tự động xuất hiện ở góc phải dưới cùng của trang backend.

**Ví dụ truy vấn:**

- "Danh sách nhân viên phòng IT"
- "Tìm tài sản ID 123"
- "Tạo hóa đơn 500 triệu"
- "Thống kê lương tháng 1"
- "Cập nhật tín chỉ nhân viên ABC"

## Yêu cầu Hệ thống

- **Python**: 3.8+
- **Odoo**: 15.0
- **GPU**: RTX 3050 4GB (4-bit quantization)
- **RAM**: 8GB tối thiểu
- **Disk**: 10GB cho model Qwen2.5

## Quy trình Xử lý

```
1. Rule Detector
   ├─ Confidence >= 0.7 → Sử dụng rule-based
   │  ├─ Navigation Handler
   │  ├─ Data Handler (CRUD)
   │  └─ Query Handler (search, statistics)
   └─ Confidence < 0.7 → Chuyển sang LLM

2. LLM Detector (nếu cần)
   ├─ Load model Qwen2.5-3B
   ├─ Process query
   └─ Return response

3. Fallback (nếu cả 2 thất bại)
   └─ Return generic response
```

## Cấu hình

Chỉnh sửa confidence threshold trong `ai_engine/hybrid.py`:

```python
self.rule_threshold = 0.7  # Thay đổi giá trị theo nhu cầu
```

## Troubleshooting

### Model không load

- Kiểm tra GPU: `nvidia-smi`
- Cài đặt CUDA/cuDNN
- Fallback tự động sang CPU (chậm hơn)

### Timeout

- Tăng timeout trong settings
- Giảm max_tokens trong LLM

### Memory error

- Giảm batch size
- Sử dụng 4-bit quantization (đã được enable)

## Phát triển

### Thêm Intent mới

1. Sửa `INTENT_PATTERNS` trong `ai_engine/rules.py`
2. Tạo handler tương ứng trong `ai_engine/handlers/`
3. Update `HybridEngine.process_query()` để route intent

### Thêm Module mới

1. Sửa `MODULE_MAPPINGS` trong `ai_engine/rules.py`
2. Update handlers để support module mới
3. Thêm entity patterns nếu cần

## License

Proprietary - My Company

## Support

Liên hệ: support@mycompany.com
