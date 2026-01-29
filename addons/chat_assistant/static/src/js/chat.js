odoo.define("chat_assistant.chat", function (require) {
  "use strict";

  const rpc = require("web.rpc");
  const core = require("web.core");
  const _t = core._t;

  class ChatAssistant {
    constructor() {
      this.isOpen = false;
      this.init();
    }

    init() {
      this.createUI();
      this.attachEvents();
    }

    createUI() {
      // Nút toggle chat
      const toggle = document.createElement("div");
      toggle.id = "chat-toggle";
      toggle.innerHTML = '<span class="chat-icon">💬</span>';
      toggle.title = "Mở chat assistant";

      // Chat box
      const box = document.createElement("div");
      box.id = "chat-box";
      box.innerHTML = `
        <div id="chat-header">
          <span class="chat-title">🤖 AI Assistant</span>
          <button id="chat-close" title="Đóng">×</button>
        </div>
        <div id="chat-body">
          <div class="chat-welcome">
            Xin chào! Tôi có thể giúp gì cho bạn?
          </div>
        </div>
        <div id="chat-input-wrapper">
          <input 
            type="text" 
            id="chat-input" 
            placeholder="Nhập câu hỏi của bạn..." 
            autocomplete="off"
          />
          <button id="chat-send" title="Gửi">
            <span>➤</span>
          </button>
        </div>
      `;

      document.body.appendChild(toggle);
      document.body.appendChild(box);

      this.toggle = toggle;
      this.box = box;
      this.input = box.querySelector("#chat-input");
      this.sendBtn = box.querySelector("#chat-send");
      this.closeBtn = box.querySelector("#chat-close");
      this.body = box.querySelector("#chat-body");
    }

    attachEvents() {
      // Toggle chat
      this.toggle.onclick = () => this.toggleChat();
      this.closeBtn.onclick = () => this.toggleChat();

      // Send message
      this.sendBtn.onclick = () => this.sendMessage();
      this.input.onkeypress = (e) => {
        if (e.key === "Enter") {
          this.sendMessage();
        }
      };
    }

    toggleChat() {
      this.isOpen = !this.isOpen;
      this.box.classList.toggle("open", this.isOpen);

      if (this.isOpen) {
        this.input.focus();
      }
    }

    addMessage(text, isUser = false, isAction = false) {
      const msgDiv = document.createElement("div");
      msgDiv.className = `chat-message ${isUser ? "user" : "bot"}`;

      const bubble = document.createElement("div");
      bubble.className = "message-bubble";

      if (isAction) {
        bubble.innerHTML = `<div class="action-message">${text}</div>`;
      } else {
        bubble.textContent = text;
      }

      msgDiv.appendChild(bubble);
      this.body.appendChild(msgDiv);

      // Scroll to bottom
      this.body.scrollTop = this.body.scrollHeight;
    }

    addTypingIndicator() {
      const indicator = document.createElement("div");
      indicator.className = "chat-message bot";
      indicator.id = "typing-indicator";
      indicator.innerHTML = `
        <div class="message-bubble">
          <div class="typing-dots">
            <span></span><span></span><span></span>
          </div>
        </div>
      `;
      this.body.appendChild(indicator);
      this.body.scrollTop = this.body.scrollHeight;
      return indicator;
    }

    removeTypingIndicator() {
      const indicator = document.getElementById("typing-indicator");
      if (indicator) {
        indicator.remove();
      }
    }

    async sendMessage() {
      const text = this.input.value.trim();
      if (!text) return;

      // Hiển thị tin nhắn người dùng
      this.addMessage(text, true);
      this.input.value = "";

      // Hiển thị typing indicator
      const typingIndicator = this.addTypingIndicator();

      try {
        const response = await rpc.query({
          route: "/chat/send",
          params: { message: text },
        });

        // Xóa typing indicator
        this.removeTypingIndicator();

        // Hiển thị phản hồi
        this.addMessage(response.reply, false, response.type === "action");

        // Nếu là action, thực hiện điều hướng
        if (response.type === "action" && response.action) {
          setTimeout(() => {
            this.executeAction(response.action);
          }, 800);
        }
      } catch (error) {
        this.removeTypingIndicator();
        this.addMessage("❌ Đã có lỗi xảy ra. Vui lòng thử lại!", false);
        console.error("Chat error:", error);
      }
    }

    executeAction(actionXmlId) {
      console.log("Executing action:", actionXmlId);

      // Lấy action từ server bằng XML ID
      rpc
        .query({
          route: "/web/action/load",
          params: {
            action_id: actionXmlId,
          },
        })
        .then((action) => {
          if (action) {
            console.log("Action loaded:", action);
            this.doAction(action);
          } else {
            console.error("Action not found:", actionXmlId);
            this.addMessage("❌ Không tìm thấy trang này!", false);
          }
        })
        .catch((error) => {
          console.error("Error loading action:", error);

          // Thử cách khác: Tìm menu item và click
          this.tryOpenByMenu(actionXmlId);
        });
    }

    doAction(action) {
      console.log("Do action:", action);

      try {
        // Method 1: Sử dụng web client
        if (typeof require !== "undefined") {
          const webClient = require("web.web_client");
          if (webClient && webClient.do_action) {
            console.log("Using web_client.do_action");
            webClient.do_action(action);
            return;
          }
        }

        // Method 2: Sử dụng action service từ OWL
        const actionManager = document.querySelector(".o_action_manager");
        if (actionManager && actionManager.__owl__) {
          const actionService =
            actionManager.__owl__.component.env.services.action;
          if (actionService && actionService.doAction) {
            console.log("Using OWL action service");
            actionService.doAction(action);
            return;
          }
        }

        // Method 3: Fallback - Navigate bằng URL
        console.log("Using URL fallback");
        const url = `/web#action=${action.id}&model=${action.res_model}&view_type=${action.view_mode.split(",")[0]}`;
        window.location.href = url;
      } catch (error) {
        console.error("Error in doAction:", error);
        this.addMessage("❌ Không thể mở trang. Vui lòng thử lại!", false);
      }
    }

    tryOpenByMenu(actionXmlId) {
      // Tìm và click vào menu item tương ứng
      console.log("Trying to open by menu:", actionXmlId);

      // Map action ID to menu text
      const menuMap = {
        action_nhan_vien: "Quản lý nhân viên",
        action_phong_ban: "Danh mục phòng ban",
        action_chuc_vu: "Danh mục chức vụ",
        action_chung_chi: "Danh mục chứng chỉ",
        action_lich_su_cong_tac: "Quản lý lịch sử công tác",
      };

      const menuText = menuMap[actionXmlId];
      if (menuText) {
        // Tìm tất cả menu items
        const menuItems = document.querySelectorAll(
          ".o_menu_sections a, .o_menu_sections button",
        );
        for (let item of menuItems) {
          if (item.textContent.trim().includes(menuText)) {
            console.log("Found menu item, clicking:", item);
            item.click();
            return;
          }
        }
      }

      this.addMessage("❌ Không thể mở trang này. Vui lòng thử lại!", false);
    }
  }

  // Khởi tạo khi DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      new ChatAssistant();
    });
  } else {
    new ChatAssistant();
  }
});
