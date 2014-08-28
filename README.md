yySubDownloader
===============

一个下载 YYETS 上字幕的 python 脚本

## 功能
- 下载 YYETS 上搜索结果第一页的字幕。
- 可以连续选择(e.g., 1-7)，也可以非顺序选择（1,3,5)。
- 默认优先下载简体&英文的字幕，然后是简体，繁体&英文，繁体,英文）。
-  默认支持 OS X, 因为我选择了 The Unarchiver 来解压压缩包（rar, zip), 如果要换解压软件，请在下面 `"app"`修改。（不确定其他解压缩软件能正常工作）
- 可以修改下载字幕的优先级（在 .yysub 文件里, 隐藏文件，请用终端打开）
```javascript
{

	"langPriority" :[
	"简体-英文-srt", "chs-eng-srt", 
	"[^&]简体[^&]-srt", "[^&]chs[^&]-srt", 
	"繁体-英文-srt", "cht-eng-srt", 
	"[^&]繁体[^&]-srt", "[^&]cht[^&]-srt",
	"[^&]英文[^&]-srt", "[^&]eng[^&]-srt",

	"简体-英文-ass", "chs-eng-ass",
	"[^&]简体[^&]-ass", "[^&]chs[^&]-ass",
	"繁体-英文-ass", "cht-eng-ass",
	"[^&]繁体[^&]-ass", "[^&]cht[^&]-ass",
	"[^&]英文[^&]-ass","[^&]eng[^&]-ass"
	],

	"app": "/Applications/The Unarchiver.app/Contents/MacOS/The Unarchiver"
}



## 使用

下载并解压后
- `sudo pip install -e yySubDownloader`
- 需要 lxml 库才能运行，`sudo pip install lxml`
- 下载的字幕在终端所在目录下

## 第三方库

- lxml 解析网页


## 致谢
所有在制作字幕上无私奉献的人
