import logging
import sys


class UTFStreamHandler(logging.StreamHandler):
    """Custom stream handler with UTF-8 support"""
    
    def __init__(self, stream=None):
        super().__init__(stream)
        if hasattr(self.stream, 'reconfigure'):
            try:
                self.stream.reconfigure(encoding='utf-8')
            except:
                pass


def setup_logging(log_file: str = 'telegram_messenger.log') -> logging.Logger:
    """Set up logging with UTF-8 support"""
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = UTFStreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler],
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    return logging.getLogger(__name__)