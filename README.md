# 小说管理系统

一个基于 PyQt5 的小说管理工具，支持 EPUB 和 TXT 格式的小说管理与格式转换。

## ✨ 功能特性

- 📚 **小说管理** - 支持 EPUB 和 TXT 格式的小说扫描与管理
- 🔍 **搜索过滤** - 支持按书名、作者搜索，按格式过滤
- 📄 **格式转换** - EPUB 转 TXT 格式，支持批量转换
- ⚙️ **目录设置** - 自定义 EPUB 和 TXT 文件目录
- 📊 **统计面板** - 实时显示小说数量和大小统计
- 🎨 **精美界面** - 现代化 UI 设计，支持颜色区分格式

## 🚀 快速开始

### 环境要求

- Python 3.8+
- PyQt5 5.15+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
python src/main.py
```

### 打包运行

已打包的可执行文件位于 `dist/NovelManager/NovelManager.exe`

```bash
dist/NovelManager/NovelManager.exe
```

## 📁 项目结构

```
src/
├── main.py                    # 入口文件
├── manager/                   # 业务逻辑层
│   ├── converter.py           # 格式转换工具
│   ├── epub_parser.py         # EPUB 解析器
│   └── file_manager.py        # 文件管理器
├── model/                     # 数据模型
│   └── novel.py               # 小说数据模型
└── ui/                        # 界面层
    ├── main_window.py         # 主窗口
    └── widgets/               # 自定义组件
        ├── novel_card.py      # 小说卡片组件
        ├── toast.py           # Toast 通知组件
        ├── convert_worker.py  # 后台转换线程
        ├── settings_dialog.py # 设置对话框
        └── progress_dialog.py # 进度对话框
```

## 🎯 使用说明

### 首次启动

首次启动时会弹出设置对话框，请设置 EPUB 和 TXT 文件所在的目录。

### 格式过滤

点击顶部工具栏的「全部」「EPUB」「TXT」按钮切换格式过滤。

### 搜索功能

在搜索框中输入关键词，可以按书名或作者进行搜索。

### 批量操作

- 支持多选小说（按住 Ctrl 或 Shift 键）
- 批量转换：将选中的 EPUB 小说转换为 TXT 格式
- 批量删除：删除选中的小说

### 目录设置

点击右上角 ⚙️ 按钮打开设置对话框，修改 EPUB 和 TXT 目录。

## 📝 配置说明

程序使用 Qt 的 QSettings 持久化配置：

- **EPUB 目录**: 存放 EPUB 格式小说的文件夹
- **TXT 目录**: 存放 TXT 格式小说的文件夹

配置会自动保存，下次启动时自动加载。

## 🛠️ 开发

### 打包命令

```bash
pyinstaller build.spec
```

### 依赖列表

| 依赖 | 版本 | 说明 |
|------|------|------|
| PyQt5 | >=5.15.0 | GUI 框架 |
| ebooklib | >=0.17.1 | EPUB 解析 |
| beautifulsoup4 | >=4.12.0 | HTML 解析 |

## 📄 许可证

Apache License 2.0

详见 [LICENSE](LICENSE) 文件
