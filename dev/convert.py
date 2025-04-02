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


yun = parse_mapping(yun)
yun = invert_mapping(yun)

print(yun)
