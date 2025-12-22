"""
API Key Management for Elicitron
Supports multiple API keys for load balancing across agents
Reads keys from environment variables for security
"""
import os
import random
from typing import List, Optional

class APIKeyManager:
    """Manages multiple Google Gemini API keys for load balancing"""
    
    def __init__(self):
        """Initialize API key manager and load keys from environment"""
        # Load API keys from environment variables
        # Format: 
        # GOOGLE_API_KEY_1=key_value
        # GOOGLE_API_KEY_1_NAME=Agent-1-TentDesign (optional description)
        self.API_KEYS, self.KEY_NAMES = self._load_api_keys_from_env()
        
        if not self.API_KEYS:
            raise ValueError(
                "No API keys found in environment variables. "
                "Please set GOOGLE_API_KEY_1, GOOGLE_API_KEY_2, etc. "
                "in your Render dashboard or .env file."
            )
        
        self._current_key_index = 0
        self._key_usage_count = {key: 0 for key in self.API_KEYS}
        
        # Print loaded keys with names
        print(f"✅ Loaded {len(self.API_KEYS)} API key(s) from environment")
        for i, (key, name) in enumerate(zip(self.API_KEYS, self.KEY_NAMES), 1):
            print(f"   Key {i}: {name}")
    
    def _load_api_keys_from_env(self) -> tuple[List[str], List[str]]:
        """
        Load API keys and their names from environment variables
        Looks for:
        - GOOGLE_API_KEY_1, GOOGLE_API_KEY_2, etc. (required)
        - GOOGLE_API_KEY_1_NAME, GOOGLE_API_KEY_2_NAME, etc. (optional)
        
        Returns:
            Tuple of (keys_list, names_list)
        """
        keys = []
        names = []
        index = 1
        
        # Try to load numbered keys (GOOGLE_API_KEY_1, GOOGLE_API_KEY_2, ...)
        while True:
            key_name = f"GOOGLE_API_KEY_{index}"
            key_value = os.getenv(key_name)
            
            if key_value:
                keys.append(key_value)
                
                # Try to load optional name/description
                name_var = f"GOOGLE_API_KEY_{index}_NAME"
                name_value = os.getenv(name_var)
                if name_value:
                    names.append(name_value)
                else:
                    names.append(f"API Key {index}")  # Default name
                
                index += 1
            else:
                break
        
        # If no numbered keys, try legacy GOOGLE_API_KEY
        if not keys:
            legacy_key = os.getenv("GOOGLE_API_KEY")
            if legacy_key:
                keys.append(legacy_key)
                names.append("Legacy API Key")
        
        return keys, names
        
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
        key_name = self.KEY_NAMES[key_index]
        self._key_usage_count[key] += 1
        
        print(f"🔑 Agent {agent_id} using: {key_name}")
        return key
    
    def get_key_info(self, key: str) -> str:
        """Get the name/description for a specific key"""
        try:
            index = self.API_KEYS.index(key)
            return self.KEY_NAMES[index]
        except (ValueError, IndexError):
            return "Unknown Key"
    
    def get_all_keys(self) -> List[str]:
        """Get all available API keys"""
        return self.API_KEYS.copy()
    
    def get_all_key_names(self) -> List[str]:
        """Get all key names/descriptions"""
        return self.KEY_NAMES.copy()
    
    def get_key_count(self) -> int:
        """Get number of available API keys"""
        return len(self.API_KEYS)
    
    def get_usage_stats(self) -> dict:
        """Get usage statistics for each key with names"""
        stats = {}
        for key, count in self._key_usage_count.items():
            key_name = self.get_key_info(key)
            stats[key_name] = count
        return stats
    
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
