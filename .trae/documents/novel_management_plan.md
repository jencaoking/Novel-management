# 小说管理软件开发计划

## 1. 项目概述

本项目旨在开发一个Windows平台的小说管理软件，用于管理EPUB和TXT格式的小说文件，面向管理人员使用。

### 1.1 需求分析

根据用户提供的数据目录：
- **EPUB目录** (`j:\PROJECT\Python project\Novel management\EPUB`): 包含5本EPUB格式小说
- **TXT目录** (`j:\PROJECT\Python project\Novel management\Novel txt`): 包含70+本TXT格式小说

### 1.2 功能需求

| 功能模块 | 功能描述 |
|---------|---------|
| 文件管理 | 扫描EPUB和TXT目录，展示小说列表 |
| 搜索功能 | 支持按书名、作者进行搜索 |
| 格式转换 | EPUB转TXT、TXT转EPUB |
| 批量操作 | 批量转换、批量重命名 |
| 统计功能 | 小说数量、格式分布统计 |

## 2. 技术方案

### 2.1 技术选型

| 分类 | 技术 | 版本 | 选型理由 |
|-----|------|------|---------|
| GUI框架 | PyQt5 | 5.15+ | 跨平台、功能强大、社区成熟 |
| EPUB解析 | ebooklib | 0.17+ | 成熟的EPUB解析库 |
| 打包工具 | PyInstaller | 5.0+ | 支持Windows打包为EXE |

### 2.2 项目结构

```
Novel management/
├── src/
│   ├── main.py              # 主程序入口
│   ├── ui/
│   │   ├── main_window.py   # 主窗口界面
│   │   └── widgets/         # 自定义控件
│   ├── model/
│   │   └── novel.py         # 小说数据模型
│   ├── manager/
│   │   ├── file_manager.py  # 文件管理
│   │   ├── epub_parser.py   # EPUB解析
│   │   └── converter.py     # 格式转换
│   └── utils/
│       └── config.py        # 配置管理
├── requirements.txt         # 依赖列表
└── README.md               # 项目说明
```

## 3. 开发计划

### 3.1 阶段一：项目初始化与环境配置

**任务1**: 创建项目目录结构
- 创建src目录及子目录
- 创建requirements.txt

**任务2**: 安装依赖
- PyQt5
- ebooklib
- beautifulsoup4 (用于EPUB解析)

### 3.2 阶段二：数据模型与文件管理

**任务3**: 实现小说数据模型 (`model/novel.py`)
- Novel类：id, title, author, path, format, size, modified_time

**任务4**: 实现文件管理 (`manager/file_manager.py`)
- 扫描目录获取小说列表
- 提取书名、作者信息
- 支持EPUB和TXT格式

**任务5**: 实现EPUB解析 (`manager/epub_parser.py`)
- 解析EPUB元数据
- 提取章节内容
- 获取封面图片

### 3.3 阶段三：格式转换功能

**任务6**: 实现格式转换 (`manager/converter.py`)
- EPUB转TXT
- TXT转EPUB
- 批量转换支持

### 3.4 阶段四：GUI界面开发

**任务7**: 实现主窗口 (`ui/main_window.py`)
- 左侧：小说列表（支持搜索筛选）
- 右侧：小说详情
- 工具栏：转换、批量操作
- 底部：统计信息

**任务8**: 实现自定义控件
- 小说卡片组件
- 进度对话框

### 3.5 阶段五：功能集成与测试

**任务9**: 集成所有功能模块
- 文件扫描与展示
- 搜索筛选
- 格式转换
- 统计功能

**任务10**: 打包测试
- 使用PyInstaller打包
- 测试EXE运行效果

## 4. 依赖列表

```txt
PyQt5>=5.15.0
ebooklib>=0.17.1
beautifulsoup4>=4.12.0
python-dateutil>=2.8.0
```

## 5. 风险评估

| 风险 | 描述 | 应对措施 |
|-----|------|---------|
| EPUB兼容性 | 不同EPUB格式可能存在解析问题 | 使用成熟库，增加异常处理 |
| 大文件性能 | 大TXT文件处理缓慢 | 分段处理，进度显示 |
| 编码问题 | TXT文件编码不一致 | 自动检测编码 |
| 打包体积 | PyQt5打包后体积较大 | 使用UPX压缩 |

## 6. 交付物

- 完整的Python源代码
- 可执行的Windows EXE文件
- 项目说明文档

---

*计划创建时间: 2026-05-27*
*版本: v1.1*
