"""
Agent Generator Module

This module handles the generation of diverse user agents/personas
for requirements elicitation studies.
"""

from typing import List, Dict, Any
import os

from ..llm.gemini_client import GeminiClient
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AgentGenerator:
    """
    Generates diverse user agents for product research.
    
    This class creates user personas by iteratively prompting the LLM
    while maintaining context to ensure diversity across generated agents.
    
    Attributes:
        llm_client (GeminiClient): The LLM client for generation
        prompt_template (str): Template for agent generation prompts
    """
    
    def __init__(self, llm_client: GeminiClient):
        """
        Initialize the agent generator.
        
        Args:
            llm_client: An initialized Gemini client instance
        """
        self.llm_client = llm_client
        self.prompt_template = self._load_prompt_template()
        logger.info("AgentGenerator initialized")
    
    def _load_prompt_template(self) -> str:
        """
        Load the agent generation prompt template from file.
        
        Returns:
            The prompt template as a string
        """
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..", "llm", "prompts", "agent_generation.txt"
        )
        
        with open(template_path, "r") as f:
            return f.read()
    
    def generate_agents(
        self,
        n_agents: int = 5,
        design_context: str = "camping tent"
    ) -> List[str]:
        """
        Generate multiple diverse user agents.
        
        This method uses serial generation with context accumulation
        to ensure diversity across generated agents.
        
        Args:
            n_agents: Number of agents to generate
            design_context: The product or context for agent generation
            
        Returns:
            List of agent descriptions as strings
        """
        logger.info(f"Generating {n_agents} agents for context: {design_context}")
        
        agents = []
        context_block = "None yet - this is the first agent."
        
        for i in range(n_agents):
            logger.debug(f"Generating agent {i + 1}/{n_agents}")
            
            prompt = self.prompt_template.format(
                design_context=design_context,
                context_block=context_block
            )
            
            agent_text = self.llm_client.run(prompt, _stage="agent_generation", _agent_id=str(i + 1))
            agents.append(agent_text)
            
            # Update context for next iteration
            context_block += f"\n\n---\n\n{agent_text}"
            
            logger.debug(f"Agent {i + 1} generated successfully")
        
        logger.info(f"Successfully generated {len(agents)} agents")
        return agents
    
    def generate_agents_structured(
        self,
        n_agents: int = 5,
        design_context: str = "camping tent"
    ) -> List[Dict[str, Any]]:
        """
        Generate agents and return them as structured dictionaries.
        
        Args:
            n_agents: Number of agents to generate
            design_context: The product or context for agent generation
            
        Returns:
            List of dictionaries containing agent information
        """
        agents_text = self.generate_agents(n_agents, design_context)
        
        structured_agents = []
        for idx, agent_text in enumerate(agents_text, 1):
            structured_agents.append({
                "id": idx,
                "description": agent_text,
                "design_context": design_context
            })
        
        return structured_agents
    
    def regenerate_agent(
        self,
        design_context: str,
        existing_agents: List[str]
    ) -> str:
        """
        Generate a single new agent given existing agents for context.
        
        Args:
            design_context: The product or context for agent generation
            existing_agents: List of already-generated agent descriptions
            
        Returns:
            A new agent description
        """
        logger.info("Regenerating single agent")
        
        context_block = "\n\n---\n\n".join(existing_agents) if existing_agents else "None yet."
        
        prompt = self.prompt_template.format(
            design_context=design_context,
            context_block=context_block
        )
        
        agent_text = self.llm_client.run(prompt, _stage="agent_generation", _agent_id="regeneration")
        logger.info("Agent regenerated successfully")
        
        return agent_text
