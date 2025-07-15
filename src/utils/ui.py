def main_menu() -> str:
    """Display main menu"""
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                        TELEGRAM BULK MESSENGER                              ║
    ╠══════════════════════════════════════════════════════════════════════════════╣
    ║                                                                              ║
    ║ 1. Run bulk messaging                                                       ║
    ║ 2. Create sample CSV file                                                   ║
    ║ 3. Show setup instructions                                                  ║
    ║ 4. Exit                                                                     ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    return input("Enter your choice (1-4): ").strip()


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
