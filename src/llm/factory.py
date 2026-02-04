"""
LLM Client Factory

Centralized LLM client initialization to avoid code duplication.
"""

from typing import Dict, Any, Optional
from ..llm.gemini_client import GeminiClient
from ..llm.openai_client import OpenAIClient
from ..utils.analytics import AnalyticsCollector
from ..utils.logger import get_logger

logger = get_logger(__name__)


def create_llm_client(
    config: Dict[str, Any],
    analytics_collector: Optional[AnalyticsCollector] = None,
    job_id: Optional[str] = None
):
    """
    Create an LLM client based on configuration.
    
    Args:
        config: Full application config dictionary
        analytics_collector: Optional analytics collector for tracking
        job_id: Optional job ID for logging
        
    Returns:
        Initialized LLM client (OpenAIClient or GeminiClient)
        
    Raises:
        ValueError: If provider is not supported
    """
    llm_config = config.get('llm', {})
    provider = llm_config.get('provider', 'gemini').lower()
    
    log_prefix = f"Job {job_id}: " if job_id else ""
    
    if provider == 'openai':
        client = OpenAIClient(
            model_name=llm_config.get('model_name', 'gpt-4o-mini'),
            temperature=llm_config.get('temperature', 0.7),
            max_retries=llm_config.get('max_retries', 3),
            retry_delay=llm_config.get('retry_delay', 2),
            rate_limit_delay=llm_config.get('rate_limit_delay', 0.0),
            analytics_collector=analytics_collector
        )
        logger.info(f"{log_prefix}Using OpenAI with model {llm_config.get('model_name', 'gpt-4o-mini')}")
        
    elif provider == 'gemini':
        client = GeminiClient(
            model_name=llm_config.get('model_name', 'gemini-1.5-flash'),
            temperature=llm_config.get('temperature', 0.7),
            max_retries=llm_config.get('max_retries', 3),
            retry_delay=llm_config.get('retry_delay', 2),
            rate_limit_delay=llm_config.get('rate_limit_delay', 12.0),
            analytics_collector=analytics_collector
        )
        logger.info(f"{log_prefix}Using Gemini with model {llm_config.get('model_name', 'gemini-1.5-flash')}")
        
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Choose 'gemini' or 'openai'")
    
    return client


def get_provider_name(config: Dict[str, Any]) -> str:
    """Get the configured provider name."""
    return config.get('llm', {}).get('provider', 'gemini').lower()


def get_model_name(config: Dict[str, Any]) -> str:
    """Get the configured model name."""
    llm_config = config.get('llm', {})
    provider = llm_config.get('provider', 'gemini').lower()
    
    if provider == 'openai':
        return llm_config.get('model_name', 'gpt-4o-mini')
    else:
        return llm_config.get('model_name', 'gemini-1.5-flash')
