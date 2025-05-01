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