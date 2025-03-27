#!/usr/bin/env python3

import json
from collections import defaultdict

yun_data = {
    "ā":"l","á":"u","ǎ":"m","à":"i",
    "ē":"r","é":"e","ě":"l","è":"i",
    "ī":"j","í":"b","ǐ":"g","ì":"t",
    "ō":"p","ó":"e","ǒ":"i","ò":"g",
    "ū":"a","ú":"l","ǔ":"m","ù":"h",
    "ǖ":"h","ǘ":"m","ǚ":"h","ǜ":"f",
    "āi":"b","ái":"d","ǎi":"u","ài":"o",
    "ān":"n","án":"k","ǎn":"o","àn":"j",
    "āng":"u","áng":"w","ǎng":"p","àng":"d",
    "āo":"q","áo":"i","ǎo":"x","ào":"v",
    "ēi":"i","éi":"r","ěi":"j","èi":"f",
    "ēn":"e","én":"s","ěn":"o","èn":"o",
    "ēng":"c","éng":"f","ěng":"y","èng":"f",
    "ēr":"q","ér":"k","ěr":"u","èr":"h",
    "īn":"h","ín":"c","ǐn":"x","ìn":"v",
    "īng":"e","íng":"n","ǐng":"w","ìng":"w",
    "ōng":"k","óng":"j","ǒng":"n","òng":"y",
    "ōu":"x","óu":"a","ǒu":"z","òu":"r",
    "ūn":"g","ún":"f","ǔn":"o","ùn":"r",
    "iā":"d","iá":"c","iǎ":"n","ià":"x",
    "iān":"r","ián":"v","iǎn":"p","iàn":"a",
    "iāng":"y","iáng":"i","iǎng":"u","iàng":"e",
    "iāo":"m","iáo":"u","iǎo":"l","iào":"l",
    "iē":"k","ié":"s","iě":"c","iè":"q",
    "iōng":"p","ióng":"k","iǒng":"e",
    "iū":"z","iú":"m","iǔ":"z","iù":"o",
    "uā":"s","uá":"t","uǎ":"g","uà":"g",
    "uāi":"g","uái":"s","uǎi":"p","uài":"f",
    "uān":"d","uán":"o","uǎn":"s","uàn":"c",
    "uāng":"w","uáng":"b","uǎng":"u","uàng":"e",
    "uī":"t","uí":"w","uǐ":"v","uì":"f",
    "uō":"s","uó":"l","uǒ":"l","uò":"p",
    "üē":"u","üé":"i","üě":"o","üè":"d"
}

# 反向映射成 key->多个 yun 的格式
reverse_mapping = defaultdict(list)
for yun, alphabet in yun_data.items():
    reverse_mapping[alphabet.upper()].append(yun)

# 构造 rows（自然码布局）
# 按照键盘顺序
rows = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

# 组织 rows 数据
row_data = {}
for i, row in enumerate(rows, 1):
    row_data[f'row{i}'] = [
        {"alphabet": key, "yun1": values[0]} if len(values) == 1 else {"alphabet": key, "yun1": values[0], "yun2": values[1]}
        for key, values in reverse_mapping.items() if key in row
    ]

# 生成 table 数据
table_data = defaultdict(list)
for yun, alphabet in yun_data.items():
    first_letter = yun[0]  # 获取韵母的首字母
    table_data[first_letter].append({"yun": yun, "bianma": alphabet * 2})  # 假设编码为字母的两次重复

# 组织最终数据
ziranma = {
    "name": "ziranma",
    "name1": "自然码",
    "tableName": "零声母",
    **row_data,
    "table1": table_data.get('a', []),
    "table2": table_data.get('e', []),
    "table3": table_data.get('o', []),
    "const": {"name1StartX": 1622},
    "hant": {"name1": "自然碼", "tableName": "零聲母"}
}

# 转换为 JavaScript 格式
js_code = "module.exports = " + json.dumps(ziranma, ensure_ascii=False, indent=2)

# 输出 JavaScript 代码
print(js_code)
