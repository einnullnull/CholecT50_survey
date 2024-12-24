from flask import Flask, send_from_directory, render_template, jsonify, request
import os
import json

app = Flask(__name__, static_folder='static')

# 项目所在的根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# 图片所在的绝对路径
VIDEO_FOLDER = os.path.join('F:', os.sep, 'CholecT50', 'videos')

# 有效的 VID 和对应数字映射
VALID_VIDEOS = {
    'VID01': '001', 'VID02': '002', 'VID04': '004',
    'VID05': '005', 'VID06': '006', 'VID08': '008',
    'VID10': '010', 'VID12': '012', 'VID13': '013',
    'VID14': '014', 'VID15': '015', 'VID18': '018',
    'VID22': '022', 'VID23': '023', 'VID25': '025',
    'VID26': '026', 'VID27': '027', 'VID29': '029',
    'VID31': '031', 'VID32': '032', 'VID35': '035',
    'VID36': '036', 'VID40': '040', 'VID42': '042',
    'VID43': '043', 'VID47': '047', 'VID48': '048',
    'VID49': '049', 'VID50': '050', 'VID51': '051',
    'VID52': '052', 'VID56': '056', 'VID57': '057',
    'VID60': '060', 'VID62': '062', 'VID65': '065',
    'VID66': '066', 'VID68': '068', 'VID70': '070',
    'VID73': '073', 'VID74': '074', 'VID75': '075',
    'VID78': '078', 'VID79': '079', 'VID80': '080',
    'VID92': '092', 'VID96': '096', 'VID103': '103',
    'VID110': '110', 'VID111': '111'
}

# 创建一个反向映射，从数字到 VID
NUMBER_TO_VID = {value: key for key, value in VALID_VIDEOS.items()}

# 添加在 VALID_VIDEOS 映射后面
VIDEO_GROUPS = {
    1: [79, 2, 51, 6, 25, 14, 66, 23, 50, 111],
    2: [80, 32, 5, 15, 40, 47, 26, 48, 70, 96],
    3: [31, 57, 36, 18, 52, 68, 10, 8, 73, 103],
    4: [42, 29, 60, 27, 65, 75, 22, 49, 12, 110],
    5: [78, 43, 62, 35, 74, 1, 56, 4, 13, 92]
}

RESPONSES_DIR = os.path.join(PROJECT_ROOT, 'responses')
os.makedirs(RESPONSES_DIR, exist_ok=True)

# 维护当前组号和访问者计数
current_group_id = 1
visitor_count = 0  # 新增变量来跟踪访问者数量

def normalize_vid(vid):
    """
    标准化VID格式：
    - 如果是 'VID001' 格式，转换为 'VID01'
    - 如果是 'VID111' 这样的三位数，保持不变
    """
    if vid.startswith('VID'):
        number_part = vid[3:]  # 获取数字部分
        if number_part.isdigit():
            num = int(number_part)
            if num < 100:  # 两位数
                return f'VID{num:02d}'
            else:  # 三位数
                return f'VID{num}'
    return vid


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/images/<vid>/<filename>')
def load_image(vid, filename):
    # 标准化VID格式
    normalized_vid = normalize_vid(vid)

    # 检查标准化后的 VID 是否有效
    if normalized_vid not in VALID_VIDEOS:
        print(f"无效的 VID: {vid} (标准化后: {normalized_vid})")
        return send_from_directory(PROJECT_ROOT, 'static/blank.png')

    vid_folder = os.path.join(VIDEO_FOLDER, normalized_vid)
    print(f"访问文件夹: {vid_folder}")
    print(f"请求文件: {filename}")

    if filename == '0000-1.png' or int(filename.split('.')[0]) == -1:
        return send_from_directory(PROJECT_ROOT, 'static/blank.png')

    try:
        return send_from_directory(vid_folder, filename)
    except FileNotFoundError:
        print(f"文件未找到: {os.path.join(vid_folder, filename)}")
        return send_from_directory(PROJECT_ROOT, 'static/blank.png')


@app.route('/options.json')
def options():
    return send_from_directory(PROJECT_ROOT, 'options.json')


@app.route('/start_frame/<vid>.json')
def start_frame(vid):
    try:
        # 如果直接使用数字（如 "001"）
        if vid.isdigit() or (len(vid) == 3 and vid.isdigit()):
            num = vid.zfill(3)
            if num not in NUMBER_TO_VID:
                print(f"请求的数字不在有效列表中: {num}")
                return {'error': 'Invalid number'}, 404
            json_filename = f"{num}.json"

        # 如果使用 VID 格式
        elif vid.startswith('VID'):
            normalized_vid = normalize_vid(vid)
            if normalized_vid not in VALID_VIDEOS:
                print(f"请求的 VID 不在有效列表中: {vid} (标准化后: {normalized_vid})")
                return {'error': 'Invalid VID'}, 404
            json_filename = f"{VALID_VIDEOS[normalized_vid]}.json"

        # 其他无效格式
        else:
            print(f"无效的请求格式: {vid}")
            return {'error': 'Invalid format'}, 404

        json_path = os.path.join(PROJECT_ROOT, 'start_frame', json_filename)
        if not os.path.exists(json_path):
            print(f"文件不存在: {json_filename}")
            return {'error': 'File not found'}, 404

        return send_from_directory(os.path.join(PROJECT_ROOT, 'start_frame'), json_filename)

    except Exception as e:
        print(f"处理 {vid} 时发生错误: {str(e)}")
        return {'error': 'Internal server error'}, 500


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, 'static'), filename)


@app.route('/valid-vids')
def get_valid_vids():
    return jsonify({
        'vids': list(VALID_VIDEOS.keys()),
        'numbers': list(VALID_VIDEOS.values())
    })


@app.route('/group_videos')
def get_group_videos():
    group_id = request.args.get('groupId', type=int)
    if group_id and group_id in VIDEO_GROUPS:
        return jsonify(VIDEO_GROUPS[group_id])
    return jsonify({'error': 'Invalid group ID'}), 404


@app.route('/save_responses', methods=['POST'])
def save_responses():
    try:
        data = request.json
        user_info = data['userInfo']
        
        # 获取所有已有用户的信息
        existing_users = []
        for file in os.listdir(RESPONSES_DIR):
            with open(os.path.join(RESPONSES_DIR, file), 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                existing_users.append(existing_data['userInfo'])
        
        # 检查是否为新用户
        is_new_user = True
        for existing_user in existing_users:
            if (user_info['name'] == existing_user['name'] and 
                user_info['age'] == existing_user['age'] and 
                user_info['gender'] == existing_user['gender']):
                is_new_user = False
                group_id = existing_user['groupId']
                break
                
        if is_new_user:
            # 新用户: 计算实际访问者数量并分配组
            visitor_count = len(existing_users) + 1
            group_id = ((visitor_count - 1) % 5) + 1
            data['userInfo']['groupId'] = group_id
        else:
            # 老用户: 使用已有的组号
            data['userInfo']['groupId'] = group_id
            
        # 保存响应
        filename = os.path.join(RESPONSES_DIR, f"{user_info['name']}_{data['userInfo']['groupId']}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        return jsonify({'status': 'success', 'groupId': data['userInfo']['groupId']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/load_responses/<name>/<group_id>')
def load_responses(name, group_id):
    try:
        filename = os.path.join(RESPONSES_DIR, f"{name}_{group_id}.json")
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        return jsonify({'status': 'not_found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)