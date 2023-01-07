# Netkeiba Horse Data

## 简介

通过Python正则爬取[netkeiba.com](https://netkeiba.com)的赛马数据，通过PHP将信息返回到前端。

包括赛马的基本信息、赛马的赛事信息等。

## 使用方法

### 1. 安装PHP和Python

我们需要PHP和Python来运行本项目，通过Python爬取数据，通过PHP将数据返回到前端。

默认运行环境为PHP8.1.12和Python3.9.9。

### 2. 安装Python依赖

```bash
cd core
pip install -r requirements.txt
```

### 3. PHP配置

PHP需要开启`exec`函数，以便于调用Python脚本。

### 4. 运行

按照上述步骤安装好环境后，直接访问即可，若无法正常输出数据，请检查您的服务器是否开启了`exec`函数及服务器是否可以链接到[netkeiba.com](https://netkeiba.com)

## 须知

本项目仅供学习交流使用，不得用于商业用途。

数据来源于[netkeiba.com](https://netkeiba.com)，版权归[netkeiba.com](https://netkeiba.com)所有。

## 其他

### 关于翻译数据

部分处于赛马娘企划当中的赛马中文译名由项目[MinamiChiwa/Trainers-Legend-G](https://github.com/MinamiChiwa/Trainers-Legend-G) 和 [萌娘百科](http://moegirl.org.cn/%E8%B5%9B%E9%A9%AC%E5%A8%98) 提供数据并保存在[horse_name.json](https://github.com/TNXG/Netkeiba-Horse_Data/blob/master/core/horse_name.json)。

不属于赛马娘企划的赛马中文译名由 [WP Stud](https://www.wpstud.com/) 提供。

[horse_name.json](https://github.com/TNXG/Netkeiba-Horse_Data/blob/master/core/horse_name.json)当中的赛马中文译名优先级最高，若有翻译错误或补充翻译，欢迎提交PR。

### 翻译信息须知

* [ハッピーミーク](https://zh.moegirl.org.cn/%E5%BF%AB%E4%B9%90%E7%B1%B3%E5%8F%AF)、[ビターグラッセ](https://zh.moegirl.org.cn/Bitter_Glasse)、[リトルココン](https://zh.moegirl.org.cn/Little_Cocon)为CyGames原创马娘 ，但在我整理翻译数据时，我发现Netkeiba当中有这些赛马的数据，其登记时间为2020年，所以我保留了这些赛马的台版翻译，这些翻译未获共识，仅供参考。
* 提交PR前，请先检查翻译是否已经存在。请注意，马主翻译优先级最高，其次是香港马会的中文译名，最后是人们共识的中文译名。（コントレイル：铁鸟翱天>飞机云，セイウンスカイ：青云天空>星云天空）
* json内`"all"`、`"jp2cn"`、`"cn2jp"`都需要填写，请按照原先内容格式进行补充，请将新的补充放在最后一行。

