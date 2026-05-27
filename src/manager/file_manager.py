import os
from src.model.novel import Novel

class FileManager:
    def __init__(self):
        self.epub_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'EPUB')
        self.txt_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'Novel txt')
        self.novels = []
    
    def scan_directory(self, dir_path, ext):
        novels = []
        if not os.path.exists(dir_path):
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
        else:
            size_str = f"{total_size / (1024 * 1024):.2f} MB"
        
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
