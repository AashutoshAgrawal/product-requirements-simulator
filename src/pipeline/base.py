"""
Base Pipeline Class

Shared functionality for all pipeline implementations.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path

from ..llm.gemini_client import GeminiClient
from ..agents.generator import AgentGenerator
from ..agents.simulator import ExperienceSimulator
from ..agents.interviewer import Interviewer
from ..agents.latent_extractor import LatentNeedExtractor
from ..utils.logger import get_logger
from ..utils.analytics import AnalyticsCollector

logger = get_logger(__name__)


class BasePipeline:
    """
    Base class for requirements elicitation pipelines.
    
    Provides shared initialization and utility methods for both
    sequential and parallel pipeline implementations.
    """
    
    def __init__(
        self,
        llm_client: GeminiClient,
        interview_questions: Optional[List[str]] = None,
        analytics_collector: Optional[AnalyticsCollector] = None
    ):
        """
        Initialize the base pipeline with all components.
        
        Args:
            llm_client: An initialized LLM client instance
            interview_questions: Optional list of questions for interviews
            analytics_collector: Optional AnalyticsCollector for metrics tracking
        """
        self.llm_client = llm_client
        self.analytics = analytics_collector or AnalyticsCollector()
        
        # Initialize all components (shared by all pipelines)
        self.agent_generator = AgentGenerator(llm_client)
        self.experience_simulator = ExperienceSimulator(llm_client)
        self.interviewer = Interviewer(llm_client, interview_questions)
        self.need_extractor = LatentNeedExtractor(llm_client)
    
    def set_interview_questions(self, questions: List[str]) -> None:
        """
        Set or update interview questions.
        
        Args:
            questions: List of interview question strings
        """
        self.interviewer.set_questions(questions)
        logger.info(f"Pipeline interview questions updated: {len(questions)} questions")
    
    def _create_metadata(
        self,
        start_time: datetime,
        n_agents: int,
        design_context: str,
        product: str,
        mode: str = "sequential"
    ) -> Dict[str, Any]:
        """Create standard metadata for pipeline results."""
        return {
            "start_time": start_time.isoformat(),
            "n_agents": n_agents,
            "design_context": design_context,
            "product": product,
            "pipeline_version": "2.0.0",
            "mode": mode
        }
    
    def _finalize_metadata(
        self,
        metadata: Dict[str, Any],
        end_time: datetime,
        duration: float,
        status: str = "completed"
    ) -> Dict[str, Any]:
        """Finalize metadata with end time and duration."""
        metadata["end_time"] = end_time.isoformat()
        metadata["duration_seconds"] = duration
        metadata["status"] = status
        return metadata
    
    def _flatten_needs(self, need_extractions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flatten needs from multiple extractions into a single list."""
        all_needs = []
        for extraction in need_extractions:
            all_needs.extend(extraction.get("needs", []))
        return all_needs
    
    def _save_results(
        self,
        results: Dict[str, Any],
        results_dir: str = "results",
        filename_prefix: str = "pipeline_results"
    ) -> str:
        """
        Save pipeline results to a JSON file.
        
        Args:
            results: Pipeline results dictionary
            results_dir: Directory to save results
            filename_prefix: Prefix for the filename
            
        Returns:
            Path to the saved file
        """
        path = Path(results_dir)
        path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = path / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to {filepath}")
        return str(filepath)
    
    def _save_intermediate(self, stage_name: str, data: Any) -> None:
        """
        Save intermediate results to a JSON file.
        
        Args:
            stage_name: Name of the pipeline stage
            data: Data to save
        """
        filename = f"intermediate_{stage_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Saved intermediate results to {filename}")
        except Exception as e:
            logger.warning(f"Failed to save intermediate results: {e}")
    
    def get_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of pipeline results.
        
        Args:
            results: Complete pipeline results dictionary
            
        Returns:
            Summary dictionary with key metrics
        """
        return {
            "total_agents": len(results.get("agents", [])),
            "total_experiences": len(results.get("experiences", [])),
            "total_interviews": len(results.get("interviews", [])),
            "total_qa_pairs": sum(
                len(i.get("interview", [])) 
                for i in results.get("interviews", [])
            ),
            "total_needs_extracted": results.get("aggregated_needs", {}).get("total_needs", 0),
            "needs_by_category": results.get("aggregated_needs", {}).get("summary", {}).get("by_category", {}),
            "needs_by_priority": results.get("aggregated_needs", {}).get("summary", {}).get("by_priority", {}),
            "duration_seconds": results.get("metadata", {}).get("duration_seconds", 0)
        }
