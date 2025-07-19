import os
import json
def main_menu() -> str:
    """Display main menu"""
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                        TELEGRAM BULK MESSENGER                              ║
    ╠══════════════════════════════════════════════════════════════════════════════╣
    ║                                                                              ║
    ║ 1. Run bulk messaging                                                       ║
    ║ 2. Create sample CSV file                                                   ║
    ║ 3. View session history                                                     ║
    ║ 4. Show setup instructions                                                  ║
    ║ 5. Exit                                                                     ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    return input("Enter your choice (1-5): ").strip()

def show_session_history(session_manager):
    """Display session history"""
    sessions = session_manager.list_sessions()
    
    if not sessions:
        print("No sessions found.")
        return
        
    print(f"\nFound {len(sessions)} sessions:")
    print("-" * 50)
    
    for i, session_id in enumerate(sessions[:10], 1):  # Show last 10 sessions
        session_path = os.path.join(session_manager.sessions_dir, session_id)
        metadata_path = os.path.join(session_path, 'metadata.json')
        
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            print(f"{i}. {session_id}")
            print(f"   Success: {metadata.get('successful_sends', 'N/A')}")
            print(f"   Failed: {metadata.get('failed_sends', 'N/A')}")
            print(f"   Total: {metadata.get('total_contacts', 'N/A')}")
            print()
            
        except Exception as e:
            print(f"{i}. {session_id} (metadata unavailable)")


def get_user_confirmation(contacts_count: int, delay: float) -> bool:
    """Get user confirmation for messaging"""
    print(f"\nReady to send messages with these settings:")
    print(f"- Recipients: {contacts_count}")
    print(f"- Delay between messages: {delay} seconds")
    print(f"- Processing: One contact at a time")
    print(f"- Estimated time: {(contacts_count * delay) / 60:.1f} minutes")
    
    confirm = input("\nContinue? (y/N): ").lower().strip()
    return confirm == 'y'


def setup_instructions():
    """Print setup instructions"""
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                           SETUP INSTRUCTIONS                                 ║
    ╠══════════════════════════════════════════════════════════════════════════════╣
    ║                                                                              ║
    ║ 1. Install required packages:                                               ║
    ║    pip install telethon                                                     ║
    ║                                                                              ║
    ║ 2. Get Telegram API credentials:                                            ║
    ║    - Go to https://my.telegram.org/apps                                     ║
    ║    - Create new application                                                 ║
    ║    - Get API ID and API Hash                                                ║
    ║                                                                              ║
    ║ 3. Update configuration in config.py                                       ║
    ║                                                                              ║
    ║ 4. Prepare your contacts CSV file (contacts.csv)                           ║
    ║                                                                              ║
    ║ 5. Run the program: python main.py                                         ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)


def create_sample_csv(file_path: str = 'contacts_sample.csv'):
    """Create a sample CSV file"""
    sample_data = """name,username,user_id,phone
John Doe,john_doe,123456789,+1234567890
Alice Smith,alice_smith,,+1987654321
Bob Johnson,,,+1122334455
Carol White,carol_white,987654321,
Mike Brown,,555666777,+1999888777
Sarah Davis,sarah_d,111222333,
"""
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_data)
        print(f"Sample CSV file created: {file_path}")
        print("You can use this as a template for your contacts.")
        return True
    except Exception as e:
        print(f"Error creating sample CSV: {e}")
        return False
