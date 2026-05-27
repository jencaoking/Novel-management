import os
from ebooklib import epub
from bs4 import BeautifulSoup

class EPUBParser:
    def __init__(self):
        pass
    
    def parse_metadata(self, epub_path):
        try:
            book = epub.read_epub(epub_path)
            metadata = {
                'title': book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else '',
                'author': book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else '',
                'language': book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else '',
                'description': book.get_metadata('DC', 'description')[0][0] if book.get_metadata('DC', 'description') else ''
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
                    content = soup.get_text(strip=False)
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
                    text += soup.get_text() + '\n\n'
        except Exception as e:
            print(f"Error extracting text: {e}")
        return text.strip()
