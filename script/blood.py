import json
import logging
import re
import requests

import pandas as pd

url = "https://db.netkeiba.com/horse/ped/1985102167"
html = requests.get(url)
html.encoding = 'EUC-JP'
data = pd.read_html(html.text)[0]
pd.set_option('max_colwidth', 400)
# 显示所有列，把行显示设置成最大
pd.set_option('display.max_columns', None)
# 显示所有行，把列显示设置成最大
pd.set_option('display.max_rows', None)
# pandas输出不换行
pd.set_option('expand_frame_repr', False)
# 通过logging模块输出本地日志
logging.basicConfig(level=logging.DEBUG, filename='panda_test.json', filemode='w', format='')
# 获取表格中0,0的数据
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
# 组合json数据
data = {"父": 父, "母": 母, "祖父": 祖父, "祖母": 祖母, "母父": 母父, "外祖母": 外祖母}
# 转换成json格式
data = json.dumps(data, ensure_ascii=False)
print(data)
