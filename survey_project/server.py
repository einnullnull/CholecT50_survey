from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__, static_folder='static')

# 项目所在的根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 图片所在的绝对路径
VIDEO_FOLDER = os.path.join('F:', os.sep, 'CholecT50', 'videos')


@app.route('/')
def index():
    # 提供主页模板（index.html），用来渲染问卷页面
    return render_template('index.html')


# 从外部文件夹中加载图片
@app.route('/images/<vid>/<filename>')
def load_image(vid, filename):
    # 转换 VID 格式
    if vid.startswith('VID'):
        vid_num = vid[3:]  # 提取数字部分
        # 如果是两位数，不需要补零
        if len(vid_num) == 3 and vid_num.startswith('0'):
            vid_num = vid_num[1:]  # 去掉前导零
        vid = f"VID{vid_num}"  # 重新组合 VID

    # 根据处理后的 VID 构建文件夹路径
    vid_folder = os.path.join(VIDEO_FOLDER, vid)
    print(vid_folder)
    print(filename)

    if filename == '0000-1.png' or int(filename.split('.')[0]) == -1:
        return send_from_directory(PROJECT_ROOT, 'static/blank.png')
    try:
        return send_from_directory(vid_folder, filename)
    except FileNotFoundError:
        return send_from_directory(PROJECT_ROOT, 'static/blank.png')


# 提供 JSON 数据（选项）
@app.route('/options.json')
def options():
    # 提供选项数据的 JSON 文件
    return send_from_directory(PROJECT_ROOT, 'options.json')


# 提供 JSON 数据（开始的帧）
@app.route('/start_frame/<vid>.json')
def start_frame(vid):
    # 对于 VID 格式的处理
    if vid.startswith('VID'):
        vid_num = vid[3:]  # 提取数字部分
        # 补齐为三位数，用于 json 文件名
        vid_num = vid_num.zfill(3)
        json_filename = f"json{vid_num}.json"
    else:
        json_filename = f"{vid}.json"
    return send_from_directory(os.path.join(PROJECT_ROOT, 'start_frame'), json_filename)


# 静态资源，例如 JavaScript 和 CSS 文件
@app.route('/static/<path:filename>')
def static_files(filename):
    # 确保 Flask 可以正确提供静态文件
    return send_from_directory(os.path.join(PROJECT_ROOT, 'static'), filename)


if __name__ == '__main__':
    app.run(debug=True)