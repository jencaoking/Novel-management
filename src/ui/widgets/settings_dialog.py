from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QFileDialog, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt, QSettings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setMinimumSize(500, 300)
        self.settings = QSettings('NovelManagement', 'NovelApp')
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("⚙️ 目录设置")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)
        
        epub_group = QGroupBox("EPUB 目录")
        epub_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
                margin-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }
        """)
        epub_layout = QHBoxLayout()
        
        self.epub_path_input = QLineEdit()
        self.epub_path_input.setPlaceholderText("选择EPUB文件所在目录...")
        self.epub_path_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                font-size: 13px;
            }
        """)
        
        epub_btn = QPushButton("浏览...")
        epub_btn.setFixedWidth(80)
        epub_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #2196F3;
                border-radius: 6px;
                background-color: white;
                color: #2196F3;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #e3f2fd;
            }
        """)
        epub_btn.clicked.connect(self.browse_epub_dir)
        
        epub_layout.addWidget(self.epub_path_input)
        epub_layout.addWidget(epub_btn)
        epub_group.setLayout(epub_layout)
        layout.addWidget(epub_group)
        
        txt_group = QGroupBox("TXT 目录")
        txt_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 16px;
                margin-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }
        """)
        txt_layout = QHBoxLayout()
        
        self.txt_path_input = QLineEdit()
        self.txt_path_input.setPlaceholderText("选择TXT文件所在目录...")
        self.txt_path_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                font-size: 13px;
            }
        """)
        
        txt_btn = QPushButton("浏览...")
        txt_btn.setFixedWidth(80)
        txt_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #2196F3;
                border-radius: 6px;
                background-color: white;
                color: #2196F3;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #e3f2fd;
            }
        """)
        txt_btn.clicked.connect(self.browse_txt_dir)
        
        txt_layout.addWidget(self.txt_path_input)
        txt_layout.addWidget(txt_btn)
        txt_group.setLayout(txt_layout)
        layout.addWidget(txt_group)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton("保存")
        save_btn.setFixedWidth(100)
        save_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 24px;
                border: none;
                border-radius: 6px;
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedWidth(100)
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 24px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
                color: #666;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.load_settings()
        
    def browse_epub_dir(self):
        path = QFileDialog.getExistingDirectory(self, "选择EPUB目录")
        if path:
            self.epub_path_input.setText(path)
            
    def browse_txt_dir(self):
        path = QFileDialog.getExistingDirectory(self, "选择TXT目录")
        if path:
            self.txt_path_input.setText(path)
            
    def load_settings(self):
        epub_dir = self.settings.value('epub_dir', '')
        txt_dir = self.settings.value('txt_dir', '')
        self.epub_path_input.setText(epub_dir)
        self.txt_path_input.setText(txt_dir)
        
    def save_settings(self):
        epub_dir = self.epub_path_input.text().strip()
        txt_dir = self.txt_path_input.text().strip()
        
        if not epub_dir or not txt_dir:
            QMessageBox.warning(self, "提示", "请设置所有目录路径")
            return
            
        self.settings.setValue('epub_dir', epub_dir)
        self.settings.setValue('txt_dir', txt_dir)
        self.accept()
