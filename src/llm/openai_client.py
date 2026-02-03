"""
OpenAI LLM Client Module

This module provides a clean interface to interact with OpenAI's API.
It encapsulates all LLM-specific logic and configuration for OpenAI models.
"""

import time
from typing import Optional, Dict, Any
from openai import OpenAI

from ..utils.logger import get_logger
from config.api_keys import get_openai_api_key
from .base_client import BaseLLMClient

logger = get_logger(__name__)


class OpenAIClient(BaseLLMClient):
    """
    A client for interacting with OpenAI's API.
    
    This class handles API authentication, request management, and response handling
    for OpenAI language models.
    
    Attributes:
        model_name (str): The name of the OpenAI model to use
        temperature (float): Controls randomness in generation (0.0 to 1.0)
        max_retries (int): Maximum number of retry attempts for failed requests
        retry_delay (int): Delay in seconds between retry attempts
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_retries: int = 3,
        retry_delay: int = 2,
        rate_limit_delay: float = 0.0,
        analytics_collector=None
    ):
        """
        Initialize the OpenAI client.
        
        Args:
            model_name: Name of the OpenAI model to use (e.g., gpt-4, gpt-3.5-turbo)
            temperature: Sampling temperature (0.0 to 1.0)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            rate_limit_delay: Delay between requests to avoid rate limits (seconds)
            analytics_collector: Optional AnalyticsCollector instance for tracking metrics
            
        Raises:
            ValueError: If OPENAI_API_KEY is not set in environment
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0
        self.analytics_collector = analytics_collector
        self._call_counter = 0
        
        # Configure API key
        api_key = get_openai_api_key()
        if not api_key:
            raise ValueError(
                "No OpenAI API keys available in config/api_keys.py. "
                "Please set OPENAI_API_KEY_1 or OPENAI_API_KEY in environment."
            )
        
        self.client = OpenAI(api_key=api_key)
        
        logger.info(f"Initialized OpenAIClient with model: {model_name}")
        if rate_limit_delay > 0:
            logger.info(f"Rate limit protection: {rate_limit_delay}s delay between requests")
    
    def run(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
        _stage: str = "unknown",
        _agent_id: Optional[str] = None
    ) -> str:
        """
        Execute a prompt using the OpenAI API.
        
        Args:
            prompt: The text prompt to send to the model
            temperature: Optional override for the default temperature
            max_output_tokens: Optional maximum number of tokens to generate
            _stage: Stage name for analytics tracking (internal use)
            _agent_id: Agent ID for analytics tracking (internal use)
            
        Returns:
            The generated text response from the model
            
        Raises:
            Exception: If all retry attempts fail
        """
        # Rate limit protection: wait if needed
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit_delay and self.last_request_time > 0:
            wait_time = self.rate_limit_delay - time_since_last_request
            logger.debug(f"Rate limit protection: waiting {wait_time:.1f}s before next request")
            time.sleep(wait_time)
        
        # Prepare API parameters
        params = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature if temperature is not None else self.temperature,
        }
        
        if max_output_tokens:
            params["max_tokens"] = max_output_tokens
        
        for attempt in range(self.max_retries):
            try:
                logger.debug(f"Sending request to OpenAI (attempt {attempt + 1}/{self.max_retries})")
                
                start_time = time.time()
                response = self.client.chat.completions.create(**params)
                end_time = time.time()
                
                result = response.choices[0].message.content
                self.last_request_time = end_time  # Update last request time
                logger.debug(f"Successfully received response ({len(result)} characters)")
                
                # Track analytics if collector is available
                if self.analytics_collector:
                    self._call_counter += 1
                    self.analytics_collector.track_api_call(
                        call_id=f"openai_{self._call_counter}",
                        stage=_stage,
                        agent_id=_agent_id,
                        start_time=start_time,
                        end_time=end_time,
                        input_tokens=response.usage.prompt_tokens if hasattr(response, 'usage') else 0,
                        output_tokens=response.usage.completion_tokens if hasattr(response, 'usage') else 0,
                        model=self.model_name,
                        status="success",
                        retry_count=attempt
                    )
                
                return result
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                
                # Track failed attempt
                if self.analytics_collector and attempt == self.max_retries - 1:
                    self._call_counter += 1
                    self.analytics_collector.track_api_call(
                        call_id=f"openai_{self._call_counter}",
                        stage=_stage,
                        agent_id=_agent_id,
                        start_time=time.time(),
                        end_time=time.time(),
                        model=self.model_name,
                        status="error",
                        error=str(e),
                        retry_count=attempt
                    )
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"All {self.max_retries} attempts failed")
                    raise
    
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
        return self.run(
            prompt=prompt,
            temperature=config.get("temperature"),
            max_output_tokens=config.get("max_output_tokens")
        )
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model configuration.
        
        Returns:
            Dictionary containing model configuration details
        """
        return {
            "provider": "openai",
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay,
            "rate_limit_delay": self.rate_limit_delay
        }
