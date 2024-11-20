from flask import Flask, render_template, jsonify, request
import os
import json
from datetime import datetime

app = Flask(__name__)

def find_all_package_jsons():
    username = os.getenv('USERNAME')
    base_path = f"C:/Users/{username}/AppData/Local/ShadowBot/users"
    results = []
    
    if os.path.exists(base_path):
        for user_dir in os.listdir(base_path):
            user_path = os.path.join(base_path, user_dir)
            apps_path = os.path.join(user_path, "apps")
            
            if os.path.exists(apps_path):
                for app_dir in os.listdir(apps_path):
                    app_path = os.path.join(apps_path, app_dir)
                    xbot_robot_path = os.path.join(app_path, "xbot_robot")
                    
                    if os.path.exists(xbot_robot_path):
                        package_json = os.path.join(xbot_robot_path, "package.json")
                        if os.path.exists(package_json):
                            try:
                                with open(package_json, 'r', encoding='utf-8') as f:
                                    package_data = json.load(f)
                                    project_name = package_data.get('name', '')
                                mod_time = os.path.getmtime(package_json)
                                # 使用父目录名（项目编码）作为项目标识
                                project_id = os.path.basename(app_path)
                                results.append({
                                    'path': xbot_robot_path,
                                    'name': project_name,
                                    'mod_time': mod_time,
                                    'project_id': project_id
                                })
                            except:
                                continue
    
    return sorted(results, key=lambda x: x['mod_time'], reverse=True)

def get_py_files(path):
    if not os.path.exists(path):
        return []
    
    files = []
    for file in os.listdir(path):
        if file.endswith('.py'):
            name = os.path.splitext(file)[0]
            if name not in ['__init__', 'main', 'package'] and 'process' not in name:
                files.append(name)
    return files

def load_remarks(path):
    # 获取项目编码
    project_id = os.path.basename(os.path.dirname(path))
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.txt')
    remarks = {}
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if '|' in line:
                        project, content = line.strip().split('|', 1)
                        if project == project_id and '=' in content:
                            module, remark = content.split('=', 1)
                            remarks[module] = remark
        except:
            pass
    return remarks

def save_remarks(path, remarks):
    # 获取项目编码
    project_id = os.path.basename(os.path.dirname(path))
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.txt')
    
    # 读取现有配置
    existing_lines = []
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                existing_lines = [line.strip() for line in f if line.strip()]
        except:
            pass
    
    # 移除当前项目的旧配置
    existing_lines = [line for line in existing_lines if not line.startswith(f"{project_id}|")]
    
    # 添加新的配置
    for module, remark in remarks.items():
        if remark:  # 只保存非空的备注
            existing_lines.append(f"{project_id}|{module}={remark}")
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            for line in existing_lines:
                f.write(line + '\n')
        return True
    except:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/projects')
def get_projects():
    projects = find_all_package_jsons()
    if projects:
        return jsonify({
            'success': True,
            'project': projects[0]
        })
    return jsonify({
        'success': False,
        'message': '未找到项目文件'
    })

@app.route('/api/modules')
def get_modules():
    path = request.args.get('path')
    if not path:
        return jsonify({
            'success': False,
            'message': '路径不能为空'
        })
    
    files = get_py_files(path)
    remarks = load_remarks(path)
    
    modules = [{
        'name': file,
        'remark': remarks.get(file, '')
    } for file in files]
    
    return jsonify({
        'success': True,
        'modules': modules
    })

@app.route('/api/save', methods=['POST'])
def save():
    data = request.json
    path = data.get('path')
    remarks = data.get('remarks')
    
    if not path or not remarks:
        return jsonify({
            'success': False,
            'message': '参数错误'
        })
    
    if save_remarks(path, remarks):
        return jsonify({
            'success': True
        })
    return jsonify({
        'success': False,
        'message': '保存失败'
    })

if __name__ == '__main__':
    app.run(debug=False)
