import re
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ChatController(http.Controller):
    """
    Controller xử lý chat với khả năng hiểu ngôn ngữ tự nhiên
    """

    # Cấu hình actions với XML ID ĐẦY ĐỦ (module_name.action_id)
    ACTIONS_CONFIG = [
        {
            "id": "nhan_su.action_nhan_vien",  # ✅ XML ID đầy đủ
            "name": "Quản lý nhân viên",
            "patterns": [
                r"(nhân viên|nhan vien|employee|staff|cán bộ|can bo)",
                r"(xem|hiển thị|show|list|danh sách).*(nhân viên|employee)",
                r"(quản lý|manage).*(nhân viên|employee)"
            ],
            "response": "🔎 Đang mở danh sách nhân viên..."
        },
        {
            "id": "nhan_su.action_phong_ban",  # ✅ Sửa lại với module prefix
            "name": "Danh mục phòng ban",
            "patterns": [
                r"(phòng ban|phong ban|department|bộ phận|bo phan|đơn vị|don vi)",
                r"(xem|hiển thị|show|list|danh sách).*(phòng|department)",
                r"(các|tất cả).*(phòng ban|department)"
            ],
            "response": "🔎 Đang mở danh mục phòng ban..."
        },
        {
            "id": "nhan_su.action_chuc_vu",  # ✅ Sửa lại với module prefix
            "name": "Danh mục chức vụ",
            "patterns": [
                r"(chức vụ|chuc vu|position|vị trí|vi tri|cấp bậc|cap bac)",
                r"(xem|hiển thị|show|list|danh sách).*(chức vụ|position)",
                r"(các|tất cả).*(chức vụ|cấp bậc)"
            ],
            "response": "🔎 Đang mở danh mục chức vụ..."
        },
        {
            "id": "nhan_su.action_chung_chi",  # ✅ Sửa lại với module prefix
            "name": "Danh mục chứng chỉ",
            "patterns": [
                r"(chứng chỉ|chung chi|certificate|bằng cấp|bang cap|văn bằng|van bang)",
                r"(xem|hiển thị|show|list|danh sách).*(chứng chỉ|certificate)",
                r"(các|tất cả).*(chứng chỉ|bằng cấp)"
            ],
            "response": "🔎 Đang mở danh mục chứng chỉ..."
        },
        {
            "id": "nhan_su.action_lich_su_cong_tac",  # ✅ Sửa lại với module prefix
            "name": "Quản lý lịch sử công tác",
            "patterns": [
                r"(lịch sử|lich su|history|quá trình|qua trinh).*(công tác|cong tac|career)",
                r"(xem|hiển thị|show).*(lịch sử|history)",
                r"(quá trình|qua trinh).*(làm việc|lam viec|công tác)"
            ],
            "response": "🔎 Đang mở lịch sử công tác..."
        },
        {
            "id": "quan_ly_tai_san.action_tai_san",
            "name": "Quản lý tài sản",
            "patterns": [
                r"(tài sản|tai san|asset|thiết bị|thiet bi)",
                r"(xem|hiển thị|show|list|danh sách).*(tài sản|asset)",
                r"(quản lý|manage).*(tài sản|asset)"
            ],
            "response": "🔎 Đang mở quản lý tài sản..."
        },
        {
            "id": "quan_ly_tai_san.action_loai_tai_san",
            "name": "Loại tài sản",
            "patterns": [
                r"(loại tài sản|loai tai san)",
                r"(xem|hiển thị|show).*(loại tài sản)",
                r"(phân loại|phan loai)"
            ],
            "response": "🔎 Đang mở loại tài sản..."
        },
        {
            "id": "quan_ly_tai_san.action_vi_tri",
            "name": "Vị trí tài sản",
            "patterns": [
                r"(vị trí|vi tri|location|địa điểm|dia diem).*(tài sản|tai san)",
                r"(xem|hiển thị).*(vị trí|location)"
            ],
            "response": "🔎 Đang mở vị trí tài sản..."
        },
        {
            "id": "quan_ly_tai_san.action_nha_cung_cap",
            "name": "Nhà cung cấp",
            "patterns": [
                r"(nhà cung cấp|nha cung cap|supplier|vendor)",
                r"(xem|hiển thị|list).*(nhà cung cấp)"
            ],
            "response": "🔎 Đang mở nhà cung cấp..."
        },
        {
            "id": "quan_ly_tai_san.action_phieu_muon",
            "name": "Phiếu mượn",
            "patterns": [
                r"(phiếu mượn|phieu muon|mượn|muon).*(tài sản|tai san)",
                r"(xem|hiển thị).*(phiếu mượn)"
            ],
            "response": "🔎 Đang mở phiếu mượn..."
        },
        {
            "id": "quan_ly_tai_san.action_phieu_bao_tri",
            "name": "Phiếu bảo trì",
            "patterns": [
                r"(bảo trì|bao tri|maintenance|sửa chữa|sua chua)",
                r"(xem|hiển thị).*(bảo trì)"
            ],
            "response": "🔎 Đang mở phiếu bảo trì..."
        },
        {
            "id": "quan_ly_tai_san.action_phieu_dieu_chuyen",
            "name": "Phiếu điều chuyển",
            "patterns": [
                r"(điều chuyển|dieu chuyen|transfer)",
                r"(xem|hiển thị).*(điều chuyển)"
            ],
            "response": "🔎 Đang mở phiếu điều chuyển..."
        },
        {
            "id": "quan_ly_tai_san.action_lich_su_di_chuyen",
            "name": "Lịch sử điều chuyển",
            "patterns": [
                r"(lịch sử|lich su).*(điều chuyển|di chuyển)",
                r"(xem|hiển thị).*(lịch sử)"
            ],
            "response": "🔎 Đang mở lịch sử điều chuyển..."
        },
        {
            "id": "quan_ly_tai_san.action_lich_su_su_dung",
            "name": "Lịch sử sử dụng",
            "patterns": [
                r"(lịch sử|lich su).*(sử dụng|su dung)",
                r"(xem|hiển thị).*(sử dụng)"
            ],
            "response": "🔎 Đang mở lịch sử sử dụng..."
        },
        {
            "id": "quan_ly_tai_san.action_lich_su_bao_tri",
            "name": "Lịch sử bảo trì",
            "patterns": [
                r"(lịch sử|lich su).*(bảo trì|bao tri)",
                r"(xem|hiển thị).*(bảo trì)"
            ],
            "response": "🔎 Đang mở lịch sử bảo trì..."
        },
        {
            "id": "quan_ly_tai_san.action_khau_hao",
            "name": "Khấu hao tài sản",
            "patterns": [
                r"(khấu hao|khau hao).*(tài sản|tai san)",
                r"(xem|hiển thị).*(khấu hao)"
            ],
            "response": "🔎 Đang mở khấu hao tài sản..."
        },
        {
            "id": "quan_ly_tai_san.action_thanh_ly",
            "name": "Thanh lý tài sản",
            "patterns": [
                r"(thanh lý|thanh ly).*(tài sản|tai san)",
                r"(xem|hiển thị).*(thanh lý)"
            ],
            "response": "🔎 Đang mở thanh lý tài sản..."
        },
        {
            "id": "quan_ly_tai_san.action_phieu_kiem_ke",
            "name": "Phiếu kiểm kê",
            "patterns": [
                r"(phiếu kiểm kê|phieu kiem ke|inventory)",
                r"(xem|hiển thị).*(kiểm kê)"
            ],
            "response": "🔎 Đang mở phiếu kiểm kê..."
        },
        {
            "id": "quan_ly_tai_san.action_lich_su_kiem_ke",
            "name": "Lịch sử kiểm kê",
            "patterns": [
                r"(lịch sử|lich su).*(kiểm kê|kiem ke)",
                r"(xem|hiển thị).*(kiểm kê)"
            ],
            "response": "🔎 Đang mở lịch sử kiểm kê..."
        },
        {
            "id": "quan_ly_tai_san.action_thong_ke",
            "name": "Thống kê tài sản",
            "patterns": [
                r"(thống kê|thong ke).*(tài sản|tai san)",
                r"(xem|hiển thị).*(thống kê)"
            ],
            "response": "🔎 Đang mở thống kê tài sản..."
        },
        {
    "id": "tai_chinh_ke_toan.action_but_toan_ke_toan",
    "name": "Bút toán kế toán",
    "patterns": [
        r"(bút toán|but toan|journal entry)",
        r"(xem|hiển thị|show|list).*(bút toán)",
        r"(ghi|tạo).*(bút toán)"
    ],
    "response": "🔎 Đang mở bút toán kế toán..."
},
{
    "id": "tai_chinh_ke_toan.action_chi_tiet_but_toan",
    "name": "Chi tiết bút toán",
    "patterns": [
        r"(chi tiết|chi tiet).*(bút toán)",
        r"(xem|hiển thị).*(chi tiết bút toán)"
    ],
    "response": "🔎 Đang mở chi tiết bút toán..."
},
{
    "id": "tai_chinh_ke_toan.action_hoa_don_ban",
    "name": "Hóa đơn bán hàng",
    "patterns": [
        r"(hóa đơn|hoa don).*(bán|ban|sale)",
        r"(xem|hiển thị).*(hóa đơn bán)"
    ],
    "response": "🔎 Đang mở hóa đơn bán hàng..."
},
{
    "id": "tai_chinh_ke_toan.action_hoa_don_mua",
    "name": "Hóa đơn mua hàng",
    "patterns": [
        r"(hóa đơn|hoa don).*(mua|purchase)",
        r"(xem|hiển thị).*(hóa đơn mua)"
    ],
    "response": "🔎 Đang mở hóa đơn mua hàng..."
},
{
    "id": "tai_chinh_ke_toan.action_chi_tiet_hoa_don_ban",
    "name": "Chi tiết hóa đơn bán",
    "patterns": [
        r"(chi tiết|chi tiet).*(hóa đơn).*(bán)",
        r"(xem|hiển thị).*(chi tiết hóa đơn bán)"
    ],
    "response": "🔎 Đang mở chi tiết hóa đơn bán..."
},
{
    "id": "tai_chinh_ke_toan.action_chi_tiet_hoa_don_mua",
    "name": "Chi tiết hóa đơn mua",
    "patterns": [
        r"(chi tiết|chi tiet).*(hóa đơn).*(mua)",
        r"(xem|hiển thị).*(chi tiết hóa đơn mua)"
    ],
    "response": "🔎 Đang mở chi tiết hóa đơn mua..."
},
{
    "id": "tai_chinh_ke_toan.action_phieu_thu_chi",
    "name": "Phiếu thu chi",
    "patterns": [
        r"(phiếu thu chi|phieu thu chi|receipt|payment)",
        r"(xem|hiển thị).*(phiếu thu|phiếu chi)"
    ],
    "response": "🔎 Đang mở phiếu thu chi..."
},
{
    "id": "tai_chinh_ke_toan.action_tai_khoan_ke_toan",
    "name": "Tài khoản kế toán",
    "patterns": [
        r"(tài khoản kế toán|tai khoan ke toan|chart of account)",
        r"(xem|hiển thị).*(tài khoản kế toán)"
    ],
    "response": "🔎 Đang mở tài khoản kế toán..."
},
{
    "id": "tai_chinh_ke_toan.action_tai_khoan_ngan_hang",
    "name": "Tài khoản ngân hàng",
    "patterns": [
        r"(tài khoản ngân hàng|tai khoan ngan hang|bank account)",
        r"(xem|hiển thị).*(ngân hàng)"
    ],
    "response": "🔎 Đang mở tài khoản ngân hàng..."
},
{
    "id": "tai_chinh_ke_toan.action_khau_hao",
    "name": "Khấu hao kế toán",
    "patterns": [
        r"(khấu hao|khau hao).*(kế toán)",
        r"(xem|hiển thị).*(khấu hao)"
    ],
    "response": "🔎 Đang mở khấu hao kế toán..."
},
{
    "id": "tai_chinh_ke_toan.action_thanh_ly",
    "name": "Thanh lý kế toán",
    "patterns": [
        r"(thanh lý|thanh ly).*(kế toán)",
        r"(xem|hiển thị).*(thanh lý)"
    ],
    "response": "🔎 Đang mở thanh lý kế toán..."
},
{
    "id": "tai_chinh_ke_toan.action_cong_no",
    "name": "Công nợ",
    "patterns": [
        r"(công nợ|cong no|receivable|payable)",
        r"(xem|hiển thị).*(công nợ)"
    ],
    "response": "🔎 Đang mở công nợ..."
},
{
    "id": "tai_chinh_ke_toan.action_to_khai_thue",
    "name": "Tờ khai thuế",
    "patterns": [
        r"(tờ khai|to khai|thuế|thue|tax return)",
        r"(xem|hiển thị).*(tờ khai)"
    ],
    "response": "🔎 Đang mở tờ khai thuế..."
},
{
    "id": "tai_chinh_ke_toan.action_chi_tiet_to_khai_thue",
    "name": "Chi tiết tờ khai thuế",
    "patterns": [
        r"(chi tiết|chi tiet).*(tờ khai|thuế)",
        r"(xem|hiển thị).*(chi tiết tờ khai)"
    ],
    "response": "🔎 Đang mở chi tiết tờ khai thuế..."
},
{
    "id": "tai_chinh_ke_toan.action_chinh_sach_thue",
    "name": "Chính sách thuế",
    "patterns": [
        r"(chính sách|chinh sach).*(thuế)",
        r"(xem|hiển thị).*(chính sách thuế)"
    ],
    "response": "🔎 Đang mở chính sách thuế..."
},
{
    "id": "tai_chinh_ke_toan.action_ky_ke_toan",
    "name": "Kỳ kế toán",
    "patterns": [
        r"(kỳ kế toán|ky ke toan|period)",
        r"(xem|hiển thị).*(kỳ kế toán)"
    ],
    "response": "🔎 Đang mở kỳ kế toán..."
},
{
    "id": "tai_chinh_ke_toan.action_bao_cao_tai_chinh",
    "name": "Báo cáo tài chính",
    "patterns": [
        r"(báo cáo|bao cao).*(tài chính|tai chinh)",
        r"(xem|hiển thị).*(báo cáo tài chính)"
    ],
    "response": "🔎 Đang mở báo cáo tài chính..."
},
{
    "id": "tai_chinh_ke_toan.action_so_cai",
    "name": "Sổ cái",
    "patterns": [
        r"(sổ cái|so cai|general ledger)",
        r"(xem|hiển thị).*(sổ cái)"
    ],
    "response": "🔎 Đang mở sổ cái..."
},
{
    "id": "tai_chinh_ke_toan.action_so_chi_tiet",
    "name": "Sổ chi tiết",
    "patterns": [
        r"(sổ chi tiết|so chi tiet|subsidiary)",
        r"(xem|hiển thị).*(sổ chi tiết)"
    ],
    "response": "🔎 Đang mở sổ chi tiết..."
},
{
    "id": "tai_chinh_ke_toan.action_doi_soat_ngan_hang",
    "name": "Đối soát ngân hàng",
    "patterns": [
        r"(đối soát|doi soat).*(ngân hàng|bank)",
        r"(xem|hiển thị).*(đối soát)"
    ],
    "response": "🔎 Đang mở đối soát ngân hàng..."
}


    ]

    def _normalize_text(self, text):
        """Chuẩn hóa text để dễ so sánh"""
        text = text.lower().strip()
        # Loại bỏ dấu câu thừa
        text = re.sub(r'[?!.,:;]+', ' ', text)
        # Loại bỏ khoảng trắng thừa
        text = re.sub(r'\s+', ' ', text)
        return text

    def _match_action(self, message):
        """
        Tìm action phù hợp với message sử dụng regex patterns
        Returns: dict hoặc None
        """
        normalized_msg = self._normalize_text(message)
        
        # Tính điểm cho mỗi action
        scores = []
        for action in self.ACTIONS_CONFIG:
            score = 0
            matched_patterns = []
            
            for pattern in action["patterns"]:
                if re.search(pattern, normalized_msg, re.IGNORECASE):
                    score += 1
                    matched_patterns.append(pattern)
            
            if score > 0:
                scores.append({
                    "action": action,
                    "score": score,
                    "matched_patterns": matched_patterns
                })
        
        # Sắp xếp theo điểm và trả về action tốt nhất
        if scores:
            scores.sort(key=lambda x: x["score"], reverse=True)
            best_match = scores[0]
            _logger.info(f"Matched action: {best_match['action']['id']} with score {best_match['score']}")
            return best_match["action"]
        
        return None

    def _get_help_message(self):
        """Tạo message gợi ý sử dụng"""
        suggestions = [action["name"] for action in self.ACTIONS_CONFIG[:3]]
        return f"🤖 Tôi có thể giúp bạn:\n• " + "\n• ".join(suggestions) + "\n\nHãy thử hỏi tôi!"

    @http.route('/chat/send', type='json', auth='user')
    def chat_send(self, message=None):
        """
        Xử lý tin nhắn từ người dùng
        """
        if not message:
            return {
                "type": "text",
                "reply": self._get_help_message()
            }

        # Tìm action phù hợp
        matched_action = self._match_action(message)
        
        if matched_action:
            _logger.info(f"Sending action to frontend: {matched_action['id']}")
            return {
                "type": "action",
                "action": matched_action["id"],
                "reply": matched_action["response"]
            }
        
        # Không tìm thấy action phù hợp
        return {
            "type": "text",
            "reply": self._get_help_message()
        }

    @http.route('/chat/actions', type='json', auth='user')
    def get_available_actions(self):
        """
        API để lấy danh sách actions có sẵn
        """
        return [
            {
                "id": action["id"],
                "name": action["name"]
            }
            for action in self.ACTIONS_CONFIG
        ]
    
    @http.route('/chat/debug/actions', type='json', auth='user')
    def debug_actions(self):
        """
        API debug để kiểm tra các action có sẵn trong database
        """
        try:
            IrModelData = request.env['ir.model.data']
            actions_info = []
            
            for action_config in self.ACTIONS_CONFIG:
                xml_id = action_config["id"]
                try:
                    # Tách module và action_id
                    module_name, action_name = xml_id.split('.')
                    
                    # Tìm action trong database
                    model_data = IrModelData.search([
                        ('module', '=', module_name),
                        ('name', '=', action_name),
                        ('model', '=', 'ir.actions.act_window')
                    ], limit=1)
                    
                    if model_data:
                        action = request.env['ir.actions.act_window'].browse(model_data.res_id)
                        actions_info.append({
                            "xml_id": xml_id,
                            "exists": True,
                            "action_name": action.name,
                            "model": action.res_model
                        })
                    else:
                        actions_info.append({
                            "xml_id": xml_id,
                            "exists": False,
                            "error": "Action not found in database"
                        })
                except Exception as e:
                    actions_info.append({
                        "xml_id": xml_id,
                        "exists": False,
                        "error": str(e)
                    })
            
            return {
                "success": True,
                "actions": actions_info
            }
        except Exception as e:
            _logger.error(f"Error in debug_actions: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }