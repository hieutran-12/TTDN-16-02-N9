{
    'name': 'Tài chính - Kế toán',
    'summary': 'Quản lý tài chính, kế toán, hóa đơn, bút toán, phiếu thu chi',
    'version': '15.0.1.0.0',
    'author': 'Hieu',
    'category': 'Accounting',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/tai_khoan_default.xml',
        'data/sequence.xml',
        'views/tai_khoan_ke_toan.xml',
        'views/but_toan_ke_toan.xml',
        'views/so_cai.xml',
        'views/so_chi_tiet.xml',
        'views/hoa_don_mua.xml',
        'views/hoa_don_mua_form.xml',
        'views/chi_tiet_hoa_don_mua.xml',
        'views/thue.xml',
        'views/khau_hao_tai_san.xml',
        'views/thanh_ly_tai_san.xml',
        'views/bao_cao_tai_chinh.xml',
        'views/actions.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'sequence': 1,
    'description': '''
    Quản lý tài chính, kế toán, hóa đơn, bút toán.

    Tính năng chính:
    - Hệ thống tài khoản kế toán theo TT200/133
    - Bút toán kế toán tự động (mua hàng, khấu hao, thanh lý)
    - Hóa đơn mua hàng và quản lý công nợ
    - Sổ cái, sổ chi tiết
    - Báo cáo tài chính

    Ngôn ngữ: Tiếng Việt
    '''
}
