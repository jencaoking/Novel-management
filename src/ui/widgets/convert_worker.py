from PyQt5.QtCore import QThread, pyqtSignal


class ConvertWorker(QThread):
    progress_updated = pyqtSignal(int, int, str)
    single_finished = pyqtSignal(str, bool, str)
    batch_finished = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, converter, novels, target_format='TXT', output_dir=None):
        super().__init__()
        self.converter = converter
        self.novels = novels
        self.target_format = target_format
        self.output_dir = output_dir
        self._is_running = True
        
    def run(self):
        results = {'success': [], 'failed': []}
        total = len(self.novels)
        
        for i, novel in enumerate(self.novels):
            if not self._is_running:
                break
                
            self.progress_updated.emit(i + 1, total, novel.title)
            
            try:
                if novel.format == 'EPUB' and self.target_format == 'TXT':
                    result = self.converter.epub_to_txt(novel.path, self.output_dir)
                elif novel.format == 'TXT' and self.target_format == 'EPUB':
                    result = self.converter.txt_to_epub(
                        novel.path, self.output_dir, novel.title, novel.author
                    )
                else:
                    results['failed'].append((novel.filename, '格式不匹配'))
                    continue
                
                if result:
                    results['success'].append(result)
                    self.single_finished.emit(result, True, novel.title)
                else:
                    results['failed'].append((novel.filename, '转换失败'))
                    self.single_finished.emit('', False, novel.title)
                    
            except Exception as e:
                error_msg = str(e)
                results['failed'].append((novel.filename, error_msg))
                self.single_finished.emit('', False, novel.title)
        
        self.batch_finished.emit(results)
        
    def stop(self):
        self._is_running = False
