import json
import csv
from datetime import datetime
from typing import Dict, Optional
import logging


class ContactDatabase:
    """Manages contact storage and retrieval"""
    
    def __init__(self, file_path: str = 'contacts_database.json'):
        self.file_path = file_path
        self.contacts = {}
        self.logger = logging.getLogger(__name__)
        
    def load_from_file(self) -> None:
        """Load contacts from JSON file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.contacts = json.load(f)
            self.logger.info(f"Database loaded: {len(self.contacts)} contacts")
        except FileNotFoundError:
            self.logger.warning("Database file not found, starting empty")
            self.contacts = {}
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON in database file")
            self.contacts = {}
            
    def save_to_file(self) -> None:
        """Save contacts to JSON file"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.contacts, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Database saved: {len(self.contacts)} contacts")
        except Exception as e:
            self.logger.error(f"Error saving database: {e}")
            
    def add_contact(self, phone: str = None, username: str = None, 
                   user_id: int = None, first_name: str = None, 
                   last_name: str = None) -> str:
        """Add or update contact in database"""
        # Use user_id as primary key if available
        key = str(user_id) if user_id else phone or username
        
        if key not in self.contacts:
            self.contacts[key] = {}
            
        contact = self.contacts[key]
        
        if phone:
            contact['phone'] = phone
        if username:
            contact['username'] = username.lstrip('@')
        if user_id:
            contact['user_id'] = user_id
        if first_name:
            contact['first_name'] = first_name
        if last_name:
            contact['last_name'] = last_name
            
        contact['last_updated'] = datetime.now().isoformat()
        return key
        
    def get_contact(self, key: str) -> Optional[Dict]:
        """Get contact by key"""
        return self.contacts.get(key)
        
    def get_all_contacts(self) -> Dict:
        """Get all contacts"""
        return self.contacts
        
    def get_contact_keys(self) -> list:
        """Get all contact keys"""
        return list(self.contacts.keys())
        
    def load_from_csv(self, csv_file: str) -> Dict:
        
        """Load contacts from CSV file"""
        contacts = {}
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Use user_id as primary key if available
                    key = row.get('user_id') if row.get('user_id') and row.get('user_id').strip() else (
                        row.get('phone') or f"@{row.get('username')}"
                    )
                    
                    if key:
                        full_name = row.get('name', '').strip()
                        name_parts = full_name.split() if full_name else []
                        
                        contact_data = {
                            'first_name': name_parts[0] if name_parts else '',
                            'last_name': ' '.join(name_parts[1:]) if len(name_parts) > 1 else '',
                            'username': row.get('username', '').strip(),
                            'user_id': int(row.get('user_id')) if row.get('user_id') and row.get('user_id').strip() else None,
                            'phone': row.get('phone', '').strip()
                        }
                        
                        # Remove empty values
                        contact_data = {k: v for k, v in contact_data.items() if v}
                        contacts[key] = contact_data
                        
                        # Also add to main database
                        self.add_contact(**contact_data)
                        
        except Exception as e:
            self.logger.error(f"Error loading CSV: {e}")
            
        return contacts