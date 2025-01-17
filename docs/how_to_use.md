# How to use:

## 本项目提供了自动化脚本

```bash
chmod a+x setup.sh
./setup.sh
```

### 编译 JS and CSS

   ```bash
   npm run dev      # build in development environment
   npm run build    # build production
   ```

## 手动创建

1. Create venv：

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Unix/macOS
    .venv\Scripts\activate  # Windows
    ```

2. 安装 requirements：

    ```bash
    pip install -r requirements.txt
    ```

3. 设置 uwsgi.ini

   ```bash
   cp uwsgi.ini.example uwsgi.ini
   ```
   Then replace %PATH-TO-APP% to your app path
   
4. 设置 system service (if in Linux or macOS)

   ```bash
   cp app.uwsgi.service.example %APPNAME%.uwsgi.service
   ```
   **记得替换 <u>%APPNAME%</u> 为你的 app name**.

   然后替换文件中的 <u>%PATH-TO-APP%</u> 为你的 app path, 替换 <u>%APPNAME%</u> 为你的 app name

5. 安装 npm packages
   
   ```bash
   npm i    # use npm
   yarn     # use yarn
   ```

6. 编译 JS and CSS

   ```bash
   npm run dev      # build in development environment
   npm run build    # build production
   ```