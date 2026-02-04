"""
Hybrid Parallel Requirements Elicitation Pipeline

This module provides a faster pipeline implementation that:
1. Generates agents SERIALLY (to maintain diversity)
2. Runs experience simulation + interviews in PARALLEL per agent
3. Handles failures gracefully - continues with other agents if one fails

Use this for faster execution when API rate limits allow.
"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from threading import Semaphore

from ..llm.gemini_client import GeminiClient
from ..agents.generator import AgentGenerator
from ..agents.simulator import ExperienceSimulator
from ..agents.interviewer import Interviewer
from ..agents.latent_extractor import LatentNeedExtractor
from ..utils.logger import get_logger
from ..utils.analytics import AnalyticsCollector

logger = get_logger(__name__)


class ParallelRequirementsPipeline:
    """
    Hybrid parallel pipeline for requirements elicitation.
    
    This pipeline:
    - Generates agents serially (for diversity)
    - Processes experience + interview in parallel per agent
    - Uses rate limiting to avoid API throttling
    - Continues processing even if individual agents fail
    """
    
    def __init__(
        self,
        llm_client: GeminiClient,
        interview_questions: Optional[List[str]] = None,
        analytics_collector: Optional[AnalyticsCollector] = None,
        max_concurrent_calls: int = 0,  # 0 = unlimited
        rate_limit_delay: float = 0.0   # No delay by default
    ):
        """
        Initialize the parallel requirements pipeline.
        
        Args:
            llm_client: An initialized LLM client instance
            interview_questions: Optional list of questions for interviews
            analytics_collector: Optional AnalyticsCollector for metrics tracking
            max_concurrent_calls: Maximum concurrent API calls (0 = unlimited)
            rate_limit_delay: Delay between API calls (0 = no delay)
        """
        self.llm_client = llm_client
        self.analytics = analytics_collector or AnalyticsCollector()
        self.max_concurrent_calls = max_concurrent_calls
        self.rate_limit_delay = rate_limit_delay
        
        # Semaphore for rate limiting (only if max_concurrent_calls > 0)
        self._api_semaphore = Semaphore(max_concurrent_calls) if max_concurrent_calls > 0 else None
        
        # Initialize all components
        self.agent_generator = AgentGenerator(llm_client)
        self.experience_simulator = ExperienceSimulator(llm_client)
        self.interviewer = Interviewer(llm_client, interview_questions)
        self.need_extractor = LatentNeedExtractor(llm_client)
        
        logger.info(f"ParallelRequirementsPipeline initialized (max_concurrent={'unlimited' if max_concurrent_calls == 0 else max_concurrent_calls})")
    
    def set_interview_questions(self, questions: List[str]) -> None:
        """Set or update interview questions."""
        self.interviewer.set_questions(questions)
        logger.info(f"Pipeline interview questions updated: {len(questions)} questions")
    
    def _process_single_agent(
        self,
        agent_id: int,
        agent: str,
        product: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Process a single agent through experience simulation and interview.
        
        This runs in a thread and handles its own errors gracefully.
        
        Args:
            agent_id: The agent's ID
            agent: The agent description
            product: The product being studied
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary with agent results or error information
        """
        result = {
            "agent_id": agent_id,
            "agent": agent,
            "product": product,
            "success": False,
            "experience": None,
            "interview": None,
            "error": None
        }
        
        try:
            # Step 1: Simulate experience
            logger.info(f"[Agent {agent_id}] Starting experience simulation...")
            if progress_callback:
                progress_callback({
                    "agent_id": agent_id,
                    "stage": "experience",
                    "message": f"Agent {agent_id}: Simulating experience..."
                })
            
            # Optionally use semaphore for rate limiting
            if self._api_semaphore:
                with self._api_semaphore:
                    if self.rate_limit_delay > 0:
                        time.sleep(self.rate_limit_delay)
                    experience = self.experience_simulator.simulate_experience(
                        agent, product, agent_id=agent_id
                    )
            else:
                experience = self.experience_simulator.simulate_experience(
                    agent, product, agent_id=agent_id
                )
            
            result["experience"] = experience
            logger.info(f"[Agent {agent_id}] Experience simulation completed")
            
            # Step 2: Conduct interview
            logger.info(f"[Agent {agent_id}] Starting interview...")
            if progress_callback:
                progress_callback({
                    "agent_id": agent_id,
                    "stage": "interview",
                    "message": f"Agent {agent_id}: Conducting interview..."
                })
            
            qa_pairs = []
            for q_idx, question in enumerate(self.interviewer.questions, 1):
                # Optionally use semaphore for rate limiting
                if self._api_semaphore:
                    with self._api_semaphore:
                        if self.rate_limit_delay > 0:
                            time.sleep(self.rate_limit_delay)
                        answer = self.interviewer.ask_question(
                            agent, experience, question, product, agent_id=agent_id
                        )
                        qa_pairs.append({
                            "question": question,
                            "answer": answer
                        })
                else:
                    answer = self.interviewer.ask_question(
                        agent, experience, question, product, agent_id=agent_id
                    )
                    qa_pairs.append({
                        "question": question,
                        "answer": answer
                    })
                
                logger.debug(f"[Agent {agent_id}] Question {q_idx}/{len(self.interviewer.questions)} completed")
            
            result["interview"] = qa_pairs
            result["success"] = True
            logger.info(f"[Agent {agent_id}] Interview completed successfully")
            
            if progress_callback:
                progress_callback({
                    "agent_id": agent_id,
                    "stage": "completed",
                    "message": f"Agent {agent_id}: Completed!"
                })
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[Agent {agent_id}] Failed: {error_msg}")
            result["error"] = error_msg
            
            if progress_callback:
                progress_callback({
                    "agent_id": agent_id,
                    "stage": "failed",
                    "message": f"Agent {agent_id}: Failed - {error_msg}"
                })
        
        return result
    
    def run(
        self,
        n_agents: int = 5,
        design_context: str = "camping tent",
        product: str = "tent",
        save_intermediate: bool = False,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Run the hybrid parallel requirements elicitation pipeline.
        
        Agent generation is serial (for diversity), but experience simulation
        and interviews run in parallel across agents.
        
        Args:
            n_agents: Number of user agents to generate
            design_context: Context for agent generation
            product: Product being studied
            save_intermediate: Whether to save intermediate results
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary containing all pipeline results and metadata
        """
        logger.info("="*60)
        logger.info("Starting PARALLEL Requirements Elicitation Pipeline")
        logger.info(f"Configuration: {n_agents} agents, max_concurrent={self.max_concurrent_calls}")
        logger.info("="*60)
        
        start_time = datetime.now()
        start_timestamp = time.time()
        
        # Start analytics tracking
        self.analytics.start_tracking()
        self.analytics.log_activity("info", f"Parallel Pipeline initialized - Product: {product}", {
            "n_agents": n_agents,
            "design_context": design_context,
            "mode": "parallel"
        })
        
        results = {
            "metadata": {
                "start_time": start_time.isoformat(),
                "n_agents": n_agents,
                "design_context": design_context,
                "product": product,
                "pipeline_version": "2.0.0-parallel",
                "mode": "parallel",
                "max_concurrent_calls": self.max_concurrent_calls
            }
        }
        
        # ============================================================
        # Stage 1: Generate Agents (SERIAL - for diversity)
        # ============================================================
        logger.info("\n[STAGE 1/4] Generating User Agents (Serial for diversity)...")
        stage_start = time.time()
        
        if progress_callback:
            progress_callback({
                "stage": "agent_generation",
                "message": "Generating diverse user agents...",
                "progress": 0
            })
        
        agents = self.agent_generator.generate_agents(n_agents, design_context)
        results["agents"] = agents
        
        stage_end = time.time()
        agent_gen_time = stage_end - stage_start
        self.analytics.track_stage("agent_generation", stage_start, stage_end, len(agents))
        logger.info(f"✓ Generated {len(agents)} agents in {agent_gen_time:.2f}s")
        
        # ============================================================
        # Stage 2 & 3: Experience Simulation + Interviews (PARALLEL)
        # ============================================================
        logger.info("\n[STAGE 2-3/4] Simulating Experiences & Conducting Interviews (Parallel)...")
        stage_start = time.time()
        
        if progress_callback:
            progress_callback({
                "stage": "parallel_processing",
                "message": f"Processing {len(agents)} agents in parallel...",
                "progress": 0
            })
        
        # Process all agents in parallel using ThreadPoolExecutor
        agent_results = []
        failed_agents = []
        
        # Use None for max_workers to let Python decide (based on CPU cores)
        # or use the specified limit if > 0
        max_workers = self.max_concurrent_calls if self.max_concurrent_calls > 0 else None
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all agent processing tasks
            futures = {
                executor.submit(
                    self._process_single_agent,
                    idx,
                    agent,
                    product,
                    progress_callback
                ): idx
                for idx, agent in enumerate(agents, 1)
            }
            
            # Collect results as they complete
            for future in as_completed(futures):
                agent_id = futures[future]
                try:
                    result = future.result()
                    agent_results.append(result)
                    
                    if result["success"]:
                        logger.info(f"✓ Agent {agent_id} completed successfully")
                    else:
                        failed_agents.append(agent_id)
                        logger.warning(f"✗ Agent {agent_id} failed: {result.get('error')}")
                        
                except Exception as e:
                    logger.error(f"✗ Agent {agent_id} thread failed: {str(e)}")
                    failed_agents.append(agent_id)
                    agent_results.append({
                        "agent_id": agent_id,
                        "success": False,
                        "error": str(e)
                    })
        
        # Sort results by agent_id for consistent ordering
        agent_results.sort(key=lambda x: x.get("agent_id", 0))
        
        stage_end = time.time()
        parallel_time = stage_end - stage_start
        
        # Build experiences and interviews lists from results
        experiences = []
        interviews = []
        
        for res in agent_results:
            if res["success"]:
                experiences.append({
                    "agent_id": res["agent_id"],
                    "agent": res["agent"],
                    "product": res["product"],
                    "experience": res["experience"]
                })
                interviews.append({
                    "agent_id": res["agent_id"],
                    "agent": res["agent"],
                    "experience": res["experience"],
                    "product": res["product"],
                    "interview": res["interview"]
                })
        
        results["experiences"] = experiences
        results["interviews"] = interviews
        results["agent_results"] = agent_results
        results["failed_agents"] = failed_agents
        
        successful_count = len([r for r in agent_results if r["success"]])
        total_qa = sum(len(i["interview"]) for i in interviews)
        
        self.analytics.track_stage("parallel_processing", stage_start, stage_end, successful_count)
        logger.info(f"✓ Parallel processing completed in {parallel_time:.2f}s")
        logger.info(f"  - Successful: {successful_count}/{len(agents)} agents")
        logger.info(f"  - Failed: {len(failed_agents)} agents")
        logger.info(f"  - Total Q&A pairs: {total_qa}")
        
        # ============================================================
        # Stage 4: Extract Latent Needs (from successful interviews)
        # ============================================================
        if interviews:
            logger.info("\n[STAGE 4/4] Extracting Latent Needs...")
            stage_start = time.time()
            
            if progress_callback:
                progress_callback({
                    "stage": "need_extraction",
                    "message": "Extracting latent needs from interviews...",
                    "progress": 80
                })
            
            need_extractions = self.need_extractor.extract_from_multiple_interviews(interviews)
            results["need_extractions"] = need_extractions
            
            # Aggregate needs
            aggregated_needs = self.need_extractor.aggregate_needs(need_extractions)
            results["aggregated_needs"] = aggregated_needs
            
            stage_end = time.time()
            self.analytics.track_stage("need_extraction", stage_start, stage_end, aggregated_needs['total_needs'])
            
            logger.info(f"✓ Extracted {aggregated_needs['total_needs']} total needs")
            logger.info(f"  - Categories: {list(aggregated_needs['summary']['by_category'].keys())}")
            logger.info(f"  - High Priority: {aggregated_needs['summary']['by_priority'].get('High', 0)}")
        else:
            logger.warning("No successful interviews to extract needs from!")
            results["need_extractions"] = []
            results["aggregated_needs"] = {
                "total_needs": 0,
                "categories": {},
                "summary": {"by_category": {}, "by_priority": {}}
            }
        
        # Finalize metadata
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        results["metadata"]["end_time"] = end_time.isoformat()
        results["metadata"]["duration_seconds"] = duration
        results["metadata"]["status"] = "completed" if not failed_agents else "completed_with_errors"
        results["metadata"]["successful_agents"] = successful_count
        results["metadata"]["failed_agents_count"] = len(failed_agents)
        
        # Timing breakdown
        results["metadata"]["timing"] = {
            "agent_generation_seconds": agent_gen_time,
            "parallel_processing_seconds": parallel_time,
            "total_seconds": duration
        }
        
        # Add analytics to results
        analytics_summary = self.analytics.get_summary()
        results["analytics"] = analytics_summary
        
        logger.info("="*60)
        logger.info(f"PARALLEL Pipeline Completed in {duration:.2f}s")
        logger.info(f"  - Agent Generation: {agent_gen_time:.2f}s (serial)")
        logger.info(f"  - Experience + Interview: {parallel_time:.2f}s (parallel)")
        logger.info(f"  - Successful Agents: {successful_count}/{len(agents)}")
        if failed_agents:
            logger.info(f"  - Failed Agents: {failed_agents}")
        logger.info(f"Total API Calls: {analytics_summary['overview']['total_api_calls']}")
        logger.info(f"Total Cost: ${analytics_summary['overview']['total_cost']:.4f}")
        logger.info("="*60)
        
        if progress_callback:
            progress_callback({
                "stage": "completed",
                "message": f"Pipeline completed! {successful_count}/{len(agents)} agents processed.",
                "progress": 100
            })
        
        return results
