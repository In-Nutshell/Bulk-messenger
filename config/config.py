import os
from dotenv import load_dotenv
class Config:
    # API Configuration
    load_dotenv()

    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    
    # Get the directory where config.py is located
    CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
    # Get the project root directory (parent of config folder)
    PROJECT_ROOT = os.path.dirname(CONFIG_DIR)
    
    # Session management
    DATA_DIR = 'data'
    SESSIONS_DIR = os.path.join(DATA_DIR, 'sessions')
    
    # Safety Settings
    SAFE_DAILY_LIMIT = 50
    SAFE_DELAY = 5.0  # seconds between messages
    SAFE_BATCH_SIZE = 1
    
    # File Paths - Now pointing to correct folders
    DATABASE_FILE = os.path.join(PROJECT_ROOT, 'data', 'contacts_database.json')
    CONTACTS_CSV = os.path.join(PROJECT_ROOT, 'data', 'contacts.csv')
    LOG_FILE = os.path.join(PROJECT_ROOT, 'logs', 'telegram_messenger.log')
    REPORT_FILE = os.path.join(PROJECT_ROOT, 'data', 'messaging_report.json')
    SAMPLE_CSV = os.path.join(PROJECT_ROOT, 'data', 'contacts_sample.csv')
    
    # Session
    SESSION_NAME = 'bulk_messenger'
    SESSION_PATH = os.path.join(PROJECT_ROOT, 'sessions', f'{SESSION_NAME}.session')
    if __name__ == "__main__":
        print("File paths:")
        print(f"DATABASE_FILE: {DATABASE_FILE}")
        print(f"CONTACTS_CSV: {CONTACTS_CSV}")
        print(f"LOG_FILE: {LOG_FILE}")
        print(f"REPORT_FILE: {REPORT_FILE}")
        print(f"SAMPLE_CSV: {SAMPLE_CSV}")
        print(f"SESSION_PATH: {SESSION_PATH}")

        print("\nFile existence check:")
        print(f"DATABASE_FILE exists: {os.path.exists(DATABASE_FILE)}")
        print(f"CONTACTS_CSV exists: {os.path.exists(CONTACTS_CSV)}")
        print(f"LOG_FILE exists: {os.path.exists(LOG_FILE)}")
        print(f"REPORT_FILE exists: {os.path.exists(REPORT_FILE)}")
        print(f"SAMPLE_CSV exists: {os.path.exists(SAMPLE_CSV)}")
        print(f"SESSION_PATH exists: {os.path.exists(SESSION_PATH)}")