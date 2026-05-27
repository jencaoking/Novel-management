import sys
import os
from model.novel import Novel
from PyQt5.QtCore import QSettings


def get_base_path():
    """获取程序运行的真实基准路径，兼容源码运行和 PyInstaller 打包运行"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FileManager:
    def __init__(self):
        self.settings = QSettings('NovelManagement', 'NovelApp')
        self.novels = []
        self._init_directories()
        
    def _init_directories(self):
        epub_dir = self.settings.value('epub_dir', '')
        txt_dir = self.settings.value('txt_dir', '')
        
        base_path = get_base_path()
        
        if epub_dir and os.path.exists(epub_dir):
            self.epub_dir = epub_dir
        else:
            self.epub_dir = os.path.join(base_path, 'EPUB')
            
        if txt_dir and os.path.exists(txt_dir):
            self.txt_dir = txt_dir
        else:
            self.txt_dir = os.path.join(base_path, 'Novel txt')
            
        os.makedirs(self.epub_dir, exist_ok=True)
        os.makedirs(self.txt_dir, exist_ok=True)
    
    def set_directories(self, epub_dir, txt_dir):
        self.epub_dir = epub_dir
        self.txt_dir = txt_dir
        self.settings.setValue('epub_dir', epub_dir)
        self.settings.setValue('txt_dir', txt_dir)
        
    def get_directories(self):
        return {
            'epub_dir': self.epub_dir,
            'txt_dir': self.txt_dir
        }
    
    def has_valid_directories(self):
        epub_valid = os.path.exists(self.epub_dir) if self.epub_dir else False
        txt_valid = os.path.exists(self.txt_dir) if self.txt_dir else False
        return epub_valid and txt_valid
    
    def scan_directory(self, dir_path, ext):
        novels = []
        if not dir_path or not os.path.exists(dir_path):
            return novels
        
        for filename in os.listdir(dir_path):
            if filename.lower().endswith(ext):
                file_path = os.path.join(dir_path, filename)
                try:
                    novel = Novel(file_path)
                    novels.append(novel)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        
        return novels
    
    def load_all_novels(self):
        self.novels = []
        epub_novels = self.scan_directory(self.epub_dir, '.epub')
        txt_novels = self.scan_directory(self.txt_dir, '.txt')
        self.novels = epub_novels + txt_novels
        self.novels.sort(key=lambda x: x.title)
        return self.novels
    
    def search_novels(self, keyword, search_type='all'):
        if not keyword:
            return self.novels
        
        keyword = keyword.lower()
        results = []
        
        for novel in self.novels:
            match = False
            if search_type == 'title' or search_type == 'all':
                if keyword in novel.title.lower():
                    match = True
            if search_type == 'author' or search_type == 'all':
                if keyword in novel.author.lower():
                    match = True
            if match:
                results.append(novel)
        
        return results
    
    def filter_by_format(self, format_type):
        if format_type == 'all':
            return self.novels
        return [n for n in self.novels if n.format == format_type]
    
    def get_statistics(self):
        total = len(self.novels)
        epub_count = len([n for n in self.novels if n.format == 'EPUB'])
        txt_count = len([n for n in self.novels if n.format == 'TXT'])
        total_size = sum(n.size for n in self.novels)
        
        if total_size < 1024:
            size_str = f"{total_size} B"
        elif total_size < 1024 * 1024:
            size_str = f"{total_size / 1024:.2f} KB"
        elif total_size < 1024 * 1024 * 1024:
            size_str = f"{total_size / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{total_size / (1024 * 1024 * 1024):.2f} GB"
        
        return {
            'total': total,
            'epub_count': epub_count,
            'txt_count': txt_count,
            'total_size': size_str
        }
    
    def get_novel_by_path(self, path):
        for novel in self.novels:
            if novel.path == path:
                return novel
        return None
