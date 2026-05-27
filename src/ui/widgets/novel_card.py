import qtawesome as qta
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class NovelCard(QWidget):
    EPUB_COLOR = '#2196F3'
    EPUB_BG = '#e3f2fd'
    TXT_COLOR = '#FF9800'
    TXT_BG = '#fff3e0'
    
    def __init__(self, novel, parent=None):
        super().__init__(parent)
        self.novel = novel
        self._selected = False
        self.icon_color = self.EPUB_COLOR if novel.format == 'EPUB' else self.TXT_COLOR
        self.icon_bg = self.EPUB_BG if novel.format == 'EPUB' else self.TXT_BG
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)
        
        icon_label = QLabel()
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.icon_bg};
                border-radius: 8px;
            }}
        """)
        icon_name = 'fa5s.book' if self.novel.format == 'EPUB' else 'fa5s.file-alt'
        icon_label.setPixmap(qta.icon(icon_name, color=self.icon_color).pixmap(28, 28))
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        title_label = QLabel(self.novel.title)
        title_label.setStyleSheet(f"font-weight: bold; font-size: 14px; color: {self.icon_color};")
        title_label.setWordWrap(True)
        title_label.setMaximumWidth(200)
        
        author_label = QLabel(f"作者: {self.novel.author}")
        author_label.setStyleSheet("font-size: 12px; color: #666;")
        
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(8)
        
        format_label = QLabel(self.novel.format)
        format_label.setAlignment(Qt.AlignCenter)
        format_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.icon_color};
                color: white;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 10px;
                min-width: 32px;
            }}
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
        
        self._base_style = f"""
            QWidget {{
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }}
            QWidget:hover {{
                border-color: {self.icon_color};
                background-color: #f8fafc;
            }}
        """
        self._selected_style = f"""
            QWidget {{
                background-color: {self.icon_bg};
                border: 3px solid {self.icon_color};
                border-left: 4px solid {self.icon_color};
                border-radius: 8px;
            }}
        """
        self.setStyleSheet(self._base_style)
    
    def set_selected(self, selected):
        self._selected = selected
        if selected:
            self.setStyleSheet(self._selected_style)
        else:
            self.setStyleSheet(self._base_style)
    
    def isSelected(self):
        return self._selected
