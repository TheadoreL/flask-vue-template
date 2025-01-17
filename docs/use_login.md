# 如何添加登录功能

介绍一个简单的方法创建一个登录，如果需要增加权限管理，请自行修改 model

## 数据表结构

| 列名          | 数据类型      | 约束条件                | 描述                     |
|---------------|---------------|-------------------------|--------------------------|
| id            | Integer       | 主键，自动递增          | 用户唯一标识符            |
| username      | String(150)   | 非空，唯一              | 用户名，最大长度 150 个字符 |
| password_hash | String(200)   | 非空                    | 存储用户密码的哈希值      |
| update_token  | String(200)   | 非空，唯一              | 用户的更新令牌，用于密码重置等操作 |


### 字段说明：

- **id**: 这是一个自动递增的主键，用于唯一标识每个用户。
- **username**: 用户的用户名，要求唯一且非空，最大长度为 150 个字符。用于登录时验证用户身份。
- **password_hash**: 存储加密后的用户密码，非空。密码不以明文形式存储，而是存储加密后的哈希值。
- **update_token**: 用户的更新令牌，通常用于密码重置等功能。该字段是唯一的，确保每个用户的令牌唯一。

## 创建 models

1. 新建 `modules/models/user.py` 如下：

    ```python
    from werkzeug.security import generate_password_hash, check_password_hash
    from . import db
    
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(150), nullable=False, unique=True)
        password_hash = db.Column(db.String(200), nullable=False)
        update_token = db.Column(db.String(200), nullable=False, unique=True)
    
        def set_password(self, password):
            # 使用 werkzeug.security 生成密码哈希
            self.password_hash = generate_password_hash(password)
    
        def check_password(self, password):
            # 检查密码是否匹配
            return check_password_hash(self.password_hash, password)
    
    ```
   
    ### 方法说明：
    
    - **set_password(password)**: 该方法接受一个明文密码，并使用 `werkzeug.security` 提供的 `generate_password_hash` 函数将其加密后保存到 `password_hash` 字段。
      - **check_password(password)**: 该方法用于检查给定的明文密码与存储的加密密码是否匹配，使用 `check_password_hash` 函数进行验证。
    
    此模型使用 SQLAlchemy ORM 进行数据库操作，确保了数据的安全性和易用性。

   修改 `modules/models/__init__.py` 新增：

   ```python
   # 导入模型
   from .user import User
   ```
   

2. 修改 `app.py` 添加登录路由：

    ```python
    from flask import Flask, render_template, url_for, send_from_directory, request, redirect, session
    from modules.models import db, User
    from functools import wraps
    
    # 登录页面路由
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # 获取表单提交的用户名和密码
            username = request.form.get('username')
            password = request.form.get('password')
    
            # 从数据库中查询用户
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                # 用户认证成功，保存会话
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))  # 重定向到首页
            else:
                # 用户认证失败
                return render_template('login.html', error='用户名或密码错误')
    
        return render_template('login.html')
    
    # 登录认证装饰器
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('login'))  # 未登录，重定向到登录页面
            return f(*args, **kwargs)
        return decorated_function
    
    # 保护的路由：需要登录认证
    @app.route('/')
    @login_required
    def index(filename):
        return render_template('index.html')
    
    ```
   
3. 如果不开放注册，可以添加一个如下的脚本 `manage_user.py` 来命令行添加用户：

    ```python
    import os
import random
import string
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from modules.config.config import Config

# 获取当前脚本文件所在的目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录
project_root = os.path.abspath(os.path.join(current_directory, '.'))

# 读取配置
config = Config(f"{project_root}/config.ini")

# 初始化 Flask 和 SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('db', 'uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.getboolean('db', 'track_modifications')
db = SQLAlchemy(app)

# 用户模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    update_token = db.Column(db.String(200), nullable=False, unique=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

# 启动 Flask 应用上下文
with app.app_context():
    db.create_all()  # 创建表结构（如果表不存在）

# 生成随机 token
def generate_token(length=50):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

# 添加新用户
def add_user():
    username = input("请输入用户名: ").strip()
    password = input("请输入密码: ").strip()

    # 检查用户名是否已存在
    with app.app_context():
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"用户名 '{username}' 已存在！")
            return

        # 创建新用户
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.update_token = generate_token()
        db.session.add(new_user)
        db.session.commit()

        print(f"用户 '{username}' 添加成功！")
        print(f"更新地址 Token: {new_user.update_token}")

# 显示所有用户
def list_users():
    with app.app_context():
        users = User.query.all()
        print(f"{'ID':<5} {'用户名':<20} {'Token':<50}")
        print("=" * 80)
        for user in users:
            print(f"{user.id:<5} {user.username:<20} {user.update_token:<50}")

# 主菜单
def main():
    while True:
        print("\n用户管理菜单:")
        print("1. 添加用户")
        print("2. 查看所有用户")
        print("3. 退出")

        choice = input("请选择操作: ").strip()
        if choice == "1":
            add_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            print("退出程序。")
            break
        else:
            print("无效选择，请重新输入！")

if __name__ == "__main__":
    main()



    ```

4. 新建登录页面模板 `templates/login.html`

    ```html
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>登录</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                background-color: #f6f9fc;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
    
            .login-container {
                background-color: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                width: 300px;
            }
    
            h2 {
                text-align: center;
                color: #2D7BF0; /* 蓝色 */
                margin-bottom: 30px;
            }
    
            .form-group {
                margin-bottom: 20px;
            }
    
            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
            }
    
            .form-group input {
                width: 100%;
                padding: 10px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                font-size: 16px;
            }
    
            .form-group input:focus {
                border-color: #2D7BF0;
                outline: none;
            }
    
            .btn {
                width: 100%;
                padding: 12px;
                background-color: #2D7BF0;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
    
            .btn:hover {
                background-color: #1c64d4;
            }
    
            .error {
                color: red;
                font-size: 14px;
                text-align: center;
            }
        </style>
    </head>
    <body>
    
    <div class="login-container">
        <h2>登录</h2>
        <form method="POST">
            <div class="form-group">
                <label for="username">用户名</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">密码</label>
                <input type="password" id="password" name="password" required>
            </div>
            {% if error %}
                <div class="error">{{ error }}</div>
            {% endif %}
            <button type="submit" class="btn">登录</button>
        </form>
    </div>
    
    </body>
    </html>
   
    ```
