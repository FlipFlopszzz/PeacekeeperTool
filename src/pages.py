from components import CandleDecryptor, CoordinateSystem, AudioMorseDecoder, CipherDecryptor, SingleLineInput, SingleLineTextDisplay
from basic_components import ImageDisplayer, MarkdownTextBrowser
from methods import find_missing_letters,  get_last_gold_text
from PySide6.QtWidgets import QVBoxLayout, QWidget, QTextEdit, QHBoxLayout
import resources_rc


class HomePage(QWidget):
  def __init__(self):
    super().__init__()
    md_text = '''
# 简介
这是一个战地一维和者菜单解密工具，用于简化维和者获取的过程。本工具不包含关于彩蛋背后故事的内容。
# 功能
- 彩蛋过程指引
- 音频录制
- 根据音频自动解密摩斯电码
- 多种密文和谜题的解密器
# 相关视频及网站
- [本工具的完整教程](https://www.bilibili.com/video/BV1MdLRztEEf) 和 [对滑动条功能的补充说明](https://www.bilibili.com/video/BV15HGvzuEG2)。
- [维和者彩蛋教程-up:鸽子王歌姬poi](https://www.bilibili.com/video/BV1FK411M7GN)
- [铜牌点位教程(26个)-up:博丽-雾希明](https://www.bilibili.com/video/BV1fu4y1o7a6)，这个视频缺少了1个点位，可以去[彩蛋网站](https://wiki.gamedetectives.net/index.php?title=Battlefield_1)找到剩下那个点位的具体位置,也可以直接看[本工具的完整教程最后那P](https://www.bilibili.com/video/BV1MdLRztEEf?p=9)。
- [彩蛋网站](https://wiki.gamedetectives.net/index.php?title=Battlefield_1)
- [摩斯电码翻译网站](https://morsecode.world/international/translator.html)
- [另一个彩蛋网站](https://wiki.bfee.co/index.php?title=Battlefield_1/A_Conflict)
- [银牌点灯解密](https://tools.bfee.co/conflict)
- [解密器](https://rumkin.com/tools/cipher)
- [录制软件Bandicam](https://www.bandicam.cn)
- [音频软件Audacity](https://www.audacityteam.org/download/windows)
# 引用声明
- 银牌点灯解密参考了网站[银牌点灯解密](https://tools.bfee.co/conflict)
- 银牌解密使用到的图片来自网站[另一个彩蛋网站](https://wiki.bfee.co/index.php?title=Battlefield_1/A_Conflict)
# 相关问题
- 本项目开源免费，Github地址：[https://github.com/FlipFlopszzz/PeacekeeperTool](https://github.com/FlipFlopszzz/PeacekeeperTool)。
- 开发环境: python 3.13.0,win11 23H2,GUI使用pyside6编写，打包使用pyinstaller，安装包编译使用Inno Setup。
- 这个软件不读取也不修改战地一的内存，是独立运行的一个外部程序，不会触发反作弊，测试时多次和游戏同时运行也没有被EAAC上市。
- 这个软件的字比较小看不清的话，就Ctrl+滚轮上下滑动调整。
- 本人以前做过两次维和者彩蛋，有点经验，这次全程大约花费3个小时。初次上手的话大概4-5小时就能结束。这个软件主要简化的是金银铜牌和逐步升级的获取，具体体现在摩斯电码的自动识别，解密器的集成，金牌的灯开关序列的遍历，银牌点灯解密器以及坐标系的显示。而且考虑到过去的视频教程中提到的彩蛋网站，有的年久失修，有的使用麻烦，有的在大陆不方便访问，从这个意义上讲，这个软件顺便把目前(2025-4-17)能用的资源和网站汇总了，并把一部分功能简化并搬到软件上。
- 就测试的几十段素材(包括逐步升级、铜牌和金牌)而言，摩斯电码的自动识别准确度在90%以上。有一些片段由于识别错误或把关键片段之外的摩斯电码合并进来等原因，导致转换得到的英文字符中有错误的部分，在解密器解密之后更加难以解读。但是如果通过自己模糊判断或使用“查看图像”功能来排除错误,多余部分，是能够知悉正确的答案的。目前测试样本量还是太小了，而且不知道录音功能在其他电脑上能否正常工作。
# 更新
- v1.3版本对很多人反馈的识别不出来，识别出乱码还有只能识别出E,I,T等字母等情况进行了修复。原因目前认为是幅值阈值高于幅值导致的，而本人测试得到的固定阈值并不适合很多用户，因此增加了根据具体波形得到对应阈值的逻辑，并且允许用户自己修改阈值。
- v1.4版本，将耗时的音频分析逻辑放到了单独的线程中，避免阻塞主线程及其导致的窗口无响应现象。此外增加了开始识别和显示图像两个按钮在加载时的样式，以匹配前面的更改。
- v1.5版本，新增银牌页面的坐标系4层颜色，方便理解和标记。此外精简了软件大小。
'''
    layout = QVBoxLayout(self)
    self.browser = MarkdownTextBrowser(md_text)
    layout.addWidget(self.browser)


class UsagePage(QWidget):
  def __init__(self):
    super().__init__()
    md_text = '''
# 使用说明
## 彩蛋流程简介
彩蛋总共有七个部分，包括2个背面狗牌：野兽之源和看见天使，3个正面狗牌：金牌不祥之兆，银牌冲突，铜牌初显身手，1个皮肤：M1917-逐步升级，以及最后的维和者所在的地道。其中比较麻烦的是银牌冲突，铜牌初显身手。不能跳过前面6个任务直接去做维和者任务，没有完成前置的话在地道会被毒气秒杀。本软件的教程只是简单的指示而已，如果需要完整的流程以及任务点位，查看视频[维和者彩蛋教程-up:鸽子王歌姬poi](https://www.bilibili.com/video/BV1FK411M7GN)。
## 服务器选择
到伺服器浏览界面，按顺序点击：重设筛选条件-模式选择征服-地图选择某个彩蛋对应的地图-人数不作限制-游戏规模不作限制，在服务器列表中选择没人的服务器，延迟大无所谓没有影响，官服（Official）也无所谓，做彩蛋不怕碰到挂。注意尽量不要选择硬核服（Hardcore）和其他的一些带限制的服（比如B2BCQ,Snipers Paradise），这些服务器的限制（比如硬核服没有小地图，狙服不给用某些武器配备等）会拖慢或影响某些任务的完成。有些服务器进去之后会显示“需要更多玩家才能开始回合”，这个不会影响彩蛋的完成。此外，如果正在做金牌的彩蛋，进去前先点击伺服器资讯，看一下有没有禁用精英兵，如果禁用了就不会刷新精英兵了。关于**天气**对自动识别的影响，铜牌宴厅下雨经过测试是没有问题的，金牌泽布吕赫下雨也没有影响，但是**逐步升级阿尔比恩是有严重影响的，因此做这个任务时不能是下雪天气**。
## 狗牌查看
回到主页，点开士兵，有一栏最顶上是自订士兵，向下滑动，能看到狗牌界面。进去后，分为正面和反面的狗牌，各自有一栏叫进度，里面就放着你获取的前置任务的狗牌。你可能通过近战击杀从敌人身上获取了上述的几个狗牌，但是那是无效的，需要自己做彩蛋才能完成维和者的前置。
## 武器皮肤
回到主页，点开士兵，自订士兵，下面可以选择兵种。选择支援兵，主武器选择M1917机枪（担架），型号无所谓。有一栏是皮肤，后续需要在这里更换为逐步升级。
## 相关设置和说明
- 选项-影像-全萤幕模式，改成无边界，避免后面使用alt+tab切屏时出现问题。然后选项-音效-主音量和音乐音量都拉到100%，避免录制的音频强度过低导致摩斯电码识别出错，也方便听到获取狗牌的音效，系统音量开多少都无所谓，没有影响。
- 听摩斯电码前，把电脑桌面除了战地一外所有声音（比如音乐软件，QQ，开黑软件）关闭，避免干扰摩斯电码的自动识别。麦克风声音理论上不会被捕获，不过还是尽量关掉。地图最好选择流血宴厅，因为摩斯电码的识别测试用的音频都是在这个图录制的，其他图由于背景音不同可能出现错误。听之前，确保拿到耳机，靠近电报机所在的那个壕沟的拐角，alt+tab切屏出去打开软件，开始录制，然后切屏回来，慢慢走到电报机旁边，面对电报机蹲下，比对灯的颜色是不是和软件上提示的相同，同时避免视角转动，这时可以使用手机进行计时，大概录制个30-40秒就行(软件会在60s时自动停止录制)，切屏出去关闭录制，自动保存。
- 在切屏出去解密时，记得隔个一两分钟就要切回来动一下鼠标开几枪，避免挂机太久服务器给你踢了。
- 解密摩斯电码和显示图像时可能会卡一会并且变成无响应，一般是正常的，因为解密需要花费较长时间，等一下就行了。测试后不影响正常使用。
'''
    layout = QVBoxLayout(self)
    self.browser = MarkdownTextBrowser(md_text)
    layout.addWidget(self.browser)


class BeastPage(QWidget):
  def __init__(self):
    super().__init__()
    md_text = '''
# 野兽之源
1. 按照前面讲的选择服务器的方法，进入卡波雷托，选择奥匈帝国，可以开飞机或者骑马，到达指定地点后，面对三个天使雕像，依次用枪打掉相应的身体部分，不能多也不能少，然后向后面走，能看到一个单独的天使雕像，使用G键对着雕像底座丢出手雷。上述步骤完成后能听到一声尖啸。
2. 随后面朝三个天使的方向一直向前走，能看到另一个单独的天使雕像，走到它的后边蹲下，底座是可以互动的，互动后播放音效，获得狗牌，退出查看。
'''
    layout = QVBoxLayout(self)
    self.browser = MarkdownTextBrowser(md_text)
    layout.addWidget(self.browser)


class AngelPage(QWidget):
  def __init__(self):
    super().__init__()
    md_text = '''
# 看见天使
1. 进入索姆河，选择英国，支援兵，带弹药箱和磁吸地雷，部署后向前走到A点也就是最近的房区，会刷新一辆鬼火，然后开车到指定地点（E点），能看到两个水罐。尽量把鬼火停在比较靠近的地方，不然会消失。往前走能看到一个井口，用慈溪丢到这个井的正中间，炸开后能看到一个装置，有五个灯以及上边的一个确认按钮。把灯从左到右依次命名为1-5号灯，接下来我会给出灯的序号，你需要根据灯的序号进行互动，然后按确认按钮，比如我说1-4，就是需要把1，2，3，4号灯都各自互动一下，然后按下确认按钮，随后灯会自动全部亮起来。
## 第一轮按灯
- 1-5
- 1
- 3-5
- 1-2
2. 按完后如果播放音效，并且灯开始闪烁，说明第一轮按灯成功。骑上鬼火回到A点房区（或者重新部署应该也行），找到有烟囱的房子，在烟囱的旁边有个小棚子，用慈溪贴到棚子下这面墙的中央炸开墙，然后爬上房子找到烟囱断掉的地方，爬上去（这个地方可能有点难爬），趴下，会发现里边的左边有一个小小的圆形装置，互动一次，听到音效说明这一步完成。
3. 骑上鬼火回到刚刚的井口，发现灯变成绿色的了。按照上面的方法继续进行互动。
## 第二轮按灯
- 1-5
- 4-5
- 3-5
- 3-5
- 3-5
- 2-5
- 2-5
- 1-5

结束后如果灯变红并且听到音效，说明这个任务完成，退出查看狗牌。
'''
    layout = QVBoxLayout(self)
    self.browser = MarkdownTextBrowser(md_text)
    layout.addWidget(self.browser)


class SkinPage(QWidget):
  def __init__(self):
    super().__init__()

    # 创建主布局
    layout = QVBoxLayout(self)

    # Markdown文本浏览器
    md_text = '''
# 逐步升级（皮肤）
1. 在做这个任务之前确保你已经解锁了M1917机枪也就是担架的任意型号，不然拿了皮肤也没用。选择地图阿尔比恩，**绝对不能是下雪天气，因为自动识别无法工作**，德国，飞机，朝前飞找到D点的一个铁塔，地上有很多铁箱子和木箱子，用枪(别用手雷，后边要用)给木箱子打了，总共9个铁箱子，各自互动1次，这次和下次都不需要特定顺序。不能多也不能少，错了直接重开。
2. 然后走到指定地点，也就是F点的一个房子，里边开门有个木柜子，给它拿手雷炸了，露出一个开关，上边有个骷髅头。跟开关互动1次。
3. 回到刚才的铁塔那里，依然是各自互动一次。然后回到房子里边那个开关那，互动4次。
4. 回到铁塔那里，已经在播放摩斯电码了，直接趴到地上，右耳朵紧贴着这个铁塔，切屏并开始录制，解密得到一串字母。可以录制稍微长一点时间，比如40-50s，可以相互对照提高正确率。不出意外的话，应该是5个字母不断循环。至于判断这五个字母的顺序的方法，需要点击“显示图像”，找到其中的间隔比较大的部分，它的前面/后面就是那5个字母。用5个字母替代下面那串字母中的 XXXXX ，得到完整的一串字母。

- **CAEEB XXXXX FEAADDAD**

5. 回到地图的A点，也就是有一个灯塔的点，附近有6个房子，把这6个房子的煤油灯打碎之后（无顺序），获得灯塔内部6个开关的互动权。给6个开关编号，从下往上依次为FEDCBA。然后根据刚才得到的那串完整的字母，按顺序对开关进行互动，最后跑到灯塔最顶上，可以看到有一个很大的灯，旁边还有一个小灯，灯的互动顺序没问题的话，小灯是可以进行互动的。互动完后，出现烟雾和音效，重新部署查看皮肤。
6. 如果互动出现错误，可以直接停下，等30秒，这时互动的进度就会直接重置。也是由于这个机制，互动的相邻两个开关之间不能超过30秒，否则就会直接被重置，因此动作要稍微快点。
'''
    self.browser = MarkdownTextBrowser(md_text)
    layout.addWidget(self.browser)

    self.input_box = SingleLineInput("输入解密出的5个字母")
    self.text_display = SingleLineTextDisplay("这里将会显示最终的那串字母")
    self.audioMorseDecoder = AudioMorseDecoder(0)

    layout.addWidget(self.audioMorseDecoder)
    layout.addSpacing(60)

    layout.addWidget(self.input_box)
    layout.addSpacing(5)

    layout.addWidget(self.text_display)
    layout.addSpacing(170)

    self.input_box.onTextChanged(self.on_text_changed)

  def on_text_changed(self, text):
    if text:
      self.text_display.setText(
          'CAEEB '+text.upper()+' FEAADDAD')
    else:
      self.text_display.setText("这里将会显示最终的那串字母")


class GoldPage(QWidget):
  def __init__(self):
    super().__init__()

    # 创建主布局
    layout = QVBoxLayout(self)
    layout.setSpacing(10)  # 设置组件之间的垂直间距

    # Markdown文本浏览器
    md_text = '''
# 不祥之兆（金牌）
1.选择泽布吕赫地图，注意服务器必须允许精英兵。尽可能选择不下雨的天气，这样杂音会比较小。选择德国，到达E点拿到入侵者，然后坐船到A点，上岸之后找到一个很高的水塔，爬完第一段梯子之后，切屏打开软件，开始录制，然后爬完第二段梯子，趴下。过一会能听到一个音效，然后开始播放摩斯电码。录制40-50秒那样，停止录制。然后开始解密，总共是22个字母（遇到相同的部分说明是进入下一个循环了）。它们是以下30个字母中的一部分，按顺序找出缺少的8个字母。这里可能解密出多种可能的结果，这种情况需要几种可能性都进行测试，这个彩蛋没有什么试错成本，只需要回去调整灯亮灭顺序即可。

**DULCE ET DECORUM EST PRO PATRIA MORI**  30个字母

然后根据缺少的字母对照下面的这个表格找出对应的数字。比如C对应1，E对应7。总共得到8个数字。

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C | D | A | R | B | N | E | G | M | P |
| F | O | U | Z | I | X | L | K | S | T |

这8个数字对应的是8组灯的亮灭序列。比如数字0对应的那组灯，从左到右就是5个都是灭。

|数字|灯1|灯2|灯3|灯4|灯5|
| --- | --- | --- | --- | --- | --- |
| 0 | 灭 | 灭 | 灭 | 灭 | 灭 |
| 1 | 亮 | 灭 | 灭 | 灭 | 灭 |
| 2 | 亮 | 亮 | 灭 | 灭 | 灭 |
| 3 | 亮 | 亮 | 亮 | 灭 | 灭 |
| 4 | 亮 | 亮 | 亮 | 亮 | 灭 |
| 5 | 亮 | 亮 | 亮 | 亮 | 亮 |
| 6 | 灭 | 亮 | 亮 | 亮 | 亮 |
| 7 | 灭 | 灭 | 亮 | 亮 | 亮 |
| 8 | 灭 | 灭 | 灭 | 亮 | 亮 |
| 9 | 灭 | 灭 | 灭 | 灭 | 亮 |

2.接下来找到在陆地上往E点的方向跑，找到房间“1”，从这个房间的右边进去，左手边是1号机器，往前往右依次为2，3，4号机器，依次对应的就是1-4组灯。如果我上面解密出来的第一个数字是1，那么第一台机器的5个灯从左到右依次设置为亮灭灭灭灭，其他同理。

3.按完四台机器后，继续按原来的方向走，找到房间“3”，从房间右边进去，进门依次为5-8号机器。按完这四个机器，看见烟雾并且听到音效，说明本任务完成，退出查看狗牌。如果没有完成的话可能是摩斯电码解密出错了，可能需要手动查看图像确保解密没有出现错误，解密完可以接着之前的进度接着按灯，不需要重新开始。
'''
    self.browser = MarkdownTextBrowser(md_text)
    layout.addWidget(self.browser)

    self.audioMorseDecoder = AudioMorseDecoder(1)
    layout.addWidget(self.audioMorseDecoder)
    layout.addSpacing(30)

    # 创建输入框
    self.input_box = SingleLineInput("请输入解密摩斯电码得到的22个字母")
    self.input_box.onTextChanged(self.on_text_changed)

    layout.addWidget(self.input_box)

    self.text_display = QTextEdit()
    self.text_display.setObjectName("readOnlyTextDisplay")
    self.text_display.setReadOnly(True)
    self.text_display.setFixedHeight(180)

    layout.addWidget(self.text_display)

    self.text_display.setText("这里将会根据8个字母得到8个数字，对应的灯 状态以及开关序列")  # 显示8行默认文本
    layout.addSpacing(40)

  def on_text_changed(self, text):
    letters = find_missing_letters(text)
    if (len(text) == 0):
      self.text_display.setText("这里将会显示缺少的8个字母，对应的8个数字以及灯的开关序列")
    elif (len(letters) == 1):
      if (letters[0].find('error') != -1):
        self.text_display.setText(
            letters[0]
        )
      else:
        self.text_display.setText(
            get_last_gold_text(letters[0])
        )
    else:
      last_str = f'可能存在以下{len(letters)}种情况:'
      for i, l in enumerate(letters):
        last_str = last_str + \
            (f'\n\n第{i+1}种情况:\n'+get_last_gold_text(letters[i]))
      self.text_display.setText(
          last_str
      )


class SilverPage(QWidget):
  def __init__(self):
    super().__init__()
    md_text = '''
# 冲突（银牌）
1. 地图选择苏瓦松（蘇瓦鬆），尽可能选择雾天，方便后续看地板的灯亮灭，没有也没关系。德国，骑兵，到E点的大房子，进门后，找到所有天花板和位于墙上的灯用枪打掉，落地灯使用医疗包和弹药包扑灭，其中有一个落地灯的底座被很多木箱子挡住了，直接丢手雷给它炸开，后面可能需要和这个灯互动。所有灯被灭掉之后会听到一个很阴间的音效，这一步完成。
2. 走到1号灯那里，趴下，对着底座互动1次，统计有哪些灯亮起来了，比如2，3，5号灯亮了，就找到软件的点灯解密那里找到“第1次”，输入“2 3 5”。同理再重复这样的步骤6次，注意每次都是和1号灯互动。注意6号灯那里会有阳光，很容易误判，可以靠近点，声音开大点，如果听到有“滋滋”的电流声说明是亮的。输入完7次，点击解密，会显示需要互动的灯列表，比如“2，2，3”，所以找到2号灯底座互动2次，3号灯底座互动1次。听到一个很阴间的音效第2步也完成了。
3. 走到雕像那里，可以看到池子里边有一些石头。池子底部是“地上”，地上的两层台阶为“下”，再往上2层台阶为“中”，再往上为“上”。注意，站在房子和雕像中间，背对房子面对雕像为正面。根据给出的图标记出石头所在的位置。总共12个。从仰视图看，中间是雕像，玩家面对雕像，那么左下角就是坐标原点，向上为y轴，右边x轴。
4. 回头面向房子，从左到右依次有8根柱子（除掉最左边和最右边两根），设为1-8号柱。跑到房子的另一面，面对房子，同样有8个柱子，定为9-16号。回到房子里边，正中间有一块区域面对着窗户，这就是灯亮起来的地点，在太阳比较大的时候比较难分清地板是否亮起，所以这就是推荐雾天做这个的原因。面对阳光照进来的那个窗户，左边柱子最近的那个黑色瓷砖的左边那个角向上2格作为坐标原点，朝着两条边延长各自8个瓷砖，其中朝向自己的方向为x轴，朝向窗户的是y轴，得到一个8×8的坐标系。为了方便后续对照坐标，可以重新部署（不会清空前面的进度），选择侦察兵，带上拌雷和狙击手诱饵，放置在坐标系的边角位置，这样可以快速辨认出坐标系的坐标。
5. 接下来我们的任务就是让这个坐标系亮起和石头位置对应的瓷砖。但是有个问题，柱子和坐标的对应关系我们是不知道的，因此我们需要手动测试从而获取对应的关系。我们来到1号柱子，蹲下互动一次，然后同样的方法2号互动一次，回到坐标系查看，如果没有地板亮起来，说明这两个柱子都位于同一个坐标轴；如果有地板亮起来，比如说(3,4)，那么我们可以确定这两个柱子有一个在x轴另一个在y轴，接下来我们需要测试它们具体对应的坐标。因此我们先各自和1，2互动一次（注意在测试坐标轴阶段必须把两根柱子都熄灭，确保不会导致后面混乱）熄灭灯，然后再各自和1，3互动一次，如果这时亮了(3,5)，那么我们就可以确定，1号柱子对应x轴的3，2号柱子对应y轴的4，3号柱子对应y轴的5。后续其他所有柱子都可以用类似的方法获取对应坐标。
6. 绘出完整的坐标系后，就把石头对应的坐标对应的灯画在坐标系上。这时候就可以不熄灭灯了，需要一直亮下去。等到把所有灯都亮起后，会出现烟雾并且听到音效，退出查看狗牌。
'''
    layout = QVBoxLayout(self)
    self.browser = MarkdownTextBrowser(md_text)
    layout.addWidget(self.browser)
    layout_tool = QHBoxLayout()
    self.candleDecryptor = CandleDecryptor()
    layout_tool.addWidget(self.candleDecryptor)
    self.coordinateSystem = CoordinateSystem()
    layout_tool.addWidget(self.coordinateSystem)
    self.sandbags_img = ImageDisplayer(
        ":/resources/silver_sandbags.png", 370)
    layout_tool.addWidget(self.sandbags_img)
    layout.addLayout(layout_tool)
    layout.addSpacing(100)


class CopperPage(QWidget):
  def __init__(self):
    super().__init__()
    md_text = '''
# 初显身手（铜牌）
- 来到最坐牢的铜牌，听电报的地图选择流血宴厅，下不下雨无所谓，美军，骑兵，依次寻找五个耳机刷新点，找到后返回美军出生点的右边战壕那里，提前下马，走到离收音机很近的拐角，切屏打开软件，录制，走到电报机前，面对电报机（注意查看电报机上的灯的颜色，可以用来确定自己现在处于第几步），视角不要动，不要发出任何噪音。可以用手机计时约30-40秒，停止录音，把音频文件交给软件分析摩斯电码。录完之后暂时别离开电报站，防止录音出现问题还得重新进游戏找耳机。后续的录音和分析流程都是这样。
- 按照下面的指示得到密文后，和27个地点名对照，找到对应的地图的地点（可以参考视频[铜牌点位教程(26个)-up:博丽-雾希明](https://www.bilibili.com/video/BV1fu4y1o7a6)和视频[本工具的完整教程](https://www.bilibili.com/video/BV1MdLRztEEf)的最后一P，补充了最后一个地点HILL BARN ADRIATIC），发现标志后鼠标指着一小段时间，听到声音后马上移开，避免触发两次，触发两次会导致本次任务失败。以下的指示只是告诉你解密的流程，可以不用管，直接复制到解密器里边就行了。比如我正在做任务5(以下面的任务序号为准)，那么在解密器那里选择“任务5:栅栏密码(Rail Fence)”，复制摩斯电码进去即可。其他的也是同理，参数都不需要你填。
1. 电报机灯为白色，密文就是原始的摩斯电码。
2. 黄色，摩斯电码需要进行反转。小技巧，比如我解密出正序的摩斯密码为SNEIMAEUTA，发现刚好就是LONGUEVILLE STATUE AMIENS这个地点的后面几个字母，并且其他地点没有完全相同的尾巴，因此可以确定这个地点。
3. 紫色，替换密码（Atbash），摩斯密码复制到Atbash解密器即可得到解密后的密文。
4. 绿色，凯撒密码（ROT），同样复制到解密器里边就行。
5. 透明，先倒置再栅栏密码（Rail Fence）。由于栅栏密码输入密文字数不对会导致解密结果和正确结果天差地别，因此这里解密不出来的话，可以试试增/删字数。这里解密器默认是开启倒置的，如果在倒置状态下删减内容，就在输入框的最右边开始删，反之就从最左边开始一个一个删。还有一种方法，就是这条信息完整解密后的结果的一部分为“<地名> FOURTH RULE.”，也就是说，你可以寻找解密摩斯电码得到的结果中的FOURTH这个单词，它的前面那部分就是地名了。
6. 橙色，解密后的摩斯电码只有E和T，然后E用A替换，T用B替换，使用培根密码（Baconian）解密再使用替换密码解密。这里解密器会自动替换E和T。
7. 粉色，维吉尼亚密码（Vigenère），key=Edward。
8. 黄绿色，自动密钥密码（Autokey），key=George，alphabet key=z。这是最后一个需要解密的任务，当你看到London这个标志后就结束了。
9. 青色，听电报就行了不需要录音也不需要解密，听多长时间随便，然后走开让电报机爆炸。
10. 打开地图庞然暗影，德国，开飞机，飞到指定的风车塔那里（显著特征是左边有棵树），上到顶层的瞭望台那块，等大概2分钟，就会有一只白色的鸽子从左手边飞过来，拿着枪右键瞄准准星一直跟着它，大概几秒后就会听到音效，退出查看狗牌。
- 以下为27个地点(总共9个地图，每个地图3个地点)及其对应的密文：

|地图|密文1|密文2|密文3|
|--|--|--|--|
|亚眠(亚眠)|AMIENS NEUF FURNITURE|CHURCH RUINS AMIENS|LONGUEVILLE STATUE AMIENS|
|流血宴厅(流血宴廳)|BALLROOM MAP VARENNES|STATUES GARDEN VARENNES|VARENNES SERVANT BED|
|法欧堡(法歐堡)|BUCKET MARSHLANDS FAW|OUTPOST BARREL FAW|TREE FORTRESS FAW|
|苏伊士(蘇伊士)|CANAL KANTARA VASES|CRATE TRENCH CANAL|HILL TOWER CANAL|
|帝国边境(帝國邊境)|CASTELLO ISLE ADRIATIC|COASTAL FORTRESS ADRIATIC|HILL BARN ADRIATIC|
|西奈沙漠(西奈沙漠)|CRATE JABAL JIFAR|PILLAR OUTSKIRTS JIFAR|PILLOW MAZAR JIFAR|
|格拉巴山(格拉巴山)|CRATE SEREN VENETIAN|FERRO FIRE VENETIAN|STOVE TURRET VENETIAN|
|圣康坦的伤痕(聖康坦的傷痕)|HOTEL CHECK PERONNE|RUIN VENTURE PERONNE|TRAVECY ATTIC PERONNE|
|阿尔贡森林(阿爾貢森林)|LUGGAGE BASEMENT APREMONT|PANEL WATER APREMONT|TREE TRAIN APREMONT|

- 以下为从任务1到任务8完整的摩斯电码解密出来的原文。
1. GO STRAIGHT TO <location_name>. OLD METHODS COMPROMISED. MUST ACQUIRE NEW KEY. WILL MISS DROPOFF IF DELAY OR INCORRECT LOCATION.
2. <reversed_location_name> REMEMBER FIRST RULE. IF COMPROMISED L PILL.
3. <atbash_cipher> SECOND RULE. ON SIGHTING. REPORT AND WAIT. INVESTIGATING ALONE COULD LEAD TO DEATH
4. <rot_cipher> THIRD RULE. IF TAKEN BY THE OTHERS DISCOVER MEANS TO COMMUNICATE TO HOUSE
5. <rail_fence> FOURTH RULE. KILL ALL ON SAME TRAIL. REMOVE DOG TAGS AND REPORT TO HOUSE
6. <double_cipher> MORSE MESSAGES BEING INTERCEPTED. BEGINNING FULL ENCRYPTION SOON
7. LUGGAGEBASEMENTVARENNESALLIESCANBECLOTHEDASENEMIESENEMIESCANBECLOTHEDASALLIESALWAYSUSEID（这里是示例，地名为LUGGAGE BASEMENT VARENNES）
8. HILLBARNADRIATICFINALBELIEVEEVERYTHINGREPORTEVERYTHING（这里是示例，地名为HILL BARN ADRIATIC）
'''
    layout = QVBoxLayout(self)
    self.browser = MarkdownTextBrowser(md_text)
    layout.addWidget(self.browser)

    self.audioMorseDecoder = AudioMorseDecoder(2)
    layout.addWidget(self.audioMorseDecoder)

    layout.addSpacing(40)

    self.cipherDecryptor = CipherDecryptor()
    layout.addWidget(self.cipherDecryptor)

    layout.addSpacing(70)


class LastPage(QWidget):
  def __init__(self):
    super().__init__()
    md_text = '''
# 最终任务
1. 恭喜你坚持到了最后一个任务！首先打开士兵-狗牌，在正面-进度那里选择金银铜中任意一个进行装备，背面-进度，选择野兽支援和看见天使中任意一个装备。然后退回上一级彩蛋，点击自订士兵-支援兵，主武器选择M1917机枪，皮肤装备逐步升级。确保你已经完成了前置的所有6个任务，不然在地道的某一层会被毒气直接秒杀。
2. 地图选择帕斯尚尔，尽可能选择延迟低一点的，不然操作不跟手可能会影响跑路。德国，支援兵，装备M1917+逐步升级，其他的无所谓（那个拿着扳手加速的小技能不是必须的）。
3. 在进地道之前，先了解以下知识。地道总共15层，每层都有毒气追你，越到后边伤害越高。里边啥都不能干只能走路（注意不是奔跑），防毒面具也带不了。有节奏地走+跳会比走快一点，不过就算一直走也死不了。走到每一层的尽头后，你会看到一片木排，前面还有一个阀门，互动就会让你过大概1秒后进入下一层，但是如果不按的话就不会掉下去并且毒气也不会追你，因此在这段时间可以用来回血和查看下一层的路线。尽可能回到80血以上最好是满血，这样即使摔掉了一些血也不至于被毒死。准备下去时，人站在这个阀门所在的区域，尽量不要直接站在木排上，面对下一层前进的方向，并且直到掉下去之前全程按着蹲键不松手，这样能够尽可能减少摔掉很多血的风险。
4. 向前边走能看到一个木桥，下去以后有一个洞口，上边有个木牌，拿枪给它打烂，露出骷髅头。蹲下，可以发现左右各有一个阀门，接下来需要按照顺序和阀门进行互动。L：左，R：右。注意不要狂按，按完一下确认听到声音证明这次生效后再按下一次。
- LLRR
- LRLR
- RL
- RRR
- LRR
- LRR
- LLLL
- R
- LLL
5. 等一小会洞口会被炸开，里边有个阀门，互动之后就会进到地道里边。按M键放大小地图，可以发现小地图上标记了4个方向NSWE，同时你可以看到你自己的视角是一个白色的扇形，比如本层的方向是W，那么就用你的人物这个扇形对着小地图上的W，朝这个方向走就是正确的。以下为15层的方向。
- **WESWE WWNSW NWSWS**

到达最后一层的尽头后，有一个铁箱子，上边的就是维和者左轮(Peacekeeper)，长按R捡起来它就是你的了。这时候直接退出游戏或者重新部署都可以，自订士兵可以直接装备了。后续使用维和者左轮击杀100个敌人即可获得狗牌“觉醒”。

# 恭喜你完成了维和者彩蛋！
使用完这个工具可以直接卸载，记得把录制的那些音频删掉。
如果使用中遇到任何问题都可以去本工具的B站视频评论或者私信本人，或者去Github上提issue。
'''
    layout = QVBoxLayout(self)
    self.browser = MarkdownTextBrowser(md_text)
    layout.addWidget(self.browser)
