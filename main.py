import asyncio
from datetime import datetime
from config.config import Config
from src.utils.logger import setup_logging
from src.core.database import ContactDatabase
from src.core.telegram_client import TelegramClientWrapper
from src.messaging.message_sender import MessageSender
from src.utils.safety_manager import SafetyManager
from src.reporting.reporter import Reporter
from src.utils.session_manager import SessionManager
print("SessionManager imported successfully") 
from src.utils.ui import main_menu, get_user_confirmation, setup_instructions, create_sample_csv, show_session_history


class TelegramBulkMessenger:
    """Main application class"""
    
    def __init__(self):
        self.config = Config()
        self.logger = setup_logging(self.config.LOG_FILE)
        try:
            self.session_manager = SessionManager()
            print(f"SessionManager initialized: {self.session_manager}")
        except Exception as e:
            print(f"Failed to initialize SessionManager: {e}")
            self.session_manager = None
        self.database = ContactDatabase(self.config.DATABASE_FILE, self.session_manager)
        self.telegram_client = TelegramClientWrapper(
            self.config.API_ID, 
            self.config.API_HASH, 
            self.config.SESSION_NAME
        )
        self.message_sender = MessageSender(self.telegram_client, self.database)
        self.safety_manager = SafetyManager(
            self.config.SAFE_DAILY_LIMIT, 
            self.config.SAFE_DELAY
        )
        self.reporter = Reporter(self.config.REPORT_FILE, self.session_manager)
        
    async def run_bulk_messaging(self):
        """Run the bulk messaging process"""
        try:
            session_id = self.session_manager.create_session()
            self.logger.info(f"Starting new session: {session_id}")
            # Start Telegram client
            await self.telegram_client.start()
            
            # Load contacts
            self.database.load_from_csv(self.config.CONTACTS_CSV)
            all_contacts = self.database.get_contact_keys()
            
            if not all_contacts:
                print("No contacts found. Please check your CSV file.")
                return
                
            print(f"Loaded {len(all_contacts)} contacts from database")
            
            # Apply safety limits
            safe_contacts = self.safety_manager.limit_contacts(all_contacts)
            safe_delay = self.safety_manager.get_safe_delay(self.config.SAFE_DELAY)
            
            # Get user confirmation
            if not get_user_confirmation(len(safe_contacts), safe_delay):
                print("Operation cancelled by user")
                return
                
            # Send messages
            message = "Hello! This is a test message from the bulk messenger."
            print("\nStarting bulk messaging...")
            
            summary = await self.message_sender.send_bulk_messages(
                safe_contacts, message, safe_delay
            )
            
            # Generate and save report
            report = self.reporter.generate_report(
                self.message_sender.successful_sends,
                self.message_sender.failed_contacts
            )
            
            # Print summary
            
            metadata = {
                'session_id': session_id,
                'start_time': datetime.now().isoformat(),
                'total_contacts': len(all_contacts),
                'processed_contacts': len(safe_contacts),
                'successful_sends': len(self.message_sender.successful_sends),
                'failed_sends': len(self.message_sender.failed_contacts),
                'message': message,
                'delay_used': safe_delay
            }
            self.session_manager.save_session_metadata(metadata)
            
            self.reporter.print_summary(
                summary,
                self.message_sender.successful_sends,
                self.message_sender.failed_contacts
            )
            # Save database
            self.database.save_to_file()
            print(f"\nDatabase and report saved successfully!")
            print(f"Session ID: {session_id}")
        except Exception as e:
            self.logger.error(f"Error in bulk messaging: {e}")
            print(f"Error: {e}")
            
        finally:
            await self.telegram_client.stop()


async def main():
    """Main function"""
    messenger = TelegramBulkMessenger()
    
    # Check if API credentials are configured
    if not messenger.config.API_ID or not messenger.config.API_HASH:
        print("Please configure your API credentials in config.py first!")
        setup_instructions()
        return
        
    while True:
        choice = main_menu()
        
        if choice == '1':
            await messenger.run_bulk_messaging()
            break
        elif choice == '2':
            create_sample_csv(messenger.config.SAMPLE_CSV if hasattr(messenger.config, 'SAMPLE_CSV') else 'contacts_sample.csv')
        elif choice == '3':  # NEW: View session history
            show_session_history(messenger.session_manager)
        elif choice == '4':  # UPDATED: Setup instructions
            setup_instructions()
        elif choice == '5':  # UPDATED: Exit
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    asyncio.run(main())