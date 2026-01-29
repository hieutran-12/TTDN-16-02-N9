# HƯỚNG DẪN DEMO QUẢN LÝ VÒNG ĐỜI TÀI SẢN LIÊN KẾT KẾ TOÁN

## 1. Tạo tài khoản kế toán liên quan

- Vào module Kế toán (tai_chinh_ke_toan), tạo các tài khoản:
  - Tài khoản tài sản (VD: 211, 213...)
  - Tài khoản hao mòn lũy kế (VD: 214...)
  - Tài khoản chi phí khấu hao (VD: 642...)

## 2. Tạo mới tài sản

- Vào module Quản lý tài sản, tạo mới tài sản:
  - Chọn các tài khoản kế toán liên quan (tài khoản tài sản, hao mòn, chi phí khấu hao).
  - Nhập đầy đủ thông tin tài sản.

## 3. Ghi nhận khấu hao tài sản

- Vào menu Khấu hao, tạo mới bản ghi khấu hao cho tài sản.
- Sau khi lưu, hệ thống sẽ tự động sinh bút toán kế toán:
  - Nợ: Tài khoản chi phí khấu hao
  - Có: Tài khoản hao mòn lũy kế
- Có thể xem liên kết bút toán ngay trên form khấu hao.

## 4. Thanh lý tài sản

- Vào menu Thanh lý tài sản, tạo phiếu thanh lý cho tài sản cần thanh lý.
- Xác nhận và hoàn thành phiếu thanh lý.
- Hệ thống sẽ tự động sinh bút toán kế toán:
  - Nợ: Tài khoản hao mòn lũy kế (xóa hao mòn)
  - Có: Tài khoản tài sản (ghi giảm nguyên giá)
  - Nợ: Tài khoản tài sản (ghi nhận tiền thu về từ thanh lý)
- Có thể xem liên kết bút toán ngay trên form thanh lý.

## 5. Kiểm tra sổ cái/sổ chi tiết

- Vào module Kế toán, kiểm tra các bút toán vừa sinh ra trong sổ cái, sổ chi tiết.

## 6. Lưu ý

- Các trường tài khoản kế toán là bắt buộc khi tạo tài sản.
- Nếu thiếu thông tin hoặc chọn sai tài khoản, bút toán sẽ không sinh đúng nghiệp vụ.
- Có thể phân quyền chi tiết hơn nếu cần.

---

Mọi thắc mắc hoặc cần mở rộng nghiệp vụ, vui lòng liên hệ đội phát triển!
