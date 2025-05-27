import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget,
                               QHBoxLayout, QVBoxLayout, QStackedWidget, QComboBox, QLabel)
from PySide6.QtCore import QTranslator, QLocale, QTimer
from theme_manager import ThemeManager
from pages import GoldPage, HomePage, LastPage, SkinPage, AngelPage, BeastPage, UsagePage, BronzePage, SilverPage
from components import audioAnalyzer
from methods import get_resource_path
from threading import Thread


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle(self.tr("维和者工具"))
    self.setMinimumSize(1280, 800)
    # self.showMaximized()

    self.warmup_started = False

    # 初始化翻译器
    self.translator = QTranslator()
    self.current_language = "zh_CN"  # 默认中文

    # 初始化主题管理器
    self.theme_manager = ThemeManager()

    # 创建主部件和布局
    main_widget = QWidget()
    self.setCentralWidget(main_widget)
    main_layout = QHBoxLayout(main_widget)
    main_layout.setContentsMargins(0, 0, 0, 0)

    # 创建侧边栏
    sidebar = QWidget()
    sidebar.setFixedWidth(220)
    sidebar.setObjectName("sidebar")
    sidebar_layout = QVBoxLayout(sidebar)
    sidebar_layout.setContentsMargins(10, 20, 10, 20)
    sidebar_layout.setSpacing(2)  # 保持原始间距

    # 创建页面堆栈
    self.stack = QStackedWidget()

    # 定义页面配置
    self.pages = [
        {"name": self.tr("首页"), "page_class": HomePage},
        {"name": self.tr("使用说明"), "page_class": UsagePage},
        {"name": self.tr("野兽之源"), "page_class": BeastPage},
        {"name": self.tr("看见天使"), "page_class": AngelPage},
        {"name": self.tr("逐步升级（皮肤）"), "page_class": SkinPage},
        {"name": self.tr("不祥之兆（金牌）"), "page_class": GoldPage},
        {"name": self.tr("冲突（银牌）"), "page_class": SilverPage},
        {"name": self.tr("初显身手（铜牌）"), "page_class": BronzePage},
        {"name": self.tr("维和者"), "page_class": LastPage}
    ]

    # 创建导航按钮（保持原始间距）
    self.buttons = []
    for i, page in enumerate(self.pages):
      btn = QPushButton(page["name"])
      btn.setCheckable(True)
      btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))
      sidebar_layout.addWidget(btn)
      self.buttons.append(btn)

      # 添加页面到堆栈
      self.stack.addWidget(page["page_class"]())

    # 添加间隔（关键修改点：在导航按钮和主题/语言按钮之间添加间隔）
    sidebar_layout.addStretch(1)

    self.warmup_label = QLabel(self.tr("正在预热摩斯电码分析模块..."))
    self.warmup_label.setFixedWidth(200)
    self.warmup_label.setWordWrap(True)
    self.warmup_label.setStyleSheet("padding-left: 5px;")
    # 0:warming 1:finished 2:failed
    self.warmup_label_status = 0
    sidebar_layout.addWidget(self.warmup_label)
    sidebar_layout.addSpacing(5)

    # 创建语言选择下拉框（替代原语言按钮）
    self.language_combo = QComboBox()
    self.language_combo.setFixedSize(200, 55)  # 保持与原按钮相同的尺寸
    self.language_combo.setObjectName("themeButton")  # 使用与主题按钮相同的样式

    self.language_combo.addItem("简体中文", "zh_CN")
    self.language_combo.addItem("繁體中文", "zh_TW")
    self.language_combo.addItem("English", "en_US")

    self.language_combo.currentIndexChanged.connect(self.change_language)
    sidebar_layout.addWidget(self.language_combo)
    sidebar_layout.addSpacing(6)

    # 创建主题选择下拉框（替代原主题按钮）
    self.theme_combo = QComboBox()
    self.theme_combo.setFixedSize(200, 55)  # 保持与原按钮相同的尺寸
    self.theme_combo.setObjectName("themeButton")

    # 添加主题选项
    self.theme_combo.addItem(self.tr("浅色模式"))
    self.theme_combo.addItem(self.tr("深色模式"))

    self.theme_combo.currentIndexChanged.connect(self.theme_combo_handler)
    sidebar_layout.addWidget(self.theme_combo)

    # 添加侧边栏和页面堆栈到主布局
    main_layout.addWidget(sidebar)
    main_layout.addWidget(self.stack)

    # 设置初始页面
    self.switch_page(0)

    # 设置初始主题和语言
    self.update_theme_combo()
    self.language_combo.setCurrentText("简体中文")  # 默认选择简体中文

  def switch_page(self, index):
    """切换当前显示的页面"""
    self.stack.setCurrentIndex(index)
    # 更新按钮状态
    for i, btn in enumerate(self.buttons):
      btn.setChecked(i == index)

  def change_language(self, index):
    """切换语言"""
    app = QApplication.instance()
    language_code = self.language_combo.currentData()

    # 移除当前翻译器
    if self.translator:
      app.removeTranslator(self.translator)

    # 加载新语言
    self.current_language = language_code
    qm_path = get_resource_path(f"{language_code}.qm")
    if self.translator.load(qm_path):
      app.installTranslator(self.translator)
    self.retranslate_ui()

  def retranslate_ui(self):
    """重新翻译所有UI元素"""
    # 更新窗口标题
    self.setWindowTitle(self.tr("维和者工具"))

    # 更新导航按钮文本
    for i, page in enumerate(self.pages):
      self.buttons[i].setText(self.tr(page["name"]))

    self.update_warmup_text()

    # 更新主题下拉框文本
    self.theme_combo.setItemText(0, self.tr("浅色模式"))
    self.theme_combo.setItemText(1, self.tr("深色模式"))

    # 调用每个页面的 retranslate_ui 方法
    for i in range(self.stack.count()):
      page_widget = self.stack.widget(i)
      page_widget.retranslate_ui()

  def theme_combo_handler(self, index):
    """切换明暗主题"""
    if index == 0:
      self.theme_manager.set_theme('light')
    elif index == 1:
      self.theme_manager.set_theme('dark')

  def update_theme_combo(self):
    """更新切换主题下拉框"""
    theme_name = self.theme_manager.current_theme["name"]
    index = None
    if theme_name == 'light':
      index = 0
    elif theme_name == 'dark':
      index = 1
    self.theme_combo.setCurrentIndex(index)

  def showEvent(self, event):
    super().showEvent(event)
    if not self.warmup_started:
      self.warmup_started = True
      QTimer.singleShot(200, self.load_warmup_wav)

  def load_warmup_wav(self):
    audio_file_path = get_resource_path(
        "warmup.wav", "assets", "../resources")

    def run_analysis():
      try:
        audioAnalyzer.analyze(audio_file_path)
        self.warmup_label_status = 1
        self.update_warmup_text()
      except:
        self.warmup_label_status = 2
        self.update_warmup_text()
    thread = Thread(target=run_analysis, daemon=True)
    thread.start()

  def update_warmup_text(self):
    status = self.warmup_label_status
    if status == 0:
      self.warmup_label.setText(self.tr("正在预热摩斯电码分析模块..."))
    elif status == 1:
      self.warmup_label.setText(self.tr("摩斯电码分析模块已预热完成"))
    elif status == 2:
      self.warmup_label.setText(self.tr("预热失败，但不会影响使用"))


if __name__ == "__main__":
  app = QApplication(sys.argv)

  # 尝试加载系统语言翻译
  system_locale = QLocale.system().name()
  translator = QTranslator()

  # 优先加载系统语言，否则使用默认语言
  if system_locale == "zh_CN":
    pass
  else:
    qm_path = get_resource_path(f"{system_locale}.qm")
    if translator.load(qm_path):
      app.installTranslator(translator)

  window = MainWindow()
  window.show()
  sys.exit(app.exec())
