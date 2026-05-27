# 小说管理系统

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-green)
![License](https://img.shields.io/badge/License-Apache%202.0-orange)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

一个基于 PyQt5 的现代化小说管理工具，支持 EPUB 和 TXT 格式的小说管理与格式转换。

## 功能特性

### 核心功能

- 📚 **小说管理** - 支持 EPUB 和 TXT 格式的小说扫描与管理
- 🔍 **搜索过滤** - 支持按书名、作者搜索，按格式过滤
- 📄 **格式转换** - EPUB 转 TXT、TXT 转 EPUB 双向转换，支持批量转换
- ⚙️ **目录设置** - 自定义 EPUB 和 TXT 文件目录
- 📊 **统计面板** - 实时显示小说数量和大小统计
- 🎨 **精美界面** - 现代化 UI 设计，支持颜色区分格式

### 技术亮点

- **智能章节识别** - 支持带空格的章节标题（如 `  第一章`）
- **EPUB 排版优化** - 正确处理文本换行，保持段落格式
- **HTML 安全转义** - 自动转义特殊字符（`<`, `>`, `&`），防止解析错误
- **编码兼容** - 支持 UTF-8 和 GBK 编码的 TXT 文件
- **异步处理** - 后台线程处理转换任务，界面流畅不卡顿

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- Windows 操作系统

### 安装步骤

1. 克隆项目

```bash
git clone <repository-url>
cd "Novel management"
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 运行程序

```bash
python src/main.py
```

### 打包运行

已打包的可执行文件：

```bash
dist/NovelManager/NovelManager.exe
```

打包命令：

```bash
pyinstaller build.spec
```

## 项目结构

```
Novel management/
├── src/                        # 源代码目录
│   ├── main.py                 # 程序入口
│   ├── manager/                # 业务逻辑层
│   │   ├── converter.py        # 格式转换工具
│