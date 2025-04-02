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

def create_tables(grouped_dict):
    """Create tables similar to ziranma.js structure with tone marks preserved"""
    # Group yuns by first letter (considering tone marks)
    a_table = []
    e_table = []
    i_table = []
    o_table = []
    u_table = []
    v_table = []  # For 'ü'
    
    # Process each yun with tone marks
    for key, values in inverted_dict.items():
        for yun_str in values:
            # Create entry with the yun and bianma
            entry = {"yun": yun_str}
            
            # Generate bianma based on the key
            entry["bianma"] = key.lower()
            
            # Determine which table to add to based on first letter
            first_char = remove_tone_marks(yun_str[0])
            if first_char == 'a':
                a_table.append(entry)
            elif first_char == 'e':
                e_table.append(entry)
            elif first_char == 'i':
                i_table.append(entry)
            elif first_char == 'o':
                o_table.append(entry)
            elif first_char == 'u':
                u_table.append(entry)
            elif first_char == 'ü':
                v_table.append(entry)
    
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
tables = create_tables(inverted_dict)

# Generate the output in ziranma.js format
js_output = generate_js_output([row1, row2, row3], tables)

# Write to file
with open("zrlong.js", "w", encoding="utf-8") as f:
    f.write(js_output)

print("Conversion complete. Output written to zrlong.js")

