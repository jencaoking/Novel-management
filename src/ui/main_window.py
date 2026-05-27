import os
import qtawesome as qta
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem,
    QLabel, QSplitter, QComboBox, QGroupBox, QTextEdit,
    QMessageBox, QStatusBar, QScrollArea, QFrame, QProgressBar
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize
from manager.file_manager import FileManager
from manager.converter import Converter
from ui.widgets.novel_card import NovelCard
from ui.widgets.progress_dialog import ProgressDialog
from ui.widgets.toast import Toast
from ui.widgets.convert_worker import ConvertWorker
from ui.widgets.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("小说管理系统")
        self.setMinimumSize(1000, 700)
        
        self.file_manager = FileManager()
        self.converter = Converter()
        self.selected_novels = []
        self.convert_worker = None
        self.current_filter = 'all'
        
        self.init_ui()
        self.check_first_run()
        
    def check_first_run(self):
        if not self.file_manager.has_valid_directories():
            dialog = SettingsDialog(self)
            if dialog.exec_():
                self.file_manager._init_directories()
                self.load_novels()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.create_toolbar(main_layout)
        self.create_stats_panel(main_layout)
        self.create_main_content(main_layout)
        
        self.load_novels()
    
    def create_toolbar(self, parent_layout):
        toolbar = QWidget()
        toolbar.setStyleSheet("background-color: #2196F3; padding: 12px;")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(16, 8, 16, 8)
        toolbar_layout.setSpacing(12)
        
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.book', color='white').pixmap(24, 24))
        title_label = QLabel("小说管理")
        title_label.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        
        toolbar_layout.addWidget(title_icon)
        toolbar_layout.addWidget(title_label)
        toolbar_layout.addStretch()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索书名或作者...")
        self.search_input.setFixedWidth(200)
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
        self.search_type.setFixedWidth(70)
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
        
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(self.search_type)
        
        self.filter_all_btn = QPushButton("全部")
        self.filter_epub_btn = QPushButton("EPUB")
        self.filter_txt_btn = QPushButton("TXT")
        
        filter_btn_style_inactive = """
            QPushButton {{
                padding: 6px 16px;
                border: 2px solid rgba(255,255,255,0.5);
                border-radius: 20px;
                font-size: 13px;
                background-color: transparent;
                color: white;
            }}
            QPushButton:hover {{
                background-color: rgba(255,255,255,0.2);
            }}
        """
        filter_btn_style_active = """
            QPushButton {{
                padding: 6px 16px;
                border: none;
                border-radius: 20px;
                font-size: 13px;
                background-color: white;
                color: #2196F3;
                font-weight: bold;
            }}
        """
        
        self.filter_all_btn.setStyleSheet(filter_btn_style_active)
        self.filter_epub_btn.setStyleSheet(filter_btn_style_inactive)
        self.filter_txt_btn.setStyleSheet(filter_btn_style_inactive)
        
        self.filter_all_btn.clicked.connect(lambda: self.on_filter_toggle('all'))
        self.filter_epub_btn.clicked.connect(lambda: self.on_filter_toggle('EPUB'))
        self.filter_txt_btn.clicked.connect(lambda: self.on_filter_toggle('TXT'))
        
        toolbar_layout.addWidget(self.filter_all_btn)
        toolbar_layout.addWidget(self.filter_epub_btn)
        toolbar_layout.addWidget(self.filter_txt_btn)
        
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(qta.icon('fa5s.cog', color='white'))
        self.settings_btn.setIconSize(QSize(20, 20))
        self.settings_btn.setFixedWidth(40)
        self.settings_btn.setStyleSheet("""
            QPushButton {
                padding: 6px;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                background-color: transparent;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.2);
            }
        """)
        self.settings_btn.clicked.connect(self.open_settings)
        
        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(qta.icon('fa5s.sync-alt', color='white'))
        self.refresh_btn.setIconSize(QSize(20, 20))
        self.refresh_btn.setFixedWidth(40)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 6px;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                background-color: transparent;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.2);
            }
        """)
        self.refresh_btn.clicked.connect(self.load_novels)
        
        toolbar_layout.addWidget(self.settings_btn)
        toolbar_layout.addWidget(self.refresh_btn)
        
        parent_layout.addWidget(toolbar)
    
    def create_stats_panel(self, parent_layout):
        stats_panel = QWidget()
        stats_panel.setStyleSheet("background-color: #f5f5f5; padding: 8px;")
        stats_layout = QHBoxLayout(stats_panel)
        stats_layout.setContentsMargins(16, 8, 16, 8)
        stats_layout.setSpacing(16)
        
        self.stat_cards = {}
        
        card_configs = [
            ('total', 'fa5s.book', '总计', '#333'),
            ('epub', 'fa5s.book-open', 'EPUB', '#2196F3'),
            ('txt', 'fa5s.file-alt', 'TXT', '#FF9800'),
            ('size', 'fa5s.hdd', '总大小', '#666')
        ]
        
        for key, icon_name, label, color in card_configs:
            card = self.create_stat_card(icon_name, label, '0', color)
            self.stat_cards[key] = card
            stats_layout.addWidget(card)
        
        stats_layout.addStretch()
        parent_layout.addWidget(stats_panel)
    
    def create_stat_card(self, icon_name, label, value, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 8px;
                padding: 8px 16px;
            }}
        """)
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(8, 4, 8, 4)
        card_layout.setSpacing(8)
        
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color=color).pixmap(24, 24))
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        
        label_label = QLabel(label)
        label_label.setStyleSheet(f"font-size: 11px; color: #999;")
        
        value_label = QLabel(value)
        value_label.setObjectName('stat_value')
        value_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {color};")
        
        text_layout.addWidget(label_label)
        text_layout.addWidget(value_label)
        
        card_layout.addWidget(icon_label)
        card_layout.addLayout(text_layout)
        
        return card
    
    def update_stats_panel(self):
        stats = self.file_manager.get_statistics()
        
        for card_key, card in self.stat_cards.items():
            value_label = card.findChild(QLabel, 'stat_value')
            if value_label:
                if card_key == 'total':
                    value_label.setText(str(stats['total']))
                elif card_key == 'epub':
                    value_label.setText(str(stats['epub_count']))
                elif card_key == 'txt':
                    value_label.setText(str(stats['txt_count']))
                elif card_key == 'size':
                    value_label.setText(stats['total_size'])
    
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
        
        self.empty_state = QWidget()
        empty_layout = QVBoxLayout(self.empty_state)
        empty_layout.setAlignment(Qt.AlignCenter)
        
        empty_icon = QLabel()
        empty_icon.setPixmap(qta.icon('fa5s.inbox', color='#ccc').pixmap(64, 64))
        empty_icon.setAlignment(Qt.AlignCenter)
        
        self.empty_text = QLabel("没有找到小说")
        self.empty_text.setStyleSheet("font-size: 16px; color: #999;")
        self.empty_text.setAlignment(Qt.AlignCenter)
        
        empty_hint = QLabel("请检查目录设置或刷新列表")
        empty_hint.setStyleSheet("font-size: 13px; color: #bbb;")
        empty_hint.setAlignment(Qt.AlignCenter)
        
        empty_layout.addWidget(empty_icon)
        empty_layout.addWidget(self.empty_text)
        empty_layout.addWidget(empty_hint)
        
        left_layout.addWidget(self.novel_list)
        left_layout.addWidget(self.empty_state)
        self.empty_state.hide()
        
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
        
        self.convert_btn = QPushButton("EPUB → TXT")
        self.convert_btn.setIcon(qta.icon('fa5s.file-export', color='white'))
        self.convert_btn.setIconSize(QSize(18, 18))
        self.convert_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
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
        
        self.batch_convert_btn = QPushButton("批量转换")
        self.batch_convert_btn.setIcon(qta.icon('fa5s.clone', color='#2196F3'))
        self.batch_convert_btn.setIconSize(QSize(18, 18))
        self.batch_convert_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                border: 2px solid #2196F3;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #2196F3;
            }
            QPushButton:hover {
                background-color: #e3f2fd;
            }
            QPushButton:disabled {
                border-color: #ccc;
                color: #ccc;
                background-color: #f5f5f5;
            }
        """)
        self.batch_convert_btn.clicked.connect(self.batch_convert)
        self.batch_convert_btn.setEnabled(False)
        
        self.delete_btn = QPushButton("删除")
        self.delete_btn.setIcon(qta.icon('fa5s.trash-alt', color='white'))
        self.delete_btn.setIconSize(QSize(18, 18))
        self.delete_btn.setStyleSheet("""
            QPushButton {
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f44336;
                color: white;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:disabled {
                background-color: #ffcdd2;
                color: #999;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_selected)
        self.delete_btn.setEnabled(False)
        
        action_layout.addWidget(self.convert_btn)
        action_layout.addWidget(self.batch_convert_btn)
        action_layout.addSpacing(8)
        action_layout.addWidget(self.delete_btn)
        
        right_layout.addWidget(action_group)
        
        progress_group = QGroupBox("转换进度")
        progress_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
        """)
        
        self.progress_label = QLabel()
        self.progress_label.setVisible(False)
        self.progress_label.setStyleSheet("font-size: 12px; color: #666;")
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        
        right_layout.addWidget(progress_group)
        
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 1)
        
        parent_layout.addWidget(splitter)
    
    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_():
            self.file_manager._init_directories()
            self.load_novels()
    
    def load_novels(self):
        self.novel_list.clear()
        self.file_manager.load_all_novels()
        
        for novel in self.file_manager.novels:
            item = QListWidgetItem()
            card = NovelCard(novel)
            item.setSizeHint(card.sizeHint())
            self.novel_list.addItem(item)
            self.novel_list.setItemWidget(item, card)
        
        self.update_stats_panel()
        self.update_empty_state()
    
    def update_empty_state(self):
        if self.novel_list.count() == 0:
            self.novel_list.hide()
            self.empty_state.show()
        else:
            self.empty_state.hide()
            self.novel_list.show()
    
    def on_search(self):
        keyword = self.search_input.text()
        search_type = self.search_type.currentText()
        search_type_map = {"全部": "all", "书名": "title", "作者": "author"}
        
        results = self.file_manager.search_novels(keyword, search_type_map[search_type])
        
        if self.current_filter != 'all':
            results = [n for n in results if n.format == self.current_filter]
        
        self.display_results(results)
    
    def on_filter_toggle(self, filter_type):
        self.current_filter = filter_type
        
        filter_btn_style_inactive = """
            QPushButton {
                padding: 6px 16px;
                border: 2px solid rgba(255,255,255,0.5);
                border-radius: 20px;
                font-size: 13px;
                background-color: transparent;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.2);
            }
        """
        filter_btn_style_active = """
            QPushButton {
                padding: 6px 16px;
                border: none;
                border-radius: 20px;
                font-size: 13px;
                background-color: white;
                color: #2196F3;
                font-weight: bold;
            }
        """
        
        self.filter_all_btn.setStyleSheet(filter_btn_style_active if filter_type == 'all' else filter_btn_style_inactive)
        self.filter_epub_btn.setStyleSheet(filter_btn_style_active if filter_type == 'EPUB' else filter_btn_style_inactive)
        self.filter_txt_btn.setStyleSheet(filter_btn_style_active if filter_type == 'TXT' else filter_btn_style_inactive)
        
        results = self.file_manager.filter_by_format(filter_type)
        
        keyword = self.search_input.text()
        if keyword:
            search_type = self.search_type.currentText()
            keyword = keyword.lower()
            if search_type == "全部":
                results = [n for n in results if keyword in n.title.lower() or keyword in n.author.lower()]
            elif search_type == "书名":
                results = [n for n in results if keyword in n.title.lower()]
            elif search_type == "作者":
                results = [n for n in results if keyword in n.author.lower()]
        
        self.display_results(results)
    
    def display_results(self, novels):
        self.novel_list.clear()
        
        for novel in novels:
            item = QListWidgetItem()
            card = NovelCard(novel)
            item.setSizeHint(card.sizeHint())
            self.novel_list.addItem(item)
            self.novel_list.setItemWidget(item, card)
        
        self.update_empty_state_for_search(len(novels) == 0)
    
    def update_empty_state_for_search(self, is_empty):
        if is_empty:
            self.novel_list.hide()
            self.empty_state.show()
            self.empty_text.setText("没有找到匹配的小说")
        else:
            self.empty_state.hide()
            self.novel_list.show()
    
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
                card.set_selected(True)
        
        for i in range(self.novel_list.count()):
            item = self.novel_list.item(i)
            card = self.novel_list.itemWidget(item)
            if card and card.novel not in self.selected_novels:
                card.set_selected(False)
        
        has_single = len(self.selected_novels) == 1
        has_multiple = len(self.selected_novels) >= 1
        
        self.convert_btn.setEnabled(has_single and self.selected_novels[0].format == 'EPUB')
        self.batch_convert_btn.setEnabled(has_multiple)
        self.delete_btn.setEnabled(has_multiple)
    
    def show_detail(self, novel):
        while self.detail_layout.count():
            item = self.detail_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                layout = item.layout()
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                layout.deleteLater()
        
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
    
    def show_toast(self, message, toast_type='success'):
        toast = Toast(message, self, toast_type)
        toast.show_toast()
    
    def convert_single(self):
        if not self.selected_novels:
            return
        
        novel = self.selected_novels[0]
        if novel.format != 'EPUB':
            QMessageBox.warning(self, "提示", "仅支持EPUB转TXT")
            return
        
        self.start_conversion([novel])
    
    def batch_convert(self):
        if not self.selected_novels:
            return
        
        epub_novels = [n for n in self.selected_novels if n.format == 'EPUB']
        
        if not epub_novels:
            QMessageBox.warning(self, "提示", "没有可转换的EPUB文件")
            return
        
        self.start_conversion(epub_novels)
    
    def start_conversion(self, novels):
        self.convert_btn.setEnabled(False)
        self.batch_convert_btn.setEnabled(False)
        
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_bar.setRange(0, len(novels))
        self.progress_bar.setValue(0)
        
        self.convert_worker = ConvertWorker(self.converter, novels, 'TXT')
        self.convert_worker.progress_updated.connect(self.on_progress_updated)
        self.convert_worker.batch_finished.connect(self.on_conversion_finished)
        self.convert_worker.error_occurred.connect(self.on_conversion_error)
        self.convert_worker.start()
    
    def on_progress_updated(self, current, total, title):
        self.progress_bar.setValue(current)
        self.progress_label.setText(f"正在转换: {title} ({current}/{total})")
    
    def on_conversion_finished(self, results):
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        
        success_count = len(results['success'])
        failed_count = len(results['failed'])
        
        if failed_count == 0:
            self.show_toast(f"转换完成! 成功 {success_count} 个", Toast.SUCCESS)
        else:
            msg = f"成功: {success_count} 个\n失败: {failed_count} 个"
            if results['failed']:
                msg += "\n\n失败列表:\n" + "\n".join(f"- {name}: {reason}" for name, reason in results['failed'])
            QMessageBox.critical(self, "转换结果", msg)
        
        self.load_novels()
        self.update_selected_novels()
    
    def on_conversion_error(self, error_msg):
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        QMessageBox.critical(self, "错误", error_msg)
        self.update_selected_novels()
    
    def delete_selected(self):
        if not self.selected_novels:
            return
        
        count = len(self.selected_novels)
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除选中的 {count} 本小说吗？\n此操作不可撤销！",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            deleted_count = 0
            for novel in self.selected_novels:
                try:
                    os.remove(novel.path)
                    deleted_count += 1
                except Exception as e:
                    QMessageBox.critical(self, "删除失败", f"无法删除 {novel.title}:\n{str(e)}")
            
            if deleted_count > 0:
                self.show_toast(f"已删除 {deleted_count} 本小说", Toast.SUCCESS)
            
            self.load_novels()
            self.selected_novels = []
