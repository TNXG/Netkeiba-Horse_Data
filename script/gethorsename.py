import requests
import json
import zhconv
import re


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
        print('自定义字典中找到该马名'+horse_chinese_name)
    except:
        status = False
        print('自定义字典中未找到该马名')

    if not status:
        print('开始爬取wpstud')
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
            print(response.text)
            horse_chinese_name = re.findall(
                r'<td width=70>(.*?)</td><td width=70>', response.text)[0]
            horse_chinese_name = zhconv.convert(horse_chinese_name, 'zh-cn')
            return horse_chinese_name
        except:
            return ''
    else:
        return horse_chinese_name


print(gethorsechinese('デアリングタクト'))
