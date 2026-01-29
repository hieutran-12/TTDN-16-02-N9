# -*- coding: utf-8 -*-
import logging
from typing import Dict

_logger = logging.getLogger(__name__)


class NavigationHandler:
    """
    Xử lý các yêu cầu điều hướng/mở views
    """
    
    MODULE_VIEWS = {
        'nhan_su': {
            'views': ['hr.employee', 'hr.department', 'hr.job'],
            'actions': ['action_hr_employee', 'action_hr_department'],
        },
        'quan_ly_tai_san': {
            'views': ['tai.san', 'loai.tai.san', 'vi.tri'],
            'actions': ['action_tai_san', 'action_khau_hao'],
        },
        'tai_chinh_ke_toan': {
            'views': ['account.move', 'account.invoice', 'account.chart.template'],
            'actions': ['action_move_in_invoice_type', 'action_account_moves'],
        },
    }
    
    def __init__(self, env):
        self.env = env
    
    def handle(self, message: str, module: str, entities: Dict) -> str:
        """
        Xử lý yêu cầu điều hướng
        """
        try:
            if module not in self.MODULE_VIEWS:
                return f"Module {module} không được hỗ trợ."
            
            views = self.MODULE_VIEWS[module]['views']
            actions = self.MODULE_VIEWS[module]['actions']
            
            response = f"Điều hướng đến module {module}:\n"
            response += f"- Có sẵn {len(views)} view\n"
            response += f"- Có sẵn {len(actions)} action\n"
            response += "Vui lòng chọn view/action cụ thể."
            
            return response
        
        except Exception as e:
            _logger.error(f"Navigation handling error: {str(e)}")
            return f"Lỗi điều hướng: {str(e)}"
