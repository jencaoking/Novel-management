from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class NovelCard(QWidget):
    def __init__(self, novel, parent=None):
        super().__init__(parent)
        self.novel = novel
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)
        
        icon_label = QLabel()
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            QLabel {
                background-color: #e8f4f8;
                border-radius: 8px;
                font-size: 24px;
            }
        """)
        
        format_icon = '📖' if self.novel.format == 'EPUB' else '📝'
        icon_label.setText(format_icon)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        title_label = QLabel(self.novel.title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        title_label.setWordWrap(True)
        title_label.setMaximumWidth(200)
        
        author_label = QLabel(f"作者: {self.novel.author}")
        author_label.setStyleSheet("font-size: 12px; color: #666;")
        
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(8)
        
        format_label = QLabel(self.novel.format)
        format_label.setAlignment(Qt.AlignCenter)
        format_label.setStyleSheet("""
            QLabel {
                background-color: #4CAF50;
                color: white;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 10px;
                min-width: 32px;
            }
        """)
        
        size_label = QLabel(self.novel.get_size_str())
        size_label.setStyleSheet("font-size: 12px; color: #999;")
        
        meta_layout.addWidget(format_label)
        meta_layout.addWidget(size_label)
        meta_layout.addStretch()
        
        info_layout.addWidget(title_label)
        info_layout.addWidget(author_label)
        info_layout.addLayout(meta_layout)
        
        layout.addWidget(icon_label)
        layout.addLayout(info_layout)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
            QWidget:hover {
                border-color: #2196F3;
                background-color: #f8fafc;
            }
        """)
