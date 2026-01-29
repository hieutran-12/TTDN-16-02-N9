# 📊 DỰ ÁN ODOO 15 - HỆ THỐNG KỂ TOÁN & QUẢN LÝ TÀI SẢN

## 🏗️ KIẾN TRÚC TỔNG QUÁT

```mermaid
graph TB
    subgraph ODOO["🚀 ODOO 15 Server"]
        subgraph TAI_CHINH["📊 Module: Kế toán"]
            direction LR
            TK["Tài khoản<br/>Kế toán"]
            BT["Bút toán"]
            HD["Hóa đơn<br/>Mua"]
            CN["Công nợ<br/>Mua"]
            SC["Sổ Cái"]
        end

        subgraph QUAN_LY["🏢 Module: Quản lý Tài sản"]
            direction LR
            TS["Tài sản"]
            KH["Khách hàng"]
            BH["Bảo hành"]
        end
    end

    DB[("💾 PostgreSQL<br/>Database")]
    REDIS[("⚡ Redis<br/>Cache")]

    ODOO --> DB
    ODOO --> REDIS
```

---

## 🔗 SƠ ĐỒ LIÊN KẾT DỮ LIỆU

```mermaid
graph LR
    subgraph TAI_CHINH["📊 KỂ TOÁN (tai_chinh_ke_toan)"]
        TK["`📊 Tài khoản
        (Chart of Accounts)
        - 1000: Tài sản
        - 2000: Nợ phải trả
        - 6000: Chi phí
        - 6200: Khấu hao`"]

        BT["`📝 Bút toán
        (Journal Entry)
        - Trạng thái: nhập/ghi_sổ
        - Auto-post khi xác nhận`"]

        CTB["`📄 Chi tiết Bút toán
        (Journal Line)
        - Debit/Credit
        - Tham chiếu Tài khoản`"]

        HD["`🧾 Hóa đơn Mua
        (Invoice)
        - Nhà cung cấp
        - Chi tiết hàng hóa
        - Auto-create BT`"]

        CN["`💳 Công nợ Mua
        (Payables)
        - Số tiền nợ
        - Ngày thanh toán
        - Chi tiết thanh toán`"]

        CTHD["`📋 Chi tiết Hóa đơn
        (Invoice Line)
        - Mặt hàng
        - Giá, số lượng`"]
    end

    subgraph QUAN_LY["🏢 QUẢN LÝ TÀI SẢN (quan_ly_tai_san)"]
        TS["`🏗️ Tài sản
        (Asset)
        - Giá mua
        - Ngày mua
        - Liên kết Hóa đơn
        - Khấu hao 10%/năm`"]

        KH["`👥 Khách hàng/NCC
        (Partner)
        - Tên, địa chỉ
        - Loại KH/NCC`"]
    end

    %% Relationships
    TK -->|"1:N"| BT
    BT -->|"1:N"| CTB
    CTB -->|"N:1"| TK

    HD -->|"1:N"| CTHD
    HD -->|"1:1"| BT
    HD -->|"1:1"| CN

    HD -.->|"Many2one<br/>hoa_don_mua_id"| TS
    HD -->|"N:1"| KH

    TS -.->|"Auto-generate<br/>Depreciation Entry"| BT

    style TAI_CHINH fill:#e1f5ff
    style QUAN_LY fill:#fff3e0
```

---

## 🔄 QUY TRÌNH: HÓA ĐƠN → BỤT TOÁN (INVOICE WORKFLOW)

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant HD as 🧾 Hóa đơn Mua<br/>(state=nhập)
    participant BT as 📝 Bút toán
    participant CN as 💳 Công nợ
    participant SC as 📑 Sổ Cái

    User->>HD: 1️⃣ Tạo hóa đơn mới<br/>- Nhập nhà cung cấp<br/>- Nhập chi tiết hàng hóa
    HD-->>User: ✓ Hóa đơn lưu (state=nhập)

    User->>HD: 2️⃣ Nhấn nút "Xác nhận"

    activate HD
    HD->>BT: 3️⃣ Auto-create Bút toán
    activate BT
    BT->>BT: - Dòng Debit: Tài sản/Chi phí (1000 hoặc 6000)
    BT->>BT: - Dòng Credit: Nợ phải trả (2000)
    BT-->>HD: ✓ Bút toán tạo xong
    deactivate BT

    HD->>CN: 4️⃣ Auto-create Công nợ
    activate CN
    CN->>CN: - Ghi lại: Số tiền, NCC, ngày TT
    CN-->>HD: ✓ Công nợ tạo xong
    deactivate CN

    HD->>BT: 5️⃣ Auto-post Bút toán
    activate BT
    BT->>SC: Ghi vào Sổ cái
    BT-->>HD: ✓ Bút toán đã ghi sổ
    deactivate BT

    HD-->>User: ✅ Hoàn thành (state=xác_nhận)
    deactivate HD

    User->>SC: 6️⃣ Xem Sổ Cái
    SC-->>User: Hiển thị 2 dòng vừa tạo
```

---

## 📈 QUY TRÌNH: KHẤU HAO TÀI SẢN (DEPRECIATION WORKFLOW)

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant TS as 🏗️ Tài sản<br/>(Asset)
    participant HD as 🧾 Hóa đơn<br/>(Linked)
    participant BT as 📝 Bút toán<br/>Khấu hao
    participant SC as 📑 Sổ Cái

    User->>TS: 1️⃣ Tạo Tài sản mới
    TS-->>TS: - Chọn Hóa đơn<br/>- Nhập giá mua

    TS->>HD: Liên kết Hóa đơn
    HD-->>TS: ✓ Linked (many2one)

    User->>TS: 2️⃣ Nhấn "Tạo Bút toán Khấu hao"<br/>(Năm sau)

    activate TS
    TS->>BT: 3️⃣ Auto-create Bút toán Khấu hao
    activate BT
    BT->>BT: Tính: Khấu hao 10% = Giá mua × 10%
    BT->>BT: - Dòng Debit: Chi phí khấu hao (6200)
    BT->>BT: - Dòng Credit: Tích lũy khấu hao (1100)
    BT->>SC: Ghi vào Sổ Cái
    BT-->>TS: ✓ Bút toán ghi sổ
    deactivate BT
    TS-->>User: ✅ Hoàn thành
    deactivate TS
```

---

## 📋 DANH SÁCH MODELS & TRƯỜNG DỮ LIỆU

### **Module: Kế toán (tai_chinh_ke_toan)**

| Model                      | Trường chính                                                            | Mối liên kết                 |
| -------------------------- | ----------------------------------------------------------------------- | ---------------------------- |
| **tai_khoan_ke_toan**      | code, name, parent_id                                                   | Phân cấp (1:N)               |
| **but_toan_ke_toan**       | name, ngay, trang_thai, but_toan_id                                     | 1:N chi tiết                 |
| **chi_tiet_but_toan**      | account_id, debit, credit, but_toan_id                                  | N:1 bút toán                 |
| **hoa_don_mua**            | ma_HD, ngay, nha_cung_cap_id, chi_tiet_ids, but_toan_id, cong_no_mua_id | 1:N chi tiết, 1:1 BT, 1:1 CN |
| **chi_tiet_hoa_don_mua**   | ten_hang, gia, so_luong, thue_id, hoa_don_id                            | N:1 hóa đơn                  |
| **cong_no_mua**            | hoa_don_id, so_tien, nha_cung_cap_id, ngay_thanh_toan                   | 1:1 HD                       |
| **chi_tiet_thanh_toan_no** | phuong_thuc, so_tien, cong_no_id                                        | N:1 CN                       |
| **thue**                   | ten, ty_le                                                              | -                            |
| **so_cai** (VIEW)          | tai_khoan, debit, credit, so_du                                         | SQL View                     |
| **so_chi_tiet** (VIEW)     | tai_khoan, chi_tiet_but_toan, debit, credit                             | SQL View                     |

### **Module: Quản lý Tài sản (quan_ly_tai_san)**

| Model             | Trường chính                                     | Mối liên kết |
| ----------------- | ------------------------------------------------ | ------------ |
| **tai_san**       | ten, gia_mua, ngay_mua, hoa_don_mua_id, khau_hao | N:1 hóa đơn  |
| **khach_hang**    | ten, dia_chi, loai                               | -            |
| **bao_hanh**      | tai_san_id, han_sd, ngay_ket_thuc                | N:1 tài sản  |
| + 12+ models khác | ...                                              | ...          |

---

## 🎯 TÍNH NĂNG CHÍNH

### ✅ Đã hoàn thành:

```mermaid
graph LR
    A["✅ Quản lý Tài khoản"]
    B["✅ Quản lý Bút toán"]
    C["✅ Quản lý Hóa đơn"]
    D["✅ Auto-create Bút toán<br/>khi xác nhận HD"]
    E["✅ Auto-post Bút toán<br/>vào Sổ Cái"]
    F["✅ Liên kết HD ↔ TS"]
    G["✅ Auto-generate Khấu hao"]
    H["✅ Quản lý Công nợ"]
    I["✅ Sổ Cái & Sổ Chi tiết<br/>SQL View"]

    style A fill:#c8e6c9
    style B fill:#c8e6c9
    style C fill:#c8e6c9
    style D fill:#c8e6c9
    style E fill:#c8e6c9
    style F fill:#c8e6c9
    style G fill:#c8e6c9
    style H fill:#c8e6c9
    style I fill:#c8e6c9
```

---

## 🔌 CÔNG NGHỆ SỬ DỤNG

```mermaid
graph LR
    ODOO["🚀 Odoo 15.0<br/>(Enterprise)"]
    PYTHON["🐍 Python 3.10+<br/>(Backend)"]
    PG["💾 PostgreSQL 12+<br/>(Database)"]
    REDIS["⚡ Redis 6+<br/>(Cache)"]
    DOCKER["🐳 Docker<br/>(Containerization)"]
    XML["📝 XML<br/>(Views/Data)"]

    ODOO --> PYTHON
    ODOO --> PG
    ODOO --> REDIS
    ODOO --> XML
    PYTHON --> DOCKER

    style ODOO fill:#FF6B6B
    style PYTHON fill:#4A90E2
    style PG fill:#336791
    style REDIS fill:#DC382D
    style DOCKER fill:#2496ED
    style XML fill:#90EE90
```

---

## 📁 CẤU TRÚC THƯ MỤC

```
TTDN-15-05-N1/
├── addons/
│   ├── tai_chinh_ke_toan/          # 📊 Module Kế toán
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── tai_khoan_ke_toan.py
│   │   │   ├── but_toan_ke_toan.py
│   │   │   ├── chi_tiet_but_toan.py
│   │   │   ├── hoa_don_mua.py       # ⭐ Hóa đơn với auto-BT
│   │   │   ├── cong_no_mua.py       # ⭐ Công nợ
│   │   │   ├── chi_tiet_hoa_don_mua.py
│   │   │   ├── thue.py
│   │   │   ├── so_cai.py            # SQL View
│   │   │   └── so_chi_tiet.py       # SQL View
│   │   ├── views/
│   │   │   ├── hoa_don_mua_form.xml # ⭐ Form + Buttons
│   │   │   ├── but_toan_ke_toan.xml
│   │   │   ├── actions.xml
│   │   │   ├── menu.xml
│   │   │   └── ...
│   │   ├── data/
│   │   │   ├── tai_khoan_default.xml # 5 default accounts
│   │   │   └── ...
│   │   ├── security/
│   │   │   └── ir.model.access.csv
│   │   ├── __manifest__.py
│   │   └── __init__.py
│   │
│   └── quan_ly_tai_san/             # 🏢 Module Quản lý Tài sản
│       ├── models/
│       │   ├── tai_san.py           # ⭐ hoa_don_mua_id + Khấu hao
│       │   └── ...
│       ├── views/
│       └── ...
│
├── odoo-bin                         # Odoo executable
├── odoo.conf                        # Config
├── docker-compose.yml
└── README.md
```

---

## 🚀 HƯỚNG PHÁT TRIỂN

```mermaid
graph LR
    A["✅ Phase 1:<br/>Core Module"]
    B["✅ Phase 2:<br/>Integration"]
    C["⏳ Phase 3:<br/>View & UI"]
    D["⏳ Phase 4:<br/>Testing"]
    E["⏳ Phase 5:<br/>Production"]

    A --> B --> C --> D --> E

    style A fill:#90EE90
    style B fill:#90EE90
    style C fill:#FFD700
    style D fill:#FFD700
    style E fill:#FFD700
```

---

## 📞 LIÊN HỆ & THÔNG TIN

**Dự án:** Odoo 15 - Hệ thống Kế toán & Quản lý Tài sản  
**Ngôn ngữ:** Vietnamese (Tiếng Việt)  
**Cơ sở dữ liệu:** PostgreSQL 12+  
**Phiên bản Odoo:** 15.0  
**Trạng thái:** Đang phát triển 🔨
