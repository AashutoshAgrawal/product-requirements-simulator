"""
Requirements Elicitation Pipeline

This module orchestrates the end-to-end workflow for requirements elicitation:
1. Agent generation
2. Experience simulation
3. Interview conduction
4. Latent need extraction
"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime

from ..llm.gemini_client import GeminiClient
from ..agents.generator import AgentGenerator
from ..agents.simulator import ExperienceSimulator
from ..agents.interviewer import Interviewer
from ..agents.latent_extractor import LatentNeedExtractor
from ..utils.logger import get_logger

logger = get_logger(__name__)


class RequirementsPipeline:
    """
    Orchestrates the complete requirements elicitation pipeline.
    
    This class manages the workflow from agent generation through need extraction,
    coordinating all components and maintaining state throughout the process.
    
    Attributes:
        llm_client (GeminiClient): The LLM client used by all components
        agent_generator (AgentGenerator): Component for generating user agents
        experience_simulator (ExperienceSimulator): Component for simulating experiences
        interviewer (Interviewer): Component for conducting interviews
        need_extractor (LatentNeedExtractor): Component for extracting needs
    """
    
    def __init__(
        self,
        llm_client: GeminiClient,
        interview_questions: Optional[List[str]] = None
    ):
        """
        Initialize the requirements pipeline.
        
        Args:
            llm_client: An initialized Gemini client instance
            interview_questions: Optional list of questions for interviews
        """
        self.llm_client = llm_client
        
        # Initialize all components
        self.agent_generator = AgentGenerator(llm_client)
        self.experience_simulator = ExperienceSimulator(llm_client)
        self.interviewer = Interviewer(llm_client, interview_questions)
        self.need_extractor = LatentNeedExtractor(llm_client)
        
        logger.info("RequirementsPipeline initialized with all components")
    
    def set_interview_questions(self, questions: List[str]) -> None:
        """
        Set or update interview questions.
        
        Args:
            questions: List of interview question strings
        """
        self.interviewer.set_questions(questions)
        logger.info(f"Pipeline interview questions updated: {len(questions)} questions")
    
    def run(
        self,
        n_agents: int = 5,
        design_context: str = "camping tent",
        product: str = "tent",
        save_intermediate: bool = False
    ) -> Dict[str, Any]:
        """
        Run the complete requirements elicitation pipeline.
        
        This method executes all stages in sequence and returns comprehensive results.
        
        Args:
            n_agents: Number of user agents to generate
            design_context: Context for agent generation
            product: Product being studied
            save_intermediate: Whether to save intermediate results
            
        Returns:
            Dictionary containing all pipeline results and metadata
        """
        logger.info("="*60)
        logger.info("Starting Requirements Elicitation Pipeline")
        logger.info(f"Configuration: {n_agents} agents, context='{design_context}', product='{product}'")
        logger.info("="*60)
        
        start_time = datetime.now()
        results = {
            "metadata": {
                "start_time": start_time.isoformat(),
                "n_agents": n_agents,
                "design_context": design_context,
                "product": product,
                "pipeline_version": "1.0.0"
            }
        }
        
        # Stage 1: Generate Agents
        logger.info("\n[STAGE 1/4] Generating User Agents...")
        agents = self.agent_generator.generate_agents(n_agents, design_context)
        results["agents"] = agents
        logger.info(f"✓ Generated {len(agents)} agents")
        
        if save_intermediate:
            self._save_intermediate("agents", agents)
        
        # Stage 2: Simulate Experiences
        logger.info("\n[STAGE 2/4] Simulating User Experiences...")
        experiences = self.experience_simulator.simulate_multiple_experiences(agents, product)
        results["experiences"] = experiences
        logger.info(f"✓ Simulated {len(experiences)} experiences")
        
        if save_intermediate:
            self._save_intermediate("experiences", experiences)
        
        # Stage 3: Conduct Interviews
        logger.info("\n[STAGE 3/4] Conducting Interviews...")
        interviews = self.interviewer.conduct_multiple_interviews(experiences)
        results["interviews"] = interviews
        total_qa = sum(len(i["interview"]) for i in interviews)
        logger.info(f"✓ Completed {len(interviews)} interviews ({total_qa} Q&A pairs)")
        
        if save_intermediate:
            self._save_intermediate("interviews", interviews)
        
        # Stage 4: Extract Latent Needs
        logger.info("\n[STAGE 4/4] Extracting Latent Needs...")
        need_extractions = self.need_extractor.extract_from_multiple_interviews(interviews)
        results["need_extractions"] = need_extractions
        
        # Aggregate needs
        aggregated_needs = self.need_extractor.aggregate_needs(need_extractions)
        results["aggregated_needs"] = aggregated_needs
        
        logger.info(f"✓ Extracted {aggregated_needs['total_needs']} total needs")
        logger.info(f"  - Categories: {list(aggregated_needs['summary']['by_category'].keys())}")
        logger.info(f"  - High Priority: {aggregated_needs['summary']['by_priority'].get('High', 0)}")
        
        if save_intermediate:
            self._save_intermediate("need_extractions", need_extractions)
            self._save_intermediate("aggregated_needs", aggregated_needs)
        
        # Finalize metadata
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        results["metadata"]["end_time"] = end_time.isoformat()
        results["metadata"]["duration_seconds"] = duration
        results["metadata"]["status"] = "completed"
        
        logger.info("="*60)
        logger.info(f"Pipeline Completed Successfully in {duration:.2f}s")
        logger.info("="*60)
        
        return results
    
    def run_partial(
        self,
        start_stage: str = "agents",
        end_stage: str = "needs",
        input_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run a partial pipeline starting from a specific stage.
        
        Args:
            start_stage: Starting stage (agents, experiences, interviews, needs)
            end_stage: Ending stage (agents, experiences, interviews, needs)
            input_data: Input data for the starting stage
            **kwargs: Additional configuration parameters
            
        Returns:
            Dictionary containing results from executed stages
        """
        logger.info(f"Running partial pipeline: {start_stage} → {end_stage}")
        
        stages = ["agents", "experiences", "interviews", "needs"]
        if start_stage not in stages or end_stage not in stages:
            raise ValueError(f"Invalid stage. Must be one of: {stages}")
        
        start_idx = stages.index(start_stage)
        end_idx = stages.index(end_stage)
        
        if start_idx > end_idx:
            raise ValueError("start_stage must come before end_stage")
        
        # Execute stages
        results = {}
        current_data = input_data
        
        for stage in stages[start_idx:end_idx+1]:
            if stage == "agents":
                agents = self.agent_generator.generate_agents(
                    kwargs.get("n_agents", 5),
                    kwargs.get("design_context", "camping tent")
                )
                results["agents"] = agents
                current_data = agents
                
            elif stage == "experiences":
                experiences = self.experience_simulator.simulate_multiple_experiences(
                    current_data,
                    kwargs.get("product", "tent")
                )
                results["experiences"] = experiences
                current_data = experiences
                
            elif stage == "interviews":
                interviews = self.interviewer.conduct_multiple_interviews(current_data)
                results["interviews"] = interviews
                current_data = interviews
                
            elif stage == "needs":
                need_extractions = self.need_extractor.extract_from_multiple_interviews(current_data)
                aggregated = self.need_extractor.aggregate_needs(need_extractions)
                results["need_extractions"] = need_extractions
                results["aggregated_needs"] = aggregated
        
        logger.info(f"Partial pipeline completed: {start_stage} → {end_stage}")
        return results
    
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
        summary = {
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
        
        return summary
    
    def export_results(
        self,
        results: Dict[str, Any],
        filename: Optional[str] = None,
        format: str = "json"
    ) -> str:
        """
        Export pipeline results to a file.
        
        Args:
            results: Pipeline results to export
            filename: Optional custom filename
            format: Export format (currently only 'json' supported)
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"pipeline_results_{timestamp}.json"
        
        if format == "json":
            with open(filename, "w") as f:
                json.dump(results, f, indent=2)
            logger.info(f"Results exported to {filename}")
            return filename
        else:
            raise ValueError(f"Unsupported export format: {format}")
