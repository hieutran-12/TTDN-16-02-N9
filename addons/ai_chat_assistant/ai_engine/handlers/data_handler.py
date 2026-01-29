# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)


class DataHandler:
    """
    Xử lý các thao tác CRUD: tạo, cập nhật, xóa bản ghi
    """
    
    MODEL_MAPPINGS = {
        'nhan_su': {
            'create': 'hr.employee',
            'update': 'hr.employee',
            'delete': 'hr.employee',
        },
        'quan_ly_tai_san': {
            'create': 'tai.san',
            'update': 'tai.san',
            'delete': 'tai.san',
        },
        'tai_chinh_ke_toan': {
            'create': 'account.move',
            'update': 'account.move',
            'delete': 'account.move',
        },
    }
    
    def __init__(self, env):
        self.env = env
    
    def handle_create(self, module: str, entities: dict) -> str:
        """
        Xử lý tạo bản ghi mới
        """
        try:
            if module not in self.MODEL_MAPPINGS:
                return f"Module {module} không được hỗ trợ."
            
            model_name = self.MODEL_MAPPINGS[module]['create']
            
            # Validate required entities
            if not entities.get('names') and not entities.get('ids'):
                return "Vui lòng cung cấp tên hoặc mã định danh để tạo bản ghi."
            
            # Create record (simplified - actual implementation depends on model structure)
            response = f"Sẵn sàng tạo bản ghi mới trong module {module}\n"
            response += f"Model: {model_name}\n"
            response += f"Dữ liệu: {entities}\n"
            response += "Vui lòng xác nhận để tiếp tục."
            
            return response
        
        except Exception as e:
            _logger.error(f"Create handling error: {str(e)}")
            return f"Lỗi tạo bản ghi: {str(e)}"
    
    def handle_update(self, module: str, entities: dict) -> str:
        """
        Xử lý cập nhật bản ghi
        """
        try:
            if module not in self.MODEL_MAPPINGS:
                return f"Module {module} không được hỗ trợ."
            
            model_name = self.MODEL_MAPPINGS[module]['update']
            
            # Validate required ID
            if not entities.get('ids') and not entities.get('numbers'):
                return "Vui lòng cung cấp ID của bản ghi cần cập nhật."
            
            response = f"Sẵn sàng cập nhật bản ghi trong module {module}\n"
            response += f"Model: {model_name}\n"
            response += f"Dữ liệu cập nhật: {entities}\n"
            response += "Vui lòng xác nhận để tiếp tục."
            
            return response
        
        except Exception as e:
            _logger.error(f"Update handling error: {str(e)}")
            return f"Lỗi cập nhật bản ghi: {str(e)}"
    
    def handle_delete(self, module: str, entities: dict) -> str:
        """
        Xử lý xóa bản ghi
        """
        try:
            if module not in self.MODEL_MAPPINGS:
                return f"Module {module} không được hỗ trợ."
            
            model_name = self.MODEL_MAPPINGS[module]['delete']
            
            # Validate required ID
            if not entities.get('ids') and not entities.get('numbers'):
                return "Vui lòng cung cấp ID của bản ghi cần xóa."
            
            response = f"⚠️ Cảnh báo: Sắp xóa bản ghi trong module {module}\n"
            response += f"Model: {model_name}\n"
            response += f"ID/Mã: {entities.get('ids') or entities.get('numbers')}\n"
            response += "Vui lòng xác nhận để xóa."
            
            return response
        
        except Exception as e:
            _logger.error(f"Delete handling error: {str(e)}")
            return f"Lỗi xóa bản ghi: {str(e)}"
