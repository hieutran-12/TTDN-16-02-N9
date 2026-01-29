## 2.1. Sơ đồ liên kết và thứ tự tạo dữ liệu

### Mối liên kết giữa các model:

- **res.partner (Nhà cung cấp)**: Dùng chung cho cả hai module, là đối tượng gốc để liên kết các nghiệp vụ mua sắm và tài sản.
- **hoa_don_mua (Hóa đơn mua)**: Tạo trước, liên kết với nhà cung cấp qua trường `nha_cung_cap_id`. Đây là chứng từ gốc cho nghiệp vụ mua sắm tài sản.
- **tai_san (Tài sản)**: Khi tạo tài sản, có thể chọn nhà cung cấp (`nha_cung_cap_id`) và liên kết với hóa đơn mua (`hoa_don_mua_id`).
- **but_toan_ke_toan (Bút toán)**: Được sinh ra khi xác nhận hóa đơn hoặc tài sản, có thể liên kết với cả hóa đơn mua (`hoa_don_mua_id`) và tài sản (`tai_san_id`).

### Thứ tự tạo dữ liệu và liên kết bắt buộc:

1. **Tạo nhà cung cấp (res.partner)** trước (bắt buộc).
2. **Tạo hóa đơn mua (hoa_don_mua)**, chọn nhà cung cấp vừa tạo. Nếu chưa có hóa đơn mua thì phải tạo mới.
3. **Tạo tài sản (tai_san)**, luôn chọn nhà cung cấp và bắt buộc liên kết với hóa đơn mua vừa tạo (không được bỏ trống). Nếu chưa có hóa đơn mua thì phải quay lại bước 2 để tạo.
4. **Xác nhận hóa đơn mua và tài sản** để sinh bút toán liên quan.

### Demo thực tế (luôn đảm bảo liên kết):

1. Vào menu **Danh bạ** (Contacts), tạo mới nhà cung cấp (ví dụ: Dell).
2. Vào **Hóa đơn mua**, tạo mới hóa đơn:

- Chọn nhà cung cấp vừa tạo
- Nhập các thông tin hóa đơn, lưu lại

3. Vào **Tài sản**, tạo mới tài sản:

- Chọn nhà cung cấp (giống hóa đơn)
- Bắt buộc chọn liên kết hóa đơn mua vừa tạo (không được để trống)
- Nhập các thông tin tài sản, lưu lại

4. Xác nhận hóa đơn và tài sản để sinh bút toán, kiểm tra các liên kết trong các bút toán và báo cáo.

> **Lưu ý:** Luôn tạo hóa đơn mua trước, sau đó mới tạo tài sản và liên kết với hóa đơn này. Không được tạo tài sản mà không liên kết hóa đơn mua.

# Hướng dẫn Demo Luồng Nghiệp Vụ Kế Toán – Quản Lý Tài Sản

## 1. Chuẩn bị dữ liệu

- Đảm bảo đã có các tài khoản kế toán (211, 214, 331, 642...)
- Đảm bảo đã có nhà cung cấp (res.partner)

## 2. Demo nghiệp vụ mua tài sản

### Bước 1: Tạo nhà cung cấp (nếu chưa có)

- Vào menu **Danh bạ** (Contacts)
- Tạo mới hoặc kiểm tra đã có nhà cung cấp (ví dụ: Dell)

### Bước 2: Tạo hóa đơn mua (module Kế toán – tài chính)

- Vào menu **Hóa đơn mua** (`hoa_don_mua`)
- Nhấn Tạo mới
- Nhập các trường:
  - `ma_hoa_don`: Số hóa đơn
  - `ngay_hoa_don`: Ngày hóa đơn
  - `nha_cung_cap_id`: Chọn nhà cung cấp (res.partner)
  - Thêm các dòng chi tiết (`chi_tiet_ids`): sản phẩm, số lượng, đơn giá, thuế suất
  - `dien_giai`: Diễn giải nghiệp vụ
- Lưu hóa đơn

### Bước 3: Xác nhận hóa đơn mua

- Nhấn nút **Xác nhận**
- Hệ thống tự động sinh các bút toán (`but_toan_ids`):
  - Nợ `tai_khoan_no_id` (ví dụ: 211)
  - Có `tai_khoan_co_id` (ví dụ: 331)
  - Số tiền (`so_tien`), diễn giải (`dien_giai`), liên kết nhà cung cấp (`nha_cung_cap_id`)

### Bước 4: Ghi nhận tài sản (module Quản lý tài sản)

- Vào menu **Tài sản** (`tai_san`)
- Nhấn Tạo mới
- Nhập các trường:
  - `ma_tai_san`: Mã tài sản (tự sinh)
  - `ten_tai_san`: Tên tài sản
  - `so_serial`: Số serial
  - `ngay_mua`: Ngày mua
  - `ngay_het_han_bao_hanh`: Ngày hết hạn bảo hành
  - `gia_tien_mua`: Giá tiền mua
  - `gia_tri_hien_tai`: Giá trị hiện tại (tự động tính)
  - `trang_thai`: Trạng thái
  - `loai_tai_san_id`: Loại tài sản
  - `vi_tri_hien_tai_id`: Vị trí hiện tại
  - `nha_cung_cap_id`: Nhà cung cấp (res.partner)
  - `quan_ly_id`: Người quản lý (nếu có)
  - `nguoi_dang_dung_id`: Người đang sử dụng (nếu có)
- Lưu và xác nhận tài sản

### Bước 5: Theo dõi khấu hao tài sản

- Hệ thống tự động tính khấu hao hàng tháng dựa trên các trường:
  - `nguyen_gia`, `thoi_gian_su_dung`, `phuong_phap_khau_hao`
- Định kỳ sinh bút toán khấu hao:
  - Nợ 642 (chi phí)
  - Có 214 (hao mòn)

### Bước 6: Xem báo cáo

- Vào các menu báo cáo tài sản, báo cáo kế toán để kiểm tra số liệu tài sản, khấu hao, công nợ nhà cung cấp.

---

## 3. Liên kết dữ liệu giữa 2 module

- `nha_cung_cap_id`: Dùng chung res.partner ở tất cả các model liên quan
- `hoa_don_mua_id`: Liên kết giữa tài sản và hóa đơn mua
- `but_toan_ids`, `chi_tiet_ids`: Tự động sinh khi xác nhận hóa đơn hoặc khấu hao tài sản
- `tai_san_id`: Liên kết bút toán với tài sản nếu phát sinh nghiệp vụ liên quan

---

## 4. Tác dụng của từng module

- **Kế toán – tài chính**: Ghi nhận nghiệp vụ mua sắm, công nợ, sinh bút toán, tổng hợp báo cáo tài chính
- **Quản lý tài sản**: Quản lý vòng đời tài sản, khấu hao, liên kết chặt chẽ với kế toán để đảm bảo số liệu chính xác

---

## 5. Lưu ý khi demo

- Luôn chọn đúng nhà cung cấp (res.partner) cho tất cả các trường `nha_cung_cap_id`
- Khi xóa nhà cung cấp, các bản ghi liên quan sẽ tự động set null, không gây lỗi khoá ngoại
- Đảm bảo các trường bắt buộc (required) được nhập đầy đủ khi tạo mới bản ghi

---

Bạn có thể trình bày demo trực tiếp trên giao diện Odoo theo từng bước trên, đối chiếu các trường dữ liệu thực tế trong từng model.
