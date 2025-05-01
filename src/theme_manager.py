from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication


class ThemeManager(QObject):
  theme_changed = Signal(str)  # 主题变更信号

  LIGHT_THEME = {
      "name": "light",
      "window_bg": "#F3F3F3",
      "text": "#070707",
      "sidebar_border": "#E0E0E0",
      "button": {
          "normal":   {"bg": "#FEFEFE", "fg": "#101010"},
          "hovered":  {"bg": "#F6F6F6", "fg": "#0F0F0F"},
          "pressed":  {"bg": "#F6F6F6", "fg": "#696969"},
          "disabled": {"bg": "#FBFBFB", "fg": "#B8A5A7"},
      },
      "button_silver": {
          "normal": {"unchecked": "#f0f0f0", "checked": "#0078D4"},
          "hovered": {"unchecked": "#e0e0e0", "checked": "#006CBD"},
          "pressed": {"unchecked": "#d0d0d0", "checked": "#005aaa"},
          "border": ["#EC1B23", "#FB7E29", "#EAAE00", "#21B04B"]
      },
      "button_sidebar": {
          "normal":   {"bg": "#F3F3F3", "fg": "#070707"},
          "hovered":  {"bg": "#EBEBEB", "fg": "#070707"},
          "pressed":  {"bg": "#DDDDDD", "fg": "#7B7977"},
          "checked":  {"bg": "#DDDDDD", "fg": "#070707"},
      },
      "input_display": {"bg": "#FFFFFF", "fg": "#070707", "placeholder": "#AB95A0", "focus_border_color": "#0066B4"},
      "slider": {"active": "#0066B4", "inactive": "#8A8A8A", "disabled": "#8A8A8A"},
  }

  DARK_THEME = {
      "name": "dark",
      "window_bg": "#1A1A1A",
      "text": "#E0E0E0",
      "sidebar_border": "#303030",
      "button": {
          "normal":   {"bg": "#3E3E3E", "fg": "#F3F3F3"},
          "hovered":  {"bg": "#444444", "fg": "#F4F5F8"},
          "pressed":  {"bg": "#444444", "fg": "#A1A1A1"},
          "disabled": {"bg": "#3B3B3B", "fg": "#7E7E7E"},
      },
      "button_silver": {
          "normal": {"unchecked": "#303030", "checked": "#4CA0E0"},
          "hovered": {"unchecked": "#3a3a3a", "checked": "#64b5f6"},
          "pressed": {"unchecked": "#404040", "checked": "#90caf9"},
          "border": ["#EC1B23", "#FB7E29", "#EAAE00", "#21B04B"]
      },
      "button_sidebar": {
          "normal":   {"bg": "#1A1A1A", "fg": "#F8F8F8"},
          "hovered":  {"bg": "#272727", "fg": "#F8F8F8"},
          "pressed":  {"bg": "#363636", "fg": "#B0ADAA"},
          "checked":  {"bg": "#363636", "fg": "#F8F8F8"},
      },
      "input_display": {"bg": "#3E3E3E", "fg": "#F8F8F8", "placeholder": "#959595", "focus_border_color": "#4CA0E0"},
      "slider": {"active": "#4CA0E0", "inactive": "#A2A2A2", "disabled": "#A2A2A2"},
  }

  def __init__(self):
    super().__init__()
    self.current_theme = self.LIGHT_THEME
    self._init_styles()
    self.style_sheet = ""
    self._apply_theme()  # 初始化时立即应用主题

  def _init_styles(self):
    """预处理样式结构，避免重复字符串拼接"""
    self.styles = {
        "button": {
            "normal": "background-color: {bg}; color: {fg};",
            "hovered": "background-color: {bg}; color: {fg};",
            "pressed": "background-color: {bg}; color: {fg};",
            "disabled": "background-color: {bg}; color: {fg};",
        },
        "button_sidebar": {
            "normal": "background-color: {bg}; color: {fg};",
            "hovered": "background-color: {bg}; color: {fg};",
            "pressed": "background-color: {bg}; color: {fg};",
            "checked": "background-color: {bg}; color: {fg}; font-weight: 600;",
        },
        "button_silver": {
            "normal": "background-color: {unchecked};",
            "hovered": "background-color: {unchecked};",
            "pressed": "background-color: {unchecked};",
            "checked_normal": "background-color: {checked};",
            "checked_hovered": "background-color: {checked};",
            "checked_pressed": "background-color: {checked};",
            "border": "border: 1px solid {border};",
        },
        "theme_button": "border: 1px solid {sidebar_border};",
        "input_display": "background-color: {bg}; color: {fg};",
    }

  def apply_light_theme(self):
    self.current_theme = self.LIGHT_THEME
    self._apply_theme()
    self.theme_changed.emit("light")

  def apply_dark_theme(self):
    self.current_theme = self.DARK_THEME
    self._apply_theme()
    self.theme_changed.emit("dark")

  def toggle_theme(self):
    self.current_theme = self.DARK_THEME if self.current_theme[
        "name"] == "light" else self.LIGHT_THEME
    self._apply_theme()
    self.theme_changed.emit(self.current_theme["name"])

  def _apply_theme(self):
    app = QApplication.instance()
    if not app:
      return

    self._update_palette(app)
    self.style_sheet = self._build_style_sheet()  # 生成并保存样式表
    app.setStyleSheet(self.style_sheet)

  def _update_palette(self, app):
    """更新基础窗口和文本颜色"""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(
        self.current_theme["window_bg"]))
    palette.setColor(QPalette.WindowText, QColor(
        self.current_theme["text"]))
    app.setPalette(palette)

  def _build_style_sheet(self):
    """结构化构建完整样式表"""
    btn = self.current_theme["button"]
    sidebar_btn = self.current_theme["button_sidebar"]
    slider = self.current_theme["slider"]
    input_display = self.current_theme["input_display"]
    sidebar_border = self.current_theme["sidebar_border"]
    btn_silver = self.current_theme["button_silver"]

    return f"""
            /* 全局基础样式 */
            QWidget {{
                font-family: 'Microsoft YaHei', sans-serif;
                color: {self.current_theme["text"]};
            }}

            /* 侧边栏样式 */
            QWidget#sidebar {{
                background-color: {self.current_theme["window_bg"]};
                border-right: 1px solid {self.current_theme["sidebar_border"]};
            }}

            /* 普通按钮样式 */
            QPushButton {{
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                height: 40px;
                {self.styles["button"]["normal"].format(**btn["normal"])}
            }}
            QPushButton:hover {{ {self.styles["button"]["hovered"].format(**btn["hovered"])} }}
            QPushButton:pressed {{ {self.styles["button"]["pressed"].format(**btn["pressed"])} }}
            QPushButton:disabled {{ {self.styles["button"]["disabled"].format(**btn["disabled"])} }}

            /* 侧边栏按钮样式 */
            QWidget#sidebar QPushButton {{
                padding: 12px 16px;
                text-align: left;
                height: 40px;
                font-size: 14px;
                {self.styles["button_sidebar"]["normal"].format(**sidebar_btn["normal"])}
            }}
            QWidget#sidebar QPushButton:hover {{
                {self.styles["button_sidebar"]["hovered"].format(**sidebar_btn["hovered"])}
            }}
            QWidget#sidebar QPushButton:pressed {{
                {self.styles["button_sidebar"]["pressed"].format(**sidebar_btn["pressed"])}
            }}
            QWidget#sidebar QPushButton:checked {{
                {self.styles["button_sidebar"]["checked"].format(**sidebar_btn["checked"])}
            }}

            /* 银色按钮样式（无文本，双状态） */
            QPushButton.silver {{
                background-color: {btn_silver["normal"]["unchecked"]};
                border-radius: 4px;
                border-width: 2px;
                border-style: solid;
            }}
            
            QPushButton.silver:hover {{
                background-color: {btn_silver["hovered"]["unchecked"]};
            }}
            
            QPushButton.silver:pressed {{
                background-color: {btn_silver["pressed"]["unchecked"]};
            }}
            
            /* 选中状态样式 */
            QPushButton.silver:checked {{
                background-color: {btn_silver["normal"]["checked"]};
            }}
            
            QPushButton.silver:checked:hover {{
                background-color: {btn_silver["hovered"]["checked"]};
            }}
            
            QPushButton.silver:checked:pressed {{
                background-color: {btn_silver["pressed"]["checked"]};
            }}
            
            /* 根据 layer 属性设置不同的边框颜色 */
            QPushButton.silver[layer="0"] {{ border-color: {btn_silver["border"][0]}; }}
            QPushButton.silver[layer="1"] {{ border-color: {btn_silver["border"][1]}; }}
            QPushButton.silver[layer="2"] {{ border-color: {btn_silver["border"][2]}; }}
            QPushButton.silver[layer="3"] {{ border-color: {btn_silver["border"][3]}; }}
            
            /* 选中状态下保持边框颜色不变 */
            QPushButton.silver:checked[layer="0"] {{ border-color: {btn_silver["border"][0]}; }}
            QPushButton.silver:checked[layer="1"] {{ border-color: {btn_silver["border"][1]}; }}
            QPushButton.silver:checked[layer="2"] {{ border-color: {btn_silver["border"][2]}; }}
            QPushButton.silver:checked[layer="3"] {{ border-color: {btn_silver["border"][3]}; }}

            /* 主题切换按钮样式 */
            QPushButton#themeButton {{
                text-align: center;
                font-size: 13px;
                margin: 10px;
                padding: 6px 12px;
                {self.styles["theme_button"].format(**self.current_theme)}
                border-radius: 4px;
            }}

            /* 输入框样式 */
            QLineEdit {{
                {self.styles["input_display"].format(**input_display)}
                border: 1px solid {self.current_theme["sidebar_border"]};
                border-radius: 4px;
                padding: 6px;
            }}
            QLineEdit:focus {{
                border-bottom: 2px solid {input_display["focus_border_color"]};
            }}

            /* 滑块样式 */
            QSlider::groove:horizontal {{
                border: 1px solid {self.current_theme["sidebar_border"]};
                height: 8px;
                background: {slider["inactive"]};
                margin: 2px 0;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {slider["active"]};
                border: 1px solid {self.current_theme["sidebar_border"]};
                width: 18px;
                margin: -2px 0;
                border-radius: 4px;
            }}
            QSlider::groove:horizontal:disabled {{
                background: {slider["disabled"]};
            }}
            QSlider::handle:horizontal:disabled {{
                background: {slider["disabled"]};
            }}

            /* markdown区域样式 */
            QTextBrowser#markdownBrowser {{
                background-color: {self.current_theme["window_bg"]};
                color:{self.current_theme["text"]};
                border: none;
            }}

            /* 仅对 text_display 组件生效的只读文本区域样式 */
            QTextEdit#readOnlyTextDisplay[readOnly="true"] {{
                background-color: {input_display["bg"]};
                color: {input_display["fg"]};
                border: 1px solid {sidebar_border};
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
                line-height: 1.5;
            }}
            
            QTextEdit#readOnlyTextDisplay[readOnly="true"]:focus {{
                border: 1px solid {self.current_theme["button_silver"]["normal"]["checked"]};
            }}

            /* QComboBox 主样式 */
            QComboBox {{
                {self.styles["button"]["normal"].format(**btn["normal"])}
                border: 1px solid {sidebar_border};
                border-radius: 6px;
                padding: 12px 16px;
                text-align: left;
            }}
            
            QComboBox:hover {{
                {self.styles["button"]["hovered"].format(**btn["hovered"])}
            }}
            
            QComboBox:on {{
                {self.styles["button"]["pressed"].format(**btn["pressed"])}
            }}
            
            QComboBox:disabled {{
                {self.styles["button"]["disabled"].format(**btn["disabled"])}
            }}
            
            /* 下拉箭头样式 */
            QComboBox::drop-down {{
                width: 20px;
                border:none;
            }}
            
            /* 下拉列表样式 */
            QComboBox QAbstractItemView {{
                background-color: {btn["normal"]["bg"]};
                color: {btn["normal"]["fg"]};
                border: 1px solid {sidebar_border};
                border-radius: 6px;
                padding: 4px;
                selection-background-color: {self.current_theme["button_silver"]["normal"]["checked"]};
                selection-color: white;
                outline: none;
            }}
            
            /* 下拉列表项样式 */
            QComboBox QAbstractItemView::item {{
                padding: 12px 16px;
                border-radius: 4px;
                height: 20px;
            }}
            
            QComboBox QAbstractItemView::item:selected {{
                background-color: {self.current_theme["button_silver"]["normal"]["checked"]};
                color: white;
            }}
        """
