"""
JSON Parser Utility Module

This module provides safe JSON parsing with fallback mechanisms
for handling malformed or incomplete JSON responses from LLMs.
"""

import json
import re
from typing import Any, Optional, Dict

from .logger import get_logger

logger = get_logger(__name__)


def safe_parse_json(
    text: str,
    default: Optional[Any] = None
) -> Optional[Dict[str, Any]]:
    """
    Safely parse JSON from text, with fallback mechanisms.
    
    This function handles common issues with LLM-generated JSON:
    - Markdown code blocks wrapping JSON
    - Extra whitespace or text before/after JSON
    - Malformed JSON structures
    
    Args:
        text: Text that may contain JSON
        default: Default value to return if parsing fails
        
    Returns:
        Parsed JSON as dictionary, or default value if parsing fails
    """
    if not text or not isinstance(text, str):
        logger.warning("Empty or invalid text provided for JSON parsing")
        return default
    
    # Try direct parsing first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try extracting JSON from markdown code blocks
    json_text = extract_json_from_markdown(text)
    if json_text:
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            pass
    
    # Try finding JSON object in text
    json_text = extract_json_object(text)
    if json_text:
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            pass
    
    # Try fixing common JSON issues
    fixed_text = fix_common_json_issues(text)
    if fixed_text:
        try:
            return json.loads(fixed_text)
        except json.JSONDecodeError:
            pass
    
    logger.warning("Failed to parse JSON from text after all attempts")
    logger.debug(f"Text that failed to parse: {text[:200]}...")
    
    return default


def extract_json_from_markdown(text: str) -> Optional[str]:
    """
    Extract JSON from markdown code blocks.
    
    Args:
        text: Text that may contain markdown-wrapped JSON
        
    Returns:
        Extracted JSON string or None
    """
    # Pattern for ```json ... ``` or ``` ... ```
    patterns = [
        r'```json\s*\n(.*?)\n```',
        r'```\s*\n(.*?)\n```',
        r'```json\s*(.*?)```',
        r'```\s*(.*?)```'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
    
    return None


def extract_json_object(text: str) -> Optional[str]:
    """
    Extract the first JSON object or array from text.
    
    Args:
        text: Text that may contain JSON
        
    Returns:
        Extracted JSON string or None
    """
    # Try to find JSON object
    obj_match = re.search(r'\{.*\}', text, re.DOTALL)
    if obj_match:
        return obj_match.group(0)
    
    # Try to find JSON array
    arr_match = re.search(r'\[.*\]', text, re.DOTALL)
    if arr_match:
        return arr_match.group(0)
    
    return None


def fix_common_json_issues(text: str) -> Optional[str]:
    """
    Attempt to fix common JSON formatting issues.
    
    Args:
        text: Potentially malformed JSON string
        
    Returns:
        Fixed JSON string or None
    """
    if not text:
        return None
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove trailing commas before closing braces/brackets
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    
    # Fix single quotes to double quotes (risky but sometimes needed)
    # Only do this if there are no double quotes in the string
    if '"' not in text and "'" in text:
        text = text.replace("'", '"')
    
    return text


def parse_json_list(
    text: str,
    item_pattern: str = r'\{.*?\}',
    default: Optional[list] = None
) -> list:
    """
    Parse a list of JSON objects from text.
    
    Useful when LLM returns multiple JSON objects separated by text.
    
    Args:
        text: Text containing multiple JSON objects
        item_pattern: Regex pattern to match individual items
        default: Default value if no items found
        
    Returns:
        List of parsed JSON objects
    """
    if default is None:
        default = []
    
    if not text:
        return default
    
    items = []
    matches = re.finditer(item_pattern, text, re.DOTALL)
    
    for match in matches:
        try:
            obj = json.loads(match.group(0))
            items.append(obj)
        except json.JSONDecodeError:
            continue
    
    return items if items else default


def validate_json_structure(
    data: Dict[str, Any],
    required_keys: list,
    strict: bool = False
) -> bool:
    """
    Validate that a JSON object has required keys.
    
    Args:
        data: JSON data to validate
        required_keys: List of required key names
        strict: If True, no extra keys allowed
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(data, dict):
        return False
    
    # Check for required keys
    for key in required_keys:
        if key not in data:
            logger.warning(f"Missing required key: {key}")
            return False
    
    # Check for extra keys in strict mode
    if strict:
        extra_keys = set(data.keys()) - set(required_keys)
        if extra_keys:
            logger.warning(f"Extra keys found in strict mode: {extra_keys}")
            return False
    
    return True


def safe_json_dumps(
    obj: Any,
    indent: int = 2,
    default: str = "{}"
) -> str:
    """
    Safely serialize object to JSON string.
    
    Args:
        obj: Object to serialize
        indent: Indentation level
        default: Default string if serialization fails
        
    Returns:
        JSON string
    """
    try:
        return json.dumps(obj, indent=indent, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        logger.warning(f"Failed to serialize object to JSON: {e}")
        return default
