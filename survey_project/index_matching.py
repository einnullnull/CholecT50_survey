"""
Created on 2024/10/17

@author: ZHANG Jie

Description:

"""

import json
import re


def process_line(line):
    # 替换文件中的特殊字符，确保正确的【】符号
    line = line.replace('¡¾', '【').replace('¡¿', '】')

    # 使用正则表达式提取 description 和 frame_id，忽略开头的 "* " 和尾部的 "#"（如果有）
    pattern = r'(\S+?)【(\d+)】'
    # 去掉行首的 "* " 和行尾的 "#"，只处理中间的部分
    line = line.strip().lstrip('*').rstrip('#').strip()

    matches = re.findall(pattern, line)

    descriptions = [m[0] for m in matches]
    frame_ids = [int(m[1]) for m in matches]

    return descriptions, frame_ids


def generate_json(descriptions, frame_ids):
    json_list = []
    window_size = 6

    # 填充 frame_id 和 description 不足的部分
    padded_frame_ids = [-1] * (window_size - 1) + frame_ids
    padded_descriptions = ['None'] * (window_size - 1) + descriptions

    # 生成滑动窗口形式的 JSON 数据
    for i in range(len(frame_ids)):
        window_frame_ids = padded_frame_ids[i:i + window_size]
        window_descriptions = padded_descriptions[i:i + window_size - 1] + ['next action']

        json_list.append({
            "frame_id": window_frame_ids,
            "description": window_descriptions
        })

    return json_list


def process_txt_file(txt_file_path, json_file_names):
    # 使用合适的编码读取文件
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

        # 检查数据是否正确提取
        print(f"Processing line {i + 1}: descriptions={descriptions}, frame_ids={frame_ids}")

        # 保存为 JSON 文件
        json_filename = f"start_frame/{json_file_names[i]:03d}.json"
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)


# 示例用法
txt_file_path = './val_set/cholec50_six1016_noSIL_cross5_val.txt'  # 替换为你的 txt 文件路径
# json_file_names = [79, 2, 51, 6, 25, 14, 66, 23, 50, 111]  # 示例文件名列表
# json_file_names = [80, 32, 5, 15, 40, 47, 26, 48, 70, 96]  # 示例文件名列表
# json_file_names = [31, 57, 36, 18, 52, 68, 10, 8, 73, 103]  # 示例文件名列表
# json_file_names = [42, 29, 60, 27, 65, 75, 22, 49, 12, 110]  # 示例文件名列表
json_file_names = [78, 43, 62, 35, 74, 1, 56, 4, 13, 92]  # 示例文件名列表

# 调用函数处理 txt 文件
process_txt_file(txt_file_path, json_file_names)


