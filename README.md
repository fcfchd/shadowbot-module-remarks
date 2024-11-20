# 影刀Python模块备注工具 Web版

这是影刀Python模块备注工具的Web版本，提供了与桌面版相同的功能，但使用更现代的Web界面。

## 功能特点

- 自动检测并显示最新的影刀项目
- 列出所有Python模块
- 支持为每个模块添加中文备注
- 自动保存备注到config.txt文件
- 现代化的Web界面

## 安装要求

- Python 3.7+
- Flask
- python-dotenv

## 安装步骤

1. 克隆或下载此项目
2. 安装依赖包：
```bash
pip install -r requirements.txt
```

## 运行方法

在项目目录下运行：
```bash
python app.py
```

然后在浏览器中访问：http://localhost:5000

## 使用说明

1. 打开网页后，系统会自动检测并显示最新的影刀项目
2. 点击"刷新"按钮可以重新检测项目
3. 在每个模块后的输入框中输入中文备注
4. 点击"保存"按钮将备注保存到config.txt文件中
