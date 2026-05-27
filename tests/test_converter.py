import unittest
import sys
import os
import html

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from manager.converter import Converter


class TestConverter(unittest.TestCase):
    def setUp(self):
        self.converter = Converter()
    
    def test_split_into_chapters_basic(self):
        content = """第一章 测试标题
这是第一章的内容。
第二行内容。

第二章 测试标题2
这是第二章的内容。"""
        
        chapters = self.converter._split_into_chapters(content)
        
        self.assertEqual(len(chapters), 2)
        self.assertEqual(chapters[0]['title'], '第一章 测试标题')
        self.assertIn('这是第一章的内容', chapters[0]['content'])
        self.assertEqual(chapters[1]['title'], '第二章 测试标题2')
        self.assertIn('这是第二章的内容', chapters[1]['content'])
    
    def test_split_into_chapters_with_leading_spaces(self):
        content = """  第一章 带空格标题
这是内容。
   第二章 多个空格
这是第二章节内容。"""
        
        chapters = self.converter._split_into_chapters(content)
        
        self.assertEqual(len(chapters), 2)
        self.assertEqual(chapters[0]['title'], '第一章 带空格标题')
        self.assertEqual(chapters[1]['title'], '第二章 多个空格')
    
    def test_split_into_chapters_no_chapters(self):
        content = """这是一段没有章节标题的内容。
第二行内容。"""
        
        chapters = self.converter._split_into_chapters(content)
        
        self.assertEqual(len(chapters), 1)
        self.assertIsNone(chapters[0]['title'])
        self.assertIn('这是一段没有章节标题的内容', chapters[0]['content'])
    
    def test_html_escape_special_characters(self):
        content = """第一章 测试
内容包含 <特殊> 字符 & 符号"""
        
        chapters = self.converter._split_into_chapters(content)
        formatted_content = html.escape(chapters[0]['content']).replace('\n', '<br/>')
        
        self.assertIn('&lt;特殊&gt;', formatted_content)
        self.assertIn('&amp;', formatted_content)
        self.assertNotIn('<特殊>', formatted_content)
        self.assertNotIn('& ', formatted_content)
    
    def test_newline_conversion(self):
        content = """第一章 测试
第一行
第二行
第三行"""
        
        chapters = self.converter._split_into_chapters(content)
        formatted_content = html.escape(chapters[0]['content']).replace('\n', '<br/>')
        
        self.assertIn('<br/>', formatted_content)
        self.assertNotIn('\n', formatted_content)
    
    def test_mixed_format_content(self):
        content = """第一章 混合格式
普通文本。
第二行文本。
   前导空格行
第二章 结尾
最后内容。"""
        
        chapters = self.converter._split_into_chapters(content)
        
        self.assertEqual(len(chapters), 2)
        self.assertEqual(chapters[0]['title'], '第一章 混合格式')
        self.assertEqual(chapters[1]['title'], '第二章 结尾')


class TestChapterSplittingEdgeCases(unittest.TestCase):
    def setUp(self):
        self.converter = Converter()
    
    def test_chapter_with_both_章节_keywords(self):
        content = """第一章 测试章节
内容
第二节 另一个测试
内容"""
        
        chapters = self.converter._split_into_chapters(content)
        
        self.assertEqual(len(chapters), 2)
        self.assertEqual(chapters[0]['title'], '第一章 测试章节')
        self.assertEqual(chapters[1]['title'], '第二节 另一个测试')
    
    def test_empty_content(self):
        chapters = self.converter._split_into_chapters("")
        
        self.assertEqual(len(chapters), 1)
        self.assertEqual(chapters[0]['content'], '')
    
    def test_only_chapter_title_no_content(self):
        content = """第一章 标题
        
        这里是实际内容"""
        
        chapters = self.converter._split_into_chapters(content)
        
        self.assertEqual(len(chapters), 1)
        self.assertEqual(chapters[0]['title'], '第一章 标题')
        self.assertIn('这里是实际内容', chapters[0]['content'])


if __name__ == '__main__':
    unittest.main()
