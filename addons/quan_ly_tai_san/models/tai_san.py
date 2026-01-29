# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Bảng chứa thông tin tài sản'
    _order = 'ma_tai_san'
    _rec_name = 'ten_tai_san'
    _sql_constraints = [
        ('ma_tai_san_unique', 'unique(ma_tai_san)', 'Mã tài sản phải là duy nhất!')
    ]

    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_tai_san = fields.Char(
        "Mã Tài sản", required=True, copy=False, readonly=True, default="New",
        help="Mã duy nhất của tài sản, tự động tạo khi thêm mới"
    )
    ten_tai_san = fields.Char("Tên Tài sản", required=True)
    hinh_anh = fields.Binary("Hình ảnh", attachment=True)
    so_serial = fields.Char("Số serial", copy=False)

    # ==================== LIÊN KẾT HÓA ĐƠN (MANY2ONE - CHỌN TỪ DANH SÁCH) ====================
    hoa_don_mua_id = fields.Many2one(
        'hoa_don_mua',
        string='Hóa đơn mua',
        required=True,
        ondelete='restrict',
        help='Bắt buộc: Chọn hóa đơn mua từ module kế toán (để biết nhà cung cấp, giá tiền)'
    )

    # ==================== THÔNG TIN MUA HÀNG (NHẬP TAY) ====================
    ngay_mua = fields.Date("Ngày mua", required=True, default=fields.Date.today)
    ngay_het_han_bao_hanh = fields.Date("Ngày hết hạn bảo hành")
    gia_tien_mua = fields.Monetary(
        "Giá tiền mua (Nguyên giá)",
        required=True,
        currency_field='currency_id',
        help="Nguyên giá tài sản khi mua"
    )
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    # ==================== COMPUTED FIELDS - TỰ ĐỘNG LẤY TỪ HÓA ĐƠN ====================
    @api.depends('hoa_don_mua_id')
    def _compute_from_invoice(self):
        """Tự động điền nhà cung cấp, ngày mua, giá từ hóa đơn"""
        for rec in self:
            if rec.hoa_don_mua_id:
                rec.nha_cung_cap_id = rec.hoa_don_mua_id.nha_cung_cap_id
                rec.ngay_mua = rec.hoa_don_mua_id.ngay_hoa_don
                rec.gia_tien_mua = rec.hoa_don_mua_id.tong_thanh_toan
            else:
                rec.nha_cung_cap_id = None
                rec.ngay_mua = fields.Date.today()
                rec.gia_tien_mua = 0

    # ==================== TRẠNG THÁI ====================
    TRANG_THAI = [
        ("LuuTru", "Lưu trữ"),
        ("Muon", "Mượn"),
        ("BaoTri", "Bảo trì"),
        ("Hong", "Hỏng"),
        ("DaThanhLy", "Đã thanh lý"),
    ]
    TRANG_THAI_KIEM_KE = [
        ('binh_thuong', 'Bình thường'),
        ('hong_hoc', 'Hỏng hóc'),
        ('mat', 'Mất'),
        ('sua_chua', 'Đang sửa chữa')
    ]
    trang_thai = fields.Selection(TRANG_THAI, string="Trạng thái", default="LuuTru", tracking=True)
    trang_thai_kiem_ke = fields.Selection(TRANG_THAI_KIEM_KE, string="Trạng thái Kiểm Kê", default="binh_thuong")

    # ==================== QUAN HỆ ====================
    loai_tai_san_id = fields.Many2one('loai_tai_san', string="Loại tài sản", required=True)
    vi_tri_hien_tai_id = fields.Many2one('vi_tri', string="Vị trí hiện tại")
    nha_cung_cap_id = fields.Many2one('res.partner', string="Nhà cung cấp")
    quan_ly_id = fields.Many2one('nhan_vien', string="Người quản lý")
    nguoi_dang_dung_id = fields.Many2one('nhan_vien', string="Người đang sử dụng")

    # One2many
    lich_su_su_dung_ids = fields.One2many('lich_su_su_dung', 'tai_san_id', string="Lịch sử sử dụng")
    lich_su_bao_tri_ids = fields.One2many('lich_su_bao_tri', 'tai_san_id', string="Lịch sử bảo trì")
    lich_su_di_chuyen_ids = fields.One2many('lich_su_di_chuyen', 'tai_san_id', string="Lịch sử điều chuyển")
    lich_su_kiem_ke_ids = fields.One2many('lich_su_kiem_ke', 'tai_san_id', string="Lịch sử kiểm kê")
    phieu_kiem_ke_ids = fields.Many2many('phieu_kiem_ke', string="Phiếu kiểm kê",
                                          relation='tai_san_phieu_kiem_ke_rel',
                                          column1='tai_san_id', column2='phieu_kiem_ke_id')

    # ==================== NHẬN TÍN HIỆU THANH LÝ TỪ KẾ TOÁN ====================
    ma_phieu_thanh_ly = fields.Char(
        string="Mã phiếu thanh lý",
        readonly=True,
        help="Mã tham chiếu từ module kế toán khi tài sản được thanh lý"
    )
    ngay_thanh_ly = fields.Date(
        string="Ngày thanh lý",
        readonly=True,
        help="Ngày tài sản được thanh lý (nhận từ kế toán)"
    )

    # ==================== CONSTRAINTS ====================
    @api.constrains('ngay_het_han_bao_hanh', 'ngay_mua')
    def _check_dates(self):
        for rec in self:
            if rec.ngay_het_han_bao_hanh and rec.ngay_mua:
                if rec.ngay_het_han_bao_hanh < rec.ngay_mua:
                    raise ValidationError("Ngày hết hạn bảo hành phải lớn hơn hoặc bằng ngày mua!")

    @api.constrains('gia_tien_mua')
    def _check_gia_tien_mua(self):
        for rec in self:
            if rec.gia_tien_mua <= 0:
                raise ValidationError("Giá tiền mua phải lớn hơn 0!")

    # ==================== CRUD ====================
    @api.model
    def create(self, vals):
        # Auto generate mã tài sản
        if vals.get('ma_tai_san', 'New') == 'New':
            last_asset = self.search([], order="ma_tai_san desc", limit=1)
            if last_asset and re.match(r"TS-\d{5}", last_asset.ma_tai_san):
                last_number = int(last_asset.ma_tai_san.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            vals['ma_tai_san'] = f"TS-{new_number:05d}"
        
        return super(TaiSan, self).create(vals)

    # ==================== ACTIONS ====================
    def action_tao_tai_san_tu_hoa_don(self, hoa_don_id):
        """Tạo tài sản từ hóa đơn mua (gọi từ button Quản lý tài sản)"""
        hoa_don = self.env['hoa_don_mua'].browse(hoa_don_id)
        
        if not hoa_don.co_tai_san:
            raise ValidationError('Hóa đơn không được đánh dấu "Có phát sinh tài sản"!')
        
        if hoa_don.asset_status == 'created':
            raise ValidationError('Tài sản từ hóa đơn này đã được tạo rồi!')
        
        # Tạo tài sản mới với thông tin từ hóa đơn
        tai_san_vals = {
            'ten_tai_san': f"{hoa_don.name} - {hoa_don.nha_cung_cap_id.name}",
            'ngay_mua': hoa_don.ngay_hoa_don,
            'gia_tien_mua': hoa_don.tong_thanh_toan,
            'nha_cung_cap_id': hoa_don.nha_cung_cap_id.id,
            'hoa_don_mua_id': hoa_don.id,
            # User PHẢI chọn: loai_tai_san, quan_ly, nguoi_dang_dung, vi_tri
        }
        
        new_tai_san = self.create(tai_san_vals)
        
        # Cập nhật hóa đơn
        hoa_don.write({
            'ma_tai_san_created': new_tai_san.ma_tai_san,
            'asset_status': 'created',
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'tai_san',
            'view_mode': 'form',
            'res_id': new_tai_san.id,
            'target': 'main',
        }
    
    def action_di_chuyen_tai_san(self):
        self.ensure_one()
        return {
            'name': 'Điều chuyển tài sản',
            'type': 'ir.actions.act_window',
            'res_model': 'lich_su_di_chuyen',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_tai_san_id': self.id,
                'default_vi_tri_chuyen_id': self.vi_tri_hien_tai_id.id,
            },
        }
