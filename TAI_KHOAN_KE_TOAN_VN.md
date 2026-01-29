# HỆ THỐNG TÀI KHOẢN KẾ TOÁN VIỆT NAM - DÀNH CHO MODULE

## Tài khoản liên quan đến Tài sản cố định & Khấu hao

### Tài khoản CẤP 1 (Tổng hợp)

```xml
<record id="tk_1_tai_san_ngan_han" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">1</field>
    <field name="ten_tai_khoan">TÀI SẢN NGẮN HẠN</field>
    <field name="loai_tai_khoan">tai_san</field>
    <field name="la_tai_khoan_tong_hop">True</field>
</record>

<record id="tk_2_tai_san_dai_han" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">2</field>
    <field name="ten_tai_khoan">TÀI SẢN DÀI HẠN</field>
    <field name="loai_tai_khoan">tai_san</field>
    <field name="la_tai_khoan_tong_hop">True</field>
</record>

<record id="tk_3_no_phai_tra" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">3</field>
    <field name="ten_tai_khoan">NỢ PHẢI TRẢ</field>
    <field name="loai_tai_khoan">no_phai_tra</field>
    <field name="la_tai_khoan_tong_hop">True</field>
</record>

<record id="tk_6_chi_phi" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">6</field>
    <field name="ten_tai_khoan">CHI PHÍ SẢN XUẤT KINH DOANH</field>
    <field name="loai_tai_khoan">chi_phi</field>
    <field name="la_tai_khoan_tong_hop">True</field>
</record>

<record id="tk_7_thu_nhap_khac" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">7</field>
    <field name="ten_tai_khoan">THU NHẬP KHÁC</field>
    <field name="loai_tai_khoan">doanh_thu</field>
    <field name="la_tai_khoan_tong_hop">True</field>
</record>

<record id="tk_8_chi_phi_khac" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">8</field>
    <field name="ten_tai_khoan">CHI PHÍ KHÁC</field>
    <field name="loai_tai_khoan">chi_phi</field>
    <field name="la_tai_khoan_tong_hop">True</field>
</record>
```

---

## Tài khoản CẤP 2 & 3 (Chi tiết)

### NHÓM 11: TIỀN MẶT & NGÂN HÀNG

```xml
<!-- TK 111: Tiền mặt -->
<record id="tk_111" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">111</field>
    <field name="ten_tai_khoan">Tiền mặt</field>
    <field name="loai_tai_khoan">tai_san</field>
    <field name="tai_khoan_cha_id" ref="tk_1_tai_san_ngan_han"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>

<!-- TK 112: Tiền gửi ngân hàng -->
<record id="tk_112" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">112</field>
    <field name="ten_tai_khoan">Tiền gửi ngân hàng</field>
    <field name="loai_tai_khoan">tai_san</field>
    <field name="tai_khoan_cha_id" ref="tk_1_tai_san_ngan_han"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>
```

### NHÓM 21: TÀI SẢN CỐ ĐỊNH

```xml
<!-- TK 211: Tài sản cố định hữu hình -->
<record id="tk_211" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">211</field>
    <field name="ten_tai_khoan">Tài sản cố định hữu hình</field>
    <field name="loai_tai_khoan">tai_san</field>
    <field name="tai_khoan_cha_id" ref="tk_2_tai_san_dai_han"/>
    <field name="la_tai_khoan_tong_hop">True</field>
</record>

<!-- TK 2111: Nhà cửa, vật kiến trúc -->
<record id="tk_2111" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">2111</field>
    <field name="ten_tai_khoan">Nhà cửa, vật kiến trúc</field>
    <field name="loai_tai_khoan">tai_san</field>
    <field name="tai_khoan_cha_id" ref="tk_211"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>

<!-- TK 2112: Máy móc, thiết bị -->
<record id="tk_2112" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">2112</field>
    <field name="ten_tai_khoan">Máy móc, thiết bị</field>
    <field name="loai_tai_khoan">tai_san</field>
    <field name="tai_khoan_cha_id" ref="tk_211"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>

<!-- TK 2113: Phương tiện vận tải, truyền dẫn -->
<record id="tk_2113" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">2113</field>
    <field name="ten_tai_khoan">Phương tiện vận tải, truyền dẫn</field>
    <field name="loai_tai_khoan">tai_san</field>
    <field name="tai_khoan_cha_id" ref="tk_211"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>

<!-- TK 2114: Thiết bị, dụng cụ quản lý -->
<record id="tk_2114" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">2114</field>
    <field name="ten_tai_khoan">Thiết bị, dụng cụ quản lý</field>
    <field name="loai_tai_khoan">tai_san</field>
    <field name="tai_khoan_cha_id" ref="tk_211"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>

<!-- TK 213: Tài sản cố định vô hình -->
<record id="tk_213" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">213</field>
    <field name="ten_tai_khoan">Tài sản cố định vô hình</field>
    <field name="loai_tai_khoan">tai_san</field>
    <field name="tai_khoan_cha_id" ref="tk_2_tai_san_dai_han"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>
```

### NHÓM 33: NỢ PHẢI TRẢ

```xml
<!-- TK 331: Phải trả cho người bán -->
<record id="tk_331" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">331</field>
    <field name="ten_tai_khoan">Phải trả cho người bán</field>
    <field name="loai_tai_khoan">no_phai_tra</field>
    <field name="tai_khoan_cha_id" ref="tk_3_no_phai_tra"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>

<!-- TK 3331: Thuế GTGT phải nộp -->
<record id="tk_3331" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">3331</field>
    <field name="ten_tai_khoan">Thuế GTGT được khấu trừ</field>
    <field name="loai_tai_khoan">tai_san</field>
    <field name="tai_khoan_cha_id" ref="tk_1_tai_san_ngan_han"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>

<!-- TK 334: Phải trả người lao động -->
<record id="tk_334_no_phai_tra" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">334</field>
    <field name="ten_tai_khoan">Phải trả người lao động</field>
    <field name="loai_tai_khoan">no_phai_tra</field>
    <field name="tai_khoan_cha_id" ref="tk_3_no_phai_tra"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>
```

### NHÓM 214: HAO MÒN TÀI SẢN CỐ ĐỊNH (Tài khoản ĐIỀU CHỈNH)

```xml
<!-- TK 214: Hao mòn TSCĐ hữu hình -->
<record id="tk_214" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">214</field>
    <field name="ten_tai_khoan">Hao mòn TSCĐ hữu hình</field>
    <field name="loai_tai_khoan">no_phai_tra</field>
    <field name="tai_khoan_cha_id" ref="tk_2_tai_san_dai_han"/>
    <field name="la_tai_khoan_tong_hop">False</field>
    <!-- Lưu ý: TK này có tính chất đặc biệt - giảm tài sản nhưng ghi bên Có -->
</record>
```

---

## NHÓM 64: CHI PHÍ

```xml
<!-- TK 642: Chi phí khấu hao TSCĐ -->
<record id="tk_642" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">642</field>
    <field name="ten_tai_khoan">Chi phí khấu hao TSCĐ</field>
    <field name="loai_tai_khoan">chi_phi</field>
    <field name="tai_khoan_cha_id" ref="tk_6_chi_phi"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>

<!-- TK 627: Chi phí sản xuất chung -->
<record id="tk_627" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">627</field>
    <field name="ten_tai_khoan">Chi phí sản xuất chung</field>
    <field name="loai_tai_khoan">chi_phi</field>
    <field name="tai_khoan_cha_id" ref="tk_6_chi_phi"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>

<!-- TK 641: Chi phí bán hàng -->
<record id="tk_641" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">641</field>
    <field name="ten_tai_khoan">Chi phí bán hàng</field>
    <field name="loai_tai_khoan">chi_phi</field>
    <field name="tai_khoan_cha_id" ref="tk_6_chi_phi"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>
```

---

## NHÓM 71 & 81: THU NHẬP/CHI PHÍ KHÁC (Thanh lý)

```xml
<!-- TK 711: Thu nhập khác -->
<record id="tk_711" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">711</field>
    <field name="ten_tai_khoan">Thu nhập khác</field>
    <field name="loai_tai_khoan">doanh_thu</field>
    <field name="tai_khoan_cha_id" ref="tk_7_thu_nhap_khac"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>

<!-- TK 811: Chi phí khác -->
<record id="tk_811" model="tai_khoan_ke_toan">
    <field name="ma_tai_khoan">811</field>
    <field name="ten_tai_khoan">Chi phí khác</field>
    <field name="loai_tai_khoan">chi_phi</field>
    <field name="tai_khoan_cha_id" ref="tk_8_chi_phi_khac"/>
    <field name="la_tai_khoan_tong_hop">False</field>
</record>
```

---

## CÁC BÚT TOÁN ĐIỂN HÌNH

### 1. MUA TÀI SẢN CỐ ĐỊNH (Chưa thanh toán)

```
Nợ TK 211 (TSCĐ):                  30,000,000
Nợ TK 3331 (Thuế GTGT):              3,000,000
    Có TK 331 (Phải trả NCC):       33,000,000
Diễn giải: Mua laptop theo HĐ HDM/2024/0001
```

### 2. THANH TOÁN NHÀ CUNG CẤP

```
Nợ TK 331 (Phải trả NCC):          33,000,000
    Có TK 111 (Tiền mặt):           33,000,000
Diễn giải: Thanh toán tiền mua laptop
```

### 3. KHẤU HAO HÀNG THÁNG

```
Nợ TK 642 (Chi phí KH):               833,333
    Có TK 214 (Hao mòn TSCĐ):          833,333
Diễn giải: Khấu hao tháng 01/2024 - TS/2024/0001
```

### 4. THANH LÝ TÀI SẢN (Có lãi)

**Tình huống**: Nguyên giá 30tr, KH lũy kế 25tr (còn lại 5tr), bán 6tr

```
Nợ TK 214 (Hao mòn lũy kế):        25,000,000
Nợ TK 111 (Tiền thu):               6,000,000
    Có TK 211 (TSCĐ):               30,000,000
    Có TK 711 (Lãi thanh lý):        1,000,000
Diễn giải: Thanh lý TS/2024/0001
```

### 5. THANH LÝ TÀI SẢN (Có lỗ)

**Tình huống**: Nguyên giá 30tr, KH lũy kế 20tr (còn lại 10tr), bán 8tr

```
Nợ TK 214 (Hao mòn lũy kế):        20,000,000
Nợ TK 111 (Tiền thu):               8,000,000
Nợ TK 811 (Lỗ thanh lý):            2,000,000
    Có TK 211 (TSCĐ):               30,000,000
Diễn giải: Thanh lý TS/2024/0001
```

---

## LƯU Ý QUAN TRỌNG

1. **TK 214 (Hao mòn TSCĐ)**:
   - Là tài khoản điều chỉnh (contra account)
   - Tăng bên Có (khi ghi nhận khấu hao)
   - Giảm bên Nợ (khi thanh lý)
   - Công thức: Giá trị còn lại = TK 211 - TK 214

2. **Phân loại chi tiết TK 211**:
   - 2111: Nhà cửa (KH 25 năm = 300 tháng)
   - 2112: Máy móc (KH 10 năm = 120 tháng)
   - 2113: Xe ô tô (KH 8 năm = 96 tháng)
   - 2114: Thiết bị văn phòng (KH 5 năm = 60 tháng)

3. **Thuế GTGT (TK 3331)**:
   - Được khấu trừ khi mua hàng hóa, dịch vụ
   - Bên Nợ khi phát sinh
   - Sau đó khấu trừ với thuế đầu ra (TK 33311)

---

## FILE DATA MẪU: `data/tai_khoan_ke_toan_data.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
        <!-- Copy tất cả các record ở trên vào đây -->
        <!-- ... -->
        
    </data>
</odoo>
```

**Gợi ý**: Set `noupdate="1"` để tránh ghi đè khi upgrade module

---

Hy vọng file này giúp ích cho việc tạo data mẫu! 🚀
