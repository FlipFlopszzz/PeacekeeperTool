from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QTextBrowser, QSplitter, QScrollArea, QFrame
from PySide6.QtGui import QPalette, QPixmap
from PySide6.QtCore import Qt


class SingleLineInput(QWidget):
  def __init__(self, placeholderText=""):
    super().__init__()
    layout = QVBoxLayout()
    self.input_box = QLineEdit()
    self.input_box.setFixedHeight(35)
    self.input_box.setPlaceholderText(placeholderText)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(self.input_box)
    self.setLayout(layout)

  def onTextChanged(self, func):
    self.input_box.textChanged.connect(func)

  def text(self):
    return self.input_box.text()

  def setText(self, text):
    self.input_box.setText(text)

  def setPlaceholderText(self, text):
    self.input_box.setPlaceholderText(text)


class SingleLineTextDisplay(QWidget):
  def __init__(self, initText):
    super().__init__()
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    self.tp = QLineEdit(initText)
    self.tp.setFixedHeight(35)
    self.tp.setReadOnly(True)
    layout.addWidget(self.tp)
    self.setLayout(layout)

  def setText(self, text):
    self.tp.setText(text)

  def text(self):
    return self.tp.text()


class MarkdownTextBrowser(QWidget):
  def __init__(self, markdown_text=""):
    super().__init__()

    # 创建布局
    self.layout = QVBoxLayout()

    # 创建 QTextBrowser
    self.text_browser = QTextBrowser()
    self.text_browser.setObjectName("markdownBrowser")

    # 设置传入的 Markdown 内容
    self.text_browser.setMarkdown(markdown_text)

    # 设置 QTextBrowser 背景透明
    palette = self.text_browser.palette()
    palette.setBrush(QPalette.Base, palette.window())
    self.text_browser.setPalette(palette)
    self.text_browser.setAutoFillBackground(False)
    self.text_browser.setOpenExternalLinks(True)

    # 将 QTextBrowser 添加到布局中
    self.layout.addWidget(self.text_browser)

    # 设置组件的布局
    self.setLayout(self.layout)


class DescriptionSplitter(QSplitter):
  """通过垂直分隔条调整说明区高度，工具区空间不足时可滚动。"""

  def __init__(self, browser, parent=None):
    super().__init__(Qt.Vertical, parent)
    self.setObjectName("descriptionSplitter")
    self.setHandleWidth(8)
    # 保留两个区域的最小高度，避免拖动后无法找回说明或工具。
    self.setChildrenCollapsible(False)
    browser.setMinimumHeight(80)
    self.addWidget(browser)

    content = QWidget()
    self.content_layout = QVBoxLayout(content)
    self.content_layout.setContentsMargins(0, 0, 0, 0)

    # 工具包含固定高度的控件，使用滚动区才能给说明区让出空间。
    self.content_area = QScrollArea()
    self.content_area.setFrameShape(QFrame.NoFrame)
    self.content_area.setWidgetResizable(True)
    self.content_area.setMinimumHeight(340)
    self.content_area.setWidget(content)
    content.setAutoFillBackground(False)
    self.content_area.viewport().setAutoFillBackground(False)
    self.addWidget(self.content_area)
    self.setStretchFactor(0, 1)
    self.setStretchFactor(1, 0)
    self.setSizes([200, 600])


class ImageDisplayer(QLabel):
  def __init__(self, image_path: str, height: int, parent=None):
    super().__init__(parent)
    # 加载图片并计算宽度
    pixmap = QPixmap(image_path)
    if not pixmap.isNull():
      # 计算保持宽高比的宽度
      ratio = pixmap.width() / pixmap.height()
      width = int(height * ratio)

      # 缩放图片并显示
      scaled_pixmap = pixmap.scaled(
          width,
          height,
          Qt.KeepAspectRatio,
          Qt.SmoothTransformation
      )
      self.setPixmap(scaled_pixmap)

      # 设置固定大小
      self.setFixedSize(width, height)
