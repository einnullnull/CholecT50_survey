"""
Created on 2024/11/18

@author: ZHANG Jie

Description:

"""

from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__, static_folder='static')

# 项目所在的根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 视频所在的相对路径
VIDEO_FOLDER = os.path.join(PROJECT_ROOT, 'videos_survey')

@app.route('/')
def index():
    # 提供主页模板（index.html），用来渲染问卷页面
    return render_template('index.html')

# 从项目文件夹中加载视频
@app.route('/videos/<vid>/video.mp4')
def load_video(vid):
    vid_folder = os.path.join(VIDEO_FOLDER, vid)
    return send_from_directory(vid_folder, 'video.mp4')

# 从项目文件夹中加载图片
@app.route('/images/<vid>/<filename>')
def load_image(vid, filename):
    vid_folder = os.path.join(VIDEO_FOLDER, vid)
    if filename == '0000-1.png' or int(filename.split('.')[0]) == -1:
        return send_from_directory(PROJECT_ROOT, 'static/blank.png')
    try:
        return send_from_directory(vid_folder, filename)
    except FileNotFoundError:
        return send_from_directory(PROJECT_ROOT, 'static/blank.png')

# 提供 JSON 数据（选项）
@app.route('/options.json')
def options():
    return send_from_directory(PROJECT_ROOT, 'options.json')

# 提供 JSON 数据（开始的帧）
@app.route('/start_frame/<vid>.json')
def start_frame(vid):
    json_filename = f"{vid}.json"
    return send_from_directory(os.path.join(PROJECT_ROOT, 'start_frame'), json_filename)

# 静态资源，例如 JavaScript 和 CSS 文件
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'static'), filename)

if __name__ == '__main__':
    app.run(debug=True)

