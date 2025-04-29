from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QApplication, QFileDialog, QCheckBox, QMessageBox, QTextBrowser, QGridLayout, QSizePolicy, QComboBox, QSlider
from PySide6.QtGui import QFont, QPalette, QPixmap, QColor
from PySide6.QtCore import Qt
from audio import AudioRecorder, AudioAnalyzer
import sys
from methods import compute_candles, decode_morse, decrypt_atbash, decrypt_autokey, decrypt_baconian, decrypt_rail_fence, decrypt_reverse, decrypt_rot, decrypt_vigenere, find_closest_string

font = QFont()
font.setPixelSize(14)  # 设置合适的字体大小以填充输入框
audioRecorder = AudioRecorder()
audioAnalyzer = AudioAnalyzer()


class inputbox_single_line(QWidget):
  def __init__(self, placeholderText=""):
    super().__init__()
    layout = QVBoxLayout()
    self.input_box = QLineEdit()
    self.input_box.setFixedHeight(35)
    self.input_box.setFont(font)
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


class text_diaplay_single_line(QWidget):
  def __init__(self, initText):
    super().__init__()
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    self.tp = QLineEdit(initText)
    self.tp.setFixedHeight(35)
    self.tp.setFont(font)
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

    # 设置传入的 Markdown 内容
    self.text_browser.setMarkdown(markdown_text)

    # 设置 QTextBrowser 背景透明
    palette = self.text_browser.palette()
    palette.setBrush(QPalette.Base, palette.window())
    self.text_browser.setPalette(palette)
    self.text_browser.setAutoFillBackground(False)
    self.text_browser.setOpenExternalLinks(True)

    # 设置样式表去除边框
    self.text_browser.setStyleSheet("border: none;")

    # 将 QTextBrowser 添加到布局中
    self.layout.addWidget(self.text_browser)

    # 设置组件的布局
    self.setLayout(self.layout)


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


class CoordinateSystem(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    # 创建网格布局
    self.grid_layout = QGridLayout(self)
    self.grid_layout.setSpacing(0)  # 设置间距为0
    self.grid_layout.setContentsMargins(2, 2, 2, 2)

    # 存储组件引用
    self.buttons = []
    self.bottom_inputs = []
    self.left_inputs = []

    # 在左边输入框上方添加 y 标签
    y_label = QLabel("y")
    y_label.setAlignment(Qt.AlignCenter)
    y_label.setFixedSize(40, 40)
    y_label.setFont(font)
    self.grid_layout.addWidget(y_label, 0, 0)

    # 创建左侧输入框
    for row in range(8):
      input_box = QLineEdit()
      input_box.setFixedSize(40, 40)
      input_box.setAlignment(Qt.AlignCenter)
      # 设置输入框不会随窗口调整而改变大小
      input_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
      self.grid_layout.addWidget(input_box, row + 1, 0)
      self.left_inputs.append(input_box)

    # 创建底部输入框
    for col in range(8):
      input_box = QLineEdit()
      input_box.setFixedSize(40, 40)
      input_box.setAlignment(Qt.AlignCenter)
      # 设置输入框不会随窗口调整而改变大小
      input_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
      self.grid_layout.addWidget(input_box, 9, col + 1)
      self.bottom_inputs.append(input_box)

    # 在底部输入框右边添加 x 标签
    x_label = QLabel("x")
    x_label.setAlignment(Qt.AlignCenter)
    x_label.setFixedSize(40, 40)
    x_label.setFont(font)
    self.grid_layout.addWidget(x_label, 9, 9)

    # 创建按钮网格
    for row in range(8):
      row_buttons = []
      for col in range(8):
        button = QPushButton()
        button.setFixedSize(40, 40)
        # 设置按钮不会随窗口调整而改变大小
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 设置按钮样式，确保边框紧邻
        button.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        border: 1px solid #ccc;
                        border-radius: 0px;
                        margin: 0px;
                        padding: 0px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                    QPushButton:pressed {
                        background-color: #d0d0d0;
                    }
                """)

        self.grid_layout.addWidget(button, row + 1, col + 1)
        button.clicked.connect(
            lambda _, r=row, c=col: self.toggle_button_color(r, c))
        row_buttons.append(button)
      self.buttons.append(row_buttons)

    # 设置网格布局的拉伸因子，防止布局在窗口调整时产生间距
    for i in range(10):  # 10行（8个按钮行+1个输入框行 + 1个标签行）
      self.grid_layout.setRowStretch(i, 0)
    for i in range(10):  # 10列（8个按钮列+1个输入框列 + 1个标签列）
      self.grid_layout.setColumnStretch(i, 0)

    # 添加一个弹性空间来吸收多余的空间
    spacer_widget = QWidget()
    spacer_widget.setSizePolicy(
        QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.grid_layout.addWidget(spacer_widget, 10, 9)

    # 设置组件本身的大小策略
    self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

  def get_button(self, row: int, col: int) -> QPushButton:
    """获取指定位置的按钮"""
    if 0 <= row < 8 and 0 <= col < 8:
      return self.buttons[row][col]
    return None

  def get_bottom_input(self, col: int) -> QLineEdit:
    """获取底部指定位置的输入框"""
    if 0 <= col < 8:
      return self.bottom_inputs[col]
    return None

  def get_left_input(self, row: int) -> QLineEdit:
    """获取左侧指定位置的输入框"""
    if 0 <= row < 8:
      return self.left_inputs[row]
    return None

  def set_button_text(self, row: int, col: int, text: str):
    """设置指定按钮的文本"""
    button = self.get_button(row, col)
    if button:
      button.setText(text)

  def set_bottom_input_text(self, col: int, text: str):
    """设置底部输入框的文本"""
    input_box = self.get_bottom_input(col)
    if input_box:
      input_box.setText(text)

  def set_left_input_text(self, row: int, text: str):
    """设置左侧输入框的文本"""
    input_box = self.get_left_input(row)
    if input_box:
      input_box.setText(text)

  def toggle_button_color(self, row: int, col: int):
    button = self.get_button(row, col)
    if button:
      current_color = QColor(button.palette().button().color())
      if current_color.name() == "#f0f0f0":
        button.setStyleSheet("""
                    QPushButton {
                        background-color: red;
                        border: 1px solid #ccc;
                        border-radius: 0px;
                        margin: 0px;
                        padding: 0px;
                    }
                    QPushButton:hover {
                        background-color: #FF6666;
                    }
                    QPushButton:pressed {
                        background-color: #FF3333;
                    }
                """)
      else:
        button.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        border: 1px solid #ccc;
                        border-radius: 0px;
                        margin: 0px;
                        padding: 0px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                    QPushButton:pressed {
                        background-color: #d0d0d0;
                    }
                """)


class CandleHandler(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    # 创建主布局
    self.main_layout = QVBoxLayout(self)
    self.main_layout.setSpacing(15)  # 设置垂直间距
    self.main_layout.addSpacing(50)

    # 存储输入框的引用
    self.input_boxes = []

    # 创建7个水平布局，每个包含标签和输入框
    for i in range(7):
      # 创建水平布局
      h_layout = QHBoxLayout()
      h_layout.setSpacing(5)  # 设置标签和输入框之间的间距

      # 创建标签
      label = QLabel(f"{i + 1}:")
      label.setFixedWidth(20)  # 设置标签固定宽度
      label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 右对齐

      # 创建输入框
      if i == 0:
        input_box = inputbox_single_line("示例:2,3,4,5")
      elif i == 1:
        input_box = inputbox_single_line("灯的序号之间用中/英文逗号隔开")
      else:
        input_box = inputbox_single_line()
      input_box.input_box.setFixedWidth(240)
      input_box.input_box.setSizePolicy(
          QSizePolicy.Fixed, QSizePolicy.Fixed)

      # 添加到水平布局
      h_layout.addWidget(label)
      h_layout.addWidget(input_box)

      # 添加到主布局
      self.main_layout.addLayout(h_layout)

      # 保存输入框引用
      self.input_boxes.append(input_box)

    # 创建用于显示结果的标签
    self.result_label = QLabel()
    self.result_label.setStyleSheet("font-size: 14px; margin-right: 10px;")

    # 创建解密按钮
    self.decrypt_button = QPushButton("解密")
    self.decrypt_button.setFixedSize(100, 35)  # 设置按钮大小
    self.decrypt_button.clicked.connect(self.on_btn_clicked)

    # 设置按钮样式
    self.decrypt_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #006cbd;
            }
            QPushButton:pressed {
                background-color: #005ca3;
            }
        """)

    # 创建底部布局
    bottom_layout = QHBoxLayout()
    bottom_layout.addSpacing(30)
    bottom_layout.addWidget(self.decrypt_button, alignment=Qt.AlignLeft)
    bottom_layout.addStretch()
    bottom_layout.addWidget(self.result_label, alignment=Qt.AlignRight)
    bottom_layout.addSpacing(30)

    # 添加底部布局到主布局
    self.main_layout.addLayout(bottom_layout)

    # 设置组件大小策略，防止布局溢出
    self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

  def get_input(self, index: int) -> str:
    if 0 <= index < 7:
      return self.input_boxes[index].text()
    return ""

  def set_input(self, index: int, text: str):
    if 0 <= index < 7:
      self.input_boxes[index].setText(text)

  def clear_all(self):
    for input_box in self.input_boxes:
      input_box.clear()

  def on_btn_clicked(self):
    iterations = []
    for i in range(7):
      iterations.append(self.get_input(i))
    try:
      result = compute_candles(iterations)
    except Exception:
      result = "无结果"
    self.result_label.setText(result)


class MorseCodeCom(QWidget):
  def __init__(self, mode=0):
    super().__init__()
    self.mode = mode
    # mode=0:skin,mode=1:gold,mode=2:copper
    # 创建按钮
    self.record_btn = QPushButton("开始录制")
    self.record_btn.clicked.connect(self.toggle_record_text)
    self.record_btn.setFixedHeight(35)
    self.record_btn.setDisabled(True)

    # 使用自定义输入框组件
    self.save_path_inputbox = inputbox_single_line("停止录制时，音频会保存到这个目录下")
    self.save_path_inputbox.onTextChanged(
        self.save_path_inputbox_text_handler)

    self.save_path_btn = QPushButton("选择保存目录")
    self.save_path_btn.setFixedHeight(35)
    self.save_path_btn.clicked.connect(self.save_path_btn_handler)

    save_layout = QHBoxLayout()
    save_layout.addWidget(self.record_btn)
    save_layout.addWidget(self.save_path_inputbox)
    save_layout.addWidget(self.save_path_btn)

    self.decode_btn = QPushButton("开始识别")
    self.decode_btn.setFixedHeight(35)
    self.decode_btn.setDisabled(True)
    self.decode_btn.clicked.connect(self.decode_btn_handler)

    # 使用自定义输入框组件
    self.decode_path_inputbox = inputbox_single_line("这里是将要用于自动识别的音频文件路径")
    self.decode_path_inputbox.onTextChanged(
        self.decode_path_inputbox_text_handler)

    self.decode_path_btn = QPushButton("选择用于识别的音频文件")
    self.decode_path_btn.setFixedHeight(35)
    self.decode_path_btn.clicked.connect(self.decode_path_btn_handler)

    decode_layout = QHBoxLayout()
    decode_layout.addWidget(self.decode_btn)
    decode_layout.addWidget(self.decode_path_inputbox)
    decode_layout.addWidget(self.decode_path_btn)

    amplitude_threshold_layout = QHBoxLayout()
    self.amplitude_threshold_label_left = QLabel(
        "使用这个滑块来调整摩斯电码幅值阈值    当前: 0.0")
    self.amplitude_threshold_label_left.setFont(font)
    amplitude_threshold_layout.addWidget(self.amplitude_threshold_label_left)
    self.amplitude_threshold_silder = QSlider(Qt.Horizontal)
    self.amplitude_threshold_silder.setDisabled(True)
    self.amplitude_threshold_silder.valueChanged.connect(self.sliderHandler)
    amplitude_threshold_layout.addWidget(self.amplitude_threshold_silder)
    self.amplitude_threshold_label_right = QLabel()
    self.amplitude_threshold_label_right.setFont(font)
    amplitude_threshold_layout.addWidget(self.amplitude_threshold_label_right)

    # 创建文本显示区域，使用自定义组件
    self.morse_text_display = text_diaplay_single_line("这里将会显示识别出的摩斯电码的点划")
    self.decoded_text_display = text_diaplay_single_line("这里将会显示摩斯电码解密结果")

    # 创建提示文字
    self.hint_label = QLabel("如果需要手动听写摩斯电码，可以利用下面的输入框自动翻译摩斯电码")
    self.hint_label.setFixedHeight(35)
    self.hint_label.setFont(QFont())
    self.show_img_btn = QPushButton("显示图像")
    self.show_img_btn.setFixedHeight(35)
    self.show_img_btn.setDisabled(True)
    self.show_img_btn.clicked.connect(self.show_img_btn_handler)

    show_img_layout = QHBoxLayout()
    show_img_layout.addWidget(self.show_img_btn)
    show_img_layout.addWidget(self.hint_label)

    # 使用自定义输入框组件
    self.handy_inputbox = inputbox_single_line("")
    self.handy_inputbox.onTextChanged(self.handy_inputbox_handler)

    # 创建另一个文本显示区域，使用自定义组件
    self.handy_text_display = text_diaplay_single_line("")

    # 创建主布局
    main_layout = QVBoxLayout()
    main_layout.addLayout(save_layout)
    main_layout.addLayout(decode_layout)
    main_layout.addLayout(amplitude_threshold_layout)
    main_layout.addWidget(self.morse_text_display)
    main_layout.addWidget(self.decoded_text_display)
    main_layout.addLayout(show_img_layout)
    main_layout.addWidget(self.handy_inputbox)
    main_layout.addWidget(self.handy_text_display)

    self.setLayout(main_layout)

    self.setFixedHeight(300)

  def toggle_record_text(self):
    if self.record_btn.text() == "开始录制":
      # 开始
      audioRecorder.setDirectory(self.save_path_inputbox.text())
      audioRecorder.start()
      self.record_btn.setText("停止录制")
    else:
      # 停止
      fileName = audioRecorder.stop()
      self.record_btn.setText("开始录制")
      self.decode_path_inputbox.setText(fileName)

  def decode_path_btn_handler(self):
    file_dialog = QFileDialog()
    filter_str = "WAV Files (*.wav);;All Files (*)"
    file_path, _ = file_dialog.getOpenFileName(
        self, '选择文件', filter=filter_str)
    if file_path:
      self.decode_path_inputbox.setText(file_path)

  def save_path_btn_handler(self):
    folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
    if folder_path:
      self.save_path_inputbox.setText(folder_path)

  def save_path_inputbox_text_handler(self, text):
    if not text:
      self.record_btn.setDisabled(True)
    else:
      self.record_btn.setDisabled(False)

  def decode_path_inputbox_text_handler(self, text):
    self.morse_text_display.setText("")
    self.decoded_text_display.setText("")
    self.amplitude_threshold_silder.setDisabled(True)
    self.amplitude_threshold_label_right.setText("")
    if not text:
      self.decode_btn.setDisabled(True)
      self.show_img_btn.setDisabled(True)
    else:
      self.decode_btn.setDisabled(False)
      self.show_img_btn.setDisabled(False)

  def decode_btn_handler(self):
    if self.decode_btn.text() == "开始识别":
      # 开始
      audio_file_path = self.decode_path_inputbox.text()
      self.decode_btn.setText("识别中...")
      self.decode_btn.setDisabled(True)
      try:
        self.analyze_in_mode(audio_file_path, self.mode)
        audioAnalyzer.analyze_morse_signal()
        morse_code = audioAnalyzer.get_morse_code()
        if morse_code:
          self.morse_text_display.setText(morse_code)
          decoded = decode_morse(morse_code)
          self.decoded_text_display.setText(decoded)
        self.decode_btn.setText("开始识别")
        self.decode_btn.setDisabled(False)
        self.amplitude_threshold_silder.setDisabled(False)
        self.amplitude_threshold_silder.setRange(
            0, round(audioAnalyzer.mean_max_amplitude*100))
        self.amplitude_threshold_silder.setValue(
            audioAnalyzer.init_amplitude_threshold*100)
        self.amplitude_threshold_label_right.setText(
            str(audioAnalyzer.mean_max_amplitude))
      except:
        self.decode_btn.setText("开始识别")
        self.decode_btn.setDisabled(False)
        self.show_img_btn.setDisabled(False)
        self.amplitude_threshold_silder.setDisabled(True)
        self.amplitude_threshold_label_right.setText("")
        self.show_error_message("识别音频时出错，请检查音频文件路径和格式(.wav)是否正确")

  def show_img_btn_handler(self):
    audio_file_path = self.decode_path_inputbox.text()
    if audio_file_path:
      try:
        self.analyze_in_mode(audio_file_path, self.mode)
        audioAnalyzer.analyze_morse_signal()
        plot_window = audioAnalyzer.plot()
      except:
        self.show_error_message("显示图像时出错，请检查音频文件路径和格式(.wav)是否正确")

  def analyze_in_mode(self, audio_file_path, mode):
    # mode=0:skin,mode=1:gold,mode=2:copper
    # 3.0,9.0,12.0
    if mode == 0:
      audioAnalyzer.analyze(audio_file_path)
    elif mode == 1:
      audioAnalyzer.analyze(audio_file_path, low_freq=980,
                            high_freq=1020, amplitude_threshold_coef=0.35)
    elif mode == 2:
      audioAnalyzer.analyze(audio_file_path, low_freq=770,
                            high_freq=825, amplitude_threshold_coef=0.3)

    # audioAnalyzer.analyze_morse_signal()

  def handy_inputbox_handler(self, text):
    self.handy_text_display.setText(decode_morse(text))

  def show_error_message(self, error_text):
    # 创建错误消息框
    QMessageBox.critical(self, '错误', error_text)

  def sliderHandler(self, value):
    fmt_value = value/100
    audioAnalyzer.amplitude_threshold = fmt_value
    audioAnalyzer.analyze_morse_signal()
    morse_code = audioAnalyzer.get_morse_code()
    self.amplitude_threshold_label_left.setText(
        "使用这个滑块来调整摩斯电码幅值阈值    当前: "+str(fmt_value))
    if morse_code:
      self.morse_text_display.setText(morse_code)
      decoded = decode_morse(morse_code)
      self.decoded_text_display.setText(decoded)


class DecrypterCom(QWidget):
  def __init__(self):
    super().__init__()
    self.checkbox = None
    self.mode = 0
    self.initUI()

  def initUI(self):
    layout = QVBoxLayout()
    top_layout = QHBoxLayout()

    # 创建标签
    self.label = QLabel("解密器")
    self.label.setFont(font)
    top_layout.addWidget(self.label)

    # 创建复选框
    self.checkbox = QCheckBox("解密栅栏密码前是否自动倒置")
    self.checkbox.setChecked(True)
    self.checkbox.setVisible(False)
    self.checkbox.stateChanged.connect(
        self.update_text_display_on_checkbox_change)
    top_layout.addWidget(self.checkbox)

    # 创建 QComboBox 组件
    self.combobox = QComboBox()
    self.combobox.setFixedWidth(200)
    self.combobox.setFixedHeight(40)
    self.combobox.addItem("任务1:原文")
    self.combobox.addItem("任务2:倒置(Reverse)")
    self.combobox.addItem("任务3:替换密码(Atbash)")
    self.combobox.addItem("任务4:凯撒密码(Rot)")
    self.combobox.addItem("任务5:栅栏密码(Rail Fence)")
    self.combobox.addItem("任务6:培根密码(Baconian)")
    self.combobox.addItem("任务7:维吉尼亚密码(Vigenere)")
    self.combobox.addItem("任务8:自动密钥密码(Autokey)")
    self.combobox.currentIndexChanged.connect(
        self.update_mode_on_combobox_change)
    top_layout.addWidget(self.combobox)

    layout.addLayout(top_layout)

    # 创建输入框，使用自定义组件
    self.input_box = inputbox_single_line("请输入摩斯电码解密结果(相关参数帮你填好了)")
    self.input_box.onTextChanged(self.update_text_display)
    layout.addWidget(self.input_box)

    # 创建文本显示区域，使用自定义组件
    self.text_display = text_diaplay_single_line("这里会显示解密结果")
    layout.addWidget(self.text_display)

    self.text_display_match = text_diaplay_single_line("这里会显示最匹配的地点")
    layout.addWidget(self.text_display_match)

    self.setLayout(layout)
    self.setFixedHeight(170)

  def update_text_display(self, text):
    result = ''
    mode = self.mode
    if mode == 0:
      result = text
    elif mode == 1:
      result = decrypt_reverse(text)
    elif mode == 2:
      result = decrypt_atbash(text)
    elif mode == 3:
      result = decrypt_rot(text)
    elif mode == 4:
      if self.checkbox and self.checkbox.isChecked():
        result = decrypt_reverse(text)
        result = decrypt_rail_fence(result)
      else:
        result = decrypt_rail_fence(text)
    elif mode == 5:
      result = self.replace_e_t(text)
      result = decrypt_baconian(result)
      if self.checkbox and self.checkbox.isChecked():
        result = decrypt_atbash(result)
    elif mode == 6:
      result = decrypt_vigenere(text)
    elif mode == 7:
      result = decrypt_autokey(text)

    self.text_display.setText(result or "这里会显示解密结果")

    self.update_text_display_match(mode)

  def update_text_display_match(self, mode):
    processed_text = self.text_display.text().upper()
    if mode == 6:
      if "ALLIES" in processed_text:
        processed_text = processed_text.split("ALLIES")[0]
      else:
        processed_text = processed_text[:25]
    elif mode == 7:
      if "FINAL" in processed_text:
        processed_text = processed_text.split("FINAL")[0]
      else:
        processed_text = processed_text[:25]
    result = find_closest_string(processed_text)
    if (result == "无结果"):
      self.text_display_match.setText("无结果")
    else:
      self.text_display_match.setText("目标地点可能为: "+result)

  def update_text_display_on_checkbox_change(self):
    self.update_text_display(
        self.input_box.text()
    )

  def update_mode_on_combobox_change(self, mode):
    self.mode = mode
    self.checkbox.setVisible(self.mode == 3 or self.mode == 4)
    if mode == 4:
      self.checkbox.setText("解密栅栏密码前是否自动倒置")
    elif mode == 5:
      self.checkbox.setText("解密培根密码后是否自动用替换密码解密")
    self.update_text_display(self.input_box.text())

  def replace_e_t(self, s):
    new_s = s.replace('E', 'a').replace(
        'e', 'a').replace('T', 'b').replace('t', 'b')
    return new_s


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MorseCodeCom(1)
  # window = DecrypterCom()
  window.show()
  sys.exit(app.exec())
