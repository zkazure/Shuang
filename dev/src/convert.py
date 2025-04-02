#!/usr/bin/env python3

import json
from collections import defaultdict
from datetime import datetime

# 需要从zrlong.js中读取数据
import sys
import os

# 获取当前目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
zrlong_path = os.path.join(current_dir, 'zrlong.js')

def read_zrlong_file():
    """读取zrlong.js文件并解析其内容"""
    try:
        with open(zrlong_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 由于zrlong.js是一个JavaScript模块，我们需要手动解析它
        rows = []
        tables = {}
        
        # 解析行数据
        for i in range(1, 4):
            row_pattern = f"row{i}: ["
            row_start = content.find(row_pattern)
            if row_start != -1:
                row_end = content.find("],", row_start)
                row_data = content[row_start + len(row_pattern):row_end]
                rows.append(parse_row_data(row_data))
        
        # 解析表格数据
        for i in range(1, 7):
            table_pattern = f"table{i}: ["
            table_start = content.find(table_pattern)
            if table_start != -1:
                table_end = content.find("],", table_start)
                table_data = content[table_start + len(table_pattern):table_end]
                tables[f"table{i}"] = parse_table_data(table_data)
        
        return rows, tables
    except Exception as e:
        print(f"读取zrlong.js文件时出错: {e}")
        return None, None

def parse_row_data(row_text):
    """解析行数据"""
    items = []
    item_blocks = row_text.split("},")
    
    for block in item_blocks:
        if not block.strip():
            continue
            
        item = {}
        # 处理对象中的每个属性
        # 首先去掉开头的 {
        clean_block = block.strip().lstrip('{').strip()
        
        # 按逗号分割各个属性
        properties = []
        in_quote = False
        current_property = ""
        
        # 手动解析以处理引号内的逗号
        for char in clean_block:
            if char == '"' or char == "'":
                in_quote = not in_quote
            
            if char == ',' and not in_quote:
                properties.append(current_property.strip())
                current_property = ""
            else:
                current_property += char
        
        if current_property:
            properties.append(current_property.strip())
        
        # 处理每个属性
        for prop in properties:
            if ":" in prop:
                # 分割键值对
                key_part, value_part = prop.split(":", 1)
                
                # 清理键名（去除空格和引号）
                key = key_part.strip()
                if key.startswith('"') or key.startswith("'"):
                    key = key[1:]
                if key.endswith('"') or key.endswith("'"):
                    key = key[:-1]
                
                # 清理值（去除空格和引号）
                value = value_part.strip()
                if value.startswith('"') or value.startswith("'"):
                    value = value[1:]
                if value.endswith('"') or value.endswith("'"):
                    value = value[:-1]
                
                item[key] = value
        
        if item:
            items.append(item)
    
    return items

def parse_table_data(table_text):
    """解析表格数据"""
    items = []
    item_blocks = table_text.split("},")
    
    for block in item_blocks:
        if not block.strip():
            continue
            
        item = {}
        # 处理对象中的每个属性
        # 首先去掉开头的 {
        clean_block = block.strip().lstrip('{').strip()
        
        # 按逗号分割各个属性
        properties = []
        in_quote = False
        current_property = ""
        
        # 手动解析以处理引号内的逗号
        for char in clean_block:
            if char == '"' or char == "'":
                in_quote = not in_quote
            
            if char == ',' and not in_quote:
                properties.append(current_property.strip())
                current_property = ""
            else:
                current_property += char
        
        if current_property:
            properties.append(current_property.strip())
        
        # 处理每个属性
        for prop in properties:
            if ":" in prop:
                # 分割键值对
                key_part, value_part = prop.split(":", 1)
                
                # 清理键名（去除空格和引号）
                key = key_part.strip()
                if key.startswith('"') or key.startswith("'"):
                    key = key[1:]
                if key.endswith('"') or key.endswith("'"):
                    key = key[:-1]
                
                # 清理值（去除空格和引号）
                value = value_part.strip()
                if value.startswith('"') or value.startswith("'"):
                    value = value[1:]
                if value.endswith('"') or value.endswith("'"):
                    value = value[:-1]
                
                item[key] = value
        
        if item:
            items.append(item)
    
    return items

def remove_tone_marks(yun_str):
    """移除拼音中的声调"""
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

def generate_ziranma_format(rows, tables):
    """
    将zrlong.js格式的数据转换为ziranma.js格式，保留声调信息
    
    rows: 包含键盘映射的行数据
    tables: 包含可独立输入的韵母数据
    """
    # 初始化结果结构
    result = {
        "id": "zrlong",
        "name": "自然龙",
        "tips": ["自然码的升级版，支持带声调输入"],
        "detail": {
            "sheng": {
                "b": "b", "c": "c", "d": "d", "f": "f", "g": "g", 
                "h": "h", "j": "j", "k": "k", "l": "l", "m": "m", 
                "n": "n", "p": "p", "q": "q", "r": "r", "s": "s", 
                "t": "t", "w": "w", "x": "x", "y": "y", "z": "z"
            },
            "yun": {},
            "other": {}
        }
    }
    
    # 处理键盘映射的行数据，提取声母和韵母映射关系
    # 直接使用带声调的韵母作为键
    yun_mapping = {}  # 存储带声调韵母到按键的映射
    
    # 处理所有行
    all_rows = rows[0] + rows[1] + rows[2]
    for item in all_rows:
        alphabet = item["alphabet"].lower()  # 转为小写
        
        # 检查是否有声母映射
        if alphabet in ["i", "u", "v"]:
            # 特殊处理 i->ch, u->sh, v->zh 的声母映射
            if alphabet == "i" and "ch" not in result["detail"]["sheng"]:
                result["detail"]["sheng"]["ch"] = alphabet
            elif alphabet == "u" and "sh" not in result["detail"]["sheng"]:
                result["detail"]["sheng"]["sh"] = alphabet
            elif alphabet == "v" and "zh" not in result["detail"]["sheng"]:
                result["detail"]["sheng"]["zh"] = alphabet
        
        # 处理所有韵母（保留声调）
        for key in item.keys():
            if key.startswith("yun"):
                yun_with_tone = item[key]
                
                # 直接添加带声调的韵母映射
                if yun_with_tone not in yun_mapping:
                    yun_mapping[yun_with_tone] = alphabet
    
    # 将带声调的韵母映射添加到结果中
    result["detail"]["yun"] = yun_mapping
    
    # 处理表中的单独韵母(other)映射，同样保留声调
    other_mapping = {}
    
    # 合并所有表
    all_tables = []
    for table_name in ["table1", "table2", "table3", "table4", "table5", "table6"]:
        if table_name in tables:
            all_tables.extend(tables[table_name])
    
    # 使用带声调的韵母作为键
    for item in all_tables:
        yun_with_tone = item["yun"]
        other_mapping[yun_with_tone] = item["bianma"]
    
    # 将单独韵母映射添加到结果中
    result["detail"]["other"] = other_mapping
    
    return result

def export_ziranma_format(ziranma_data):
    """将转换后的数据导出为ziranma.js格式的字符串"""
    output = "/** last changed: " + datetime.now().strftime("%Y.%m.%d") + " */\n\n"
    output += "Shuang.resource.scheme.zrlong = {\n"
    output += f"  id: '{ziranma_data['id']}',\n"
    output += f"  name: '{ziranma_data['name']}',\n"
    
    # 添加提示
    output += "  tips: [\n"
    for tip in ziranma_data["tips"]:
        output += f"    '{tip}'\n"
    output += "  ],\n"
    
    # 添加详细映射
    output += "  detail: {\n"
    
    # 添加声母映射
    output += "    sheng: {\n"
    for sheng, key in ziranma_data["detail"]["sheng"].items():
        output += f"      {sheng}: '{key}',\n"
    output += "    },\n"
    
    # 添加韵母映射
    output += "    yun: {\n"
    for yun, key in ziranma_data["detail"]["yun"].items():
        output += f"      '{yun}': '{key}',\n"
    output += "    },\n"
    
    # 添加单独韵母映射
    output += "    other: {\n"
    for yun, bianma in ziranma_data["detail"]["other"].items():
        output += f"      '{yun}': '{bianma}',\n"
    output += "    }\n"
    
    output += "  }\n"
    output += "}\n"
    
    return output

if __name__ == "__main__":
    # 读取zrlong.js文件
    rows, tables = read_zrlong_file()
    
    if rows and tables:
        # 生成ziranma.js格式的数据
        ziranma_data = generate_ziranma_format(rows, tables)
        ziranma_js_content = export_ziranma_format(ziranma_data)
        
        # 写入文件
        output_path = os.path.join(current_dir, 'zrlong_ziranma_format.js')
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ziranma_js_content)
        
        print(f"转换完成！输出文件位置: {output_path}")
    else:
        print("无法读取zrlong.js文件，请确保文件存在并格式正确。") 