"""
LLM Client Factory

Centralized LLM client initialization to avoid code duplication.
"""

from typing import Dict, Any, Optional
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
    Create an OpenAI LLM client based on configuration.

    Args:
        config: Full application config dictionary
        analytics_collector: Optional analytics collector for tracking
        job_id: Optional job ID for logging

    Returns:
        Initialized OpenAIClient
    """
    llm_config = config.get('llm', {})

    log_prefix = f"Job {job_id}: " if job_id else ""

    client = OpenAIClient(
        model_name=llm_config.get('model_name', 'gpt-4o-mini'),
        temperature=llm_config.get('temperature', 0.7),
        seed=llm_config.get('seed'),
        max_retries=llm_config.get('max_retries', 3),
        retry_delay=llm_config.get('retry_delay', 2),
        rate_limit_delay=llm_config.get('rate_limit_delay', 0.0),
        analytics_collector=analytics_collector
    )
    logger.info(f"{log_prefix}Using OpenAI with model {llm_config.get('model_name', 'gpt-4o-mini')}")

    return client


def get_provider_name(config: Dict[str, Any]) -> str:
    """Get the configured provider name."""
    return "openai"


def get_model_name(config: Dict[str, Any]) -> str:
    """Get the configured model name."""
    llm_config = config.get('llm', {})
    return llm_config.get('model_name', 'gpt-4o-mini')
