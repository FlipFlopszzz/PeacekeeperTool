import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from pages import GoldPage,HomePage,LastPage,SkinPage,AngelPage,BeastPage,UsagePage,CopperPage,SilverPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PeaceKeeperTool")
        self.setMinimumSize(1600, 800)
        self.showMaximized()

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(2)

        # Windows 11 style sidebar
        # 侧边栏样式
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #f3f3f3;
                border-right: 1px solid #e0e0e0;
            }
        """)

        # Windows 11 风格按钮样式
        button_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
                padding: 12px 16px;
                text-align: left;
                font-size: 14px;
                font-family: 'Microsoft YaHei', sans-serif;  /* 改为微软雅黑 */
                color: #202020;
                height: 40px;
            }
            QPushButton:hover {
                background-color: #eaeaea;
            }
            QPushButton:pressed {
                background-color: #e1e1e1;
            }
            QPushButton:checked {
                background-color: #dadada;
                font-weight: 600;  /* 选中状态下更粗一些 */
            }
        """
        # Create stacked widget for pages
        self.stack = QStackedWidget()

        # Define pages configuration
        self.pages = [
            {"name": "首页", "page_class": HomePage},
            {"name": "使用说明", "page_class": UsagePage},
            {"name": "野兽之源", "page_class": BeastPage},
            {"name": "看见天使", "page_class": AngelPage},
            {"name": "逐步升级", "page_class": SkinPage},
            {"name": "不祥之兆（金牌）", "page_class": GoldPage},
            {"name": "冲突（银牌）", "page_class": SilverPage},
            {"name": "初来乍到（铜牌）", "page_class": CopperPage},
            {"name": "维和者", "page_class": LastPage}
        ]

        # Create buttons and load UI files
        self.buttons = []

        for i, page in enumerate(self.pages):
            # Create and setup button
            btn = QPushButton(page["name"])
            btn.setCheckable(True)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))

            # Add button to sidebar
            sidebar_layout.addWidget(btn)
            self.buttons.append(btn)

            # Add page to stack
            self.stack.addWidget(page["page_class"]())

        # Add stretch to sidebar
        sidebar_layout.addStretch()

        # Add sidebar and stack to main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

        # Set initial page
        self.switch_page(0)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        # Update button states
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())