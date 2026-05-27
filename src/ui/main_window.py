import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem,
                             QLabel, QSplitter, QComboBox, QGroupBox, QTextEdit,
                             QMessageBox, QStatusBar, QScrollArea, QFrame)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize
from manager.file_manager import FileManager
from manager.converter import Converter
from ui.widgets.novel_card import NovelCard
from ui.widgets.progress_dialog import ProgressDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("小说管理系统")
        self.setMinimumSize(1000, 600)
        
        self.file_manager = FileManager()
        self.converter = Converter()
        self.selected_novels = []
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.create_toolbar(main_layout)
        self.create_main_content(main_layout)
        self.create_status_bar()
        
        self.load_novels()
    
    def create_toolbar(self, parent_layout):
        toolbar = QWidget()
        toolbar.setStyleSheet("background-color: #2196F3; padding: 12px;")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(16, 8, 16, 8)
        toolbar_layout.setSpacing(12)
        
        title_label = QLabel("📚 小说管理")
        title_label.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        
        toolbar_layout.addWidget(title_label)
        toolbar_layout.addStretch()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索书名或作者...")
        self.search_input.setFixedWidth(250)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 12px;
                border: none;
                border-radius: 20px;
                font-size: 13px;
            }
        """)
        self.search_input.textChanged.connect(self.on_search)
        
        self.search_type = QComboBox()
        self.search_type.addItems(["全部", "书名", "作者"])
        self.search_type.setFixedWidth(80)
        self.search_type.setStyleSheet("""
            QComboBox {
                padding: 6px 12px;
                border: none;
                border-radius: 20px;
                font-size: 13px;
                background-color: white;
            }
        """)
        self.search_type.currentTextChanged.connect(self.on_search)
        
        self.format_filter = QComboBox()
        self.format_filter.addItems(["全部格式", "EPUB", "TXT"])
        self.format_filter.setFixedWidth(100)
        self.format_filter.setStyleSheet("""
            QComboBox {
                padding: 6px 12px;
                border: none;
                border-radius: 20px;
                font-size: 13px;
                background-color: white;
            }
        """)
        self.format_filter.currentTextChanged.connect(self.on_filter)
        
        self.refresh_btn = QPushButton("🔄 刷新")
        self.refresh_btn.setFixedWidth(80)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 6px 16px;
                border: none;
                border-radius: 20px;
                font-size: 13px;
                background-color: rgba(255,255,255,0.2);
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.3);
            }
        """)
        self.refresh_btn.clicked.connect(self.load_novels)
        
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(self.search_type)
        toolbar_layout.addWidget(self.format_filter)
        toolbar_layout.addWidget(self.refresh_btn)
        
        parent_layout.addWidget(toolbar)
    
    def create_main_content(self, parent_layout):
        splitter = QSplitter(Qt.Horizontal)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(8, 8, 8, 8)
        
        self.novel_list = QListWidget()
        self.novel_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #fafafa;
            }
            QListWidget::item {
                padding: 4px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
            }
        """)
        self.novel_list.itemClicked.connect(self.on_novel_click)
        self.novel_list.setSelectionMode(QListWidget.ExtendedSelection)
        
        left_layout.addWidget(self.novel_list)
        
        splitter.addWidget(left_panel)
        splitter.setStretchFactor(0, 1)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(8, 8, 8, 8)
        right_layout.setSpacing(12)
        
        self.detail_group = QGroupBox("小说详情")
        self.detail_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        detail_layout = QVBoxLayout(self.detail_group)
        
        self.detail_content = QScrollArea()
        self.detail_content.setWidgetResizable(True)
        self.detail_content.setStyleSheet("border: none;")
        
        self.detail_widget = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_widget)
        self.detail_layout.setContentsMargins(0, 0, 0, 0)
        self.detail_layout.setSpacing(12)
        
        self.detail_empty = QLabel("请选择一本小说查看详情")
        self.detail_empty.setStyleSheet("color: #999; font-size: 14px;")
        self.detail_empty.setAlignment(Qt.AlignCenter)
        self.detail_layout.addWidget(self.detail_empty)
        
        self.detail_content.setWidget(self.detail_widget)
        detail_layout.addWidget(self.detail_content)
        
        right_layout.addWidget(self.detail_group)
        
        action_group = QGroupBox("操作")
        action_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        action_layout = QVBoxLayout(action_group)
        action_layout.setSpacing(8)
        
        self.convert_btn = QPushButton("📄 EPUB → TXT")
        self.convert_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        self.convert_btn.clicked.connect(self.convert_single)
        self.convert_btn.setEnabled(False)
        
        self.batch_convert_btn = QPushButton("📦 批量转换")
        self.batch_convert_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                background-color: #FF9800;
                color: white;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        self.batch_convert_btn.clicked.connect(self.batch_convert)
        self.batch_convert_btn.setEnabled(False)
        
        action_layout.addWidget(self.convert_btn)
        action_layout.addWidget(self.batch_convert_btn)
        
        right_layout.addWidget(action_group)
        
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 1)
        
        parent_layout.addWidget(splitter)
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status()
    
    def load_novels(self):
        self.novel_list.clear()
        self.file_manager.load_all_novels()
        
        for novel in self.file_manager.novels:
            item = QListWidgetItem()
            card = NovelCard(novel)
            item.setSizeHint(card.sizeHint())
            self.novel_list.addItem(item)
            self.novel_list.setItemWidget(item, card)
        
        self.update_status()
    
    def on_search(self):
        keyword = self.search_input.text()
        search_type = self.search_type.currentText()
        search_type_map = {"全部": "all", "书名": "title", "作者": "author"}
        
        results = self.file_manager.search_novels(keyword, search_type_map[search_type])
        self.display_results(results)
    
    def on_filter(self):
        format_type = self.format_filter.currentText()
        format_type_map = {"全部格式": "all", "EPUB": "EPUB", "TXT": "TXT"}
        
        results = self.file_manager.filter_by_format(format_type_map[format_type])
        
        keyword = self.search_input.text()
        if keyword:
            search_type = self.search_type.currentText()
            search_type_map = {"全部": "all", "书名": "title", "作者": "author"}
            self.file_manager.novels = results
            results = self.file_manager.search_novels(keyword, search_type_map[search_type])
        
        self.display_results(results)
    
    def display_results(self, novels):
        self.novel_list.clear()
        
        for novel in novels:
            item = QListWidgetItem()
            card = NovelCard(novel)
            item.setSizeHint(card.sizeHint())
            self.novel_list.addItem(item)
            self.novel_list.setItemWidget(item, card)
    
    def on_novel_click(self, item):
        card = self.novel_list.itemWidget(item)
        if card:
            self.show_detail(card.novel)
        
        self.update_selected_novels()
    
    def update_selected_novels(self):
        self.selected_novels = []
        for item in self.novel_list.selectedItems():
            card = self.novel_list.itemWidget(item)
            if card:
                self.selected_novels.append(card.novel)
        
        has_single = len(self.selected_novels) == 1
        has_multiple = len(self.selected_novels) >= 1
        
        self.convert_btn.setEnabled(has_single and self.selected_novels[0].format == 'EPUB')
        self.batch_convert_btn.setEnabled(has_multiple)
    
    def show_detail(self, novel):
        for i in reversed(range(self.detail_layout.count())):
            self.detail_layout.itemAt(i).widget().deleteLater()
        
        grid = QGridLayout()
        grid.setSpacing(8)
        
        labels = ["书名", "作者", "格式", "大小", "修改时间", "路径"]
        values = [novel.title, novel.author, novel.format, 
                  novel.get_size_str(), novel.get_modified_str(), novel.path]
        
        for i, (label, value) in enumerate(zip(labels, values)):
            grid.addWidget(QLabel(f"<b>{label}:</b>"), i, 0)
            value_label = QLabel(value)
            value_label.setWordWrap(True)
            grid.addWidget(value_label, i, 1)
        
        self.detail_layout.addLayout(grid)
        self.detail_widget.adjustSize()
    
    def convert_single(self):
        if not self.selected_novels:
            return
        
        novel = self.selected_novels[0]
        if novel.format != 'EPUB':
            QMessageBox.warning(self, "提示", "仅支持EPUB转TXT")
            return
        
        progress = ProgressDialog("转换中", self)
        progress.show()
        
        try:
            result = self.converter.epub_to_txt(novel.path)
            progress.close()
            
            if result:
                QMessageBox.information(self, "成功", f"转换完成!\n{result}")
                self.load_novels()
            else:
                QMessageBox.error(self, "失败", "转换失败")
        except Exception as e:
            progress.close()
            QMessageBox.error(self, "错误", str(e))
    
    def batch_convert(self):
        if not self.selected_novels:
            return
        
        progress = ProgressDialog("批量转换中", self)
        progress.show()
        
        epub_novels = [n for n in self.selected_novels if n.format == 'EPUB']
        
        def update_progress(current, total):
            progress.update_progress(current, total)
        
        try:
            results = self.converter.batch_convert(epub_novels, 'TXT', progress_callback=update_progress)
            progress.close()
            
            msg = f"成功: {len(results['success'])} 个\n失败: {len(results['failed'])} 个"
            if results['failed']:
                msg += "\n\n失败列表:\n" + "\n".join(f"- {name}: {reason}" for name, reason in results['failed'])
            
            QMessageBox.information(self, "批量转换完成", msg)
            self.load_novels()
        except Exception as e:
            progress.close()
            QMessageBox.error(self, "错误", str(e))
    
    def update_status(self):
        stats = self.file_manager.get_statistics()
        self.status_bar.showMessage(
            f"共 {stats['total']} 本小说 | EPUB: {stats['epub_count']} | TXT: {stats['txt_count']} | 总大小: {stats['total_size']}"
        )
