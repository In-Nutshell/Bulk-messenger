import asyncio
import os
from typing import Optional, Union
from telethon import TelegramClient
from telethon.errors import (
    PhoneNumberBannedError, PhoneNumberInvalidError, 
    UsernameNotOccupiedError, UserPrivacyRestrictedError,
    FloodWaitError, PeerFloodError, UserNotMutualContactError
)
from telethon.tl.types import User
import logging


class TelegramClientWrapper:
    """Wrapper for Telegram client with enhanced user management"""
    
    def __init__(self, api_id: str, api_hash: str, session_name: str = 'bulk_messenger'):
        session_path = os.path.join('sessions', session_name)
        
        # Make sure the sessions directory exists
        os.makedirs('sessions', exist_ok=True)
        
        self.client = TelegramClient(session_path, api_id, api_hash)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"Using session path: {session_path}.session")
        
    async def start(self) -> None:
        """Initialize the Telegram client"""
        await self.client.start()
        self.logger.info("Telegram client started successfully")
        
    async def stop(self) -> None:
        """Disconnect the Telegram client"""
        await self.client.disconnect()
        self.logger.info("Telegram client disconnected")
        
    async def get_user_info(self, identifier: Union[str, int]) -> Optional[User]:
        """Get user information from Telegram"""
        try:
            user = await self.client.get_entity(identifier)
            
            if isinstance(user, User):
                return user
                
        except (PhoneNumberInvalidError, UsernameNotOccupiedError, ValueError) as e:
            self.logger.warning(f"Could not find user {identifier}: {e}")
        except Exception as e:
            self.logger.error(f"Error getting user info for {identifier}: {e}")
            
        return None
        
    async def send_message(self, user: User, message: str) -> None:
        """Send message to user"""
        await self.client.send_message(user, message)