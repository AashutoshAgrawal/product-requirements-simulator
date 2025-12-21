"""
API Key Management for Elicitron
Supports multiple API keys for load balancing across agents
"""
import os
import random
from typing import List, Optional

class APIKeyManager:
    """Manages multiple Google Gemini API keys for load balancing"""
    
    # Primary API keys pool - add more keys here for scaling
    API_KEYS = [
        "AIzaSyC1HBVK2XY-gebCyE6N77q6IsklqMRRfxY",  # Primary key
        # Add more keys below as you scale:
        # "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",  # Key 2
        # "AIzaSyYYYYYYYYYYYYYYYYYYYYYYYYYYYYY",  # Key 3
        # "AIzaSyZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ",  # Key 4
    ]
    
    def __init__(self):
        """Initialize API key manager"""
        self._current_key_index = 0
        self._key_usage_count = {key: 0 for key in self.API_KEYS}
        
    def get_api_key(self, strategy: str = "round_robin") -> str:
        """
        Get an API key using specified strategy
        
        Args:
            strategy: 'round_robin', 'random', or 'least_used'
            
        Returns:
            API key string
        """
        if strategy == "round_robin":
            return self._get_round_robin()
        elif strategy == "random":
            return self._get_random()
        elif strategy == "least_used":
            return self._get_least_used()
        else:
            return self._get_round_robin()
    
    def _get_round_robin(self) -> str:
        """Round-robin: cycle through keys sequentially"""
        key = self.API_KEYS[self._current_key_index]
        self._current_key_index = (self._current_key_index + 1) % len(self.API_KEYS)
        self._key_usage_count[key] += 1
        return key
    
    def _get_random(self) -> str:
        """Random: pick a random key from pool"""
        key = random.choice(self.API_KEYS)
        self._key_usage_count[key] += 1
        return key
    
    def _get_least_used(self) -> str:
        """Least used: pick the key with fewest uses"""
        key = min(self._key_usage_count.items(), key=lambda x: x[1])[0]
        self._key_usage_count[key] += 1
        return key
    
    def get_key_for_agent(self, agent_id: int) -> str:
        """
        Get API key for specific agent (for consistent routing)
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            API key string
        """
        # Use modulo to distribute agents evenly across keys
        key_index = agent_id % len(self.API_KEYS)
        key = self.API_KEYS[key_index]
        self._key_usage_count[key] += 1
        return key
    
    def get_all_keys(self) -> List[str]:
        """Get all available API keys"""
        return self.API_KEYS.copy()
    
    def get_key_count(self) -> int:
        """Get number of available API keys"""
        return len(self.API_KEYS)
    
    def get_usage_stats(self) -> dict:
        """Get usage statistics for each key"""
        return self._key_usage_count.copy()
    
    @classmethod
    def get_primary_key(cls) -> str:
        """Get primary API key (for backward compatibility)"""
        return cls.API_KEYS[0]


# Global instance for easy import
api_key_manager = APIKeyManager()


def get_api_key(strategy: str = "round_robin") -> str:
    """
    Convenience function to get API key
    
    Usage:
        from config.api_keys import get_api_key
        api_key = get_api_key()  # Round-robin
        api_key = get_api_key("random")  # Random selection
        api_key = get_api_key("least_used")  # Least used key
    """
    return api_key_manager.get_api_key(strategy)


def get_api_key_for_agent(agent_id: int) -> str:
    """
    Get consistent API key for specific agent
    
    Usage:
        from config.api_keys import get_api_key_for_agent
        api_key = get_api_key_for_agent(agent_id=1)
    """
    return api_key_manager.get_key_for_agent(agent_id)
