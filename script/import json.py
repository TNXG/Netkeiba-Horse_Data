import json
import re

# 获取两段字符串中间的字符串


def get_middle_str(content, start_str, end_str):
    pattern_str = r'%s(.+?)%s' % (start_str, end_str)
    pattern = re.compile(pattern_str, re.S)
    result = pattern.findall(content)
    return result[0]


with open('113.json', 'r', encoding='utf-8') as f:
    data = f.read()
    newdata = json.loads(data)
    savedata = {}
    n = 0
    for i in newdata['all']:
        if n == 0:
            jp_name = 'スペシャルウィーク'
        else:
            print()
            jp_name = re.findall(r'"(.*?)": "' + i + r'"', data)[0]
        print(jp_name)
        savedata[i] = jp_name
        n += 1

print('------------------')
print(json.dumps(savedata, ensure_ascii=False))
