from threading import Thread
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QApplication, QFileDialog, QMessageBox, QGridLayout, QSizePolicy, QComboBox, QSlider
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal
from audio import AudioRecorder, AudioAnalyzer
import sys
from methods import compute_candles, decode_morse, decrypt_atbash, decrypt_autokey, decrypt_baconian, decrypt_rail_fence, decrypt_reverse, decrypt_rot, decrypt_vigenere, find_closest_string
from basic_components import SingleLineInput, SingleLineTextDisplay

audioRecorder = AudioRecorder()
audioAnalyzer = AudioAnalyzer()


class CoordinateSystem(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    # 创建网格布局
    self.grid_layout = QGridLayout(self)
    self.grid_layout.setSpacing(2)  # 设置按钮间距为2px
    self.grid_layout.setContentsMargins(2, 2, 2, 2)
    # 存储组件引用
    self.buttons = []
    self.bottom_inputs = []
    self.left_inputs = []

    # 定义每层的边框颜色
    self.layer_colors = ["#EC1B23", "#FB7E29", "#EAAE00", "#21B04B"]

    # 在左边输入框上方添加 y 标签
    y_label = QLabel("y")
    y_label.setAlignment(Qt.AlignCenter)
    y_label.setFixedSize(40, 40)
    self.grid_layout.addWidget(y_label, 0, 0)

    # 创建左侧输入框
    for row in range(8):
      input_box = QLineEdit()
      input_box.setFixedSize(40, 40)
      input_box.setAlignment(Qt.AlignCenter)
      input_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
      self.grid_layout.addWidget(input_box, row + 1, 0)
      self.left_inputs.append(input_box)

    # 创建底部输入框
    for col in range(8):
      input_box = QLineEdit()
      input_box.setFixedSize(40, 40)
      input_box.setAlignment(Qt.AlignCenter)
      input_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
      self.grid_layout.addWidget(input_box, 9, col + 1)
      self.bottom_inputs.append(input_box)

    # 在底部输入框右边添加 x 标签
    x_label = QLabel("x")
    x_label.setAlignment(Qt.AlignCenter)
    x_label.setFixedSize(40, 40)
    self.grid_layout.addWidget(x_label, 9, 9)

    # 创建按钮网格
    for row in range(8):
      row_buttons = []
      for col in range(8):
        button = QPushButton()
        button.setFixedSize(40, 40)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.setCheckable(True)
        button.setObjectName('silver')

        # 根据按钮所在层设置边框颜色
        layer = min(row, col, 7 - row, 7 - col)
        button.setProperty("layer", layer)

        self.grid_layout.addWidget(button, row + 1, col + 1)
        button.clicked.connect(
            lambda checked, r=row, c=col: self.toggle_button_color(r, c, checked))
        row_buttons.append(button)
      self.buttons.append(row_buttons)

    # 设置网格布局的拉伸因子
    for i in range(10):
      self.grid_layout.setRowStretch(i, 0)
    for i in range(10):
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

  def toggle_button_color(self, row: int, col: int, checked: bool):
    button = self.get_button(row, col)
    if button:
      button.setChecked(checked)


class CandleDecryptor(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    # 创建主布局
    self.main_layout = QVBoxLayout(self)
    self.main_layout.setSpacing(15)
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
        input_box = SingleLineInput(self.tr("示例:2,3,4,5"))
      elif i == 1:
        input_box = SingleLineInput(self.tr("灯的序号之间用中/英文逗号隔开"))
      else:
        input_box = SingleLineInput()
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
    self.decrypt_button = QPushButton(self.tr("解密"))
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

  def on_btn_clicked(self):
    iterations = []
    for i in range(7):
      iterations.append(self.get_input(i))
    try:
      result = compute_candles(iterations)
    except Exception:
      result = self.tr("无结果")
    self.result_label.setText(result)

  def retranslate_ui(self):
      # 输入框的提示文本
    self.input_boxes[0].setPlaceholderText(self.tr("示例:2,3,4,5"))
    self.input_boxes[1].setPlaceholderText(self.tr("灯的序号之间用中/英文逗号隔开"))
    # 其余输入框如原来没有placeholder可忽略

    # 解密按钮
    self.decrypt_button.setText(self.tr("解密"))
    # 如果结果区显示的是"无结果"，需要用tr刷新
    self.result_label.setText("")


class AudioMorseDecoder(QWidget):
  analysis_finished = Signal()
  analysis_error = Signal()
  analysis_choice = 0

  def __init__(self, mode=0):
    super().__init__()
    self.mode = mode
    # 三态：0=不可录制 1=可录制 2=录制中(停止录制)
    self.rec_status = 0
    # decode_btn三态：0=不可识别 1=可识别 2=识别中
    self.decode_status = 0
    # show_img_btn三态：0=不可显示 1=可显示 2=显示中
    self.show_img_status = 0

    # 录制相关
    self.record_btn = QPushButton(self.tr("开始录制"))
    self.record_btn.setObjectName("morseDecoder")
    self.record_btn.clicked.connect(self.record_btn_handler)
    self.record_btn.setFixedHeight(35)
    self.record_btn.setDisabled(True)

    self.save_path_inputbox = SingleLineInput(self.tr("停止录制时，音频会保存到这个目录下"))
    self.save_path_inputbox.onTextChanged(
        self.save_path_inputbox_text_handler)

    self.save_path_btn = QPushButton(self.tr("选择保存目录"))
    self.save_path_btn.setObjectName("morseDecoder")
    self.save_path_btn.setFixedHeight(35)
    self.save_path_btn.clicked.connect(self.save_path_btn_handler)

    save_layout = QHBoxLayout()
    save_layout.addWidget(self.record_btn)
    save_layout.addWidget(self.save_path_inputbox)
    save_layout.addWidget(self.save_path_btn)

    # 识别相关
    self.decode_btn = QPushButton(self.tr("开始识别"))
    self.decode_btn.setObjectName("morseDecoder")
    self.decode_btn.setFixedHeight(35)
    self.decode_btn.setDisabled(True)
    self.decode_btn.clicked.connect(self.decode_btn_handler)

    self.decode_path_inputbox = SingleLineInput(
        self.tr("这里是将要用于自动识别的音频文件路径"))
    self.decode_path_inputbox.onTextChanged(
        self.decode_path_inputbox_text_handler)

    self.decode_path_btn = QPushButton(self.tr("选择用于识别的音频文件"))
    self.decode_path_btn.setObjectName("morseDecoder")
    self.decode_path_btn.setFixedHeight(35)
    self.decode_path_btn.clicked.connect(self.decode_path_btn_handler)

    decode_layout = QHBoxLayout()
    decode_layout.addWidget(self.decode_btn)
    decode_layout.addWidget(self.decode_path_inputbox)
    decode_layout.addWidget(self.decode_path_btn)

    # 幅值阈值
    amplitude_threshold_layout = QHBoxLayout()
    self.amplitude_threshold_label_left = QLabel(
        self.tr("使用这个滑块来调整摩斯电码幅值阈值    当前: 0.00"))
    self.amplitude_threshold_label_left.setFixedWidth(275)
    amplitude_threshold_layout.addWidget(
        self.amplitude_threshold_label_left)
    self.amplitude_threshold_silder = QSlider(Qt.Horizontal)
    self.amplitude_threshold_silder.setDisabled(True)
    self.amplitude_threshold_silder.valueChanged.connect(
        self.sliderHandler)
    amplitude_threshold_layout.addWidget(self.amplitude_threshold_silder)
    self.amplitude_threshold_label_right = QLabel()
    amplitude_threshold_layout.addWidget(
        self.amplitude_threshold_label_right)

    # 文本显示区
    self.morse_text_display = SingleLineTextDisplay(
        self.tr("这里将会显示识别出的摩斯电码的点划"))
    self.decoded_text_display = SingleLineTextDisplay(
        self.tr("这里将会显示摩斯电码解密结果"))

    # 提示
    self.hint_label = QLabel(self.tr("如果需要手动听写摩斯电码，可以利用下面的输入框自动翻译摩斯电码"))
    self.hint_label.setFixedHeight(35)
    self.hint_label.setFont(QFont())

    # 显示图像
    self.show_img_btn = QPushButton(self.tr("显示图像"))
    self.show_img_btn.setObjectName("morseDecoder")
    self.show_img_btn.setFixedHeight(35)
    self.show_img_btn.setDisabled(True)
    self.show_img_btn.clicked.connect(self.show_img_btn_handler)

    show_img_layout = QHBoxLayout()
    show_img_layout.addWidget(self.show_img_btn)
    show_img_layout.addWidget(self.hint_label)

    # 手动输入/显示
    self.handy_inputbox = SingleLineInput("")
    self.handy_inputbox.onTextChanged(self.handy_inputbox_handler)
    self.handy_text_display = SingleLineTextDisplay("")

    # 主布局
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
    self.setFixedHeight(330)

    # 信号
    self.analysis_finished.connect(self.on_analysis_finished)
    self.analysis_error.connect(self.on_analysis_error)

    # 初始化按钮状态
    self.update_record_btn_status()
    self.update_decode_btn_status()
    self.update_show_img_btn_status()

  # ====== 按钮与状态管理 ======
  def update_record_btn_status(self):
    if self.rec_status == 0:
      self.record_btn.setText(self.tr("开始录制"))
      self.record_btn.setDisabled(True)
    elif self.rec_status == 1:
      self.record_btn.setText(self.tr("开始录制"))
      self.record_btn.setEnabled(True)
    elif self.rec_status == 2:
      self.record_btn.setText(self.tr("停止录制"))
      self.record_btn.setEnabled(True)

  def update_decode_btn_status(self):
    if self.decode_status == 0:
      self.decode_btn.setText(self.tr("开始识别"))
      self.decode_btn.setDisabled(True)
    elif self.decode_status == 1:
      self.decode_btn.setText(self.tr("开始识别"))
      self.decode_btn.setEnabled(True)
    elif self.decode_status == 2:
      self.decode_btn.setText(self.tr("识别中..."))
      self.decode_btn.setDisabled(True)

  def update_show_img_btn_status(self):
    if self.show_img_status == 0:
      self.show_img_btn.setText(self.tr("显示图像"))
      self.show_img_btn.setDisabled(True)
    elif self.show_img_status == 1:
      self.show_img_btn.setText(self.tr("显示图像"))
      self.show_img_btn.setEnabled(True)
    elif self.show_img_status == 2:
      self.show_img_btn.setText(self.tr("尝试显示中..."))
      self.show_img_btn.setDisabled(True)

  # ====== 业务逻辑 ======
  def record_btn_handler(self):
    if self.rec_status == 1:
      # 开始
      audioRecorder.setDirectory(self.save_path_inputbox.text())
      audioRecorder.start()
      self.rec_status = 2
    elif self.rec_status == 2:
      # 停止
      fileName = audioRecorder.stop()
      self.rec_status = 1
      self.decode_path_inputbox.setText(fileName)
    self.update_record_btn_status()

  def decode_path_btn_handler(self):
    file_dialog = QFileDialog()
    filter_str = self.tr("WAV文件 (*.wav);;所有文件 (*)")
    file_path, _ = file_dialog.getOpenFileName(
        self, self.tr('选择音频文件'), filter=filter_str)
    if file_path:
      self.decode_path_inputbox.setText(file_path)

  def save_path_btn_handler(self):
    folder_path = QFileDialog.getExistingDirectory(
        self, self.tr('选择保存音频文件的目录'))
    if folder_path:
      self.save_path_inputbox.setText(folder_path)

  def save_path_inputbox_text_handler(self, text):
    if not text:
      self.rec_status = 0
    else:
      self.rec_status = 1
    self.update_record_btn_status()

  def decode_path_inputbox_text_handler(self, text):
    self.morse_text_display.setText(self.tr("这里将会显示识别出的摩斯电码的点划"))
    self.decoded_text_display.setText(self.tr("这里将会显示摩斯电码解密结果"))
    self.amplitude_threshold_silder.setDisabled(True)
    self.amplitude_threshold_label_right.setText("")
    if not text:
      self.decode_status = 0
      self.show_img_status = 0
    else:
      self.decode_status = 1
      self.show_img_status = 1
    self.update_decode_btn_status()
    self.update_show_img_btn_status()

  def decode_btn_handler(self):
    self.analysis_choice = 0
    if self.decode_status == 1:
      audio_file_path = self.decode_path_inputbox.text()
      self.decode_status = 2
      self.show_img_status = 0
      self.update_decode_btn_status()
      self.update_show_img_btn_status()
      self.analyze_in_new_thread(audio_file_path, self.mode)

  def show_img_btn_handler(self):
    self.analysis_choice = 1
    if self.show_img_status == 1:
      audio_file_path = self.decode_path_inputbox.text()
      self.show_img_status = 2
      self.decode_status = 0
      self.update_show_img_btn_status()
      self.update_decode_btn_status()
      self.analyze_in_new_thread(audio_file_path, self.mode)

  def analyze_in_mode(self, audio_file_path, mode):
    try:
      if mode == 0:
        audioAnalyzer.analyze(audio_file_path)
      elif mode == 1:
        audioAnalyzer.analyze(
            audio_file_path, low_freq=980, high_freq=1020, amplitude_threshold_coef=0.35)
      elif mode == 2:
        audioAnalyzer.analyze(
            audio_file_path, low_freq=770, high_freq=825, amplitude_threshold_coef=0.3)
      self.analysis_finished.emit()
    except:
      self.analysis_error.emit()

  def handy_inputbox_handler(self, text):
    self.handy_text_display.setText(decode_morse(text))

  def show_error_message(self, error_text):
    QMessageBox.critical(self, self.tr('错误'), self.tr(error_text))

  def sliderHandler(self, value):
    fmt_value = value / 100
    audioAnalyzer.amplitude_threshold = fmt_value
    audioAnalyzer.analyze_morse_signal()
    morse_code = audioAnalyzer.get_morse_code()
    self.amplitude_threshold_label_left.setText(
        self.tr("使用这个滑块来调整摩斯电码幅值阈值    当前: ") + str(fmt_value))
    if morse_code:
      self.morse_text_display.setText(morse_code)
      decoded = decode_morse(morse_code)
      self.decoded_text_display.setText(decoded)

  def analyze_in_new_thread(self, audio_file_path, mode):
    thread = Thread(target=self.analyze_in_mode,
                    args=(audio_file_path, mode))
    thread.start()

  def on_analysis_finished(self):
    choice = self.analysis_choice
    try:
      if choice == 0:
        audioAnalyzer.analyze_morse_signal()
        morse_code = audioAnalyzer.get_morse_code()
        if morse_code:
          self.morse_text_display.setText(morse_code)
          decoded = decode_morse(morse_code)
          self.decoded_text_display.setText(decoded)
        self.decode_status = 1
        self.show_img_status = 1
        self.update_decode_btn_status()
        self.update_show_img_btn_status()
      elif choice == 1:
        audioAnalyzer.analyze_morse_signal()
        plot_window = audioAnalyzer.plot()
        self.show_img_status = 1
        self.decode_status = 1
        self.update_show_img_btn_status()
        self.update_decode_btn_status()

      self.amplitude_threshold_silder.setDisabled(False)
      self.amplitude_threshold_silder.setRange(
          0, round(audioAnalyzer.mean_max_amplitude * 100))
      self.amplitude_threshold_silder.setValue(
          audioAnalyzer.init_amplitude_threshold * 100)
      self.amplitude_threshold_label_right.setText(
          str(audioAnalyzer.mean_max_amplitude))
    except:
      self.analysis_error.emit()

  def on_analysis_error(self):
    choice = self.analysis_choice
    self.decode_status = 1
    self.show_img_status = 1
    self.amplitude_threshold_silder.setDisabled(True)
    self.amplitude_threshold_label_right.setText("")
    self.update_decode_btn_status()
    self.update_show_img_btn_status()
    if choice == 0:
      self.show_error_message(self.tr("识别音频时出错，请检查音频文件路径和格式(.wav)是否正确"))
    elif choice == 1:
      self.show_error_message(self.tr("显示图像时出错，请检查音频文件路径和格式(.wav)是否正确"))

  def retranslate_ui(self):
    self.update_record_btn_status()
    self.save_path_inputbox.setPlaceholderText(
        self.tr("停止录制时，音频会保存到这个目录下"))
    self.save_path_btn.setText(self.tr("选择保存目录"))
    self.update_decode_btn_status()
    self.decode_path_inputbox.setPlaceholderText(
        self.tr("这里是将要用于自动识别的音频文件路径"))
    self.decode_path_btn.setText(self.tr("选择用于识别的音频文件"))
    self.amplitude_threshold_label_left.setText(
        self.tr("使用这个滑块来调整摩斯电码幅值阈值    当前: ") +
        str(self.amplitude_threshold_silder.value() / 100)
    )
    self.morse_text_display.setText(self.tr("这里将会显示识别出的摩斯电码的点划"))
    self.decoded_text_display.setText(self.tr("这里将会显示摩斯电码解密结果"))
    self.hint_label.setText(self.tr("如果需要手动听写摩斯电码，可以利用下面的输入框自动翻译摩斯电码"))
    self.update_show_img_btn_status()


class CipherDecryptor(QWidget):
  def __init__(self):
    super().__init__()
    self.hint_label = None
    self.mode = 0
    self.initUI()

  def initUI(self):
    layout = QVBoxLayout()
    top_layout = QHBoxLayout()

    # 创建标签
    self.label = QLabel(self.tr("密文解密器"))
    top_layout.addWidget(self.label)

    # 创建提示标签
    self.hint_label = QLabel(self.tr("解密栅栏密码前会自动倒置"))
    self.hint_label.setVisible(False)
    top_layout.addWidget(self.hint_label)

    # 创建 QComboBox 组件
    self.combobox = QComboBox()
    self.combobox.setFixedWidth(240)
    self.combobox.setFixedHeight(40)
    self.combobox.addItem(self.tr("任务1:原文"))
    self.combobox.addItem(self.tr("任务2:倒置(Reverse)"))
    self.combobox.addItem(self.tr("任务3:替换密码(Atbash)"))
    self.combobox.addItem(self.tr("任务4:凯撒密码(Rot)"))
    self.combobox.addItem(self.tr("任务5:栅栏密码(Rail Fence)"))
    self.combobox.addItem(self.tr("任务6:培根密码(Baconian)"))
    self.combobox.addItem(self.tr("任务7:维吉尼亚密码(Vigenere)"))
    self.combobox.addItem(self.tr("任务8:自动密钥密码(Autokey)"))
    self.combobox.currentIndexChanged.connect(
        self.update_mode_on_combobox_change)
    top_layout.addWidget(self.combobox)

    layout.addLayout(top_layout)

    # 创建输入框，使用自定义组件
    self.input_box = SingleLineInput(self.tr("请输入摩斯电码解密结果(相关参数帮你填好了)"))
    self.input_box.onTextChanged(self.update_text_display)
    layout.addWidget(self.input_box)

    # 创建文本显示区域，使用自定义组件
    self.text_display = SingleLineTextDisplay(self.tr("这里会显示解密结果"))
    layout.addWidget(self.text_display)

    self.text_display_match = SingleLineTextDisplay(self.tr("这里会显示最匹配的地点"))
    layout.addWidget(self.text_display_match)

    self.setLayout(layout)
    self.setFixedHeight(180)

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
      result = decrypt_reverse(text)
      result = decrypt_rail_fence(result)
    elif mode == 5:
      result = self.replace_e_t(text)
      result = decrypt_baconian(result)
      result = decrypt_atbash(result)
    elif mode == 6:
      result = decrypt_vigenere(text)
    elif mode == 7:
      result = decrypt_autokey(text)

    self.text_display.setText(result or self.tr("这里会显示解密结果"))

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
    if (result == self.tr("无结果")):
      self.text_display_match.setText(self.tr("无结果"))
    else:
      self.text_display_match.setText(self.tr("目标地点可能为: ")+result)

    if not self.input_box.text():
      self.text_display_match.setText(self.tr("这里会显示最匹配的地点"))

  def update_mode_on_combobox_change(self, mode):
    self.mode = mode
    self.hint_label.setVisible(self.mode == 4 or self.mode == 5)
    if mode == 4:
      self.hint_label.setText(self.tr("解密栅栏密码前会自动倒置"))
    elif mode == 5:
      self.hint_label.setText(self.tr("解密培根密码后会自动用替换密码解密"))
    self.update_text_display(self.input_box.text())

  def replace_e_t(self, s):
    new_s = s.replace('E', 'a').replace(
        'e', 'a').replace('T', 'b').replace('t', 'b')
    return new_s

  def retranslate_ui(self):
    # 标签
    self.label.setText(self.tr("密文解密器"))
    # 复选框文本，取决于当前模式
    if self.mode == 4:
      self.hint_label.setText(self.tr("解密栅栏密码前会自动倒置"))
    elif self.mode == 5:
      self.hint_label.setText(self.tr("解密培根密码后会自动用替换密码解密"))
    else:
      self.hint_label.setText("")

    # combobox 各项文本重设
    self.combobox.setItemText(0, self.tr("任务1:原文"))
    self.combobox.setItemText(1, self.tr("任务2:倒置(Reverse)"))
    self.combobox.setItemText(2, self.tr("任务3:替换密码(Atbash)"))
    self.combobox.setItemText(3, self.tr("任务4:凯撒密码(Rot)"))
    self.combobox.setItemText(4, self.tr("任务5:栅栏密码(Rail Fence)"))
    self.combobox.setItemText(5, self.tr("任务6:培根密码(Baconian)"))
    self.combobox.setItemText(6, self.tr("任务7:维吉尼亚密码(Vigenere)"))
    self.combobox.setItemText(7, self.tr("任务8:自动密钥密码(Autokey)"))

    # 输入框 placeholder
    self.input_box.setPlaceholderText(self.tr("请输入摩斯电码解密结果(相关参数帮你填好了)"))

    self.input_box.setText("")
    self.text_display.setText(self.tr("这里会显示解密结果"))
    self.text_display_match.setText(self.tr("这里会显示最匹配的地点"))


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = AudioMorseDecoder(1)
  # window = CipherDecryptor()
  window.show()
  sys.exit(app.exec())
