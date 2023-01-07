"""
@Project   : Get_Netkeiba_data
@Author    : tianxiang_tnxg
@Blog      : https://blog.tnxg.top
@Use       : /v1/netkeiba/horse/
@Other     : 可惜你不看赛马娘，也不知道她们在我心里的意义。
"""
import json
import re
import sys

import requests
import zhconv
import logging
import scrapy


def php_get():
    print(getdata(sys.argv[1]))


def getdata(horseid):
    url = "https://db.netkeiba.com/horse/" + horseid
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.encoding = "EUC-JP"
    html = response.text
    try:
    # if True == True:
        horse_jp_name = re.findall(r'<title>(.*?)\| 競走馬データ - netkeiba\.com</title>', html)[0].replace(" ", "")
        horse_en_name = re.findall(r'\((.*?)\)の競走馬データです。', html)[0]
        horse_chinese_name = gethorsechinese(horse_jp_name)
        horse_birth = re.findall(r'<th>生年月日</th>\s<td>(.*?)</td>', html)[0].replace(" ", "")
        horse_trainer = re.findall(r'<th>調教師</th>\s<td><a href=(.*?)>(.*?)</td>', html)[0][1]
        horse_trainer = horse_trainer.replace("</a>", "").replace(" ", "")
        horse_owner = re.findall(r'<th>馬主</th>\s<td><img (.*)">(.*?)</a></td>', html)[0][1]
        horse_birthplace = re.findall(r'<th>産地</th>\s<td>(.*?)</td>', html)[0].replace(" ", "")
        horse_Bloodline_all = get_middle_str(html, '血統</p>', '血統詳細・兄弟馬</a></p>')
        horse_Bloodline = re.findall(r'<td rowspan="2" class="b_ml">\s<a (.*?)">(.*?)</a>', horse_Bloodline_all)[0][1]
        horse_Bloodline = horse_Bloodline + '/' + re.findall(r'<td rowspan="2" class="b_fml">\s<a (.*?)">(.*?)</a>', horse_Bloodline_all)[0][1]
        hores_get_money = get_middle_str(html, '<th>獲得賞金</th>', '<th>通算成績</th>')
        hores_get_money = get_middle_str(hores_get_money, '<td>', '</td>').replace(" ", "").replace("\n", "")
    except:
        return 'error'

    if horse_jp_name == "":
        horse_jp_name = "none"
    if horse_en_name == "":
        horse_en_name = "none"
    if horse_chinese_name == "":
        horse_chinese_name = "none"
    if horse_birth == "":
        horse_birth = "none"
    if horse_trainer == "":
        horse_trainer = "none"
    if horse_owner == "":
        horse_owner = "none"
    if horse_Bloodline == "":
        horse_Bloodline = "none"
    if horse_birthplace == "":
        horse_birthplace = "none"
    if hores_get_money == "":
        hores_get_money = "none"

    alldata = {}
    alldata['horse_jp_name'] = horse_jp_name
    alldata['horse_en_name'] = horse_en_name
    alldata['horse_chinese_name'] = horse_chinese_name
    alldata['horse_birth'] = horse_birth
    alldata['horse_trainer'] = horse_trainer
    alldata['horse_owner'] = horse_owner
    alldata['horse_birthplace'] = horse_birthplace
    alldata['horse_get_money'] = hores_get_money
    alldata['horse_Bloodline'] = horse_Bloodline
    return json.dumps(alldata, ensure_ascii=False)


def gethorsechinese(horsename):
    global horse_chinese_name
    url = 'https://assets.tnxg.whitenuo.cn/data/horse_name.json'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    horsejson = json.loads(response.text)
    try:
        horse_chinese_name = horsejson['jp2cn'][horsename]
        status = True
    except:
        status = False

    if not status:
        try:
            url = "https://www.wpstud.com/horsesearch/horsesearch.asp"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
            }
            # 设置post数据
            data = {
                "horseradio": "hnradio",
                "HorseText": horsename,
                "Select1": "allRegion",
                "Select2": "allSex",
            }
            response = requests.post(url, headers=headers, data=data)
            response.encoding = "utf-8"
            horse_chinese_name = re.findall(r'<td width=70>(.*?)</td><td width=70>', response.text)[0]
            horse_chinese_name = zhconv.convert(horse_chinese_name, 'zh-cn')
            return horse_chinese_name
        except:
            return ''
    else:
        return horse_chinese_name


def get_middle_str(content, start_str, end_str):
    pattern_str = r'%s(.+?)%s' % (start_str, end_str)
    pattern = re.compile(pattern_str, re.S)
    result = pattern.findall(content)
    return result[0]


if __name__ == '__main__':
    php_get()
