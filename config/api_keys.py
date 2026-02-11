"""
API Key Management for Elicitron
Reads keys from environment variables for security.
Backend can start with only OpenAI keys; Google/Gemini keys are optional (only needed if provider is gemini).
"""
import os
import random
from typing import List, Optional


def get_api_key(strategy: str = "round_robin") -> str:
    """
    Return Gemini API key. Only used when provider is gemini.
    Raises if Gemini is used but GOOGLE_API_KEY is not set.
    """
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError(
            "Gemini is not configured. Set GOOGLE_API_KEY in .env to use Gemini, "
            "or use provider: openai in config/settings.yaml with OPENAI_API_KEY in .env."
        )
    return key


def get_api_key_for_agent(agent_id: int) -> str:
    """Return Gemini API key for an agent. Only used when provider is gemini."""
    return get_api_key()


# ==================== OpenAI API Key Manager ====================

class OpenAIKeyManager:
    """Manages OpenAI API keys for load balancing"""
    
    def __init__(self):
        """Initialize OpenAI API key manager and load keys from environment"""
        # Load OpenAI API keys from environment variables
        # Format: 
        # OPENAI_API_KEY_1=key_value
        # OPENAI_API_KEY_1_NAME=Agent-1-OpenAI (optional description)
        self.API_KEYS, self.KEY_NAMES = self._load_openai_keys_from_env()
        
        if not self.API_KEYS:
            print("⚠️  No OpenAI API keys found. OpenAI models will not be available.")
            print("   To use OpenAI, set OPENAI_API_KEY_1, OPENAI_API_KEY_2, etc.")
        else:
            self._current_key_index = 0
            self._key_usage_count = {key: 0 for key in self.API_KEYS}
            
            # Print loaded keys with names
            print(f"✅ Loaded {len(self.API_KEYS)} OpenAI API key(s) from environment")
            for i, (key, name) in enumerate(zip(self.API_KEYS, self.KEY_NAMES), 1):
                print(f"   Key {i}: {name}")
    
    def _load_openai_keys_from_env(self) -> tuple[List[str], List[str]]:
        """
        Load OpenAI API keys and their names from environment variables
        Looks for:
        - OPENAI_API_KEY_1, OPENAI_API_KEY_2, etc. (required)
        - OPENAI_API_KEY_1_NAME, OPENAI_API_KEY_2_NAME, etc. (optional)
        
        Returns:
            Tuple of (keys_list, names_list)
        """
        keys = []
        names = []
        index = 1
        
        # Try to load numbered keys (OPENAI_API_KEY_1, OPENAI_API_KEY_2, ...)
        while True:
            key_name = f"OPENAI_API_KEY_{index}"
            key_value = os.getenv(key_name)
            
            if key_value:
                keys.append(key_value)
                
                # Try to load optional name/description
                name_var = f"OPENAI_API_KEY_{index}_NAME"
                name_value = os.getenv(name_var)
                if name_value:
                    names.append(name_value)
                else:
                    names.append(f"OpenAI API Key {index}")  # Default name
                
                index += 1
            else:
                break
        
        # If no numbered keys, try legacy OPENAI_API_KEY
        if not keys:
            legacy_key = os.getenv("OPENAI_API_KEY")
            if legacy_key:
                keys.append(legacy_key)
                names.append("Legacy OpenAI API Key")
        
        return keys, names
    
    def get_api_key(self, strategy: str = "round_robin") -> str:
        """
        Get an OpenAI API key using specified strategy
        
        Args:
            strategy: 'round_robin', 'random', or 'least_used'
            
        Returns:
            API key string
        """
        if not self.API_KEYS:
            raise ValueError("No OpenAI API keys available")
            
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
        Get OpenAI API key for specific agent (for consistent routing)
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            API key string
        """
        if not self.API_KEYS:
            raise ValueError("No OpenAI API keys available")
            
        # Use modulo to distribute agents evenly across keys
        key_index = agent_id % len(self.API_KEYS)
        key = self.API_KEYS[key_index]
        key_name = self.KEY_NAMES[key_index]
        self._key_usage_count[key] += 1
        
        print(f"🔑 Agent {agent_id} using: {key_name}")
        return key
    
    def has_keys(self) -> bool:
        """Check if any OpenAI API keys are available"""
        return len(self.API_KEYS) > 0


# Global instances for easy import
openai_key_manager = OpenAIKeyManager()


def get_openai_api_key(strategy: str = "round_robin") -> str:
    """
    Convenience function to get OpenAI API key
    
    Usage:
        from config.api_keys import get_openai_api_key
        api_key = get_openai_api_key()  # Round-robin
        api_key = get_openai_api_key("random")  # Random selection
        api_key = get_openai_api_key("least_used")  # Least used key
    """
    return openai_key_manager.get_api_key(strategy)


def get_openai_api_key_for_agent(agent_id: int) -> str:
    """
    Get consistent OpenAI API key for specific agent
    
    Usage:
        from config.api_keys import get_openai_api_key_for_agent
        api_key = get_openai_api_key_for_agent(agent_id=1)
    """
    return openai_key_manager.get_key_for_agent(agent_id)
