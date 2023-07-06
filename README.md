# Netkeiba Horse Data

## 简介

通过Python正则和Python Pandas爬取[netkeiba.com](https://netkeiba.com)的赛马数据

包括赛马的基本信息、赛马的赛事信息等。

目前本项目通过Python Flask提供网络服务，旧版本（php+python）请查看`v1`分支

## 使用方法

### 1. 安装Python

我们使用Python来运行本项目，所以您需要安装Python环境。

默认运行环境为Python3.9.9。

### 2. 安装Python依赖

```bash
pip install -r requirements.txt
```
### 3. 配置Netkeiba账户信息

#### 3.1 注册

首先，您需要在[netkeiba.com](https://netkeiba.com)注册一个账户，然后在`core/getdata/index.py`的`Cookie`字段中填写您的账户信息。

#### 3.2 获取网页Cookie信息

访问一匹赛马的信息页面（这里以[东海帝王](https://db.netkeiba.com/horse/1981107017/)的信息为例）

访问 [https://db.netkeiba.com/horse/1981107017/](https://db.netkeiba.com/horse/1981107017/)

使用`F12`打开开发者工具，点击`Network`，然后刷新网页，翻到最上面，找到`1981107017/`这个请求，展开

下翻找到`请求标头`，找到`cookie`项，然后其中的`nkauth`和`nd_ua`就是需要的信息 ~~(我也不知道`nd_ua`有什么用~~

#### 3.3 我们为什么需要这些信息？

部分赛马，比如[鲁道夫象征](https://db.netkeiba.com/horse/1981107017/)，需要登录才能获取完整的竞赛信息，所以我们需要通过cookie登录，才能获取到这些数据。

### 4. 运行

按照上述步骤安装好环境后，直接访问即可，若无法正常输出数据，请检查您的服务器是否可以链接到[netkeiba.com](https://netkeiba.com)

## 须知

本项目仅供学习交流使用，其子项目带来的一切后果与本项目无关。

数据来源于[netkeiba.com](https://netkeiba.com)，除去译名以外的所有数据版权归[netkeiba.com](https://netkeiba.com)所有。

项目于2023年1月8日起修改为GNU GENERAL PUBLIC LICENSE Version 3(GNU GPLv3)协议。

## 其他

### 关于翻译数据

部分处于赛马娘企划当中的赛马中文译名由项目[MinamiChiwa/Trainers-Legend-G](https://github.com/MinamiChiwa/Trainers-Legend-G) 和 [萌娘百科](http://moegirl.org.cn/%E8%B5%9B%E9%A9%AC%E5%A8%98) 提供数据并保存在[horse_name.json](https://github.com/TNXG/Netkeiba-Horse_Data/blob/master/core/horse_name.json)。

不属于赛马娘企划的赛马中文译名由 [WP Stud](https://www.wpstud.com/) 提供。

[horse_name.json](https://github.com/TNXG/Netkeiba-Horse_Data/blob/master/core/horse_name.json)当中的赛马中文译名优先级最高，若有翻译错误或补充翻译，欢迎提交PR。

### 翻译信息须知

* [ハッピーミーク](https://zh.moegirl.org.cn/%E5%BF%AB%E4%B9%90%E7%B1%B3%E5%8F%AF)、[ビターグラッセ](https://zh.moegirl.org.cn/Bitter_Glasse)、[リトルココン](https://zh.moegirl.org.cn/Little_Cocon)为CyGames原创马娘 ，但在我整理翻译数据时，我发现Netkeiba当中有这些赛马的数据，其登记时间为2020年，所以我保留了这些赛马的台版翻译，这些翻译未获共识，仅供参考。
* 提交PR前，请先检查翻译是否已经存在。请注意，马主翻译优先级最高，其次是香港马会的中文译名，最后是人们共识的中文译名。（コントレイル：铁鸟翱天>飞机云，セイウンスカイ：青云天空>星云天空）
* json内`"all"`、`"jp2cn"`、`"cn2jp"`都需要填写，请按照原先内容格式进行补充，请将新的补充放在最后一行。

# 更新日志

### 2023-7-6

* 新增血统数据的获取
* 更换Web框架为Flask
* 新增译名

### 2023-4-16

* 修复从wpstud获取中文名出现问题的Bug

### 2023-3-5

* 更换Web框架为FastAPI

### 2023-3-2

* 新增Netkeiba账户信息配置，部分赛马需要登录才能获取完整的竞赛信息，所以我们需要通过cookie登录，才能获取到这些数据。
