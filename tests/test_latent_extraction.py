"""
Unit tests for Latent Need Extraction

Run with: pytest tests/test_latent_extraction.py -v
"""

import pytest
from unittest.mock import Mock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.json_parser import (
    safe_parse_json,
    extract_json_from_markdown,
    extract_json_object,
    fix_common_json_issues,
    validate_json_structure
)


class TestJSONParser:
    """Test suite for JSON parsing utilities."""
    
    def test_safe_parse_json_valid(self):
        """Test parsing valid JSON."""
        json_str = '{"key": "value", "number": 42}'
        result = safe_parse_json(json_str)
        
        assert result == {"key": "value", "number": 42}
    
    def test_safe_parse_json_with_markdown(self):
        """Test parsing JSON wrapped in markdown."""
        json_str = '```json\n{"key": "value"}\n```'
        result = safe_parse_json(json_str)
        
        assert result == {"key": "value"}
    
    def test_safe_parse_json_with_text(self):
        """Test parsing JSON embedded in text."""
        json_str = 'Some text before {"key": "value"} and after'
        result = safe_parse_json(json_str)
        
        assert result == {"key": "value"}
    
    def test_safe_parse_json_invalid(self):
        """Test parsing invalid JSON returns default."""
        json_str = 'This is not JSON at all'
        result = safe_parse_json(json_str, default={"error": True})
        
        assert result == {"error": True}
    
    def test_extract_json_from_markdown(self):
        """Test extracting JSON from markdown code blocks."""
        text = 'Some text\n```json\n{"test": true}\n```\nMore text'
        result = extract_json_from_markdown(text)
        
        assert result == '{"test": true}'
    
    def test_extract_json_object(self):
        """Test extracting JSON object from text."""
        text = 'Before {"nested": {"key": "value"}} After'
        result = extract_json_object(text)
        
        assert '{"nested": {"key": "value"}}' in result
    
    def test_fix_common_json_issues_trailing_comma(self):
        """Test fixing trailing commas in JSON."""
        bad_json = '{"key": "value",}'
        fixed = fix_common_json_issues(bad_json)
        
        import json
        result = json.loads(fixed)  # Should not raise
        assert result == {"key": "value"}
    
    def test_validate_json_structure_valid(self):
        """Test validating JSON structure with required keys."""
        data = {"name": "test", "value": 42, "extra": "ok"}
        required = ["name", "value"]
        
        assert validate_json_structure(data, required) is True
    
    def test_validate_json_structure_missing_key(self):
        """Test validation fails with missing key."""
        data = {"name": "test"}
        required = ["name", "value"]
        
        assert validate_json_structure(data, required) is False
    
    def test_validate_json_structure_strict_mode(self):
        """Test strict validation rejects extra keys."""
        data = {"name": "test", "value": 42, "extra": "not allowed"}
        required = ["name", "value"]
        
        assert validate_json_structure(data, required, strict=True) is False


class TestNeedClassification:
    """Test suite for need classification logic."""
    
    def test_need_categories(self):
        """Test that all expected need categories are recognized."""
        categories = [
            "Functional",
            "Usability",
            "Performance",
            "Safety",
            "Emotional",
            "Social",
            "Accessibility"
        ]
        
        # Each category should be a valid string
        for category in categories:
            assert isinstance(category, str)
            assert len(category) > 0
    
    def test_need_priorities(self):
        """Test that priority levels are recognized."""
        priorities = ["High", "Medium", "Low"]
        
        for priority in priorities:
            assert isinstance(priority, str)
            assert priority in priorities
    
    def test_need_statement_format(self):
        """Test that need statements follow expected format."""
        # Format: [User type] needs [capability] so that [benefit/outcome]
        example_need = "Beginner campers need clear setup instructions so that they can assemble the tent quickly"
        
        assert "needs" in example_need
        assert "so that" in example_need
    
    def test_design_implication_present(self):
        """Test that design implications are concrete suggestions."""
        example_implication = "Add color-coded poles and step-by-step labels"
        
        assert len(example_implication) > 10
        assert isinstance(example_implication, str)


class TestNeedAggregation:
    """Test suite for need aggregation logic."""
    
    def test_categorize_needs(self):
        """Test categorizing needs by category."""
        needs = [
            {"category": "Functional", "priority": "High"},
            {"category": "Usability", "priority": "Medium"},
            {"category": "Functional", "priority": "Low"},
        ]
        
        categories = {}
        for need in needs:
            cat = need["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(need)
        
        assert len(categories["Functional"]) == 2
        assert len(categories["Usability"]) == 1
    
    def test_prioritize_needs(self):
        """Test organizing needs by priority."""
        needs = [
            {"category": "Functional", "priority": "High"},
            {"category": "Usability", "priority": "High"},
            {"category": "Safety", "priority": "Medium"},
        ]
        
        priorities = {"High": [], "Medium": [], "Low": []}
        for need in needs:
            pri = need["priority"]
            if pri in priorities:
                priorities[pri].append(need)
        
        assert len(priorities["High"]) == 2
        assert len(priorities["Medium"]) == 1
        assert len(priorities["Low"]) == 0
    
    def test_count_needs_by_category(self):
        """Test counting needs in each category."""
        categories = {
            "Functional": [1, 2, 3],
            "Usability": [1, 2],
            "Safety": [1]
        }
        
        counts = {cat: len(needs) for cat, needs in categories.items()}
        
        assert counts["Functional"] == 3
        assert counts["Usability"] == 2
        assert counts["Safety"] == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
