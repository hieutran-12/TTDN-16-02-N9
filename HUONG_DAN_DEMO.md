# 📚 HƯỚNG DẪN DEMO DỰ ÁN QUẢN LÝ TÀI SẢN & KỂ TOÁN

## 🎯 Tổng Quan Dự Án

Dự án này bao gồm **3 module Odoo 15.0** chính:

1. **nhan_su** - Quản lý nhân viên
2. **quan_ly_tai_san** - Quản lý tài sản cố định với khấu hao tự động
3. **tai_chinh_ke_toan** - Quản lý kế toán, hóa đơn mua, bút toán

---

## 🚀 CÁCH KHỞI CHẠY HỆ THỐNG

### **1. Khởi động Odoo Server**

```bash
cd /home/hieu/TTDN-15-05-N1
./odoo-bin -c odoo.conf -d odoo_hieu_test
```

**Thông tin đăng nhập:**

- **URL:** http://localhost:8069
- **Database:** odoo_hieu_test
- **Username:** admin
- **Password:** admin

### **2. Tạo Database Mới (nếu cần)**

```bash
# Khởi tạo database mới
./odoo-bin -c odoo.conf -d my_database --stop-after-init

# Cài đặt 3 modules
./odoo-bin -c odoo.conf -d my_database -i nhan_su,quan_ly_tai_san,tai_chinh_ke_toan --stop-after-init
```

---

## 📊 DEMO CÁC MODULE

### **MODULE 1: QUẢN LÝ NHÂN SỰ (nhan_su)**

#### **Truy cập:**

Menu → Nhân sự → Nhân viên

#### **Demo Flow:**

**1️⃣ Tạo Phòng Ban**

```
Menu → Nhân sự → Cấu hình → Phòng ban
→ Tạo mới:
   - Tên: "Phòng Kế Toán"
   - Mô tả: "Bộ phận xử lý kế toán"
   - Lưu
```

**2️⃣ Tạo Chức Vụ**

```
Menu → Nhân sự → Cấu hình → Chức vụ
→ Tạo mới:
   - Tên: "Kế Toán Trưởng"
   - Lưu
```

**3️⃣ Tạo Nhân Viên**

```
Menu → Nhân sự → Nhân viên
→ Tạo mới:
   - Mã nhân viên: Tự động tạo (NV-00001)
   - Tên: "Nguyễn Văn A"
   - Ngày sinh: 1990-05-15
   - Email: nvana@company.com
   - Phòng ban: Phòng Kế Toán
   - Chức vụ: Kế Toán Trưởng
   - Lưu
```

**4️⃣ Quản Lý Chứng Chỉ**

```
Menu → Nhân sự → Chứng chỉ & Bằng cấp
→ Tạo mới:
   - Mã chứng chỉ: CC-0001
   - Tên chứng chỉ: "Chứng chỉ Kế toán"
   - Nhân viên: Nguyễn Văn A
   - Lưu
```

---

### **MODULE 2: QUẢN LÝ TÀI SẢN (quan_ly_tai_san)**

#### **Truy cập:**

Menu → Tài sản → Quản lý Tài sản

#### **Demo Flow:**

**1️⃣ Tạo Loại Tài Sản**

```
Menu → Tài sản → Cấu hình → Loại tài sản
→ Tạo mới:
   - Tên: "Máy tính"
   - Mô tả: "Thiết bị công nghệ thông tin"
   - Lưu
```

**2️⃣ Tạo Vị Trí Lưu Trữ**

```
Menu → Tài sản → Cấu hình → Vị trí
→ Tạo mới:
   - Tên: "Phòng 101"
   - Mô tả: "Phòng làm việc tầng 1"
   - Lưu
```

**3️⃣ Tạo Nhà Cung Cấp**

```
Menu → Tài sản → Cấu hình → Nhà cung cấp
→ Tạo mới:
   - Tên: "DELL Vietnam"
   - Địa chỉ: "Hà Nội"
   - Liên hệ: "0123456789"
   - Lưu
```

**4️⃣ Tạo Tài Sản**

```
Menu → Tài sản → Quản lý Tài sản
→ Tạo mới:
   - Tên tài sản: "Laptop Dell XPS 13"
   - Loại: Máy tính
   - Nhà cung cấp: DELL Vietnam
   - Số serial: SN123456
   - Ngày mua: 2025-01-01
   - Giá tiền mua: 25,000,000 VND
   - Vị trí: Phòng 101
   - Người quản lý: Nguyễn Văn A

   → Tab KHẤU HAO:
   - Phương pháp: Khấu hao đường thẳng
   - Số tháng khấu hao: 60 (5 năm)
   - TK Nguyên giá: 211 - Máy móc, thiết bị
   - TK Hao mòn: 214 - Hao mòn máy móc
   - TK Chi phí khấu hao: 627 - Chi phí sản xuất

   → Lưu
```

**5️⃣ Phiếu Mượn Tài Sản**

```
Menu → Tài sản → Phiếu mượn tài sản
→ Tạo mới:
   - Nhân viên mượn: Nguyễn Văn A
   - Tài sản mượn: Laptop Dell XPS 13
   - Thời gian mượn dự kiến: 2025-01-15
   - Thời gian trả dự kiến: 2025-02-15
   - Ghi chú: "Dùng cho đào tạo"
   → Lưu
   → Nhấn "Duyệt" (Approve)
   → Nhập ngày mượn thực tế
   → Nhấn "Hoàn thành"
```

**6️⃣ Lịch Sử Sử Dụng**

```
Menu → Tài sản → Lịch sử sử dụng tài sản
→ Xem các lần mượn/trả của tài sản
→ Hiển thị: Nhân viên, thời gian, ghi chú
```

**7️⃣ Khấu Hao Tự Động**

```
Menu → Tài sản → Khấu hao tài sản
→ Xem danh sách khấu hao hàng tháng
→ Thông tin: Tài sản, ngày tính, giá trị khấu hao
→ Trạng thái: Draft (nháp) → Được ghi nhận tự động
```

**8️⃣ Thanh Lý Tài Sản**

```
Menu → Tài sản → Thanh lý tài sản
→ Chọn tài sản → Nhấn "Thanh lý"
→ Nhập thông tin:
   - Ngày thanh lý: 2025-12-01
   - Giá trị thanh lý: 5,000,000 VND
   - Lý do: "Tài sản quá cũ, không sử dụng được"
   → Lưu
   → Nhấn "Xác nhận thanh lý"
→ Hệ thống tự động tạo bút toán kế toán
→ Tính lãi/lỗ thanh lý
```

**9️⃣ Kiểm Kê Tài Sản**

```
Menu → Tài sản → Phiếu kiểm kê
→ Tạo phiếu kiểm kê:
   - Tên phiếu: "Kiểm kê Q1/2025"
   - Ngày kiểm kê: 2025-03-31
   - Thêm các tài sản cần kiểm
   - Nhập trạng thái thực tế: Bình thường/Hỏng hóc/Mất
   → Lưu → Hoàn thành
```

---

### **MODULE 3: QUẢN LÝ KỂ TOÁN (tai_chinh_ke_toan)**

#### **Truy cập:**

Menu → Kế toán → Quản lý Kế toán

#### **Demo Flow:**

**1️⃣ Cấu Hình Tài Khoản Kế Toán**

```
Menu → Kế toán → Cấu hình → Tài khoản kế toán
→ Xem danh sách tài khoản mặc định:
   - 211: Máy móc, thiết bị
   - 214: Hao mòn máy móc, thiết bị
   - 121: Hàng tồn kho mua vào
   - 331: Phải trả cho nhà cung cấp
   - 627: Chi phí sản xuất
```

**2️⃣ Lập Hóa Đơn Mua**

```
Menu → Kế toán → Hóa đơn mua
→ Tạo mới:
   - Số chứng từ: Tự động (HDM-001)
   - Nhà cung cấp: DELL Vietnam
   - Ngày hóa đơn: 2025-01-01

   → Tab CHI TIẾT HÓNG ĐƠN:
   - Thêm dòng:
     • Tên sản phẩm: "Dell XPS 13"
     • Số lượng: 1
     • Đơn giá: 25,000,000 VND
     • Là tài sản cố định: ✓ Có
   - Thêm dòng:
     • Tên sản phẩm: "Chuột không dây"
     • Số lượng: 1
     • Đơn giá: 500,000 VND
     • Là tài sản cố định: ☐ Không

   → Lưu
   → Xem tự động tính:
     • Tổng tiền: 25,500,000 VND
     • Thuế (nếu có): Tùy theo loại hàng
     • Tổng cộng: Cập nhật tự động
```

**3️⃣ Tạo Bút Toán Kế Toán**

```
Menu → Kế toán → Bút toán kế toán
→ Tạo mới:
   - Số bút toán: Tự động (BT-001)
   - Diễn giải: "Mua máy tính từ DELL Vietnam"
   - Ngày bút toán: 2025-01-01

   → Tab CHI TIẾT:
   - Bên Nợ (Debit):
     • Tài khoản: 211 - Máy móc, thiết bị
     • Diễn giải: "Mua máy tính Dell XPS"
     • Số tiền nợ: 25,000,000 VND

   - Bên Có (Credit):
     • Tài khoản: 331 - Phải trả nhà cung cấp
     • Diễn giải: "Nợ DELL Vietnam"
     • Số tiền có: 25,000,000 VND

   → Lưu
   → Nhấn "Ghi sổ" (Post)
   → Bút toán được ghi nhận
```

**4️⃣ Sổ Chi Tiết**

```
Menu → Kế toán → Báo cáo → Sổ chi tiết
→ Chọn tài khoản: 211 - Máy móc, thiết bị
→ Xem:
   - Số dư đầu kỳ
   - Các bút toán nợ/có
   - Số dư cuối kỳ
   - Chi tiết từng giao dịch
```

**5️⃣ Sổ Cái**

```
Menu → Kế toán → Báo cáo → Sổ cái
→ Xem tóm tắt tất cả tài khoản:
   - Số dư nợ/có
   - Tổng nợ/có kỳ này
   - Số dư cuối kỳ
```

**6️⃣ Thuế Suất**

```
Menu → Kế toán → Cấu hình → Thuế suất
→ Xem/Tạo mới:
   - Tên: "GTGT 10%"
   - Tỷ lệ thuế: 10%
   - Tài khoản: 333 - Phải nộp thuế GTGT
```

---

## 💡 QUY TRÌNH DEMO HOÀN CHỈNH

### **Kịch Bản: Công ty mua một chiếc laptop**

**Bước 1: Chuẩn Bị DỮ LIỆU CƠ BẢN** (5 phút)

```
1. Tạo phòng ban "Kế Toán"
2. Tạo chức vụ "Kế Toán Viên"
3. Tạo nhân viên "Trần Thị B" (Kế toán viên)
4. Tạo loại tài sản "Máy tính"
5. Tạo vị trí "VP Tầng 2"
6. Tạo nhà cung cấp "ASUS Vietnam"
```

**Bước 2: PHÁT SINH TÀI SẢN** (3 phút)

```
1. Lập hóa đơn mua: ASUS Vivobook 15
   - Số lượng: 1
   - Giá: 20,000,000 VND
2. Xem hóa đơn được tạo thành công
```

**Bước 3: QUẢN LÝ TÀI SẢN** (3 phút)

```
1. Vào Menu Tài sản
2. Tạo tài sản mới từ hóa đơn
   - Loại: Máy tính
   - Nhà cung cấp: ASUS Vietnam
   - Khấu hao: 60 tháng (5 năm)
3. Lưu tài sản
```

**Bước 4: KHẤU HAO TỰ ĐỘNG** (3 phút)

```
1. Vào Menu Khấu hao
2. Tìm bản ghi khấu hao của laptop
3. Xem:
   - Giá nguyên: 20,000,000 VND
   - Khấu hao tháng: 333,333 VND
   - Giá trị còn lại
4. Nhấn "Ghi nhận" (nếu chưa ghi)
```

**Bước 5: KIỂM SỐ SÁCH KỌC TOÁN** (2 phút)

```
1. Vào Menu Sổ chi tiết
2. Chọn TK 211 (Máy móc)
3. Xem giao dịch mua:
   - Ghi nợ: 20,000,000 VND
   - Ghi có: Ghi trong TK 331 (Phải trả)
4. Chọn TK 214 (Hao mòn)
5. Xem ghi nhận khấu hao:
   - Ghi có: 333,333 VND/tháng
```

**Bước 6: THANH LÝ TÀI SẢN** (2 phút) - _Sau 5 năm hoặc tuỳ ý_

```
1. Vào Danh sách tài sản
2. Chọn laptop → Thanh lý
3. Nhập:
   - Ngày thanh lý: 2030-01-01
   - Giá bán: 2,000,000 VND
   - Lý do: "Tài sản cũ, thay mới"
4. Xác nhận
→ Hệ thống tự động:
   - Tính lỗ thanh lý: -18,000,000 VND
   - Tạo bút toán thanh lý
   - Cập nhật sổ kế toán
```

---

## 🎓 CÁC ĐẶC ĐIỂM CHÍNH CẦN DEMO

### **Tính Năng Nổi Bật:**

| Tính Năng               | Module            | Cách Demo                             |
| ----------------------- | ----------------- | ------------------------------------- |
| ✅ **Khấu hao tự động** | quan_ly_tai_san   | Tạo tài sản → Xem khấu hao hàng tháng |
| ✅ **Bút toán tự động** | quan_ly_tai_san   | Thanh lý tài sản → Xem bút toán tạo   |
| ✅ **Quản lý mượn/trả** | quan_ly_tai_san   | Tạo phiếu mượn → Theo dõi lịch sử     |
| ✅ **Kiểm kê tài sản**  | quan_ly_tai_san   | Tạo phiếu kiểm kê → So sánh thực tế   |
| ✅ **Sổ kế toán**       | tai_chinh_ke_toan | Xem sổ chi tiết, sổ cái               |
| ✅ **Quản lý nhân sự**  | nhan_su           | Tạo nhân viên, chứng chỉ              |

---

## ⚙️ TÍNH NĂNG KỸ THUẬT

### **Computed Fields (Tính Toán Tự Động)**

```
Giá trị còn lại = Giá mua - Khấu hao lũy kế
Tỷ lệ khấu hao = (Khấu hao lũy kế / Giá mua) × 100%
Khấu hao hàng tháng = Giá mua / Số tháng khấu hao
```

### **Workflows (Quy Trình)**

```
Phiếu Mượn:     Draft → Duyệt → Hoàn thành → Hủy
Thanh Lý:       Draft → Xác nhận → Hoàn thành
Hóa Đơn:        Nháp → Xác nhận → Thanh toán
```

---

## 🔍 MẚO LẠI KHI CÓ LỖI

### **Lỗi: Field không tồn tại**

→ Kiểm tra model có kế thừa đúng base model không

### **Lỗi: Dependency không tìm thấy**

→ Cài đặt module nhan_su trước quan_ly_tai_san

### **Khấu hao không hiển thị**

→ Nhập Ngày bắt đầu khấu hao trong tài sản

### **Bút toán không tự động tạo**

→ Kiểm tra tài sản có setting TK kế toán không

---

## 📞 LIÊN HỆ & HỖ TRỢ

- **Cơ sở dữ liệu:** odoo_hieu_test
- **Database User:** admin / admin
- **Port Odoo:** 8069
- **Config File:** odoo.conf
- **Log File:** /var/log/odoo/

---

**Chúc bạn demo thành công! 🎉**
