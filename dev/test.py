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
# 反向转换后的数据储存在哪里

# 构造 rows（自然码布局）
# 按照键盘顺序
rows = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

# 组织 rows 数据
row_data = {}
for i, row in enumerate(rows, 1): # 这里看不懂
    row_data[f'row{i}'] = [
        {"alphabet": key, "yun1": values[0]} if len(values) == 1 else {"alphabet": key, "yun1": values[0], "yun2": values[1]}
        # 这一行的代码运行顺序
        for key, values in reverse_mapping.items() if key in row
    ]

table_data = defaultdict(list)
# 遍历 yun 数据并填充 table_data
for yun, alphabet in yun_data.items():
    first_letter = yun[0]  # 取韵母首字母（如 "an" -> 'a'）
    bianma = first_letter + alphabet.lower()  # 组合编码（如 "an" -> "aj"）

    # 确保首字母分组存在
    if first_letter not in table_data:
        table_data[first_letter] = []

    table_data[first_letter].append({"yun": yun, "bianma": bianma})

# 组织最终数据
zrlong = {
    "name": "zrlong",
    "name1": "自然龙",
    "tableName": "零声母",
    **row_data,
    "table1": table_data.get('a', []),
    "table2": table_data.get('e', []),
    "table3": table_data.get('o', []),
    "const": {"name1StartX": 1622},
    "hant": {"name1": "自然龍", "tableName": "零聲母"}
}

# 转换为 JavaScript 格式
js_code = "module.exports = " + json.dumps(zrlong, ensure_ascii=False, indent=2)

# 输出 JavaScript 代码
with open("zrlong.js", "w", encoding="utf-8") as file:
    file.write(js_code)

print("Export Success")
