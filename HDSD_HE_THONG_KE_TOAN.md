# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG KẾ TOÁN

## 📋 TỔNG QUAN HỆ THỐNG

Hệ thống kế toán tích hợp các chức năng:

- Quản lý hóa đơn mua hàng
- Tự động sinh bút toán kế toán
- Tự động tạo công nợ phải trả
- Tự động ghi sổ cái và sổ chi tiết
- Quản lý khấu hao tài sản
- Thanh lý tài sản cố định

---

## 🔍 KHÁI NIỆM CÁC CHỨNG CHỈ / SỔ SÁCH

### 1. **Sổ Cái (so_cai)**

- **Định nghĩa**: Sổ cái tổng hợp - ghi lại tổng nợ/có của mỗi tài khoản theo tháng
- **Tự động**: ✅ **CÓ** - Tự động cập nhật khi xác nhận hóa đơn
- **Cách xem**:
  - Menu: Kế toán > Báo cáo > Sổ cái
  - Hiển thị: Bảng pivot theo tài khoản và tháng
  - Cột: Nợ, Có (tính lũy tính)

### 2. **Sổ Chi Tiết (so_chi_tiet)**

- **Định nghĩa**: Chi tiết từng bút toán - ghi lại từng dòng chi tiết theo bút toán
- **Tự động**: ✅ **CÓ** - Tự động sinh từ chi tiết hóa đơn
- **Cách xem**:
  - Menu: Kế toán > Báo cáo > Sổ chi tiết
  - Hiển thị: Danh sách chi tiết từng dòng
  - Cột: Ngày, Bút toán, Tài khoản, Diễn giải, Nợ, Có, Đối tác

### 3. **Bút Toán Kế Toán (but_toan_ke_toan)**

- **Định nghĩa**: Ghi sổ - bút toán kép (nợ/có) từ một nghiệp vụ
- **Tự động**: ✅ **CÓ** - Sinh tự động từ hóa đơn mua
- **Trạng thái**:
  - "Nháp" → "Ghi sổ" (tự động khi xác nhận hóa đơn)

---

## 📊 QUY TRÌNH NGHIỆP VỤ

### **BƯỚC 1: Nhập Hóa Đơn Mua**

**Vị trí**: Kế toán > Nghiệp vụ > Hóa đơn mua

**Thao tác**:

1. Nhấn nút **Tạo** (Create)
2. Điền thông tin:
   - **Mã hóa đơn NCC**: Mã số từ nhà cung cấp
   - **Ngày hóa đơn**: Ngày trên hóa đơn
   - **Nhà cung cấp**: Chọn từ danh sách
   - **Nhân viên thực hiện**: Chọn nhân viên kế toán

3. **Thêm chi tiết hóa đơn**:
   - Nhấn "Thêm một dòng" trong tab "Chi tiết hóa đơn"
   - Điền:
     - **Tên sản phẩm**: Tên hàng hóa/dịch vụ
     - **Số lượng**: Số lượng mua
     - **Đơn giá**: Giá đơn vị (chưa thuế)
     - **Thuế suất**: Chọn thuế GTGT (nếu có)
     - **Là tài sản**: ☑️ Đánh dấu nếu là tài sản cố định

4. **Nếu là tài sản cố định**:
   - Đánh dấu ☑️ **"Có phát sinh tài sản"** ở phần thông tin chính

5. **Lưu và Xác nhận**:
   - Nhấn **"Xác nhận"** → Tự động:
     - ✅ Sinh bút toán kế toán
     - ✅ Sinh công nợ phải trả
     - ✅ Ghi sổ cái & sổ chi tiết
     - ✅ Nếu có tài sản → đánh dấu "Chờ tạo"

---

### **BƯỚC 2: Quản Lý Tài Sản Cố Định**

**Vị trí**: Quản lý tài sản > **Tài sản chờ tạo**

**Thao tác**:

1. Vào menu "Tài sản chờ tạo" (chỉ hiện hóa đơn có phát sinh tài sản)
2. Chọn hóa đơn cần tạo tài sản
3. Nhấn nút **"✨ Tạo tài sản"**
4. System tự động điền:
   - Mã tài sản (tự sinh)
   - Tên tài sản (từ hóa đơn)
   - Giá tài sản (tổng tiền hóa đơn)
   - Ngày mua (từ hóa đơn)
   - Nhà cung cấp
5. **Bạn cần chọn**:
   - **Loại tài sản**: Máy móc, Phương tiện, Xây dựng, etc.
   - **Người quản lý**: Nhân viên chịu trách nhiệm
6. **Lưu** → Hóa đơn chuyển sang trạng thái "Đã tạo"

---

### **BƯỚC 3: Khấu Hao Tài Sản (Tự động hàng tháng)**

**Vị trí**: Kế toán > Nghiệp vụ > Khấu hao tài sản

**Tự động**: ✅ **Cron chạy hàng tháng**

- Tính khấu hao cho tất cả tài sản đang sử dụng
- Sinh tự động bút toán khấu hao
- Ghi sổ tự động

**Xem chi tiết**:

1. Menu: Kế toán > Nghiệp vụ > Khấu hao tài sản
2. Hiển thị: Danh sách khấu hao tháng này
3. Bao gồm: Tài sản, Tháng, Năm, Tiền khấu hao, Bút toán

---

### **BƯỚC 4: Thanh Lý Tài Sản**

**Vị trí**: Kế toán > Nghiệp vụ > Thanh lý tài sản

**Thao tác** (khi tài sản hết dùng):

1. Nhấn **Tạo**
2. Chọn **Tài sản** cần thanh lý
3. Điền:
   - **Giá bán**: Giá bán khi thanh lý
   - **Ngày thanh lý**: Ngày thanh lý
4. System tự động:
   - Tính lợi/lỗ thanh lý
   - Sinh bút toán thanh lý (xóa giá trị còn lại)
   - Ghi sổ

---

## 📈 QUYẾT TOÁN CUỐI KỲ

### **Báo Cáo Sổ Cái**

- **Menu**: Kế toán > Báo cáo > Sổ cái
- **Xem**: Tổng nợ/có theo tài khoản, theo tháng

### **Báo Cáo Sổ Chi Tiết**

- **Menu**: Kế toán > Báo cáo > Sổ chi tiết
- **Xem**: Chi tiết từng bút toán
- **Lọc**: Theo tài khoản, đối tác, tháng

---

## 🎯 VÍ DỤ THỰC TẾ

### **Ví dụ 1: Mua hàng tính khấu hao**

```
1. Nhập hóa đơn:
   - Mã HĐ: HĐ001
   - NCC: Công ty XYZ
   - Ngày: 01/01/2026
   - Chi tiết:
     ├─ Máy móc: 100,000,000 VNĐ (Đánh dấu "Là tài sản")
     └─ Thuế GTGT 10%: 10,000,000 VNĐ
   - Đánh dấu: ☑️ "Có phát sinh tài sản"

2. Xác nhận hóa đơn → Tự động:
   - Sinh bút toán: Nợ 1110 (Tài sản), Có 3311 (Phải trả)
   - Ghi sổ: Cập nhật Sổ cái, Sổ chi tiết
   - Trạng thái: "Chờ tạo tài sản"

3. Tạo tài sản từ hóa đơn:
   - Vào "Tài sản chờ tạo"
   - Nhấn "Tạo tài sản" → Chọn loại "Máy móc"
   - Lưu → Trạng thái: "Đã tạo"

4. Tháng sau: Tính khấu hao
   - Cron tự động tạo: Khấu hao = 100,000,000 / 60 tháng = 1,666,667/tháng
   - Sinh bút toán khấu hao: Nợ 6421 (Chi khấu hao), Có 1111 (Khấu hao tích lũy)
   - Ghi sổ tự động
```

### **Ví dụ 2: Mua hàng tiêu dùng (không tài sản)**

```
1. Nhập hóa đơn:
   - Mã HĐ: HĐ002
   - NCC: Cửa hàng ABC
   - Ngày: 05/01/2026
   - Chi tiết:
     ├─ Giấy A4: 1,000,000 VNĐ
     ├─ Bút viết: 500,000 VNĐ
     └─ Thuế GTGT: 150,000 VNĐ
   - ❌ KHÔNG đánh dấu "Có phát sinh tài sản"

2. Xác nhận → Tự động:
   - Sinh bút toán: Nợ 6411 (Chi phí), Có 3311 (Phải trả)
   - Ghi sổ tự động
   - ✅ HOÀN THÀNH (không cần tạo tài sản)
```

---

## ⚙️ CẤU HÌNH BAN ĐẦU (Cần làm 1 lần)

### **1. Tài Khoản Kế Toán** (Menu: Kế toán > Danh mục > Tài khoản kế toán)

Cần tạo các TK cơ bản:

- **1110**: Tiền mặt
- **1130**: Tiền gửi
- **1210**: Hàng tồn kho
- **1310**: Tài sản cố định
- **1311**: Khấu hao tích lũy
- **3311**: Phải trả NCC
- **6411**: Chi phí hàng bán
- **6421**: Chi khấu hao
- **6431**: Chi thanh lý tài sản

### **2. Loại Tài Sản** (Menu: Quản lý tài sản > Danh mục > Loại tài sản)

- Máy móc
- Phương tiện
- Xây dựng
- Thiết bị
- etc.

### **3. Thuế Suất** (Menu: Kế toán > Danh mục > Thuế suất)

- 0% - Miễn thuế
- 5% - Thuế suất thấp
- 10% - Thuế suất chuẩn

---

## ❓ FAQ (Câu hỏi thường gặp)

**Q: Làm sao để biết hóa đơn nào chưa xác nhận?**
A: Vào "Hóa đơn mua" → Lọc "Nháp" → Danh sách chưa xác nhận

**Q: Sao bút toán không sinh tự động?**
A: Kiểm tra: Hóa đơn có ở trạng thái "Xác nhận" không? Quyền truy cập có được không?

**Q: Có thể sửa lại bút toán sau khi xác nhận không?**
A: Không được. Phải hủy hóa đơn (sẽ xóa bút toán), sửa lại, rồi xác nhận lại.

**Q: Khấu hao tính như thế nào?**
A: Tuyến tính: Giá tài sản / Năm sử dụng / 12 tháng

**Q: Tài sản thanh lý, bút toán ghi thế nào?**
A:

- Nợ 1111 (Khấu hao tích lũy) = Tổng khấu hao
- Nợ 1121 (Lợi lỗ thanh lý) = Lợi/lỗ
- Có 1310 (Tài sản cố định) = Giá gốc

---

## 📞 LIÊN HỆ HỖTRỢ

Nếu có vấn đề, vui lòng kiểm tra:

1. Quyền truy cập (Security)
2. Cài đặt tài khoản mặc định
3. Cơ sở dữ liệu (Database)

---

**Phiên bản**: 15.0.1.0.0
**Ngày cập nhật**: 29/01/2026
**Tác giả**: Hieu
