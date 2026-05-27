import os
import warnings
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

warnings.filterwarnings('ignore', category=UserWarning, module='ebooklib')
warnings.filterwarnings('ignore', category=FutureWarning)

class EPUBParser:
    def __init__(self):
        pass
    
    def parse_metadata(self, epub_path):
        def safe_get_meta(book, namespace, name):
            data = book.get_metadata(namespace, name)
            if not data:
                return ''
            if isinstance(data, list) and len(data) &gt; 0:
                if isinstance(data[0], tuple):
                    return str(data[0][0])
                return str(data[0])
            return str(data)
        
        try:
            book = epub.read_epub(epub_path)
            metadata = {
                'title': safe_get_meta(book, 'DC', 'title'),
                'author': safe_get_meta(book, 'DC', 'creator'),
                'language': safe_get_meta(book, 'DC', 'language'),
                'description': safe_get_meta(book, 'DC', 'description')
            }
            return metadata
        except Exception as e:
            print(f"Error parsing metadata: {e}")
            return None
    
    def get_chapters(self, epub_path):
        chapters = []
        try:
            book = epub.read_epub(epub_path)
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    title_tag = soup.find(['h1', 'h2', 'h3', 'title'])
                    title = title_tag.get_text(strip=True) if title_tag else '未知章节'
                    content = soup.get_text(separator='\n', strip=False)
                    chapters.append({
                        'title': title,
                        'content': content,
                        'id': item.get_id()
                    })
        except Exception as e:
            print(f"Error extracting chapters: {e}")
        return chapters
    
    def get_cover(self, epub_path):
        try:
            book = epub.read_epub(epub_path)
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_COVER:
                    return item.get_content()
        except Exception as e:
            print(f"Error extracting cover: {e}")
        return None
    
    def extract_text(self, epub_path):
        text = ''
        try:
            book = epub.read_epub(epub_path)
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text += soup.get_text(separator='\n') + '\n\n'
        except Exception as e:
            print(f"Error extracting text: {e}")
        return text.strip()
