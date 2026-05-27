from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QLabel, QDialogButtonBox

class ProgressDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(400, 120)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("准备开始...")
        self.label.setStyleSheet("font-size: 13px;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
    
    def update_progress(self, current, total):
        percentage = int((current / total) * 100)
        self.progress_bar.setValue(percentage)
        self.label.setText(f"正在处理: {current}/{total}")
    
    def set_message(self, message):
        self.label.setText(message)
