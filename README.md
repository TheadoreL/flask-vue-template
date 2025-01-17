# Flask-Vue Template

这是一个 Flask 与 Vue.js 的模板项目，旨在为你提供一个简单的开发环境，以便在后端使用 Flask 和前端使用 Vue.js 开发现代 Web 应用程序。此模板集成了常见的功能，如日志记录、配置管理和 uWSGI 服务配置，帮助你快速启动并构建你的应用程序。

## 特性

- Flask 后端，支持 RESTful API 和模板渲染。
- Vue.js 前端，支持动态页面渲染和单页应用（SPA）。
- 集成日志记录系统，支持控制台和文件日志输出。
- 自动化的配置文件生成，支持根据需要生成 `config.ini` 和 `uwsgi.ini` 配置。
- 支持 uWSGI 部署和系统服务设置。
- 基于 Python 3 和 Node.js，适用于开发和生产环境。

## 安装

### 前提条件

- **Python 3.x**：推荐版本 3.6 及以上。
- **Node.js 和 npm/yarn**：用于构建前端应用。
- **uWSGI**：用于在生产环境中部署 Flask 应用。

### 使用步骤

1. **安装Aloha Flask Creator**
   
   Aloha Flask Creator 是我创建的一个自动化工具，用于自动创建使用此模板的应用。

   ```bash
   pip install aloha-flask-creator
   aloha-flask-creator
   ```
   
   示例：

   ```
   $ aloha-flask-creator
   Please enter the name of the new project: my-flask-project
   New project created at: my-flask-project
   ```
   
   安装步骤在 [How to use](./docs/how_to_use.md)

## 使用

### 配置文件

项目使用 `config.ini` 作为主要的配置文件。你可以在此文件中设置应用的日志级别、日志文件路径等选项。如果没有找到该文件，脚本会自动从 `config.ini.example` 创建一个新的配置文件。

### 日志记录

该项目集成了一个自定义的日志记录系统，可以配置日志级别和日志输出。日志会同时输出到控制台和文件。你可以在 `config.ini` 文件中配置相关选项。

### 部署

你可以使用 `uwsgi` 将 Flask 应用部署到生产环境。在 `uwsgi.ini` 和 `your-app.uwsgi.service` 文件中配置正确的路径和应用名称后，执行以下命令启动服务：

```bash
sudo systemctl start your-app.uwsgi.service
```

## 如何使用登录

查看 [Add login](./docs/use_login.md) 如何添加登录功能。

## 项目结构

```
flask-vue-template/
│
├── app.py                                         # Flask 应用入口
├── config.ini.example                             # 配置模板文件
├── uwsgi.ini.example                              # uWSGI 配置模板
├── app.uwsgi.service.example                      # 系统服务文件模板
├── requirements.txt                               # Python 依赖
├── package.json                                   # Vue.js 项目配置文件
├── .venv/                                         # Python 虚拟环境
├── modules/                                       # 自定义模块目录
│   ├── __init__.py                                # init
│   ├── config/                                    # 配置模块
│   ├── controllers/                               # controllers模块
│   ├── logger/                                    # 自定义日志模块
│   └── models/                                    # models模块
├── front/                                         # Vue.js 前端项目文件夹
│   ├── app.ts                                     # 入口 ts 文件
│   ├── App.vue                                    # 入口vue文件，用于承载 vue-router 的 view
│   ├── app.css                                    # 自定义全局css
│   ├── shims-vue.ts                               # vue 配置
│   ├── components                                 # vue 配置
│   │   └── index.vue                              # 示例 vue 文件
│   ├── router                                     # vue 配置
│   │   └── index.tx                               # Vue router 配置文件
├── templates/                                     # Flask 模板文件夹
│   └── index.html                                 # Flask 模板
├── public/                                        # 公共目录，编译后的css和js文件会在这里
│   └── favicon.ico                                # favicon
├── statics/                                       # 静态资源目录
├── logs/                                          # 日志文件夹
├── instance/                                      # 数据库文件夹
│   └── mydb.db                                    # sqlite3 数据文件
└── docs/                                          # 文档文件夹
    ├── how_to_use.md                              # How to use doc
    └── use_login.md                               # Add login doc

```

