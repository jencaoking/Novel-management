import os
from datetime import datetime

class Novel:
    def __init__(self, file_path):
        self.id = id(self)
        self.path = file_path
        self.filename = os.path.basename(file_path)
        self.extension = os.path.splitext(self.filename)[1].lower()
        self.format = 'EPUB' if self.extension == '.epub' else 'TXT'
        self.size = os.path.getsize(file_path)
        self.modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        self.title = self._extract_title()
        self.author = self._extract_author()
        self.cover = None
        self.chapters = []
    
    def _extract_title(self):
        name = os.path.splitext(self.filename)[0]
        patterns = ['《', '》', '(', '（', '[', '【']
        for pattern in patterns:
            if pattern in name:
                name = name.split(pattern)[0].strip()
                break
        return name if name else '未知标题'
    
    def _extract_author(self):
        name = os.path.splitext(self.filename)[0]
        patterns = [('(', ')'), ('（', '）'), ('[', ']'), ('【', '】')]
        for start, end in patterns:
            if start in name and end in name:
                idx_start = name.find(start)
                idx_end = name.find(end, idx_start)
                if idx_end > idx_start:
                    author = name[idx_start+1:idx_end].strip()
                    if author and 'by' not in author.lower():
                        return author
        return '未知作者'
    
    def get_size_str(self):
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.2f} KB"
        else:
            return f"{self.size / (1024 * 1024):.2f} MB"
    
    def get_modified_str(self):
        return self.modified_time.strftime('%Y-%m-%d %H:%M')
    
    def __repr__(self):
        return f"Novel(title={self.title}, author={self.author}, format={self.format})"
