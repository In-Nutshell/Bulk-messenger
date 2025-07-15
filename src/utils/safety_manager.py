import logging


class SafetyManager:
    """Manages safety limits and rate limiting"""
    
    def __init__(self, daily_limit: int = 50, min_delay: float = 5.0):
        self.daily_limit = daily_limit
        self.min_delay = min_delay
        self.logger = logging.getLogger(__name__)
        
    def check_daily_limits(self, planned_messages: int) -> bool:
        """Check if planned messages exceed safe daily limits"""
        if planned_messages > self.daily_limit:
            self.logger.warning(f"Planned messages ({planned_messages}) exceed daily limit ({self.daily_limit})")
            return False
        return True
        
    def get_safe_delay(self, requested_delay: float) -> float:
        """Get safe delay between messages"""
        return max(requested_delay, self.min_delay)
        
    def limit_contacts(self, contacts: list) -> list:
        """Limit contacts to daily limit"""
        if len(contacts) > self.daily_limit:
            self.logger.warning(f"Limiting to {self.daily_limit} contacts for safety")
            return contacts[:self.daily_limit]
        return contacts