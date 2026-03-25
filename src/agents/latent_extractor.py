"""
Latent Need Extractor Module

This module analyzes interview responses to extract and classify
latent user needs according to structured criteria.
"""

from typing import List, Dict, Any, Optional
import os

import json

from ..llm.openai_client import OpenAIClient
from ..utils.logger import get_logger
from ..utils.json_parser import safe_parse_json

logger = get_logger(__name__)


class LatentNeedExtractor:
    """
    Extracts and classifies latent needs from interview responses.

    This class analyzes user responses to identify underlying needs,
    categorize them, and suggest design implications.

    Attributes:
        llm_client (OpenAIClient): The LLM client for analysis
        prompt_template (str): Template for need extraction prompts
    """

    def __init__(self, llm_client: OpenAIClient):
        """
        Initialize the latent need extractor.

        Args:
            llm_client: An initialized OpenAI client instance
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
        answer: str,
        agent_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Extract latent needs from a single Q&A pair.
        
        Args:
            agent: The agent description/persona
            question: The interview question
            answer: The agent's answer
            agent_id: Optional agent ID for analytics tracking
            
        Returns:
            Dictionary containing extracted needs and metadata
        """
        logger.debug("Extracting latent needs from response")
        
        prompt = self.prompt_template.format(
            agent_description=agent,
            question=question,
            answer=answer
        )
        
        response = self.llm_client.run(prompt, _stage="need_extraction", _agent_id=str(agent_id) if agent_id is not None else None)
        
        # Parse JSON response
        needs_data = safe_parse_json(response)
        
        if needs_data and "needs" in needs_data:
            # Cap at 3 needs per Q&A as safety net
            needs_list = needs_data['needs'][:3]
            # Remove 'evidence' field if present (prompt no longer includes it)
            for need in needs_list:
                need.pop("evidence", None)
            logger.debug(f"Extracted {len(needs_list)} needs (capped at 3)")
            return {"needs": needs_list}
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
        agent_id = interview_data.get("agent_id")
        qa_pairs = interview_data["interview"]
        
        all_needs = []
        
        for idx, qa in enumerate(qa_pairs, 1):
            logger.debug(f"Processing Q&A pair {idx}/{len(qa_pairs)}")
            
            needs_result = self.extract_needs(
                agent=agent,
                question=qa["question"],
                answer=qa["answer"],
                agent_id=agent_id
            )
            
            # Add traceability metadata (agent_id and question_index) but NOT full Q&A text
            for need in needs_result.get("needs", []):
                need["agent_id"] = agent_id
                need["question_index"] = idx - 1  # 0-indexed
                # Remove question/answer/evidence if present
                need.pop("question", None)
                need.pop("answer", None)
                need.pop("evidence", None)
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
        
        # Strip question/answer/evidence from all needs in aggregated output
        cleaned_needs = []
        for need in all_needs:
            cleaned = {k: v for k, v in need.items() if k not in ["question", "answer", "evidence"]}
            cleaned_needs.append(cleaned)
        
        # Clean categories and priorities too
        cleaned_categories = {}
        for cat, needs_list in categories.items():
            cleaned_categories[cat] = [{k: v for k, v in n.items() if k not in ["question", "answer", "evidence"]} for n in needs_list]
        
        cleaned_priorities = {}
        for pri, needs_list in priorities.items():
            cleaned_priorities[pri] = [{k: v for k, v in n.items() if k not in ["question", "answer", "evidence"]} for n in needs_list]
        
        logger.info(f"Aggregated {len(cleaned_needs)} total needs across {len(cleaned_categories)} categories")
        
        return {
            "total_needs": len(cleaned_needs),
            "total_agents": len(extraction_results),
            "categories": cleaned_categories,
            "priorities": cleaned_priorities,
            "all_needs": cleaned_needs,
            "summary": {
                "by_category": {cat: len(needs) for cat, needs in cleaned_categories.items()},
                "by_priority": {pri: len(needs) for pri, needs in cleaned_priorities.items()}
            }
        }
    
    def synthesize_needs(
        self,
        raw_needs: List[Dict[str, Any]],
        product: str
    ) -> List[Dict[str, Any]]:
        """
        Synthesize raw needs into 8-12 unique, deduplicated needs.
        
        Args:
            raw_needs: List of raw need dictionaries (without Q&A text)
            product: Product name for context
            
        Returns:
            List of synthesized needs (count decided by LLM)
        """
        if not raw_needs:
            logger.warning("No raw needs to synthesize")
            return []
        
        logger.info(f"Synthesizing {len(raw_needs)} raw needs")
        
        # Load synthesis prompt template
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..", "llm", "prompts", "need_synthesis.txt"
        )
        
        try:
            with open(template_path, "r") as f:
                synthesis_template = f.read()
        except FileNotFoundError:
            logger.error(f"Synthesis template not found at {template_path}")
            # Fallback: return full list sorted by priority
            sorted_needs = sorted(raw_needs, key=lambda n: {"High": 3, "Medium": 2, "Low": 1}.get(n.get("priority", "Medium"), 1), reverse=True)
            return sorted_needs
        
        # Prepare raw needs JSON (only include core fields)
        clean_needs = []
        for need in raw_needs:
            clean_needs.append({
                "category": need.get("category", "Unknown"),
                "need_statement": need.get("need_statement", ""),
                "priority": need.get("priority", "Medium"),
                "design_implication": need.get("design_implication", "")
            })
        
        raw_needs_json = json.dumps(clean_needs, indent=2)
        
        prompt = synthesis_template.format(
            product=product,
            raw_needs_json=raw_needs_json
        )
        
        response = self.llm_client.run(prompt, _stage="need_synthesis")
        
        # Parse JSON array response
        synthesized = safe_parse_json(response)
        
        if isinstance(synthesized, list):
            logger.info(f"Synthesized to {len(synthesized)} unique needs")
            return synthesized
        elif isinstance(synthesized, dict) and "needs" in synthesized:
            result = synthesized["needs"]
            logger.info(f"Synthesized to {len(result)} unique needs")
            return result
        else:
            logger.warning("Failed to parse synthesis response, falling back to full list by priority")
            sorted_needs = sorted(raw_needs, key=lambda n: {"High": 3, "Medium": 2, "Low": 1}.get(n.get("priority", "Medium"), 1), reverse=True)
            return sorted_needs
