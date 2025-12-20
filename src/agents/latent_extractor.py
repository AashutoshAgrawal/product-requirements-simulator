"""
Latent Need Extractor Module

This module analyzes interview responses to extract and classify
latent user needs according to structured criteria.
"""

from typing import List, Dict, Any
import os

from ..llm.gemini_client import GeminiClient
from ..utils.logger import get_logger
from ..utils.json_parser import safe_parse_json

logger = get_logger(__name__)


class LatentNeedExtractor:
    """
    Extracts and classifies latent needs from interview responses.
    
    This class analyzes user responses to identify underlying needs,
    categorize them, and suggest design implications.
    
    Attributes:
        llm_client (GeminiClient): The LLM client for analysis
        prompt_template (str): Template for need extraction prompts
    """
    
    def __init__(self, llm_client: GeminiClient):
        """
        Initialize the latent need extractor.
        
        Args:
            llm_client: An initialized Gemini client instance
        """
        self.llm_client = llm_client
        self.prompt_template = self._load_prompt_template()
        logger.info("LatentNeedExtractor initialized")
    
    def _load_prompt_template(self) -> str:
        """
        Load the latent need extraction prompt template from file.
        
        Returns:
            The prompt template as a string
        """
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..", "llm", "prompts", "latent_classifier.txt"
        )
        
        with open(template_path, "r") as f:
            return f.read()
    
    def extract_needs(
        self,
        agent: str,
        question: str,
        answer: str
    ) -> Dict[str, Any]:
        """
        Extract latent needs from a single Q&A pair.
        
        Args:
            agent: The agent description/persona
            question: The interview question
            answer: The agent's answer
            
        Returns:
            Dictionary containing extracted needs and metadata
        """
        logger.debug("Extracting latent needs from response")
        
        prompt = self.prompt_template.format(
            agent_description=agent,
            question=question,
            answer=answer
        )
        
        response = self.llm_client.run(prompt)
        
        # Parse JSON response
        needs_data = safe_parse_json(response)
        
        if needs_data and "needs" in needs_data:
            logger.debug(f"Extracted {len(needs_data['needs'])} needs")
            return needs_data
        else:
            logger.warning("Failed to parse needs from response")
            return {"needs": [], "raw_response": response}
    
    def extract_from_interview(
        self,
        interview_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract needs from a complete interview.
        
        Args:
            interview_data: Dictionary containing agent, experience, and interview Q&A
            
        Returns:
            Dictionary with agent context and all extracted needs
        """
        logger.info("Extracting needs from full interview")
        
        agent = interview_data["agent"]
        qa_pairs = interview_data["interview"]
        
        all_needs = []
        
        for idx, qa in enumerate(qa_pairs, 1):
            logger.debug(f"Processing Q&A pair {idx}/{len(qa_pairs)}")
            
            needs_result = self.extract_needs(
                agent=agent,
                question=qa["question"],
                answer=qa["answer"]
            )
            
            # Add metadata
            for need in needs_result.get("needs", []):
                need["question"] = qa["question"]
                need["answer"] = qa["answer"]
                all_needs.append(need)
        
        logger.info(f"Extracted {len(all_needs)} total needs from interview")
        
        return {
            "agent_id": interview_data.get("agent_id"),
            "agent": agent,
            "product": interview_data.get("product"),
            "total_needs": len(all_needs),
            "needs": all_needs
        }
    
    def extract_from_multiple_interviews(
        self,
        interviews: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extract needs from multiple interviews.
        
        Args:
            interviews: List of interview data dictionaries
            
        Returns:
            List of need extraction results
        """
        logger.info(f"Extracting needs from {len(interviews)} interviews")
        
        results = []
        
        for idx, interview in enumerate(interviews, 1):
            logger.debug(f"Processing interview {idx}/{len(interviews)}")
            
            needs_result = self.extract_from_interview(interview)
            results.append(needs_result)
        
        logger.info(f"Completed need extraction for {len(results)} interviews")
        return results
    
    def aggregate_needs(
        self,
        extraction_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Aggregate needs across all agents and categorize.
        
        Args:
            extraction_results: List of need extraction results
            
        Returns:
            Aggregated analysis with categorization and priorities
        """
        logger.info("Aggregating needs across all agents")
        
        all_needs = []
        for result in extraction_results:
            all_needs.extend(result.get("needs", []))
        
        # Categorize needs
        categories = {}
        priorities = {"High": [], "Medium": [], "Low": []}
        
        for need in all_needs:
            category = need.get("category", "Unknown")
            priority = need.get("priority", "Medium")
            
            if category not in categories:
                categories[category] = []
            categories[category].append(need)
            
            if priority in priorities:
                priorities[priority].append(need)
        
        logger.info(f"Aggregated {len(all_needs)} total needs across {len(categories)} categories")
        
        return {
            "total_needs": len(all_needs),
            "total_agents": len(extraction_results),
            "categories": categories,
            "priorities": priorities,
            "all_needs": all_needs,
            "summary": {
                "by_category": {cat: len(needs) for cat, needs in categories.items()},
                "by_priority": {pri: len(needs) for pri, needs in priorities.items()}
            }
        }
