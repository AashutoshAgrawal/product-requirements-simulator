"""
Unit tests for Agent modules

Run with: pytest tests/test_agents.py -v
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.llm.gemini_client import GeminiClient
from src.agents.generator import AgentGenerator
from src.agents.simulator import ExperienceSimulator
from src.agents.interviewer import Interviewer
from src.agents.latent_extractor import LatentNeedExtractor


class TestAgentGenerator:
    """Test suite for AgentGenerator class."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create a mock LLM client."""
        mock_client = Mock(spec=GeminiClient)
        mock_client.run.return_value = "Name: Test Agent\nDescription: Test description"
        return mock_client
    
    @pytest.fixture
    def generator(self, mock_llm_client):
        """Create an AgentGenerator instance."""
        with patch('builtins.open', create=True):
            with patch('os.path.join', return_value='dummy_path'):
                gen = AgentGenerator(mock_llm_client)
                gen.prompt_template = "Test template {design_context} {context_block}"
                return gen
    
    def test_generate_agents(self, generator, mock_llm_client):
        """Test generating multiple agents."""
        agents = generator.generate_agents(n_agents=3, design_context="test product")
        
        assert len(agents) == 3
        assert mock_llm_client.run.call_count == 3
    
    def test_generate_agents_structured(self, generator):
        """Test structured agent generation."""
        structured = generator.generate_agents_structured(n_agents=2, design_context="tent")
        
        assert len(structured) == 2
        assert all('id' in agent for agent in structured)
        assert all('description' in agent for agent in structured)
        assert all('design_context' in agent for agent in structured)
    
    def test_regenerate_agent(self, generator, mock_llm_client):
        """Test regenerating a single agent."""
        existing = ["Agent 1", "Agent 2"]
        new_agent = generator.regenerate_agent("tent", existing)
        
        assert new_agent is not None
        mock_llm_client.run.assert_called_once()


class TestExperienceSimulator:
    """Test suite for ExperienceSimulator class."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create a mock LLM client."""
        mock_client = Mock(spec=GeminiClient)
        mock_client.run.return_value = "Step 1: Action...\nStep 2: Action...\nStep 3: Action..."
        return mock_client
    
    @pytest.fixture
    def simulator(self, mock_llm_client):
        """Create an ExperienceSimulator instance."""
        with patch('builtins.open', create=True):
            with patch('os.path.join', return_value='dummy_path'):
                sim = ExperienceSimulator(mock_llm_client)
                sim.prompt_template = "Simulate {agent_description} with {product}"
                return sim
    
    def test_simulate_experience(self, simulator, mock_llm_client):
        """Test single experience simulation."""
        agent = "Test Agent Description"
        experience = simulator.simulate_experience(agent, "tent")
        
        assert experience is not None
        mock_llm_client.run.assert_called_once()
    
    def test_simulate_multiple_experiences(self, simulator):
        """Test multiple experience simulations."""
        agents = ["Agent 1", "Agent 2", "Agent 3"]
        results = simulator.simulate_multiple_experiences(agents, "tent")
        
        assert len(results) == 3
        assert all('agent_id' in r for r in results)
        assert all('experience' in r for r in results)


class TestInterviewer:
    """Test suite for Interviewer class."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create a mock LLM client."""
        mock_client = Mock(spec=GeminiClient)
        mock_client.run.return_value = "This is a test answer."
        return mock_client
    
    @pytest.fixture
    def interviewer(self, mock_llm_client):
        """Create an Interviewer instance."""
        questions = ["Q1?", "Q2?", "Q3?"]
        with patch('builtins.open', create=True):
            with patch('os.path.join', return_value='dummy_path'):
                inter = Interviewer(mock_llm_client, questions)
                inter.prompt_template = "Ask {question} about {product}"
                return inter
    
    def test_set_questions(self, interviewer):
        """Test setting interview questions."""
        new_questions = ["New Q1?", "New Q2?"]
        interviewer.set_questions(new_questions)
        
        assert interviewer.questions == new_questions
    
    def test_ask_question(self, interviewer, mock_llm_client):
        """Test asking a single question."""
        answer = interviewer.ask_question(
            agent="Test Agent",
            experience="Test Experience",
            question="Test Question?",
            product="tent"
        )
        
        assert answer is not None
        mock_llm_client.run.assert_called_once()
    
    def test_conduct_interview(self, interviewer, mock_llm_client):
        """Test conducting full interview."""
        qa_pairs = interviewer.conduct_interview(
            agent="Test Agent",
            experience="Test Experience",
            product="tent"
        )
        
        assert len(qa_pairs) == 3  # 3 questions
        assert all('question' in qa for qa in qa_pairs)
        assert all('answer' in qa for qa in qa_pairs)


class TestLatentNeedExtractor:
    """Test suite for LatentNeedExtractor class."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create a mock LLM client."""
        mock_client = Mock(spec=GeminiClient)
        mock_client.run.return_value = '''```json
{
  "needs": [
    {
      "category": "Functional",
      "need_statement": "User needs better access",
      "evidence": "It was hard to open",
      "priority": "High",
      "design_implication": "Add handle"
    }
  ]
}
```'''
        return mock_client
    
    @pytest.fixture
    def extractor(self, mock_llm_client):
        """Create a LatentNeedExtractor instance."""
        with patch('builtins.open', create=True):
            with patch('os.path.join', return_value='dummy_path'):
                ext = LatentNeedExtractor(mock_llm_client)
                ext.prompt_template = "Extract needs from {question} {answer}"
                return ext
    
    def test_extract_needs(self, extractor, mock_llm_client):
        """Test extracting needs from single Q&A."""
        result = extractor.extract_needs(
            agent="Test Agent",
            question="What was challenging?",
            answer="It was hard to open the tent."
        )
        
        assert 'needs' in result
        assert len(result['needs']) > 0
        mock_llm_client.run.assert_called_once()
    
    def test_extract_from_interview(self, extractor):
        """Test extracting needs from full interview."""
        interview_data = {
            'agent': 'Test Agent',
            'interview': [
                {'question': 'Q1?', 'answer': 'A1'},
                {'question': 'Q2?', 'answer': 'A2'}
            ],
            'product': 'tent'
        }
        
        result = extractor.extract_from_interview(interview_data)
        
        assert 'needs' in result
        assert 'agent' in result
        assert 'total_needs' in result
    
    def test_aggregate_needs(self, extractor):
        """Test aggregating needs across agents."""
        extraction_results = [
            {
                'needs': [
                    {'category': 'Functional', 'priority': 'High'},
                    {'category': 'Usability', 'priority': 'Medium'}
                ]
            },
            {
                'needs': [
                    {'category': 'Functional', 'priority': 'Low'},
                    {'category': 'Safety', 'priority': 'High'}
                ]
            }
        ]
        
        aggregated = extractor.aggregate_needs(extraction_results)
        
        assert aggregated['total_needs'] == 4
        assert 'categories' in aggregated
        assert 'priorities' in aggregated
        assert 'summary' in aggregated


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
