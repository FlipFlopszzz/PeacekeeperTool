import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget,
                               QHBoxLayout, QVBoxLayout, QStackedWidget)
from theme_manager import ThemeManager
from pages import GoldPage, HomePage, LastPage, SkinPage, AngelPage, BeastPage, UsagePage, CopperPage, SilverPage


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("PeaceKeeperTool")
    self.setMinimumSize(1280, 800)
    self.showMaximized()

    # 初始化主题管理器
    self.theme_manager = ThemeManager()
    self.theme_manager.theme_changed.connect(self.update_theme)

    # 创建主部件和布局
    main_widget = QWidget()
    self.setCentralWidget(main_widget)
    main_layout = QHBoxLayout(main_widget)
    main_layout.setContentsMargins(0, 0, 0, 0)

    # 创建侧边栏
    sidebar = QWidget()
    sidebar.setFixedWidth(240)
    sidebar.setObjectName("sidebar")
    sidebar_layout = QVBoxLayout(sidebar)
    sidebar_layout.setContentsMargins(10, 20, 10, 20)
    sidebar_layout.setSpacing(2)  # 保持原始间距

    # 创建页面堆栈
    self.stack = QStackedWidget()

    # 定义页面配置
    self.pages = [
        {"name": "首页", "page_class": HomePage},
        {"name": "使用说明", "page_class": UsagePage},
        {"name": "野兽之源", "page_class": BeastPage},
        {"name": "看见天使", "page_class": AngelPage},
        {"name": "逐步升级", "page_class": SkinPage},
        {"name": "不祥之兆（金牌）", "page_class": GoldPage},
        {"name": "冲突（银牌）", "page_class": SilverPage},
        {"name": "初显身手（铜牌）", "page_class": CopperPage},
        {"name": "维和者", "page_class": LastPage}
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

    # 添加间隔（关键修改点：在导航按钮和主题按钮之间添加间隔）
    sidebar_layout.addStretch(1)

    # 添加主题切换按钮到侧边栏底部（单独一组）
    self.theme_button = QPushButton("切换暗色模式")
    self.theme_button.setObjectName("themeButton")
    self.theme_button.clicked.connect(self.toggle_theme)
    sidebar_layout.addWidget(self.theme_button)

    # 添加侧边栏和页面堆栈到主布局
    main_layout.addWidget(sidebar)
    main_layout.addWidget(self.stack)

    # 设置初始页面
    self.switch_page(0)

    # 应用初始主题
    self.update_theme()

  def switch_page(self, index):
    """切换当前显示的页面"""
    self.stack.setCurrentIndex(index)
    # 更新按钮状态
    for i, btn in enumerate(self.buttons):
      btn.setChecked(i == index)

  def toggle_theme(self):
    """切换明暗主题"""
    self.theme_manager.toggle_theme()

  def update_theme(self):
    """更新应用主题"""
    theme_name = self.theme_manager.current_theme["name"]
    self.theme_button.setText(
        "切换暗色模式" if theme_name == "light" else "切换亮色模式")

    # 应用全局样式
    app = QApplication.instance()
    if app:
      app.setStyleSheet(self.theme_manager.style_sheet)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
