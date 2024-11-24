"""
Created on 2024/10/29

@author: ZHANG Jie

Description:

"""

"""
Created on 2024/10/17

@author: ZHANG Jie

Description:

"""

import json
import re


def process_line(line):
    # Replace unusual characters to ensure correct symbols
    line = line.replace('¡¾', '【').replace('¡¿', '】')

    # Remove any leading '*' and trailing '#', as well as surrounding whitespace
    line = line.strip().lstrip('*').rstrip('#').strip()

    # Updated pattern to allow spaces around 【 and 】
    pattern = r'(\S+?)\s*【\s*(\d+)\s*】'

    # Find all matches of descriptions and frame IDs
    matches = re.findall(pattern, line)

    # Process matches if found, otherwise return empty lists
    descriptions = [adjust_description(m[0]) for m in matches]
    frame_ids = [int(m[1]) for m in matches]

    return descriptions, frame_ids

def adjust_description(description):
    # Replace "AND" with "_" and "_" with a space
    description = description.replace("_", " ")
    description = description.replace("AND", "_")
    return description

def generate_json(descriptions, frame_ids):
    json_list = []
    window_size = 6

    # 填充 frame_id 和 description 的不足部分
    padded_frame_ids = [-1] * (window_size - 1) + frame_ids
    padded_descriptions = ['None'] * (window_size - 1) + descriptions

    for i in range(len(frame_ids)):
        window_frame_ids = padded_frame_ids[i:i + window_size]
        window_descriptions = padded_descriptions[i:i + window_size - 1] + ['next action']

        json_list.append({
            "frame_id": window_frame_ids,
            "description": window_descriptions
        })

    return json_list


def process_txt_file(txt_file_path, json_file_names):
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(txt_file_path, 'r', encoding='ISO-8859-1') as file:
            lines = file.readlines()

    for i, line in enumerate(lines):
        # 跳过空行
        if line.strip() == "":
            continue

        descriptions, frame_ids = process_line(line)
        json_data = generate_json(descriptions, frame_ids)

        # 调试输出，检查提取的数据
        print(f"Processing line {i + 1}: descriptions={descriptions}, frame_ids={frame_ids}")

        # 保存为 JSON 文件
        json_filename = f"start_frame_meta/{json_file_names[i]:03d}.json"
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)


# Meta action
txt_file_path_meta = './val_set/cnhk_boss_all_1029_id.txt'  # 替换为你的 txt 文件路径
json_file_names_meta = [49, 74, 36, 57, 18, 79, 2, 68, 43, 50,
                        1, 52, 13, 103, 22, 6, 62, 48, 15, 111,
                        4, 75, 78, 31, 51, 110, 26, 56, 27, 92,
                        80, 65, 5, 96, 14, 47, 32, 8, 73,
                        70, 12, 60, 40, 42, 23, 66, 29, 35, 10, 25]  # 示例文件名列表

# 调用函数处理 txt 文件
process_txt_file(txt_file_path_meta, json_file_names_meta)
