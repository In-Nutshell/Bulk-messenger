import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from telethon.errors import (
    PhoneNumberBannedError, PhoneNumberInvalidError, 
    UsernameNotOccupiedError, UserPrivacyRestrictedError,
    FloodWaitError, PeerFloodError, UserNotMutualContactError
)
import logging


class MessageSender:
    """Handles message sending with error handling and rate limiting"""
    
    def __init__(self, telegram_client, contact_database):
        self.telegram_client = telegram_client
        self.contact_database = contact_database
        self.successful_sends = []
        self.failed_contacts = []
        self.logger = logging.getLogger(__name__)
        
    def reset_tracking(self) -> None:
        """Reset tracking lists"""
        self.successful_sends = []
        self.failed_contacts = []
        
    async def send_to_single_contact(self, contact_key: str, message: str, 
                                   delay: float = 3.0) -> bool:
        """Send message to a single contact with multiple fallback methods"""
        contact = self.contact_database.get_contact(contact_key) or {}
        
        # Prepare identifiers in priority order
        identifiers = self._get_contact_identifiers(contact, contact_key)
        
        self.logger.info(f"Attempting to send to {contact_key} using {len(identifiers)} identifiers")
        
        # Try each identifier
        for i, identifier in enumerate(identifiers):
            identifier_type = self._get_identifier_type(identifier)
            self.logger.info(f"Attempt {i+1}/{len(identifiers)}: {identifier_type} - {identifier}")
            
            try:
                success = await self._attempt_send(contact_key, identifier, identifier_type, message)
                if success:
                    break
                    
            except FloodWaitError as e:
                if await self._handle_flood_wait(contact_key, identifier, identifier_type, message, e):
                    break
                    
            except (UserPrivacyRestrictedError, UserNotMutualContactError) as e:
                self._handle_privacy_error(contact_key, identifier, identifier_type, e)
                continue
                
            except (PhoneNumberBannedError, PhoneNumberInvalidError) as e:
                self._handle_phone_error(contact_key, identifier, identifier_type, e)
                continue
                
            except Exception as e:
                self.logger.error(f"Error sending via {identifier_type} ({identifier}): {e}")
                continue
        else:
            # All identifiers failed
            self._handle_all_failed(contact_key, identifiers)
            await asyncio.sleep(delay)
            return False
            
        self.logger.info(f"Successfully sent message to {contact_key}")
        await asyncio.sleep(delay)
        return True
        
    def _get_contact_identifiers(self, contact: Dict, contact_key: str) -> List:
        """Get identifiers in priority order"""
        identifiers = []
        
        # Priority 1: User ID (most reliable)
        if contact.get('user_id'):
            identifiers.append(contact['user_id'])
            
        # Priority 2: Username
        if contact.get('username'):
            username = contact['username'].lstrip('@')
            identifiers.append(f"@{username}")
            
        # Priority 3: Phone number
        if contact.get('phone'):
            identifiers.append(contact['phone'])
            
        # Fallback: contact key itself
        if not identifiers:
            identifiers.append(contact_key)
            
        return identifiers
        
    def _get_identifier_type(self, identifier) -> str:
        """Determine identifier type"""
        if isinstance(identifier, int):
            return "user_id"
        elif str(identifier).startswith("@"):
            return "username"
        else:
            return "phone"
            
    async def _attempt_send(self, contact_key: str, identifier, identifier_type: str, message: str) -> bool:
        """Attempt to send message to identifier"""
        user_info = await self.telegram_client.get_user_info(identifier)
        
        if user_info:
            await self.telegram_client.send_message(user_info, message)
            
            self.successful_sends.append({
                'contact_key': contact_key,
                'identifier_used': identifier,
                'identifier_type': identifier_type,
                'user_id': user_info.id,
                'username': user_info.username,
                'timestamp': datetime.now().isoformat()
            })
            
            self.logger.info(f"SUCCESS: Message sent to {contact_key} via {identifier_type}")
            return True
        else:
            self.logger.warning(f"Could not resolve user info for {identifier}")
            return False
            
    async def _handle_flood_wait(self, contact_key: str, identifier, identifier_type: str, 
                               message: str, error: FloodWaitError) -> bool:
        """Handle flood wait error"""
        self.logger.warning(f"Flood wait error: waiting {error.seconds} seconds")
        await asyncio.sleep(error.seconds)
        
        try:
            return await self._attempt_send(contact_key, identifier, identifier_type, message)
        except Exception as e:
            self.logger.error(f"Failed to send after flood wait: {e}")
            return False
            
    def _handle_privacy_error(self, contact_key: str, identifier, identifier_type: str, error):
        """Handle privacy restriction errors"""
        self.logger.warning(f"Privacy restriction for {identifier}: {error}")
        self.failed_contacts.append({
            'contact_key': contact_key,
            'identifier': identifier,
            'identifier_type': identifier_type,
            'error': 'Privacy restricted or not mutual contact',
            'timestamp': datetime.now().isoformat()
        })
        
    def _handle_phone_error(self, contact_key: str, identifier, identifier_type: str, error):
        """Handle phone number errors"""
        self.logger.warning(f"Phone number issue for {identifier}: {error}")
        self.failed_contacts.append({
            'contact_key': contact_key,
            'identifier': identifier,
            'identifier_type': identifier_type,
            'error': f'Phone number error: {str(error)}',
            'timestamp': datetime.now().isoformat()
        })
        
    def _handle_all_failed(self, contact_key: str, identifiers: List):
        """Handle case where all identifiers failed"""
        self.logger.error(f"All {len(identifiers)} identifiers failed for {contact_key}")
        self.failed_contacts.append({
            'contact_key': contact_key,
            'error': f'All {len(identifiers)} identifiers failed',
            'tried_identifiers': [str(id) for id in identifiers],
            'timestamp': datetime.now().isoformat()
        })
        
    async def send_bulk_messages(self, contacts: List[str], message: str, 
                               delay: float = 3.0) -> Dict:
        """Send messages to multiple contacts"""
        self.logger.info(f"Starting bulk message send to {len(contacts)} contacts")
        self.reset_tracking()
        
        for i, contact in enumerate(contacts):
            self.logger.info(f"Processing contact {i+1}/{len(contacts)}: {contact}")
            
            success = await self.send_to_single_contact(contact, message, delay)
            
            if success:
                self.logger.info(f"Successfully sent to {contact}")
            else:
                self.logger.warning(f"Failed to send to {contact}")
                
        # Generate summary
        summary = {
            'total_contacts': len(contacts),
            'successful_sends': len(self.successful_sends),
            'failed_sends': len(self.failed_contacts),
            'success_rate': len(self.successful_sends) / len(contacts) * 100 if contacts else 0
        }
        
        self.logger.info(f"Bulk messaging completed: {summary}")
        return summary