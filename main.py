import asyncio
from config.config import Config
from src.utils.logger import setup_logging
from src.core.database import ContactDatabase
from src.core.telegram_client import TelegramClientWrapper
from src.messaging.message_sender import MessageSender
from src.utils.safety_manager import SafetyManager
from src.reporting.reporter import Reporter
from src.utils.ui import main_menu, get_user_confirmation, setup_instructions, create_sample_csv


class TelegramBulkMessenger:
    """Main application class"""
    
    def __init__(self):
        self.config = Config()
        self.logger = setup_logging(self.config.LOG_FILE)
        self.database = ContactDatabase(self.config.DATABASE_FILE)
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
        self.reporter = Reporter(self.config.REPORT_FILE)
        
    async def run_bulk_messaging(self):
        """Run the bulk messaging process"""
        try:
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
            self.reporter.print_summary(
                summary,
                self.message_sender.successful_sends,
                self.message_sender.failed_contacts
            )
            
            # Save database
            self.database.save_to_file()
            print(f"\nDatabase and report saved successfully!")
            
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
            create_sample_csv(messenger.config.SAMPLE_CSV)
        elif choice == '3':
            setup_instructions()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    asyncio.run(main())