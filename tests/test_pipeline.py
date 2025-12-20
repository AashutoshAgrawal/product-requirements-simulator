"""
Unit tests for the Requirements Elicitation Pipeline

Run with: pytest tests/test_pipeline.py -v
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.llm.gemini_client import GeminiClient
from src.pipeline.pipeline import RequirementsPipeline


class TestRequirementsPipeline:
    """Test suite for RequirementsPipeline class."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create a mock LLM client."""
        mock_client = Mock(spec=GeminiClient)
        mock_client.run.return_value = "Mock response"
        return mock_client
    
    @pytest.fixture
    def pipeline(self, mock_llm_client):
        """Create a pipeline instance with mock client."""
        questions = ["Question 1?", "Question 2?"]
        return RequirementsPipeline(mock_llm_client, questions)
    
    def test_pipeline_initialization(self, mock_llm_client):
        """Test that pipeline initializes correctly."""
        pipeline = RequirementsPipeline(mock_llm_client)
        
        assert pipeline.llm_client == mock_llm_client
        assert pipeline.agent_generator is not None
        assert pipeline.experience_simulator is not None
        assert pipeline.interviewer is not None
        assert pipeline.need_extractor is not None
    
    def test_set_interview_questions(self, pipeline):
        """Test setting interview questions."""
        new_questions = ["New Q1?", "New Q2?", "New Q3?"]
        pipeline.set_interview_questions(new_questions)
        
        assert pipeline.interviewer.questions == new_questions
    
    @patch('src.agents.generator.AgentGenerator.generate_agents')
    def test_pipeline_run_agents_stage(self, mock_generate, pipeline):
        """Test pipeline runs agent generation stage."""
        mock_generate.return_value = ["Agent 1", "Agent 2"]
        
        # Mock other stages to return quickly
        with patch.object(pipeline.experience_simulator, 'simulate_multiple_experiences') as mock_exp, \
             patch.object(pipeline.interviewer, 'conduct_multiple_interviews') as mock_int, \
             patch.object(pipeline.need_extractor, 'extract_from_multiple_interviews') as mock_need, \
             patch.object(pipeline.need_extractor, 'aggregate_needs') as mock_agg:
            
            mock_exp.return_value = []
            mock_int.return_value = []
            mock_need.return_value = []
            mock_agg.return_value = {'total_needs': 0, 'summary': {'by_category': {}, 'by_priority': {}}}
            
            results = pipeline.run(n_agents=2)
            
            assert 'agents' in results
            assert len(results['agents']) == 2
            mock_generate.assert_called_once()
    
    def test_get_summary(self, pipeline):
        """Test summary generation from results."""
        results = {
            'agents': ['A1', 'A2', 'A3'],
            'experiences': [{'id': 1}, {'id': 2}, {'id': 3}],
            'interviews': [
                {'interview': [{'q': '1', 'a': '1'}]},
                {'interview': [{'q': '2', 'a': '2'}, {'q': '3', 'a': '3'}]}
            ],
            'aggregated_needs': {
                'total_needs': 10,
                'summary': {
                    'by_category': {'Functional': 5, 'Usability': 5},
                    'by_priority': {'High': 3, 'Medium': 7}
                }
            },
            'metadata': {
                'duration_seconds': 45.6
            }
        }
        
        summary = pipeline.get_summary(results)
        
        assert summary['total_agents'] == 3
        assert summary['total_experiences'] == 3
        assert summary['total_interviews'] == 2
        assert summary['total_qa_pairs'] == 3
        assert summary['total_needs_extracted'] == 10
        assert summary['duration_seconds'] == 45.6
    
    def test_export_results_json(self, pipeline, tmp_path):
        """Test exporting results to JSON."""
        results = {'test': 'data', 'value': 123}
        output_file = tmp_path / "test_results.json"
        
        exported_path = pipeline.export_results(results, str(output_file))
        
        assert os.path.exists(exported_path)
        
        import json
        with open(exported_path, 'r') as f:
            loaded = json.load(f)
        
        assert loaded == results
    
    def test_export_results_unsupported_format(self, pipeline):
        """Test that unsupported export format raises error."""
        with pytest.raises(ValueError):
            pipeline.export_results({}, format='xml')


class TestPipelineIntegration:
    """Integration tests for full pipeline workflow."""
    
    @pytest.fixture
    def mock_client_with_responses(self):
        """Create mock client with predefined responses."""
        mock_client = Mock(spec=GeminiClient)
        
        responses = {
            'agent': 'Name: Test Agent\nDescription: A test user',
            'experience': 'Step 1:\nAction: Test\nObservation: Observed\nChallenge: None',
            'answer': 'This is a test answer.',
            'needs': '```json\n{"needs": [{"category": "Functional", "need_statement": "Test need", "evidence": "test", "priority": "High", "design_implication": "Test"}]}\n```'
        }
        
        call_count = [0]
        def side_effect(prompt):
            call_count[0] += 1
            if 'generating diverse user agents' in prompt.lower():
                return responses['agent']
            elif 'simulate' in prompt.lower() and 'step' in prompt.lower():
                return responses['experience']
            elif 'interview' in prompt.lower() or 'question' in prompt.lower():
                return responses['answer']
            elif 'latent' in prompt.lower() or 'extract' in prompt.lower():
                return responses['needs']
            return "Generic response"
        
        mock_client.run.side_effect = side_effect
        return mock_client
    
    def test_minimal_pipeline_run(self, mock_client_with_responses):
        """Test a minimal end-to-end pipeline run."""
        questions = ["Test question?"]
        pipeline = RequirementsPipeline(mock_client_with_responses, questions)
        
        results = pipeline.run(n_agents=1, design_context="test product", product="test")
        
        assert 'metadata' in results
        assert 'agents' in results
        assert 'experiences' in results
        assert 'interviews' in results
        assert 'aggregated_needs' in results
        assert results['metadata']['status'] == 'completed'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
