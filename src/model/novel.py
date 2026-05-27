import os
import uuid
import re
from datetime import datetime

class Novel:
    def __init__(self, file_path):
        self.id = str(uuid.uuid4())
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
        name = re.sub(r'[\(（\[【].*?[\)）\]】]', '', name).strip()
        name = name.replace('《', '').replace('》', '').strip()
        
        return name if name else '未知标题'
    
    def _extract_author(self):
        name = os.path.splitext(self.filename)[0]
        matches = re.findall(r'[\(（\[【](.*?)[\)）\]】]', name)
        
        for match in matches:
            author = match.strip()
            if not author:
                continue
            
            ignore_tags = ['完结', '精校版', '精校全本', '全本', '校对版', 'TXT']
            if any(tag in author for tag in ignore_tags):
                continue
                
            lower_author = author.lower()
            if lower_author.startswith('by ') or lower_author.startswith('by:'):
                author = author[3:].strip()
            elif author.startswith('作者:') or author.startswith('作者：'):
                author = author[3:].strip()
                
            if author:
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
