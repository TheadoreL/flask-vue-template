import os
import secrets
from modules.config.config import Config
from modules.logger.logger import Logger
from flask import Flask, render_template, url_for, send_from_directory
from modules.models import db
import json

# 获取当前脚本文件所在的目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录
project_root = os.path.abspath(os.path.join(current_directory, '.'))

# 读取配置
config = Config(f"{project_root}/config.ini")

# 配置日志
logger = Logger(config, project_root).get_logger()

# 创建 Flask 应用
app = Flask(__name__, static_folder='public')

# 配置数据库
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('db', 'uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.getboolean('db', 'track_modifications')

# 初始化 SQLAlchemy
db.init_app(app)


# 读取 webpack 生成的 manifest.json 文件
def get_manifest():
    manifest_path = os.path.join(os.path.dirname(__file__), 'public', 'manifest.json')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            return json.load(f)
    return {}

# favicon.ico 路由
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Assets 路由
@app.route('/assets/<path:filename>')
def protected_static(filename):
    return send_from_directory('static', filename)

# 首页路由，展示表格
@app.route('/', methods=['GET'])
def index(page=1):
    # 获取静态文件的真实路径
    manifest = get_manifest()
    # 自动获取所有 JS 文件路径
    js_files = [
        url_for('protected_static', filename=manifest[key])
        for key in manifest if key.endswith('.js')
    ]
    # 自动获取所有 CSS 文件路径
    css_files = [
        url_for('protected_static', filename=manifest[key])
        for key in manifest if key.endswith('.css')
    ]
    return render_template('index.html', js_files=js_files, css_files=css_files)


# 启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
