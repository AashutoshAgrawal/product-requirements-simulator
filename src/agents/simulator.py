"""
Experience Simulator Module

This module simulates user experiences with products based on agent personas.
"""

from typing import List, Dict, Any, Optional
import os

from ..llm.gemini_client import GeminiClient
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ExperienceSimulator:
    """
    Simulates user experiences based on agent personas.
    
    This class generates step-by-step interaction scenarios including
    actions, observations, and challenges for each agent.
    
    Attributes:
        llm_client (GeminiClient): The LLM client for simulation
        prompt_template (str): Template for experience simulation prompts
    """
    
    def __init__(self, llm_client: GeminiClient):
        """
        Initialize the experience simulator.
        
        Args:
            llm_client: An initialized Gemini client instance
        """
        self.llm_client = llm_client
        self.prompt_template = self._load_prompt_template()
        logger.info("ExperienceSimulator initialized")
    
    def _load_prompt_template(self) -> str:
        """
        Load the experience simulation prompt template from file.
        
        Returns:
            The prompt template as a string
        """
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..", "llm", "prompts", "experience_simulation.txt"
        )
        
        with open(template_path, "r") as f:
            return f.read()
    
    def simulate_experience(
        self,
        agent: str,
        product: str = "tent",
        agent_id: Optional[int] = None
    ) -> str:
        """
        Simulate a single agent's experience with a product.
        
        Args:
            agent: The agent description/persona
            product: The product being interacted with
            agent_id: Optional agent ID for analytics tracking
            
        Returns:
            A detailed experience narrative with steps
        """
        logger.debug(f"Simulating experience for agent with product: {product}")
        
        prompt = self.prompt_template.format(
            agent_description=agent,
            product=product
        )
        
        experience = self.llm_client.run(prompt, _stage="experience_simulation", _agent_id=str(agent_id) if agent_id is not None else None)
        logger.debug("Experience simulation completed")
        
        return experience
    
    def simulate_multiple_experiences(
        self,
        agents: List[str],
        product: str = "tent"
    ) -> List[Dict[str, Any]]:
        """
        Simulate experiences for multiple agents.
        
        Args:
            agents: List of agent descriptions
            product: The product being interacted with
            
        Returns:
            List of dictionaries containing agent and experience data
        """
        logger.info(f"Simulating experiences for {len(agents)} agents")
        
        results = []
        
        for idx, agent in enumerate(agents, 1):
            logger.debug(f"Processing agent {idx}/{len(agents)}")
            
            experience = self.simulate_experience(agent, product, agent_id=idx)
            
            results.append({
                "agent_id": idx,
                "agent": agent,
                "product": product,
                "experience": experience
            })
        
        logger.info(f"Completed {len(results)} experience simulations")
        return results
    
    def simulate_experience_with_context(
        self,
        agent: str,
        product: str,
        additional_context: str = ""
    ) -> str:
        """
        Simulate experience with additional contextual constraints.
        
        Args:
            agent: The agent description/persona
            product: The product being interacted with
            additional_context: Extra context or constraints to consider
            
        Returns:
            A detailed experience narrative
        """
        logger.debug("Simulating experience with additional context")
        
        agent_with_context = f"{agent}\n\nAdditional Context: {additional_context}"
        
        return self.simulate_experience(agent_with_context, product)
