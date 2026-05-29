from settings_window.constants import *
from settings_window.widgets import *
from settings_window.workers import *


class ChatIntegrationPageMixin:

    def _build_chat_integration_page(self):
        page = self._make_theme_widget(QWidget())
        page.setObjectName("chatIntegrationPage")
        page.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        title = TitleLabel(_tr("SettingsWindow.chat_integration_title", default="聊天接入"), page)
        layout.addWidget(title)
        subtitle = SubtitleLabel(_tr(
            "SettingsWindow.chat_integration_subtitle",
            default="接收外部聊天软件或脚本推送的消息，写入本地上下文，并在桌宠悬浮窗显示未读摘要。",
        ), page)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        self._chat_integration_enabled = SwitchButton(page)
        self._add_switch_row(
            layout,
            page,
            _tr("SettingsWindow.chat_integration_enabled", default="启用本地聊天接入端口"),
            self._chat_integration_enabled,
        )

        self._chat_integration_overlay_enabled = SwitchButton(page)
        self._add_switch_row(
            layout,
            page,
            _tr("SettingsWindow.chat_integration_overlay_enabled", default="收到消息时显示悬浮窗摘要"),
            self._chat_integration_overlay_enabled,
        )

        self._chat_integration_include_context = SwitchButton(page)
        self._add_switch_row(
            layout,
            page,
            _tr("SettingsWindow.chat_integration_include_context", default="允许模型读取最近外部聊天上下文"),
            self._chat_integration_include_context,
        )

        layout.addWidget(SubtitleLabel(_tr(
            "SettingsWindow.chat_integration_quick_setup",
            default="快速配置",
        ), page))

        endpoint_row = QHBoxLayout()
        endpoint_row.setContentsMargins(0, 0, 0, 0)
        endpoint_row.setSpacing(8)
        self._chat_integration_endpoint_input = FluentContextLineEdit(page)
        self._chat_integration_endpoint_input.setReadOnly(True)
        self._chat_integration_endpoint_input.setFixedHeight(36)
        copy_endpoint_btn = PushButton(FluentIcon.COPY, _tr(
            "SettingsWindow.chat_integration_copy_endpoint",
            default="复制地址",
        ), page)
        copy_endpoint_btn.clicked.connect(self._copy_chat_integration_endpoint)
        endpoint_row.addWidget(BodyLabel(_tr(
            "SettingsWindow.chat_integration_endpoint",
            default="接收地址",
        ), page))
        endpoint_row.addWidget(self._chat_integration_endpoint_input, 1)
        endpoint_row.addWidget(copy_endpoint_btn)
        layout.addLayout(endpoint_row)

        config_row = QHBoxLayout()
        config_row.setContentsMargins(0, 0, 0, 0)
        config_row.setSpacing(8)
        self._chat_integration_port_input = LineEdit(page)
        self._chat_integration_port_input.setFixedWidth(120)
        self._chat_integration_port_input.setFixedHeight(36)
        self._chat_integration_port_input.setValidator(QIntValidator(1024, 65535, self))
        self._chat_integration_port_input.setPlaceholderText("38473")
        token_label = BodyLabel(_tr("SettingsWindow.chat_integration_token", default="Token"), page)
        self._chat_integration_token_input = LineEdit(page)
        self._chat_integration_token_input.setFixedHeight(36)
        self._chat_integration_token_input.setPlaceholderText(_tr(
            "SettingsWindow.chat_integration_token_placeholder",
            default="可留空；给第三方脚本使用时建议填写",
        ))
        generate_token_btn = PushButton(FluentIcon.SYNC, _tr(
            "SettingsWindow.chat_integration_generate_token",
            default="生成 Token",
        ), page)
        generate_token_btn.clicked.connect(self._generate_chat_integration_token)
        copy_token_btn = PushButton(FluentIcon.COPY, _tr(
            "SettingsWindow.chat_integration_copy_token",
            default="复制 Token",
        ), page)
        copy_token_btn.clicked.connect(self._copy_chat_integration_token)
        config_row.addWidget(BodyLabel(_tr("SettingsWindow.chat_integration_port_number", default="端口"), page))
        config_row.addWidget(self._chat_integration_port_input)
        config_row.addSpacing(12)
        config_row.addWidget(token_label)
        config_row.addWidget(self._chat_integration_token_input, 1)
        config_row.addWidget(generate_token_btn)
        config_row.addWidget(copy_token_btn)
        layout.addLayout(config_row)

        hint = BodyLabel(_tr(
            "SettingsWindow.chat_integration_hint",
            default="开启后监听 127.0.0.1，可接收 JSON、表单、纯文本或 URL 参数。外部消息会进入本地数据库；开启上下文后，下一次角色聊天会看到最近消息。",
        ), page)
        hint.setWordWrap(True)
        layout.addWidget(hint)

        self._chat_integration_preview = JsonCodeEdit(page)
        self._chat_integration_preview.setReadOnly(True)
        self._chat_integration_preview.setFixedHeight(170)
        layout.addWidget(self._chat_integration_preview)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(0, 0, 0, 0)
        save_btn = PrimaryPushButton(FluentIcon.ACCEPT, _tr("SettingsWindow.chat_integration_save", default="保存聊天接入配置"), page)
        save_btn.clicked.connect(lambda: self._save_chat_integration_config(show_info=True, emit_update=True))
        copy_setup_btn = PushButton(FluentIcon.COPY, _tr(
            "SettingsWindow.chat_integration_copy_setup",
            default="复制接入信息",
        ), page)
        copy_setup_btn.clicked.connect(self._copy_chat_integration_setup)
        test_btn = PushButton(FluentIcon.WIFI, _tr(
            "SettingsWindow.chat_integration_test",
            default="发送测试消息",
        ), page)
        test_btn.clicked.connect(self._test_chat_integration)
        guide_btn = PushButton(FluentIcon.INFO, _tr(
            "SettingsWindow.chat_integration_open_guide",
            default="打开教程",
        ), page)
        guide_btn.clicked.connect(self._open_chat_integration_guide)
        btn_row.addWidget(save_btn)
        btn_row.addWidget(copy_setup_btn)
        btn_row.addWidget(test_btn)
        btn_row.addWidget(guide_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        apply_hint = BodyLabel(_tr(
            "SettingsWindow.chat_integration_apply_hint",
            default="保存后会立即通知正在运行的桌宠刷新端口；如果没有启动桌宠，请启动后再测试。",
        ), page)
        apply_hint.setWordWrap(True)
        layout.addWidget(apply_hint)
        layout.addStretch()

        self._chat_integration_port_input.textChanged.connect(self._update_chat_integration_quick_setup)
        self._chat_integration_token_input.textChanged.connect(self._update_chat_integration_quick_setup)
        self._load_chat_integration_config()
        self._style_chat_integration_page(page)
        qconfig.themeChanged.connect(lambda: self._style_chat_integration_page(page))
        return page

    def _chat_integration_widgets_ready(self) -> bool:
        return all(
            hasattr(self, attr)
            for attr in (
                "_chat_integration_enabled",
                "_chat_integration_overlay_enabled",
                "_chat_integration_include_context",
                "_chat_integration_endpoint_input",
                "_chat_integration_port_input",
                "_chat_integration_token_input",
                "_chat_integration_preview",
            )
        )

    def _style_chat_integration_page(self, page: QWidget):
        dark = isDarkTheme()
        page_bg = _BG_DARK if dark else _BG_LIGHT
        text_border = "#4a4a4a" if dark else "#d8d8d8"
        input_bg = "#2b2b2b" if dark else "#ffffff"
        text = "#f7f7fb" if dark else "#1f2328"
        readonly_bg = "#242424" if dark else "#f8f8f8"
        page.setStyleSheet(f"""
            QWidget#chatIntegrationPage {{
                background: {page_bg};
            }}
            QLineEdit {{
                color: {text};
                background: {input_bg};
                border: 1px solid {text_border};
                border-radius: 6px;
                padding: 6px;
            }}
            QLineEdit[readOnly="true"] {{
                background: {readonly_bg};
            }}
            QPlainTextEdit#JsonCodeEdit {{
                color: {text};
                background: {readonly_bg};
                border: 1px solid {text_border};
                border-radius: 6px;
                padding-left: 0px;
                selection-background-color: {BANDORI_PRIMARY};
            }}
        """)
        self._refresh_theme_widget_styles(page)
        self._refresh_json_code_edit_theme(getattr(self, "_chat_integration_preview", None))

    def _chat_integration_endpoint_url(self) -> str:
        if self._chat_integration_widgets_ready():
            port = self._clamp_chat_integration_port(self._chat_integration_port_input.text())
        elif self._cfg:
            port = self._clamp_chat_integration_port(self._cfg.get("chat_integration_port", 38473))
        else:
            port = 38473
        return f"http://127.0.0.1:{port}/chat-events"

    def _chat_integration_sample_event(self) -> dict:
        return {
            "platform": "qq",
            "thread_id": "default",
            "thread_name": "接入测试",
            "sender_name": "测试用户",
            "text": "这是一条从聊天软件推送到 BandoriPet 的测试消息。",
        }

    def _chat_integration_setup_text(self) -> str:
        endpoint = self._chat_integration_endpoint_url()
        token = self._chat_integration_token_input.text().strip() if self._chat_integration_widgets_ready() else ""
        headers = "Content-Type: application/json"
        if token:
            headers += f"\nAuthorization: Bearer {token}"
        sample = json.dumps(self._chat_integration_sample_event(), ensure_ascii=False, indent=2)
        url_sample = (
            f"{endpoint}?platform=qq&thread_id=default&thread_name=接入测试"
            f"&sender_name=发送人&text=消息内容"
        )
        if token:
            url_sample += f"&token={token}"
        return "\n".join([
            "BandoriPet 聊天接入信息",
            f"接收地址: {endpoint}",
            "请求方式: POST（推荐）或 GET URL 参数；支持 JSON、表单和纯文本正文",
            headers,
            "",
            "最小 JSON:",
            sample,
            "",
            "URL 参数模式:",
            url_sample,
            "",
            "字段对应：text=消息内容，sender_name=发送人，thread_name=群聊/私聊名称。",
        ])

    def _update_chat_integration_quick_setup(self, *_args):
        if not self._chat_integration_widgets_ready():
            return
        self._chat_integration_endpoint_input.setText(self._chat_integration_endpoint_url())
        self._chat_integration_preview.setPlainText(self._chat_integration_setup_text())

    def _copy_chat_integration_endpoint(self):
        if not self._chat_integration_widgets_ready():
            return
        QApplication.clipboard().setText(self._chat_integration_endpoint_url())
        InfoBar.success(
            _tr("SettingsWindow.chat_integration_endpoint_copied_title", default="已复制"),
            _tr("SettingsWindow.chat_integration_endpoint_copied_content", default="聊天接入地址已复制。"),
            duration=1600,
            position=InfoBarPosition.TOP,
            parent=self,
        )

    def _generate_chat_integration_token(self):
        if not self._chat_integration_widgets_ready():
            return
        self._chat_integration_token_input.setText(secrets.token_urlsafe(18))
        InfoBar.success(
            _tr("SettingsWindow.chat_integration_token_generated_title", default="已生成 Token"),
            _tr("SettingsWindow.chat_integration_token_generated_content", default="请保存配置后，把 Token 一起填到聊天软件或转发插件里。"),
            duration=2200,
            position=InfoBarPosition.TOP,
            parent=self,
        )

    def _copy_chat_integration_token(self):
        if not self._chat_integration_widgets_ready():
            return
        token = self._chat_integration_token_input.text().strip()
        if not token:
            InfoBar.warning(
                _tr("SettingsWindow.chat_integration_token_empty_title", default="没有 Token"),
                _tr("SettingsWindow.chat_integration_token_empty_content", default="当前 Token 为空，可以先点击\u201c生成 Token\u201d。"),
                duration=2200,
                position=InfoBarPosition.TOP,
                parent=self,
            )
            return
        QApplication.clipboard().setText(token)
        InfoBar.success(
            _tr("SettingsWindow.chat_integration_token_copied_title", default="已复制"),
            _tr("SettingsWindow.chat_integration_token_copied_content", default="Token 已复制。"),
            duration=1600,
            position=InfoBarPosition.TOP,
            parent=self,
        )

    def _copy_chat_integration_setup(self):
        if not self._chat_integration_widgets_ready():
            return
        QApplication.clipboard().setText(self._chat_integration_setup_text())
        InfoBar.success(
            _tr("SettingsWindow.chat_integration_setup_copied_title", default="已复制"),
            _tr("SettingsWindow.chat_integration_setup_copied_content", default="接入信息已复制，可直接粘贴到聊天软件的 Webhook/HTTP 配置里。"),
            duration=2200,
            position=InfoBarPosition.TOP,
            parent=self,
        )

    def _open_chat_integration_guide(self):
        path = os.path.join(app_base_dir(), "CHAT_INTEGRATION_GUIDE.md")
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def _test_chat_integration(self):
        if not self._chat_integration_widgets_ready():
            return
        if not self._chat_integration_enabled.isChecked():
            self._chat_integration_enabled.setChecked(True)
        self._save_chat_integration_config(show_info=False, emit_update=True)
        QTimer.singleShot(350, self._send_chat_integration_test_request)

    def _send_chat_integration_test_request(self):
        endpoint = self._chat_integration_endpoint_url()
        token = self._chat_integration_token_input.text().strip() if self._chat_integration_widgets_ready() else ""
        data = json.dumps(self._chat_integration_sample_event(), ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                body = resp.read(4096).decode("utf-8", errors="replace")
            payload = json.loads(body) if body else {}
            if isinstance(payload, dict) and payload.get("ok"):
                InfoBar.success(
                    _tr("SettingsWindow.chat_integration_test_success_title", default="测试成功"),
                    _tr("SettingsWindow.chat_integration_test_success_content", default="BandoriPet 已收到测试消息，悬浮摘要和上下文接入可用。"),
                    duration=2600,
                    position=InfoBarPosition.TOP,
                    parent=self,
                )
                return
            raise RuntimeError(body or "empty response")
        except urllib.error.HTTPError as exc:
            body = exc.read(4096).decode("utf-8", errors="replace")
            detail = body or str(exc)
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError, RuntimeError) as exc:
            detail = str(exc)
        InfoBar.error(
            _tr("SettingsWindow.chat_integration_test_failed_title", default="测试失败"),
            _tr(
                "SettingsWindow.chat_integration_test_failed_content",
                default="没有连上本地接入口。请确认桌宠正在运行，并已保存/应用聊天接入配置。错误：{error}",
                error=detail,
            ),
            duration=4500,
            position=InfoBarPosition.TOP,
            parent=self,
        )

    def _load_chat_integration_config(self):
        if not self._cfg or not self._chat_integration_widgets_ready():
            return
        self._chat_integration_enabled.setChecked(bool(self._cfg.get("chat_integration_enabled", False)))
        self._chat_integration_overlay_enabled.setChecked(bool(self._cfg.get("chat_integration_overlay_enabled", True)))
        self._chat_integration_include_context.setChecked(bool(self._cfg.get("chat_integration_include_context", True)))
        self._chat_integration_port_input.setText(str(self._clamp_chat_integration_port(self._cfg.get("chat_integration_port", 38473))))
        self._chat_integration_token_input.setText(str(self._cfg.get("chat_integration_token", "") or ""))
        self._update_chat_integration_quick_setup()

    def _chat_integration_settings_data(self) -> dict:
        if not self._cfg:
            return {}
        return {
            "chat_integration_enabled": self._cfg.get("chat_integration_enabled", False),
            "chat_integration_overlay_enabled": self._cfg.get("chat_integration_overlay_enabled", True),
            "chat_integration_include_context": self._cfg.get("chat_integration_include_context", True),
            "chat_integration_port": self._clamp_chat_integration_port(self._cfg.get("chat_integration_port", 38473)),
            "chat_integration_token": self._cfg.get("chat_integration_token", ""),
        }

    def _save_chat_integration_config(self, show_info: bool = True, emit_update: bool = False):
        if not self._cfg or not self._chat_integration_widgets_ready():
            return
        self._cfg.set("chat_integration_enabled", self._chat_integration_enabled.isChecked())
        self._cfg.set("chat_integration_overlay_enabled", self._chat_integration_overlay_enabled.isChecked())
        self._cfg.set("chat_integration_include_context", self._chat_integration_include_context.isChecked())
        self._cfg.set("chat_integration_port", self._clamp_chat_integration_port(self._chat_integration_port_input.text()))
        self._cfg.set("chat_integration_token", self._chat_integration_token_input.text().strip())
        try:
            self._cfg.save()
            if emit_update:
                self.settings_changed.emit(self._chat_integration_settings_data())
            if show_info:
                InfoBar.success(
                    _tr("SettingsWindow.chat_integration_saved_title", default="已保存"),
                    _tr("SettingsWindow.chat_integration_saved_content", default="聊天接入配置已保存。"),
                    duration=2000,
                    position=InfoBarPosition.TOP,
                    parent=self,
                )
        except Exception as exc:
            InfoBar.error(
                _tr("SettingsWindow.chat_integration_failed_title", default="保存失败"),
                str(exc),
                duration=3000,
                position=InfoBarPosition.TOP,
                parent=self,
            )

    @staticmethod
    def _clamp_ai_status_port(value) -> int:
        try:
            port = int(value)
        except (TypeError, ValueError):
            port = 38472
        return max(1024, min(65535, port))

    @staticmethod
    def _clamp_chat_integration_port(value) -> int:
        try:
            port = int(value)
        except (TypeError, ValueError):
            port = 38473
        return max(1024, min(65535, port))
