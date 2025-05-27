from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication


class ThemeManager(QObject):
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
      "slider": {"handle": "#FFFFFF", "sub-page": "#0066B4", "add-page": "#8A8A8A", "disabled": "#8A8A8A"},
      "scrollbar": {"handle": "#8A8A8A", "bg": "#FFFFFF", "handle_border": "#C4C4C4"},
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
      "slider": {"handle": "#454545", "sub-page": "#4CA0E0", "add-page": "#A2A2A2", "disabled": "#A2A2A2"},
      "scrollbar": {"handle": "#9F9F9F", "bg": "#2C2C2C", "handle_border": "#656565"},
  }

  def __init__(self):
    super().__init__()
    self.current_theme = self.LIGHT_THEME
    self.sync_system_theme()
    self._init_styles()
    self.style_sheet = ""
    self.apply_theme()

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

  def set_theme(self, target_theme):
    app = QApplication.instance()
    if not app:
      return
    if target_theme == 'light':
      self.current_theme = self.LIGHT_THEME
      app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    elif target_theme == 'dark':
      self.current_theme = self.DARK_THEME
      app.styleHints().setColorScheme(Qt.ColorScheme.Dark)

    self.apply_theme()

  def apply_theme(self):
    app = QApplication.instance()
    if not app:
      return
    # 应用调色板和样式表
    self._update_palette(app)
    self.style_sheet = self._build_style_sheet()
    app.setStyleSheet(self.style_sheet)

  def get_current_sys_theme(self, app):
    return app.styleHints().colorScheme()

  def sync_system_theme(self):
    app = QApplication.instance()
    if not app:
      return
    theme = self.get_current_sys_theme(app)
    if theme == Qt.ColorScheme.Light:
      self.current_theme = self.LIGHT_THEME
    elif theme == Qt.ColorScheme.Dark:
      self.current_theme = self.DARK_THEME

  def _update_palette(self, app):
    """更新基础窗口和文本颜色"""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(
        self.current_theme["window_bg"]))
    palette.setColor(QPalette.WindowText, QColor(
        self.current_theme["text"]))
    palette.setColor(QPalette.Link, QColor("#1A73E8"))
    app.setPalette(palette)

  def _build_style_sheet(self):
    """结构化构建完整样式表"""
    btn = self.current_theme["button"]
    sidebar_btn = self.current_theme["button_sidebar"]
    slider = self.current_theme["slider"]
    input_display = self.current_theme["input_display"]
    sidebar_border = self.current_theme["sidebar_border"]
    btn_silver = self.current_theme["button_silver"]
    scrollbar = self.current_theme["scrollbar"]

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
            QPushButton#morseDecoder {{
                border: 1px solid {sidebar_border};
                border-radius: 4px;
                padding: 8px 12px;
                {self.styles["button"]["normal"].format(**btn["normal"])}
            }}
            QPushButton#morseDecoder:hover {{ {self.styles["button"]["hovered"].format(**btn["hovered"])} }}
            QPushButton#morseDecoder:pressed {{ {self.styles["button"]["pressed"].format(**btn["pressed"])} }}
            QPushButton#morseDecoder:disabled {{ {self.styles["button"]["disabled"].format(**btn["disabled"])} }}

            /* 侧边栏按钮样式 */
            QWidget#sidebar QPushButton {{
                border: none;
                border-radius: 4px;
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
            QPushButton#silver {{
                background-color: {btn_silver["normal"]["unchecked"]};
                border-radius: 4px;
                border-width: 2px;
                border-style: solid;
            }}
            
            QPushButton#silver:hover {{
                background-color: {btn_silver["hovered"]["unchecked"]};
            }}
            
            QPushButton#silver:pressed {{
                background-color: {btn_silver["pressed"]["unchecked"]};
            }}
            
            /* 选中状态样式 */
            QPushButton#silver:checked {{
                background-color: {btn_silver["normal"]["checked"]};
            }}
            
            QPushButton#silver:checked:hover {{
                background-color: {btn_silver["hovered"]["checked"]};
            }}
            
            QPushButton#silver:checked:pressed {{
                background-color: {btn_silver["pressed"]["checked"]};
            }}
            
            /* 根据 layer 属性设置不同的边框颜色 */
            QPushButton#silver[layer="0"] {{ border-color: {btn_silver["border"][0]}; }}
            QPushButton#silver[layer="1"] {{ border-color: {btn_silver["border"][1]}; }}
            QPushButton#silver[layer="2"] {{ border-color: {btn_silver["border"][2]}; }}
            QPushButton#silver[layer="3"] {{ border-color: {btn_silver["border"][3]}; }}
            
            /* 选中状态下保持边框颜色不变 */
            QPushButton#silver:checked[layer="0"] {{ border-color: {btn_silver["border"][0]}; }}
            QPushButton#silver:checked[layer="1"] {{ border-color: {btn_silver["border"][1]}; }}
            QPushButton#silver:checked[layer="2"] {{ border-color: {btn_silver["border"][2]}; }}
            QPushButton#silver:checked[layer="3"] {{ border-color: {btn_silver["border"][3]}; }}

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
                border-bottom: 1px solid {input_display["focus_border_color"]};
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



            QScrollBar:vertical {{
                background-color: {scrollbar["bg"]};
                width: 6px;
            }}

            QScrollBar::handle:vertical {{
                background-color: {scrollbar["handle"]};
                width: 5px;
                border-radius: 3px;
                border: 1px solid {scrollbar["handle_border"]};
            }}

            QScrollBar::handle:vertical:hover {{
                background-color: {scrollbar["handle"]};
            }}

            QScrollBar::sub-page:vertical, QScrollBar::add-page:vertical {{
                background-color: {scrollbar["bg"]};
            }}

            

            QSlider::groove:horizontal {{
                border: 0px solid #bbb;
                height: 5px; 
                border-radius: 2px;
            }}
            QSlider::sub-page:horizontal {{
                background: {slider["sub-page"]};
                border-radius: 2px;
                margin-top: 0px;
                margin-bottom: 0px;
            }}
            QSlider::add-page:horizontal {{
                background: {slider["add-page"]};
                border: 0px solid #777; 
                border-radius: 2px; 
                margin-top: 0px; 
                margin-bottom: 0px;   
            }}
            QSlider::handle:horizontal {{
                background: {slider["handle"]}; 
                border: 1px solid rgba(102,102,102,102); 
                width: 11px; 
                height: 11px;
                border-radius: 6px; 
                margin-top: -4px;   
                margin-bottom: -4px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {slider["sub-page"]}; 
                border: 1px solid rgba(102,102,102,102); 
            }}
            QSlider::sub-page:horizontal:disabled {{
                background: {slider["disabled"]}; 
                border-color: #999; 
            }}
            QSlider::add-page:horizontal:disabled {{
                background: {slider["disabled"]}; 
                border-color: #999; 
            }}
            QSlider::handle:horizontal:disabled {{
                background: #eee; 
            }}
                        
        """
