# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KhauHao(models.Model):
    _name = 'khau_hao'
    _description = 'Khấu hao tài sản'
    _order = 'nam desc, thang desc, ngay_khau_hao desc'
    _sql_constraints = [
        ('unique_tai_san_thang_nam', 'unique(tai_san_id, thang, nam)', 
         'Tài sản đã có bản ghi khấu hao trong tháng này!')
    ]

    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_khau_hao = fields.Char("Mã khấu hao", copy=False, readonly=True, default="New")
    tai_san_id = fields.Many2one('tai_san', string="Tài sản", required=True, ondelete="restrict")
    
    # Thời gian
    thang = fields.Integer("Tháng", required=True, default=lambda self: fields.Date.today().month)
    nam = fields.Integer("Năm", required=True, default=lambda self: fields.Date.today().year)
    ngay_khau_hao = fields.Date("Ngày ghi nhận", required=True, default=fields.Date.today)
    
    # Phương pháp
    phuong_phap_khau_hao = fields.Selection(
        related='tai_san_id.phuong_phap_khau_hao', string="Phương pháp", store=True
    )
    
    # Giá trị
    gia_tri_truoc_khau_hao = fields.Monetary(
        "Giá trị trước KH", currency_field='currency_id',
        help="Giá trị còn lại trước khi khấu hao tháng này"
    )
    gia_tri_khau_hao = fields.Monetary(
        "Giá trị khấu hao", required=True, currency_field='currency_id',
        help="Số tiền khấu hao trong tháng này"
    )
    gia_tri_con_lai = fields.Monetary(
        "Giá trị còn lại", compute='_compute_gia_tri_con_lai', store=True,
        currency_field='currency_id'
    )
    currency_id = fields.Many2one('res.currency', related='tai_san_id.currency_id', store=True)
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('du_kien', 'Dự kiến'),
        ('da_ghi_nhan', 'Đã ghi nhận'),
        ('huy', 'Hủy'),
    ], string="Trạng thái", default='du_kien', required=True)
    
    ghi_chu = fields.Text("Ghi chú")
    
    # Liên kết bút toán
    but_toan_id = fields.Many2one('but_toan_ke_toan', string='Bút toán', readonly=True, ondelete='set null')

    # ==================== COMPUTED ====================
    @api.depends('gia_tri_truoc_khau_hao', 'gia_tri_khau_hao')
    def _compute_gia_tri_con_lai(self):
        for rec in self:
            rec.gia_tri_con_lai = rec.gia_tri_truoc_khau_hao - rec.gia_tri_khau_hao

    # ==================== CRUD ====================
    @api.model
    def create(self, vals):
        # Auto generate mã
        if vals.get('ma_khau_hao', 'New') == 'New':
            last_record = self.search([], order='ma_khau_hao desc', limit=1)
            if last_record and last_record.ma_khau_hao.startswith('KH-'):
                try:
                    last_number = int(last_record.ma_khau_hao.split('-')[1])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            vals['ma_khau_hao'] = f'KH-{new_number:05d}'
        
        # Tự động sinh bút toán khi tạo (nếu chưa có)
        record = super(KhauHao, self).create(vals)
        
        if record.trang_thai == 'da_ghi_nhan' and not record.but_toan_id:
            record._tao_but_toan_khau_hao()
        
        return record

    def write(self, vals):
        # Nếu chuyển sang 'da_ghi_nhan' và chưa có bút toán → Tạo bút toán
        res = super(KhauHao, self).write(vals)
        
        if vals.get('trang_thai') == 'da_ghi_nhan':
            for rec in self:
                if not rec.but_toan_id:
                    rec._tao_but_toan_khau_hao()
        
        return res

    # ==================== BUSINESS LOGIC ====================
    def _tao_but_toan_khau_hao(self):
        """Tự động tạo bút toán khấu hao: Nợ 627/642 - Có 214"""
        self.ensure_one()
        
        if self.gia_tri_khau_hao <= 0:
            raise ValidationError("Giá trị khấu hao phải lớn hơn 0!")
        
        if not self.tai_san_id.tai_khoan_chi_phi_khau_hao_id:
            raise ValidationError(f"Tài sản {self.tai_san_id.ten_tai_san} chưa có TK Chi phí khấu hao!")
        
        if not self.tai_san_id.tai_khoan_hao_mon_id:
            raise ValidationError(f"Tài sản {self.tai_san_id.ten_tai_san} chưa có TK Hao mòn!")
        
        # Tạo bút toán
        but_toan = self.env['but_toan_ke_toan'].create({
            'ngay_but_toan': self.ngay_khau_hao,
            'dien_giai': f'Khấu hao tháng {self.thang}/{self.nam} - {self.tai_san_id.ten_tai_san}',
            'loai_but_toan': 'khau_hao',
            'chung_tu_lien_quan': f'khau_hao,{self.id}',
            'chi_tiet_ids': [
                # Nợ TK Chi phí khấu hao (627/642)
                (0, 0, {
                    'tai_khoan_id': self.tai_san_id.tai_khoan_chi_phi_khau_hao_id.id,
                    'tien_no': self.gia_tri_khau_hao,
                    'tien_co': 0,
                    'dien_giai': f'Chi phí khấu hao {self.tai_san_id.ten_tai_san}',
                }),
                # Có TK Hao mòn lũy kế (214)
                (0, 0, {
                    'tai_khoan_id': self.tai_san_id.tai_khoan_hao_mon_id.id,
                    'tien_no': 0,
                    'tien_co': self.gia_tri_khau_hao,
                    'dien_giai': f'Hao mòn lũy kế {self.tai_san_id.ten_tai_san}',
                })
            ]
        })
        
        # Ghi sổ luôn
        but_toan.action_ghi_so()
        
        # Link bút toán
        self.but_toan_id = but_toan.id
        
        return but_toan

    def action_xac_nhan(self):
        """Button: Xác nhận khấu hao"""
        for rec in self:
            if rec.trang_thai != 'du_kien':
                raise ValidationError("Chỉ có thể xác nhận khấu hao ở trạng thái 'Dự kiến'!")
            
            rec.trang_thai = 'da_ghi_nhan'
            
            # Tạo bút toán nếu chưa có
            if not rec.but_toan_id:
                rec._tao_but_toan_khau_hao()

    def action_huy(self):
        """Button: Hủy khấu hao"""
        for rec in self:
            if rec.trang_thai == 'da_ghi_nhan':
                # Hủy bút toán nếu có
                if rec.but_toan_id:
                    rec.but_toan_id.action_huy_ghi_so()
                    rec.but_toan_id.unlink()
            
            rec.trang_thai = 'huy'

    # ==================== CRON JOB METHOD ====================
    @api.model
    def cron_khau_hao_hang_thang(self):
        """
        Cron Job: Chạy tự động hàng tháng
        - Tìm tất cả tài sản đang hoạt động
        - Tính khấu hao theo phương pháp
        - Tạo record khau_hao + bút toán
        """
        today = fields.Date.today()
        thang_hien_tai = today.month
        nam_hien_tai = today.year
        
        # Tìm tất cả tài sản cần khấu hao
        tai_sans = self.env['tai_san'].search([
            ('trang_thai', '!=', 'DaThanhLy'),
            ('ngay_bat_dau_khau_hao', '!=', False),
            ('ngay_bat_dau_khau_hao', '<=', today),
            ('gia_tri_con_lai', '>', 0),
        ])
        
        count_success = 0
        count_skip = 0
        
        for tai_san in tai_sans:
            # Kiểm tra đã có bản ghi khấu hao tháng này chưa
            existing = self.search([
                ('tai_san_id', '=', tai_san.id),
                ('thang', '=', thang_hien_tai),
                ('nam', '=', nam_hien_tai),
            ])
            
            if existing:
                count_skip += 1
                continue
            
            # Tính giá trị khấu hao
            gia_tri_khau_hao = self._tinh_khau_hao_thang(tai_san)
            
            if gia_tri_khau_hao <= 0:
                count_skip += 1
                continue
            
            # Tạo bản ghi khấu hao
            try:
                self.create({
                    'tai_san_id': tai_san.id,
                    'thang': thang_hien_tai,
                    'nam': nam_hien_tai,
                    'ngay_khau_hao': today,
                    'gia_tri_truoc_khau_hao': tai_san.gia_tri_con_lai + gia_tri_khau_hao,
                    'gia_tri_khau_hao': gia_tri_khau_hao,
                    'trang_thai': 'da_ghi_nhan',  # Tự động xác nhận
                    'ghi_chu': f'Khấu hao tự động tháng {thang_hien_tai}/{nam_hien_tai}',
                })
                count_success += 1
            except Exception as e:
                continue
        
        return {
            'success': count_success,
            'skip': count_skip,
            'total': len(tai_sans),
        }

    @api.model
    def _tinh_khau_hao_thang(self, tai_san):
        """Tính giá trị khấu hao trong tháng cho 1 tài sản"""
        if tai_san.phuong_phap_khau_hao == 'duong_thang':
            # Khấu hao đường thẳng: Nguyên giá / Số tháng
            return tai_san.gia_tri_khau_hao_hang_thang
        
        elif tai_san.phuong_phap_khau_hao == 'so_du_giam_dan':
            # Khấu hao số dư giảm dần: Giá trị còn lại × (1/Số tháng còn lại) × Hệ số (2)
            if tai_san.so_thang_khau_hao > 0:
                ti_le_thang = (1 / tai_san.so_thang_khau_hao) * 2  # Hệ số nhanh = 2
                return tai_san.gia_tri_con_lai * ti_le_thang
            return 0
        
        else:
            # Khấu hao theo sản lượng: Cần thêm logic riêng
            return 0