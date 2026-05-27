from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint


class Toast(QWidget):
    SUCCESS = 'success'
    ERROR = 'error'
    INFO = 'info'
    
    def __init__(self, message, parent=None, toast_type='success', duration=3000):
        super().__init__(parent)
        self.duration = duration
        self.toast_type = toast_type
        self.message = message
        self.init_ui()
        
    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        icon_map = {
            self.SUCCESS: '✓',
            self.ERROR: '✗',
            self.INFO: 'ℹ'
        }
        
        color_map = {
            self.SUCCESS: '#4CAF50',
            self.ERROR: '#f44336',
            self.INFO: '#2196F3'
        }
        
        bg_color_map = {
            self.SUCCESS: '#e8f5e9',
            self.ERROR: '#ffebee',
            self.INFO: '#e3f2fd'
        }
        
        icon_label = QLabel(icon_map.get(self.toast_type, 'ℹ'))
        icon_label.setStyleSheet(f"""
            QLabel {{
                color: {color_map.get(self.toast_type, '#2196F3')};
                font-size: 16px;
                font-weight: bold;
            }}
        """)
        
        message_label = QLabel(self.message)
        message_label.setStyleSheet(f"""
            QLabel {{
                color: #333;
                font-size: 13px;
            }}
        """)
        
        layout.addWidget(icon_label)
        layout.addWidget(message_label)
        self.setLayout(layout)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color_map.get(self.toast_type, '#e3f2fd')};
                border-radius: 8px;
                border: 1px solid {color_map.get(self.toast_type, '#2196F3')};
            }}
        """)
        
        self.adjustSize()
        
    def show_toast(self):
        if self.parent():
            parent_rect = self.parent().rect()
            x = (parent_rect.width() - self.width()) // 2
            y = 60
            self.move(x, y)
        
        self.show()
        
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)
        
        self.fade_in = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.fade_in.setDuration(200)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.start()
        
        QTimer.singleShot(self.duration, self.start_fade_out)
        
    def start_fade_out(self):
        self.fade_out = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.fade_out.setDuration(300)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.finished.connect(self.close)
        self.fade_out.start()
