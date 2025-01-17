# A fast flask app template with vue

## How to use:

1. Create venv：

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Unix/macOS
    .venv\Scripts\activate  # Windows
    ```

2. Install requirements：

    ```bash
    pip install -r requirements.txt
    ```

3. Set uwsgi.ini

   ```bash
   cp uwsgi.ini.example uwsgi.ini
   ```
   Then replace %PATH-TO-APP% to your app path
   
4. Set system service (if in Linux or macOS)

   ```bash
   cp app.uwsgi.service.example %APPNAME%.uwsgi.service
   ```
   **Remember to replace <u>%APPNAME%</u> to your app name**.

   Then replace %PATH-TO-APP% in the file to your app path, replace %APPNAME% in the file to your app name

5. Install npm packages
   
   ```bash
   npm i    # use npm
   yarn     # use yarn
   ```

6. Compile JS and CSS

   ```bash
   npm run dev      # build in development environment
   npm run build    # build production
   ```
   