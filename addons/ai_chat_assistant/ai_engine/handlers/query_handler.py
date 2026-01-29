# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)


class QueryHandler:
    """
    Xử lý truy vấn: lấy dữ liệu, tìm kiếm, thống kê
    """
    
    def __init__(self, env):
        self.env = env
    
    def handle_query(self, intent: str, module: str, entities: dict) -> str:
        """
        Xử lý truy vấn lấy dữ liệu hoặc tìm kiếm
        """
        try:
            if intent == 'list_read':
                return self._handle_list(module, entities)
            elif intent == 'search':
                return self._handle_search(module, entities)
            else:
                return "Intent không được hỗ trợ."
        
        except Exception as e:
            _logger.error(f"Query handling error: {str(e)}")
            return f"Lỗi truy vấn: {str(e)}"
    
    def _handle_list(self, module: str, entities: dict) -> str:
        """
        Xử lý yêu cầu lấy danh sách
        """
        try:
            if module == 'nhan_su':
                response = "Danh sách nhân viên:\n"
                response += "- ID, Tên, Phòng ban, Chức vụ, Email, Điện thoại\n"
                response += "Lọc theo: Phòng ban, Chức vụ, Trạng thái\n"
            
            elif module == 'quan_ly_tai_san':
                response = "Danh sách tài sản:\n"
                response += "- ID, Tên tài sản, Loại, Vị trí, Giá trị, Tình trạng\n"
                response += "Lọc theo: Loại, Vị trí, Khoảng giá trị\n"
            
            elif module == 'tai_chinh_ke_toan':
                response = "Danh sách hóa đơn:\n"
                response += "- ID, Ngày, Nhà cung cấp, Số tiền, Trạng thái\n"
                response += "Lọc theo: Ngày, Nhà cung cấp, Khoảng tiền\n"
            
            else:
                response = f"Module {module} không được hỗ trợ."
            
            # Apply filters if available
            if entities.get('filters'):
                response += f"\nBộ lọc áp dụng: {entities['filters']}\n"
            
            if entities.get('amounts'):
                response += f"Khoảng tiền: {entities['amounts']}\n"
            
            if entities.get('dates'):
                response += f"Khoảng ngày: {entities['dates']}\n"
            
            response += "(Dữ liệu từ cơ sở dữ liệu)"
            return response
        
        except Exception as e:
            _logger.error(f"List handling error: {str(e)}")
            return f"Lỗi lấy danh sách: {str(e)}"
    
    def _handle_search(self, module: str, entities: dict) -> str:
        """
        Xử lý yêu cầu tìm kiếm
        """
        try:
            search_terms = entities.get('names', []) + entities.get('ids', [])
            
            if not search_terms:
                return "Vui lòng cung cấp từ khóa tìm kiếm."
            
            response = f"Tìm kiếm trong module {module}:\n"
            response += f"Từ khóa: {', '.join(search_terms)}\n"
            response += "Kết quả: (sẽ lấy từ cơ sở dữ liệu)\n"
            
            if entities.get('filters'):
                response += f"Với bộ lọc: {entities['filters']}\n"
            
            return response
        
        except Exception as e:
            _logger.error(f"Search handling error: {str(e)}")
            return f"Lỗi tìm kiếm: {str(e)}"
    
    def handle_statistics(self, module: str, entities: dict) -> str:
        """
        Xử lý yêu cầu thống kê
        """
        try:
            if module == 'nhan_su':
                response = "Thống kê Nhân sự:\n"
                response += "- Tổng số nhân viên\n"
                response += "- Phân bố theo phòng ban\n"
                response += "- Phân bố theo chức vụ\n"
            
            elif module == 'quan_ly_tai_san':
                response = "Thống kê Tài sản:\n"
                response += "- Tổng giá trị tài sản\n"
                response += "- Phân bố theo loại\n"
                response += "- Tình trạng tài sản\n"
            
            elif module == 'tai_chinh_ke_toan':
                response = "Thống kê Tài chính:\n"
                response += "- Tổng doanh thu\n"
                response += "- Tổng chi phí\n"
                response += "- Lợi nhuận\n"
            
            else:
                response = f"Module {module} không được hỗ trợ."
            
            # Apply filters if available
            if entities.get('dates'):
                response += f"\nKhoảng thời gian: {entities['dates']}\n"
            
            response += "(Dữ liệu từ cơ sở dữ liệu)"
            return response
        
        except Exception as e:
            _logger.error(f"Statistics handling error: {str(e)}")
            return f"Lỗi thống kê: {str(e)}"
