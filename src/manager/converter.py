import os
from ebooklib import epub
from bs4 import BeautifulSoup
from manager.epub_parser import EPUBParser

class Converter:
    def __init__(self):
        self.epub_parser = EPUBParser()
    
    def epub_to_txt(self, epub_path, output_dir=None):
        if output_dir is None:
            output_dir = os.path.dirname(epub_path)
        
        text = self.epub_parser.extract_text(epub_path)
        if not text:
            return None
        
        base_name = os.path.splitext(os.path.basename(epub_path))[0]
        txt_path = os.path.join(output_dir, f"{base_name}.txt")
        
        try:
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return txt_path
        except Exception as e:
            print(f"Error writing TXT file: {e}")
            return None
    
    def txt_to_epub(self, txt_path, output_dir=None, title=None, author=None):
        if output_dir is None:
            output_dir = os.path.dirname(txt_path)
        
        base_name = os.path.splitext(os.path.basename(txt_path))[0]
        epub_path = os.path.join(output_dir, f"{base_name}.epub")
        
        try:
            try:
                with open(txt_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(txt_path, 'r', encoding='gbk', errors='ignore') as f:
                    content = f.read()
            
            book = epub.EpubBook()
            
            if not title:
                title = base_name
            if not author:
                author = '未知作者'
            
            book.set_title(title)
            book.set_language('zh')
            book.add_author(author)
            
            chapters = self._split_into_chapters(content)
            
            spine = ['nav']
            toc = []
            
            for i, chapter in enumerate(chapters):
                chapter_id = f'chapter_{i+1}'
                chapter_title = chapter['title'] if chapter['title'] else f'第{i+1}章'
                
                c = epub.EpubHtml(title=chapter_title, file_name=f'{chapter_id}.xhtml', lang='zh')
                c.content = f'<html><head></head><body><h1>{chapter_title}</h1><p>{chapter["content"]}</p></body></html>'
                
                book.add_item(c)
                spine.append(chapter_id)
                toc.append(epub.Link(f'{chapter_id}.xhtml', chapter_title, chapter_id))
            
            book.toc = toc
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())
            book.spine = spine
            
            epub.write_epub(epub_path, book)
            return epub_path
        
        except Exception as e:
            print(f"Error creating EPUB: {e}")
            return None
    
    def _split_into_chapters(self, content):
        chapters = []
        lines = content.split('\n')
        current_chapter = {'title': None, 'content': ''}
        
        for line in lines:
            if line.startswith('第') and ('章' in line or '节' in line):
                if current_chapter['content'].strip():
                    chapters.append(current_chapter)
                current_chapter = {'title': line.strip(), 'content': ''}
            else:
                current_chapter['content'] += line + '\n'
        
        if current_chapter['content'].strip():
            chapters.append(current_chapter)
        
        if not chapters:
            chapters.append({'title': None, 'content': content})
        
        return chapters
    
    def batch_convert(self, novel_list, target_format, output_dir=None, progress_callback=None):
        results = {'success': [], 'failed': []}
        total = len(novel_list)
        
        for i, novel in enumerate(novel_list):
            try:
                if novel.format == 'EPUB' and target_format == 'TXT':
                    result = self.epub_to_txt(novel.path, output_dir)
                elif novel.format == 'TXT' and target_format == 'EPUB':
                    result = self.txt_to_epub(novel.path, output_dir, novel.title, novel.author)
                else:
                    results['failed'].append((novel.filename, '格式不匹配'))
                    continue
                
                if result:
                    results['success'].append(result)
                else:
                    results['failed'].append((novel.filename, '转换失败'))
            
            except Exception as e:
                results['failed'].append((novel.filename, str(e)))
            
            if progress_callback:
                progress_callback(i + 1, total)
        
        return results
