import os
import json
from datetime import datetime
from typing import Dict, Optional
import logging

class SessionManager:
    """Manages session directories and historical data"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.sessions_dir = os.path.join(data_dir, 'sessions')
        self.current_session_id = None
        self.current_session_path = None
        self.logger = logging.getLogger(__name__)
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            os.makedirs(self.sessions_dir, exist_ok=True)
            self.logger.info(f"SessionManager initialized with data_dir: {self.data_dir}")
        except Exception as e:
            self.logger.error(f"Failed to create directories: {e}")
        
    def create_session(self) -> str:
        """Create a new session directory"""
        self.current_session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.current_session_path = os.path.join(self.sessions_dir, self.current_session_id)
        
        # Create directories if they don't exist
        os.makedirs(self.current_session_path, exist_ok=True)
        os.makedirs(self.sessions_dir, exist_ok=True)
        
        self.logger.info(f"Created session: {self.current_session_id}")
        return self.current_session_id
        
    def get_session_path(self, filename: str) -> str:
        """Get full path for a file in current session"""
        if not self.current_session_path:
            raise ValueError("No active session")
        return os.path.join(self.current_session_path, filename)
        
    def save_session_metadata(self, metadata: Dict) -> None:
        """Save session metadata"""
        if not self.current_session_path:
            return
            
        metadata_path = self.get_session_path('metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
            
    def list_sessions(self) -> list:
        """List all available sessions"""
        if not os.path.exists(self.sessions_dir):
            return []
        return sorted(os.listdir(self.sessions_dir), reverse=True)