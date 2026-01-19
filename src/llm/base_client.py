"""
Base LLM Client Interface

This module provides an abstract base class for LLM clients.
All LLM providers (Gemini, OpenAI, etc.) should implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseLLMClient(ABC):
    """
    Abstract base class for LLM clients.
    
    All LLM provider implementations should inherit from this class
    and implement the required methods.
    """
    
    @abstractmethod
    def run(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None
    ) -> str:
        """
        Execute a prompt using the LLM API.
        
        Args:
            prompt: The text prompt to send to the model
            temperature: Optional override for the default temperature
            max_output_tokens: Optional maximum number of tokens to generate
            
        Returns:
            The generated text response from the model
            
        Raises:
            Exception: If all retry attempts fail
        """
        pass
    
    @abstractmethod
    def run_with_config(
        self,
        prompt: str,
        config: Dict[str, Any]
    ) -> str:
        """
        Execute a prompt with a custom configuration dictionary.
        
        Args:
            prompt: The text prompt to send to the model
            config: Dictionary containing generation parameters
            
        Returns:
            The generated text response from the model
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model configuration.
        
        Returns:
            Dictionary containing model configuration details
        """
        pass
