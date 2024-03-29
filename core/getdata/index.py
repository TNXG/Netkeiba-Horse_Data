"""
@Project   : Get_Netkeiba_data
@Author    : tianxiang_tnxg
@Blog      : https://blog.tnxg.top
@Use       : /v1/netkeiba/horse/
@Other     : 可惜你不看赛马娘，也不知道她们在我心里的意义。
"""
import json
import re

import pandas as pd
import requests
import zhconv

# 通过登录获得完整数据
cookie = {
    "nkauth": "你的Netkeiba Cookie nkauth 字符段",
    "nd_ua": "你的Netkeiba Cookie nd_ua 字符段"
}


def gethorsedata(horseid):
    url = "https://db.netkeiba.com/horse/" + horseid
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    response = requests.get(url, headers=headers, cookies=cookie)
    response.encoding = "EUC-JP"
    html = response.text

    # 获取基础信息
    try:
        # if True == True:
        horse_jp_name = re.findall(
            r'<title>(.*?)\| 競走馬データ - netkeiba\.com</title>', html)[0].replace(" ", "")
        horse_jp_name = re.sub(r'\(.*?\)', '', horse_jp_name)
        horse_en_name = re.findall(r'\((.*?)\)の競走馬データです。', html)[0]
        horse_chinese_name = gethorsechinese(horse_jp_name)
        horse_birth = re.findall(
            r'<th>生年月日</th>\s<td>(.*?)</td>', html)[0].replace(" ", "")
        horse_trainer = re.findall(
            r'<th>調教師</th>\s<td><a href=(.*?)>(.*?)</td>', html)[0][1]
        horse_trainer = horse_trainer.replace("</a>", "").replace(" ", "")
        horse_owner = re.findall(
            r'<th>馬主</th>\s<td><img (.*)">(.*?)</a></td>', html)[0][1]
        horse_birthplace = re.findall(
            r'<th>産地</th>\s<td>(.*?)</td>', html)[0].replace(" ", "")
        horse_bloodline_all = get_middle_str(
            html, '血統</p>', '血統詳細・兄弟馬</a></p>')
        horse_bloodline = re.findall(
            r'<td rowspan="2" class="b_ml">\s<a (.*?)">(.*?)</a>', horse_bloodline_all)[0][1]
        horse_bloodline = horse_bloodline + '/' + \
                          re.findall(
                              r'<td rowspan="2" class="b_fml">\s<a (.*?)">(.*?)</a>', horse_bloodline_all)[0][1]
        hores_get_money = get_middle_str(
            html, '<th>獲得賞金</th>', '<th>通算成績</th>')
        hores_get_money = get_middle_str(
            hores_get_money, '<td>', '</td>').replace(" ", "").replace("\n", "")
        hores_result_all = get_middle_str(
            html, '<th>通算成績</th>', '<th>主な勝鞍</th>')
        hores_result = re.findall(r'<td>(.*?)\[', hores_result_all)[0].replace(
            " ", "") + '[' + re.findall(r'全競走成績">(.*?)</a>]', hores_result_all)[0].replace(" ", "") + ']'
        try:
            hores_achievement = get_middle_str(
                html, '受賞歴', '<div class="db_main_deta">')
            hores_achievement = re.findall(
                r'<td>(.*?)</td>', hores_achievement)[0].replace(" ", "")
            hores_achievement = hores_achievement.split("、")
        except:
            hores_achievement = ''
    except Exception as e:
        return 'error'

    try:
        # if True == True:
        # 获取赛马成绩
        url = "https://db.netkeiba.com/horse/result/" + horseid
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        response = requests.get(url, headers=headers, cookies=cookie)
        response.encoding = "EUC-JP"
        data = pd.read_html(response.text)
        pd.set_option('max_colwidth', 400)
        # 显示所有列，把行显示设置成最大
        pd.set_option('display.max_columns', None)
        # 显示所有行，把列显示设置成最大
        pd.set_option('display.max_rows', None)
        # pandas输出不换行
        pd.set_option('expand_frame_repr', False)
        data = data.__str__()

        # 以下信息仅适配东海帝王及其类似数据使用
        # data = get_middle_str(data, '着 順', '騎手').replace('\n\n', "")
        # data = get_middle_str(data, 'ペース', '上り').replace('\n\n', "")

        # 去除首尾的中括号
        data = data[1:-1]
        # 以换行符分割字符串
        data = data.split('\n')
        # 从中去除[0]的数据
        data = data[1:]
        # json编码方便数据清洗
        data = json.dumps(data, ensure_ascii=False)
        # 删除数据中多余的空格
        clean_str = ' '.join(data.split())
        # 再解码json(什么睿智行为)
        clean_str = json.loads(clean_str)
        horse_race = []
        for i in clean_str:
            i = i.split(' ')
            race_date = i[1]
            racecourse_weather = i[3]
            race_name = i[5]
            race_horse_popularity = i[11]
            race_horse_order = i[12]
            race_horse_rider = i[13]
            race_horse_rider_weight = i[14]
            race_distance = i[15]
            racecourse_status = i[16]
            if race_date == '':
                race_date = 'none'
            if racecourse_weather == '':
                racecourse_weather = 'none'
            if race_name == '':
                race_name = 'none'
            if race_horse_popularity == '':
                race_horse_popularity = 'none'
            if race_horse_order == '':
                race_horse_order = 'none'
            if race_horse_rider == '':
                race_horse_rider = 'none'
            if race_horse_rider_weight == '':
                race_horse_rider_weight = 'none'
            if race_distance == '':
                race_distance = 'none'
            if racecourse_status == '':
                racecourse_status = 'none'
            race_all = {}
            race_all['race_date'] = race_date
            race_all['racecourse_weather'] = racecourse_weather
            race_all['race_name'] = race_name
            race_all['race_horse_popularity'] = race_horse_popularity
            race_all['race_horse_order'] = race_horse_order
            race_all['race_horse_rider'] = race_horse_rider
            race_all['race_horse_rider_weight'] = race_horse_rider_weight
            race_all['race_distance'] = race_distance
            race_all['racecourse_status'] = racecourse_status
            horse_race.append(race_all)
    except Exception as e:
        horse_race = ''

    try:
        # 获取赛马血统
        url = "https://db.netkeiba.com/horse/ped/" + horseid
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        response = requests.get(url, headers=headers, cookies=cookie)
        response.encoding = "EUC-JP"
        data = pd.read_html(response.text)[0]
        pd.set_option('max_colwidth', 400)
        # 显示所有列，把行显示设置成最大
        pd.set_option('display.max_columns', None)
        # 显示所有行，把列显示设置成最大
        pd.set_option('display.max_rows', None)
        # pandas输出不换行
        pd.set_option('expand_frame_repr', False)
        父 = data.iloc[0, 0]
        父 = re.search(r'(\D+)', 父).group(0).rstrip() + '|' + re.search(r'(\d{4})', 父).group(0)
        母 = data.iloc[16, 0]
        母 = re.search(r'(\D+)', 母).group(0).rstrip() + '|' + re.search(r'(\d{4})', 母).group(0)
        祖父 = data.iloc[0, 1]
        祖父 = re.search(r'(\D+)', 祖父).group(0).rstrip() + '|' + re.search(r'(\d{4})', 祖父).group(0)
        祖母 = data.iloc[8, 1]
        祖母 = re.search(r'(\D+)', 祖母).group(0).rstrip() + '|' + re.search(r'(\d{4})', 祖母).group(0)
        母父 = data.iloc[16, 1]
        母父 = re.search(r'(\D+)', 母父).group(0).rstrip() + '|' + re.search(r'(\d{4})', 母父).group(0)
        外祖母 = data.iloc[26, 1]
        外祖母 = re.search(r'(\D+)', 外祖母).group(0).rstrip() + '|' + re.search(r'(\d{4})', 外祖母).group(0)
        hores_blood = {"父": 父, "母": 母, "祖父": 祖父, "祖母": 祖母, "母父": 母父, "外祖母": 外祖母}
    except Exception as e:
        hores_blood = ''
        print(e)

    if horse_jp_name == '':
        horse_jp_name = 'none'
    if horse_en_name == '':
        horse_en_name = 'none'
    if horse_chinese_name == '':
        horse_chinese_name = 'none'
    if horse_birth == '':
        horse_birth = 'none'
    if horse_trainer == '':
        horse_trainer = 'none'
    if horse_owner == '':
        horse_owner = 'none'
    if horse_bloodline == '':
        horse_bloodline = 'none'
    if horse_birthplace == '':
        horse_birthplace = 'none'
    if hores_get_money == '':
        hores_get_money = 'none'
    if hores_result == '':
        hores_result = 'none'
    if hores_achievement == '':
        hores_achievement = 'none'
    if horse_race == '':
        horse_race = 'none'

    alldata = {}
    alldata['horse_jp_name'] = horse_jp_name
    alldata['horse_en_name'] = horse_en_name
    alldata['horse_chinese_name'] = horse_chinese_name
    alldata['horse_birth'] = horse_birth
    alldata['horse_trainer'] = horse_trainer
    alldata['horse_owner'] = horse_owner
    alldata['horse_birthplace'] = horse_birthplace
    alldata['horse_get_money'] = hores_get_money
    alldata['horse_bloodline'] = horse_bloodline
    alldata['horse_result'] = hores_result
    alldata['horse_achievement'] = hores_achievement
    alldata['horse_race'] = horse_race
    alldata['horse_blood'] = hores_blood
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
            horse_chinese_name = re.findall(
                r'<td width=70>(.*?)</td><td width=70>', response.text)[0]
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
