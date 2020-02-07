# Words2Card
诗词歌词格言生成配图卡片

### 实现过程
我有一个习惯，看到喜欢的句子，或有了特别的感悟，愿意记在手机的备忘录里，想必很多人都会这样。但我收藏的句子主体还是以图片的形式存在了相册里，这让句子们很分散，不方便翻看和分享，这尤其触到了我强迫症的敏感神经。于是我希望有一个类似网易云音乐推出的歌词生成图片分享的工具，来帮我整理我的摘抄。

本项目只是在[@Urinx](https://github.com/Urinx)的[NeteaseLyric](https://github.com/Urinx/NeteaseLyric)上的改进。实现过程可以参考我的博客[Python文字转图片-诗词歌词格言生成配图卡片](https://blog.csdn.net/shanchenglang/article/details/104213673)。

### 使用说明
请先安装 PIL 等第三方包依赖，然后下载本工程，工程结构说明：
```
│  data.txt  # json数据文件
│  words2card.py  # 核心程序
│
├─image   # 储存供选择的封面图片
│      1.jpg
│      2.jpg
│      3.png
│
├─output  # 输出制作的卡片的位置
│      森见登美彦1581075253.png
│
└─static  # 制作卡片时使用的静态资源
        netease_icon.png  # 图标文件
        STHeiti_Light.ttc # 字体文件
```
然后将自己的封面图片放在`image/`路径下，并编写`json`数据文件。样例如下：
```
[{
	"author": "森见登美彦",
	"quotes": "在世界蔓延滋生的‘烦恼’大致可分为两种：一是无关紧要的事，二是无能为力的事。两者同样都只是折磨自己。如果是努力就能解决的事，与其烦恼不如好好努力；若是努力也无法解决的事，那么付出再多也只是白费力气。",
	"image": ""
}]
```
`json`格式要求一个`author`关键字标识作者或标题，一个`quotes`关键字标识引用内容，一个`image`关键字标识图片地址。注意这里的图片地址既可以是本地的相对地址，也可以是网络连接地址。`author`缺省时默认为`无名氏`，`image`缺省时默认在`./image/`随机选择一幅`jpg`或`png`图片。

之后直接运行`words2card.py`即可，结果将在`output/`下生成：
![alt](https://github.com/ThomasAtlantis/Words2Card/blob/master/output/%E6%A3%AE%E8%A7%81%E7%99%BB%E7%BE%8E%E5%BD%A61581077406.png)
