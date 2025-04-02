#!/usr/bin/env python3

import json
from collections import defaultdict

yun = """
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
"""

def parse_mapping(mapping_str):
    mapping_str = mapping_str.replace("\n", "").replace(" ", "")
    pairs = mapping_str.split(",")

    mapping_dict={}
    for pair in pairs:
        key, value = pair.replace('"','').split(":")
        mapping_dict[key] = value

    return mapping_dict

def invert_mapping(mapping_dict):
    inverted_dict={}
    for key, value in mapping_dict.items():
        value = value.upper()
        if value not in inverted_dict:
            inverted_dict[value] = []
        inverted_dict[value].append(key)
    return inverted_dict

def remove_tone_marks(yun_str):
    tone_map = {
        'ā': 'a', 'á': 'a', 'ǎ': 'a', 'à': 'a',
        'ē': 'e', 'é': 'e', 'ě': 'e', 'è': 'e',
        'ī': 'i', 'í': 'i', 'ǐ': 'i', 'ì': 'i',
        'ō': 'o', 'ó': 'o', 'ǒ': 'o', 'ò': 'o',
        'ū': 'u', 'ú': 'u', 'ǔ': 'u', 'ù': 'u',
        'ǖ': 'ü', 'ǘ': 'ü', 'ǚ': 'ü', 'ǜ': 'ü',
    }
    result = ''
    for char in yun_str:
        result += tone_map.get(char, char)
    return result

def create_rows(inverted_dict):
    """Create rows similar to ziranma.js structure"""
    row1 = []
    row2 = []
    row3 = []
    
    # Map keys to vowels they can represent
    for key, yuns in inverted_dict.items():
        # Create entry object with all yuns
        entry = {"alphabet": key}
        
        # Add all yun information with tone marks preserved
        for i, yun in enumerate(yuns):
            entry[f"yun{i+1}"] = yun
        
        # Assign to appropriate row based on the key
        if key in "QWERTYUIOP":
            row1.append(entry)
        elif key in "ASDFGHJKL;":
            row2.append(entry)
        elif key in "ZXCVBNM":
            row3.append(entry)
    
    return row1, row2, row3

def get_tone_index(yun_str):
    """获取声调的索引，用于排序
    1: 阴平(ā), 2: 阳平(á), 3: 上声(ǎ), 4: 去声(à)
    """
    for char in yun_str:
        if char in 'āēīōūǖ':
            return 1
        elif char in 'áéíóúǘ':
            return 2
        elif char in 'ǎěǐǒǔǚ':
            return 3
        elif char in 'àèìòùǜ':
            return 4
    return 0  # 无声调

def create_tables(inverted_dict, original_mapping):
    """Create tables similar to ziranma.js structure with tone marks preserved"""
    # 首先按基本韵母和声调整理数据
    yun_groups = defaultdict(list)
    
    # 收集所有韵母并按基本韵母分组
    for key, values in inverted_dict.items():
        for yun_str in values:
            base_yun = remove_tone_marks(yun_str)
            tone_index = get_tone_index(yun_str)
            
            # 获取键盘位置（即原始映射中的值）
            keyboard_key = original_mapping.get(yun_str).lower()
            
            # 生成bianma: 第一个字母 + 键盘位置
            first_char = remove_tone_marks(yun_str[0])
            bianma = first_char + keyboard_key
            
            # 对于ü，使用v作为输入键
            if 'ü' in base_yun:
                bianma = 'v' + keyboard_key
                
            yun_groups[base_yun].append({
                "yun": yun_str,
                "bianma": bianma,
                "tone_index": tone_index
            })
    
    # 对每个组内的韵母按声调排序
    for base_yun, items in yun_groups.items():
        items.sort(key=lambda x: x["tone_index"])
    
    # 按首字母分组到各个表
    a_table = []
    e_table = []
    i_table = []
    o_table = []
    u_table = []
    v_table = []  # For 'ü'
    
    # 按照基本韵母的首字母分组
    for base_yun, items in yun_groups.items():
        first_char = base_yun[0]
        
        # 移除不需要的tone_index字段
        clean_items = []
        for item in items:
            clean_items.append({
                "yun": item["yun"],
                "bianma": item["bianma"]
            })
            
        if first_char == 'a':
            a_table.extend(clean_items)
        elif first_char == 'e':
            e_table.extend(clean_items)
        elif first_char == 'i':
            i_table.extend(clean_items)
        elif first_char == 'o':
            o_table.extend(clean_items)
        elif first_char == 'u':
            u_table.extend(clean_items)
        elif first_char == 'ü':
            v_table.extend(clean_items)
    
    return {
        "table1": a_table,
        "table2": e_table,
        "table3": o_table,
        "table4": i_table,
        "table5": u_table,
        "table6": v_table
    }

def generate_js_output(rows, tables):
    """Generate JavaScript output similar to ziranma.js"""
    output = "module.exports = {\n"
    output += "  name: 'zrlong',\n"
    output += "  name1: '自然长码',\n"
    output += "  tableName: '零声母',\n"
    
    # Add rows
    for i, row in enumerate([rows[0], rows[1], rows[2]]):
        output += f"  row{i+1}: [\n"
        for item in row:
            output += "    { "
            output += f"alphabet: '{item['alphabet']}'"
            
            # Add all yun entries dynamically
            yun_keys = [k for k in item.keys() if k.startswith('yun')]
            for yun_key in sorted(yun_keys):
                output += f", {yun_key}: '{item[yun_key]}'"
                
            output += " },\n"
        output += "  ],\n"
    
    # Add tables
    for i, table_name in enumerate(["table1", "table2", "table3", "table4", "table5", "table6"]):
        if table_name in tables and tables[table_name]:
            output += f"  {table_name}: [\n"
            for item in tables[table_name]:
                output += f"    {{ yun: '{item['yun']}', bianma: '{item['bianma']}' }},\n"
            output += "  ],\n"
    
    # Add constants and traditional Chinese support
    output += "  const: {\n    name1StartX: 1622,\n  },\n"
    output += "  hant: {\n    name1: '自然長碼',\n    tableName: '零聲母',\n  }\n"
    output += "}\n"
    
    return output

# Main execution
yun_dict = parse_mapping(yun)
inverted_dict = invert_mapping(yun_dict)
row1, row2, row3 = create_rows(inverted_dict)
tables = create_tables(inverted_dict, yun_dict)

# Generate the output in ziranma.js format
js_output = generate_js_output([row1, row2, row3], tables)

# Write to file
with open("zrlong.js", "w", encoding="utf-8") as f:
    f.write(js_output)

print("Conversion complete. Output written to zrlong.js")

