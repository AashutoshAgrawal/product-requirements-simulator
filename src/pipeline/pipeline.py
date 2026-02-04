"""
Sequential Requirements Elicitation Pipeline

This module orchestrates the end-to-end workflow for requirements elicitation:
1. Agent generation
2. Experience simulation
3. Interview conduction
4. Latent need extraction
"""

import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base import BasePipeline
from ..utils.logger import get_logger

logger = get_logger(__name__)


class RequirementsPipeline(BasePipeline):
    """
    Orchestrates the complete requirements elicitation pipeline (sequential mode).
    
    Inherits from BasePipeline for shared component initialization.
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize the sequential pipeline."""
        super().__init__(*args, **kwargs)
        logger.info("RequirementsPipeline initialized with all components")
    
    def run(
        self,
        n_agents: int = 5,
        design_context: str = "camping tent",
        product: str = "tent",
        save_intermediate: bool = False,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Run the complete requirements elicitation pipeline.
        
        This method executes all stages in sequence and returns comprehensive results.
        
        Args:
            n_agents: Number of user agents to generate
            design_context: Context for agent generation
            product: Product being studied
            save_intermediate: Whether to save intermediate results
            progress_callback: Optional callback for stage progress updates
            
        Returns:
            Dictionary containing all pipeline results and metadata
        """
        logger.info("="*60)
        logger.info("Starting Requirements Elicitation Pipeline")
        logger.info(f"Configuration: {n_agents} agents, context='{design_context}', product='{product}'")
        logger.info("="*60)
        
        start_time = datetime.now()
        import time
        start_timestamp = time.time()
        
        # Helper to report progress
        def report_progress(stage: str, stage_name: str, current_agent: int = None, message: str = None):
            if progress_callback:
                progress_callback({
                    "stage": stage,
                    "stage_name": stage_name,
                    "current_agent": current_agent,
                    "total_agents": n_agents,
                    "message": message or f"{stage_name}..."
                })
        
        # Start analytics tracking
        self.analytics.start_tracking()
        self.analytics.log_activity("info", f"Pipeline initialized - Product: {product}", {
            "n_agents": n_agents,
            "design_context": design_context
        })
        
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
        report_progress("agent_generation", "Generating Agents", message=f"Generating {n_agents} user personas...")
        stage_start = time.time()
        self.analytics.log_activity("stage_start", "Starting agent generation stage", {"n_agents": n_agents})
        
        agents = self.agent_generator.generate_agents(n_agents, design_context)
        results["agents"] = agents
        
        stage_end = time.time()
        self.analytics.track_stage("agent_generation", stage_start, stage_end, len(agents))
        logger.info(f"✓ Generated {len(agents)} agents")
        
        if save_intermediate:
            self._save_intermediate("agents", agents)
        
        # Stage 2: Simulate Experiences
        logger.info("\n[STAGE 2/4] Simulating User Experiences...")
        stage_start = time.time()
        self.analytics.log_activity("stage_start", "Starting experience simulation stage", {})
        
        experiences = []
        for idx, agent in enumerate(agents, 1):
            report_progress("experience_simulation", "Simulating Experiences", 
                          current_agent=idx, message=f"Simulating experience for Agent {idx}/{n_agents}...")
            exp = self.experience_simulator.simulate_experience(agent, product)
            experiences.append(exp)
        results["experiences"] = experiences
        
        stage_end = time.time()
        self.analytics.track_stage("experience_simulation", stage_start, stage_end, len(experiences))
        logger.info(f"✓ Simulated {len(experiences)} experiences")
        
        if save_intermediate:
            self._save_intermediate("experiences", experiences)
        
        # Stage 3: Conduct Interviews
        logger.info("\n[STAGE 3/4] Conducting Interviews...")
        stage_start = time.time()
        self.analytics.log_activity("stage_start", "Starting interview stage", {})
        
        interviews = []
        for idx, exp_data in enumerate(experiences, 1):
            report_progress("interviews", "Conducting Interviews",
                          current_agent=idx, message=f"Interviewing Agent {idx}/{n_agents}...")
            agent_id = exp_data.get("agent_id", idx-1)
            qa_pairs = self.interviewer.conduct_interview(
                agent=exp_data["agent"],
                experience=exp_data["experience"],
                product=exp_data.get("product", product),
                agent_id=agent_id
            )
            interviews.append({
                "agent_id": agent_id,
                "agent": exp_data["agent"],
                "experience": exp_data["experience"],
                "product": exp_data.get("product", product),
                "interview": qa_pairs
            })
        results["interviews"] = interviews
        total_qa = sum(len(i["interview"]) for i in interviews)
        
        stage_end = time.time()
        self.analytics.track_stage("interviews", stage_start, stage_end, total_qa)
        logger.info(f"✓ Completed {len(interviews)} interviews ({total_qa} Q&A pairs)")
        
        if save_intermediate:
            self._save_intermediate("interviews", interviews)
        
        # Stage 4: Extract Latent Needs
        logger.info("\n[STAGE 4/4] Extracting Latent Needs...")
        stage_start = time.time()
        self.analytics.log_activity("stage_start", "Starting need extraction stage", {})
        
        need_extractions = []
        for idx, interview in enumerate(interviews, 1):
            report_progress("need_extraction", "Extracting Needs",
                          current_agent=idx, message=f"Extracting needs from Agent {idx}/{n_agents}...")
            extraction = self.need_extractor.extract_from_interview(interview)
            need_extractions.append(extraction)
        results["need_extractions"] = need_extractions
        
        # Aggregate needs
        report_progress("aggregation", "Aggregating Needs", message="Aggregating all extracted needs...")
        aggregated_needs = self.need_extractor.aggregate_needs(need_extractions)
        results["aggregated_needs"] = aggregated_needs
        
        stage_end = time.time()
        self.analytics.track_stage("need_extraction", stage_start, stage_end, aggregated_needs['total_needs'])
        
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
        
        # Add analytics to results
        analytics_summary = self.analytics.get_summary()
        results["analytics"] = analytics_summary
        
        logger.info("="*60)
        logger.info(f"Pipeline Completed Successfully in {duration:.2f}s")
        logger.info(f"Total API Calls: {analytics_summary['overview']['total_api_calls']}")
        logger.info(f"Total Cost: ${analytics_summary['overview']['total_cost']:.4f}")
        logger.info(f"Total Tokens: {analytics_summary['overview']['total_tokens']:,}")
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
        import json
        
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
