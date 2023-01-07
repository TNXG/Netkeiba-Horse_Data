import pandas as pd
import logging
import re
import json

def get_middle_str(content, start_str, end_str):
    pattern_str = r'%s(.+?)%s' % (start_str, end_str)
    pattern = re.compile(pattern_str, re.S)
    result = pattern.findall(content)
    return result[0]

url = "https://db.netkeiba.com/horse/result/1985102167"
data = pd.read_html(url)
pd.set_option('max_colwidth',400)
#显示所有列，把行显示设置成最大
pd.set_option('display.max_columns', None)
#显示所有行，把列显示设置成最大
pd.set_option('display.max_rows', None)
# 通过logging模块输出本地日志
logging.basicConfig(level=logging.DEBUG, filename='panda_test.json', filemode='w', format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
data = data.__str__()
logging.debug(data)
# data = get_middle_str(data, '着 順', '騎手').replace('\n\n', "")
data = get_middle_str(data, 'ペース', '上り').replace('\n\n', "")
# 去掉收尾再以换行符分割字符串
data = data.split('\n')
data = json.dumps(data, ensure_ascii=False).replace('"  \\\\", ', '')
clean_str = ' '.join(data.split())
clean_str = json.loads(clean_str)
# logging.debug(clean_str)
# n = 0
# for i in clean_str:
#     i = i.split(' ')
#     print(i[1]+i[5])
