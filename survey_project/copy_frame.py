"""
Created on 2024/10/23

@author: ZHANG Jie

Description:

"""


import os
import json
import shutil
import re

# 输入的路径
source_dir = r'F:\CholecT50\videos'
# 目标路径
destination_dir = r'F:\CholecT50\videos_survey'
# 应该存在的 JSON 文件名列表
json_file_names = [79, 2, 51, 6, 25, 14, 66, 23, 50, 111]  # 示例文件名列表
# json_file_names = [80, 32, 5, 15, 40, 47, 26, 48, 70, 96]  # 示例文件名列表
# json_file_names = [31, 57, 36, 18, 52, 68, 10, 8, 73, 103]  # 示例文件名列表
# json_file_names = [42, 29, 60, 27, 65, 75, 22, 49, 12, 110]  # 示例文件名列表
# json_file_names = [78, 43, 62, 35, 74, 1, 56, 4, 13, 92]  # 示例文件名列表

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

# 从 txt 文件中读取并处理数据
def process_txt_file(txt_file_path):
    frame_data = {}
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
        frame_data[i] = frame_ids

    return frame_data

# 从 txt 文件中读取 frame_id
frame_data = process_txt_file('./val_set/cholec50_six1016_noSIL_cross1_val.txt')

# 处理文件库中所有的 JSON 文件
for idx, folder_id in enumerate(json_file_names):
    # 根据 folder_id 的长度确定 folder_name
    if folder_id < 100:
        folder_name = f'VID{folder_id:02d}'
    else:
        folder_name = f'VID{folder_id:03d}'

    # 获取当前文件对应的 frame_ids
    if idx not in frame_data:
        print(f"Warning: No frame data for JSON index {idx}.")
        continue

    frame_ids = frame_data[idx]

    for frame_id in frame_ids:
        if frame_id <= 0:
            continue

        # 处理当前帧和前一帧
        frames_to_copy = [frame_id, frame_id - 1]
        for frame in frames_to_copy:
            source_filename = f'{frame:06d}.png'
            source_path = os.path.join(source_dir, folder_name, source_filename)
            destination_folder = os.path.join(destination_dir, folder_name)
            destination_path = os.path.join(destination_folder, source_filename)

            # 如果源文件存在，则进行复制
            if os.path.exists(source_path):
                os.makedirs(destination_folder, exist_ok=True)
                shutil.copy2(source_path, destination_path)
                print(f"Copied {source_path} to {destination_path}")
            else:
                print(f"Warning: Source file {source_path} does not exist.")


