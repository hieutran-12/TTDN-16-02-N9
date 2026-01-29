/** @odoo-module **/

odoo.define("ai_chat_assistant.chat_widget", function (require) {
  "use strict";

  const core = require("web.core");
  const QWeb = core.qweb;

  class ChatWidget {
    constructor() {
      this.apiEndpoint = "/ai/chat";
      this.isMinimized = false;
      this.chatHistory = [];
      this.init();
    }

    init() {
      // Render template
      const template = QWeb.render("ai_chat_assistant.chat_widget");
      this.$widget = $(template);

      // Inject into body
      document.body.appendChild(this.$widget[0]);

      // Setup event listeners
      this.setupEventListeners();
      this.loadChatHistory();
    }

    setupEventListeners() {
      const self = this;

      // Send button click
      this.$widget.find("#sendBtn").on("click", () => self.sendMessage());

      // Enter key to send
      this.$widget.find("#chatInput").on("keypress", (e) => {
        if (e.which === 13 && !e.shiftKey) {
          e.preventDefault();
          self.sendMessage();
        }
      });

      // Auto-resize textarea
      this.$widget.find("#chatInput").on("input", function () {
        this.style.height = "auto";
        this.style.height = Math.min(this.scrollHeight, 100) + "px";
      });

      // Minimize/Maximize
      this.$widget
        .find("#minimizeBtn")
        .on("click", () => self.toggleMinimize());

      // Close
      this.$widget.find("#closeBtn").on("click", () => self.closeWidget());

      // Header click to toggle
      this.$widget.find("#chatHeader").on("click", (e) => {
        if (!$(e.target).closest("button").length) {
          self.toggleMinimize();
        }
      });
    }

    sendMessage() {
      const message = this.$widget.find("#chatInput").val().trim();

      if (!message) return;

      // Add user message to UI
      this.addMessageToUI("user", message);
      this.$widget.find("#chatInput").val("").css("height", "auto");

      // Show loading indicator
      this.addMessageToUI("ai", "⏳ Đang xử lý...");

      // Send to server
      this.sendToServer(message)
        .then((response) => {
          // Remove loading message
          this.$widget.find("#chatMessages .chat-message:last").remove();

          if (response.success) {
            this.addMessageToUI("ai", response.response, {
              method: response.method,
              confidence: response.confidence_score,
              processingTime: response.processing_time_ms,
            });
            this.chatHistory.push({
              role: "user",
              content: message,
              timestamp: new Date(),
            });
            this.chatHistory.push({
              role: "ai",
              content: response.response,
              timestamp: new Date(),
            });
          } else {
            this.addMessageToUI("ai", `❌ Lỗi: ${response.error}`);
          }
        })
        .catch((error) => {
          this.$widget.find("#chatMessages .chat-message:last").remove();
          this.addMessageToUI("ai", `❌ Lỗi kết nối: ${error}`);
        });
    }

    addMessageToUI(role, content, metadata) {
      const $container = this.$widget.find("#chatMessages");
      const isUser = role === "user";
      const avatar = isUser ? "👤" : "🤖";
      const className = isUser ? "message-user" : "message-ai";
      const now = new Date();
      const timeStr = now.toLocaleTimeString("vi-VN", {
        hour: "2-digit",
        minute: "2-digit",
      });

      let html = `
                <div class="chat-message ${className}">
                    <div class="message-avatar">${avatar}</div>
                    <div>
                        <div class="message-content">${this.escapeHtml(content)}</div>
                        <div class="message-time">${timeStr}</div>
            `;

      // Add metadata if provided
      if (metadata && !isUser) {
        let status = "✓";
        if (metadata.method === "fallback") {
          status = "⚠️";
        }
        html += `<div class="message-status" style="font-size: 11px; color: #6b7280; margin-top: 4px;">
                    ${status} Phương pháp: ${metadata.method} | Độ tin cậy: ${metadata.confidence.toFixed(1)}% | Thời gian: ${metadata.processingTime}ms
                </div>`;
      }

      html += `
                    </div>
                </div>
            `;

      $container.append(html);

      // Auto-scroll to bottom
      $container.scrollTop($container.prop("scrollHeight"));
    }

    sendToServer(message) {
      return $.ajax({
        url: this.apiEndpoint,
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
          message: message,
        }),
        dataType: "json",
      });
    }

    loadChatHistory() {
      const self = this;
      $.ajax({
        url: "/ai/chat/history?limit=5",
        type: "GET",
        dataType: "json",
        success: (response) => {
          if (response.success && response.data.length > 0) {
            // Clear default welcome message
            self.$widget.find("#chatMessages").empty();

            // Load history (reverse to show oldest first)
            response.data.reverse().forEach((log) => {
              self.addMessageToUI("user", log.message);
              self.addMessageToUI("ai", log.response, {
                method: log.method,
                confidence: log.confidence_score,
                processingTime: log.processing_time_ms,
              });
            });
          }
        },
        error: () => {
          // Keep default message if history load fails
        },
      });
    }

    toggleMinimize() {
      const $widget = this.$widget.find(".ai-chat-widget");
      this.isMinimized = !this.isMinimized;

      if (this.isMinimized) {
        $widget.addClass("minimized");
        this.$widget.find("#chatHeader h3").text("💬");
      } else {
        $widget.removeClass("minimized");
        this.$widget.find("#chatHeader h3").text("🤖 AI Assistant");
      }
    }

    closeWidget() {
      this.$widget.fadeOut(300, () => {
        this.$widget.remove();
      });
    }

    escapeHtml(text) {
      const map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
      };
      return text.replace(/[&<>"']/g, (m) => map[m]);
    }
  }

  // Auto-initialize widget on page load
  $(document).ready(function () {
    if (odoo.session && odoo.session.uid) {
      new ChatWidget();
    }
  });

  return ChatWidget;
});
