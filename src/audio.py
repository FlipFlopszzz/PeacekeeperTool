import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from scipy import signal
import librosa
import numpy as np
import pyaudiowpatch as pyaudio
import wave
import os
import threading
from datetime import datetime


class AudioRecorder:
  def __init__(self):
    self.CHUNK = 1024
    self.FORMAT = pyaudio.paInt16
    self.BIT_DEPTH = 16
    self.is_recording = False
    self.frames = []
    self.stream = None
    self.p = None
    self.directory = '.'
    self._set_filename()
    self.timer = None

  def _set_filename(self):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    self.FILENAME = os.path.join(self.directory, f"pkt-{timestamp}.wav")

  def setDirectory(self, directory):
    self.directory = directory
    self._set_filename()

  def start(self):
    # 确保输出目录存在
    output_dir = os.path.dirname(self.FILENAME)
    if output_dir and not os.path.exists(output_dir):
      os.makedirs(output_dir)

    self.p = pyaudio.PyAudio()
    # 获取WASAPI信息
    wasapi_info = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)
    default_speakers = self.p.get_device_info_by_index(
        wasapi_info["defaultOutputDevice"])

    # 查找对应的loopback设备
    if not default_speakers.get('isLoopbackDevice', False):
      for loopback in self.p.get_loopback_device_info_generator():
        if default_speakers['name'] in loopback['name']:
          default_speakers = loopback
          break

    # 获取设备的实际采样率
    self.RATE = int(default_speakers["defaultSampleRate"])

    # 创建音频流
    self.stream = self.p.open(format=self.FORMAT,
                              channels=default_speakers["maxInputChannels"],
                              rate=self.RATE,
                              frames_per_buffer=self.CHUNK,
                              input=True,
                              input_device_index=default_speakers["index"])

    self.is_recording = True
    self.frames = []

    def record():
      while self.is_recording:
        data = self.stream.read(
            self.CHUNK, exception_on_overflow=False)
        self.frames.append(data)

    self.thread = threading.Thread(target=record)
    self.thread.start()

    def timer_stop():
      if self.is_recording:
        self.stop()

    self.timer = threading.Timer(60, timer_stop)
    self.timer.start()

  def stop(self):
    if self.is_recording:
      self.is_recording = False
      if self.timer:
        self.timer.cancel()
      self.thread.join()
      # 停止并关闭音频流
      self.stream.stop_stream()
      self.stream.close()
      self.p.terminate()

      # 保存为WAV文件
      with wave.open(self.FILENAME, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))

      return self.FILENAME


class AudioAnalyzer:
  def __init__(self):
    self.file_path = None
    self.y = None
    self.sr = None
    self.y_reduced = None
    self.filtered = None
    self.amplitude_envelope = None
    self.times = None
    self.amplitudes = None
    self.morse_signals = None
    self.morse_text = None
    self.char_gaps = None
    self.word_gaps = None

    self.low_freq = None
    self.high_freq = None
    self.amplitude_threshold = None
    self.mean_max_amplitude = None
    self.init_amplitude_threshold = None

    self._plot_window = None  # 添加这个属性来保持窗口引用

  def analyze(self, file_path, low_freq=770, high_freq=810, amplitude_threshold_coef=0.25, dot_threshold=0.03,
              dash_threshold=0.14, char_gap_threshold=0.08, word_gap_threshold=0.30):
    self.low_freq = low_freq
    self.high_freq = high_freq
    self.dot_threshold = dot_threshold
    self.dash_threshold = dash_threshold
    self.char_gap_threshold = char_gap_threshold
    self.word_gap_threshold = word_gap_threshold

    self.file_path = file_path
    self.y, self.sr = self.load_audio()
    self.y_reduced = self.spectral_noise_reduction(self.y, self.sr)
    self.filtered = self.filter_audio(self.y_reduced, low_freq, high_freq)
    self.amplitude_envelope = self.calculate_envelope(self.filtered)
    self.times, self.amplitudes = self.sample_audio(
        self.amplitude_envelope)
    self.mean_max_amplitude = self.get_init_amplitude_threshold()
    self.init_amplitude_threshold = self.mean_max_amplitude*amplitude_threshold_coef

  def load_audio(self):
    """加载音频文件"""
    return librosa.load(self.file_path)

  def spectral_noise_reduction(self, y, sr):
    """
    使用频谱减法进行降噪
    基本思路：
    1. 估计噪声的频谱特征（使用信号的低能量部分）
    2. 从原始信号中减去估计的噪声
    """
    D = librosa.stft(y)
    mag = np.abs(D)
    phase = np.angle(D)

    mag_db = librosa.amplitude_to_db(mag)
    noise_threshold = np.percentile(mag_db, 20, axis=1)
    noise_estimate = librosa.db_to_amplitude(noise_threshold)[
        :, np.newaxis]

    mag_reduced = np.maximum(mag - noise_estimate, 0)

    D_reduced = mag_reduced * np.exp(1j * phase)
    y_reduced = librosa.istft(D_reduced)

    return y_reduced

  def filter_audio(self, y_reduced, low_freq, high_freq):
    """设计带通滤波器并滤波"""
    nyquist = self.sr / 2
    low = low_freq / nyquist
    high = high_freq / nyquist
    b, a = signal.butter(4, [low, high], btype='band')
    return signal.filtfilt(b, a, y_reduced)

  def calculate_envelope(self, filtered):
    """计算信号包络"""
    analytic_signal = signal.hilbert(filtered)
    return np.abs(analytic_signal)

  def sample_audio(self, amplitude_envelope):
    """采样音频"""
    interval = 0.01
    samples_per_interval = int(self.sr * interval)
    n_intervals = len(self.filtered) // samples_per_interval

    times = []
    amplitudes = []

    for i in range(n_intervals):
      start = i * samples_per_interval
      end = start + samples_per_interval
      mean_amplitude = np.mean(amplitude_envelope[start:end])
      time = i * interval
      scaled_amplitude = mean_amplitude * 1000
      times.append(time)
      amplitudes.append(scaled_amplitude)

    return times, amplitudes

  def analyze_morse_signal(self):
    """
    分析信号序列，识别摩斯电码
    规则：
    - 小于DOT_THRESHOLD的忽略
    - 大于等于DOT_THRESHOLD并且小于DASH_THRESHOLD为点
    - 大于等于DASH_THRESHOLD为线
    - 间隔大于等于CHAR_GAP为字符间隔
    - 间隔大于等于WORD_GAP为单词间隔
    """
    times = self.times
    amplitudes = self.amplitudes
    dot_threshold = self.dot_threshold
    dash_threshold = self.dash_threshold
    char_gap_threshold = self.char_gap_threshold
    word_gap_threshold = self.word_gap_threshold

    morse_signals = []
    morse_code = []
    char_gaps = []
    word_gaps = []  # 新增：用于记录所有单词间隔
    signal_start = None
    in_signal = False
    last_signal_end = None
    valid_signal_duration = 0
    last_valid_time = None

    amplitude_threshold = None
    if self.amplitude_threshold:
      amplitude_threshold = self.amplitude_threshold
    else:
      amplitude_threshold = self.init_amplitude_threshold

    for i in range(len(times)):
      current_time = times[i]
      current_amp = amplitudes[i]

      if not in_signal and current_amp > amplitude_threshold:
        signal_start = current_time
        in_signal = True
        valid_signal_duration = 0
        last_valid_time = current_time

        if last_signal_end is not None:
          gap = current_time - last_signal_end
          if gap >= word_gap_threshold:  # 检测单词间隔
            morse_code.append('  ')  # 使用两个空格表示单词间隔，而不是三个
            word_gaps.append((last_signal_end, current_time))
          elif gap >= char_gap_threshold:  # 检测字符间隔
            morse_code.append(' ')
            char_gaps.append((last_signal_end, current_time))

      elif in_signal and current_amp > amplitude_threshold:
        if last_valid_time is not None:
          valid_signal_duration += current_time - last_valid_time
        last_valid_time = current_time

      elif in_signal and current_amp <= amplitude_threshold:
        if last_valid_time is not None:
          valid_signal_duration += current_time - last_valid_time

        last_signal_end = current_time

        if valid_signal_duration >= dash_threshold:
          signal_type = 2  # 线
          morse_code.append('_')
          morse_signals.append(
              (signal_start, valid_signal_duration, signal_type))
        elif valid_signal_duration >= dot_threshold:
          signal_type = 1  # 点
          morse_code.append('.')
          morse_signals.append(
              (signal_start, valid_signal_duration, signal_type))

        in_signal = False
        last_valid_time = None
        valid_signal_duration = 0

    morse_text = ''.join(morse_code)
    # 不再需要使用 split 和 join，因为已经在 morse_code 中正确处理了间隔
    morse_text = morse_text.strip()  # 只需要清理首尾的空格

    self.morse_signals = morse_signals
    self.morse_text = morse_text
    self.char_gaps = char_gaps
    self.word_gaps = word_gaps

  def get_morse_code(self):
    """返回读取到的摩斯电码字符串"""
    return self.morse_text

  def get_init_amplitude_threshold(self):
    """
    使用统计分析（95%分位数）计算幅值阈值
    """
    if self.amplitudes is None:
      return None
    amplitudes_array = np.array(self.amplitudes)
    perc = np.percentile(amplitudes_array, 95)
    result = round(float(perc), 2)
    return result

  def plot(self):
    """显示信号分析图表"""
    # 如果已经存在窗口，就先关闭它
    if self._plot_window is not None:
      self._plot_window.close()
      self._plot_window = None

    # 创建新窗口
    self._plot_window = PlotWindow(self)
    self._plot_window.resize(1200, 800)
    self._plot_window.show()
    return self._plot_window


plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class PlotWindow(QMainWindow):
  def __init__(self, analyzer: AudioAnalyzer, parent=None):
    super().__init__(parent)
    self.analyzer = analyzer
    self.setWindowTitle("音频信号幅值-时间图")  # 暂时使用英文标题避免字体问题
    self.initUI()
    self.plot()

  def initUI(self):
    main_widget = QWidget()
    self.setCentralWidget(main_widget)
    layout = QVBoxLayout(main_widget)

    self.fig = plt.figure(figsize=(12, 6))
    self.canvas = FigureCanvasQTAgg(self.fig)
    self.toolbar = NavigationToolbar(self.canvas, self)

    layout.addWidget(self.toolbar)
    layout.addWidget(self.canvas)

  def plot(self):
    self.fig.clear()

    amplitude_threshold = None
    if self.analyzer.amplitude_threshold:
      amplitude_threshold = self.analyzer.amplitude_threshold
    else:
      amplitude_threshold = self.analyzer.init_amplitude_threshold

    high_freq = self.analyzer.high_freq
    low_freq = self.analyzer.low_freq

    ax = self.fig.add_subplot(111)

    # 绘制基本信号
    ax.plot(self.analyzer.times, self.analyzer.amplitudes,
            'b-', linewidth=1, label='信号')

    # 绘制阈值线
    ax.axhline(y=amplitude_threshold, color='r', linestyle='--',
               label=f'幅值阈值 ({amplitude_threshold})')

    # 绘制单词间隔
    for gap_start, gap_end in self.analyzer.word_gaps:
      ax.axvspan(gap_start, gap_end, color='red', alpha=0.1,
                 label='单词间隔("   ")' if gap_start == self.analyzer.word_gaps[0][0] else "")

    # 绘制字符间隔
    for gap_start, gap_end in self.analyzer.char_gaps:
      ax.axvspan(gap_start, gap_end, color='blue', alpha=0.1,
                 label='字符间隔(" ")' if gap_start == self.analyzer.char_gaps[0][0] else "")

    # 绘制点划信号
    dot_label_set = False
    dash_label_set = False
    for start, duration, signal_type in self.analyzer.morse_signals:
      if signal_type == 1:  # 点
        ax.axvspan(start, start + duration, color='g', alpha=0.3,
                   label='点(".")' if not dot_label_set else "")
        dot_label_set = True
      elif signal_type == 2:  # 划
        ax.axvspan(start, start + duration, color='y', alpha=0.3,
                   label='划("_")' if not dash_label_set else "")
        dash_label_set = True

    # 设置图表属性
    ax.set_title(f'{low_freq}-{high_freq}Hz 信号分析')
    ax.set_xlabel('时间')
    ax.set_ylabel('幅值')
    ax.grid(True)
    ax.legend()

    self.fig.tight_layout()
    self.canvas.draw()

  def closeEvent(self, event):
    # 确保在关闭窗口时正确清理资源
    plt.close(self.fig)
    super().closeEvent(event)
