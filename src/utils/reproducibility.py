"""
Reproducibility Testing Module

This module provides tools to measure the reproducibility of LLM-generated outputs
by running multiple iterations and calculating similarity metrics.
"""

import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import Counter
import re

from ..llm.base_client import BaseLLMClient
from ..pipeline.pipeline import RequirementsPipeline
from ..utils.logger import get_logger
from ..utils.analytics import AnalyticsCollector

logger = get_logger(__name__)


class ReproducibilityTester:
    """
    Tests reproducibility of the requirements elicitation pipeline
    by running multiple iterations and measuring consistency.
    """
    
    def __init__(self, llm_client: BaseLLMClient, interview_questions: Optional[List[str]] = None):
        """
        Initialize the reproducibility tester.
        
        Args:
            llm_client: LLM client for pipeline execution
            interview_questions: Optional interview questions
        """
        self.llm_client = llm_client
        self.interview_questions = interview_questions
        logger.info("ReproducibilityTester initialized")
    
    def run_iterations(
        self,
        n_iterations: int,
        product: str,
        design_context: str,
        n_agents: int = 3,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Run multiple pipeline iterations for reproducibility testing.
        
        Args:
            n_iterations: Number of times to run the pipeline
            product: Product name
            design_context: Design context
            n_agents: Number of agents per run
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary containing all runs and reproducibility metrics
        """
        logger.info(f"Starting reproducibility test: {n_iterations} iterations")
        
        start_time = datetime.now()
        test_start_time = time.time()
        runs = []
        iteration_times = []  # Track times for ETA calculation
        
        for i in range(n_iterations):
            iteration_num = i + 1
            logger.info(f"Running iteration {iteration_num}/{n_iterations}")
            
            # Calculate ETA based on previous iterations
            elapsed_time = time.time() - test_start_time
            avg_iteration_time = sum(iteration_times) / len(iteration_times) if iteration_times else 0
            remaining_iterations = n_iterations - i
            eta_seconds = avg_iteration_time * remaining_iterations if avg_iteration_time > 0 else None
            
            if progress_callback:
                progress_callback({
                    "iteration": iteration_num,
                    "total": n_iterations,
                    "status": "running",
                    "stage": "initializing",
                    "stage_name": "Initializing Pipeline",
                    "current_agent": None,
                    "total_agents": n_agents,
                    "elapsed_seconds": elapsed_time,
                    "eta_seconds": eta_seconds,
                    "message": f"Starting iteration {iteration_num} of {n_iterations}..."
                })
            
            try:
                # Create fresh pipeline for each run
                analytics = AnalyticsCollector()
                pipeline = RequirementsPipeline(
                    self.llm_client,
                    interview_questions=self.interview_questions,
                    analytics_collector=analytics
                )
                
                # Create stage progress callback for this iteration
                def create_stage_callback(iter_num, total_iters, test_start):
                    def stage_progress(stage_info):
                        if progress_callback:
                            current_elapsed = time.time() - test_start
                            # Re-calculate ETA
                            current_avg = sum(iteration_times) / len(iteration_times) if iteration_times else None
                            current_eta = current_avg * (total_iters - iter_num + 1) if current_avg else None
                            
                            progress_callback({
                                "iteration": iter_num,
                                "total": total_iters,
                                "status": "running",
                                "stage": stage_info.get("stage", "unknown"),
                                "stage_name": stage_info.get("stage_name", "Processing..."),
                                "current_agent": stage_info.get("current_agent"),
                                "total_agents": stage_info.get("total_agents", n_agents),
                                "elapsed_seconds": current_elapsed,
                                "eta_seconds": current_eta,
                                "message": stage_info.get("message", f"Iteration {iter_num}/{total_iters}")
                            })
                    return stage_progress
                
                stage_cb = create_stage_callback(iteration_num, n_iterations, test_start_time)
                
                # Run pipeline with stage callbacks
                iteration_start = time.time()
                result = pipeline.run(
                    n_agents=n_agents,
                    design_context=design_context,
                    product=product,
                    save_intermediate=False,
                    progress_callback=stage_cb
                )
                iteration_duration = time.time() - iteration_start
                iteration_times.append(iteration_duration)
                
                runs.append({
                    "iteration": iteration_num,
                    "success": True,
                    "duration": iteration_duration,
                    "result": result
                })
                
                logger.info(f"Iteration {iteration_num} completed in {iteration_duration:.2f}s")
                
            except Exception as e:
                logger.error(f"Iteration {i + 1} failed: {str(e)}")
                runs.append({
                    "iteration": i + 1,
                    "success": False,
                    "error": str(e)
                })
        
        # Calculate reproducibility metrics
        successful_runs = [r for r in runs if r.get("success")]
        
        if len(successful_runs) < 2:
            return {
                "error": "Need at least 2 successful runs to calculate reproducibility",
                "runs": runs,
                "successful_runs": len(successful_runs)
            }
        
        metrics = self._calculate_metrics(successful_runs)
        
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        return {
            "metadata": {
                "product": product,
                "design_context": design_context,
                "n_agents": n_agents,
                "n_iterations": n_iterations,
                "successful_iterations": len(successful_runs),
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "total_duration": total_duration
            },
            "runs": runs,
            "metrics": metrics
        }
    
    def _calculate_metrics(self, runs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate reproducibility metrics across runs.
        
        Args:
            runs: List of successful run results
            
        Returns:
            Dictionary containing various reproducibility metrics
        """
        metrics = {}
        
        # 1. Agent Consistency Metrics
        metrics["agent_consistency"] = self._analyze_agent_consistency(runs)
        
        # 2. Need Category Consistency
        metrics["need_category_consistency"] = self._analyze_need_categories(runs)
        
        # 3. Need Priority Consistency
        metrics["need_priority_consistency"] = self._analyze_need_priorities(runs)
        
        # 4. Need Statement Similarity
        metrics["need_statement_similarity"] = self._analyze_need_statements(runs)
        
        # 5. Interview Theme Consistency
        metrics["interview_consistency"] = self._analyze_interviews(runs)
        
        # 6. Overall Reproducibility Score
        metrics["overall_score"] = self._calculate_overall_score(metrics)
        
        return metrics
    
    def _analyze_agent_consistency(self, runs: List[Dict]) -> Dict[str, Any]:
        """Analyze consistency of generated agent personas."""
        agent_data = []
        
        for run in runs:
            result = run["result"]
            agents = result.get("agents", [])
            
            # Extract agent characteristics
            run_agents = []
            for agent_text in agents:
                # Parse age if present
                age_match = re.search(r'\*\*Age\*\*:\s*(\d+)', str(agent_text))
                age = int(age_match.group(1)) if age_match else None
                
                # Parse gender if present
                gender_match = re.search(r'\*\*Gender\*\*:\s*(Male|Female|Non-binary)', str(agent_text), re.I)
                gender = gender_match.group(1) if gender_match else None
                
                run_agents.append({
                    "age": age,
                    "gender": gender,
                    "full_text": str(agent_text)
                })
            
            agent_data.append(run_agents)
        
        # Calculate age consistency (standard deviation)
        all_ages = []
        for run_agents in agent_data:
            run_ages = [a["age"] for a in run_agents if a["age"]]
            if run_ages:
                all_ages.append(sum(run_ages) / len(run_ages))
        
        age_consistency = 1 - (self._std(all_ages) / 50) if all_ages else 0  # Normalize by expected range
        age_consistency = max(0, min(1, age_consistency))
        
        # Calculate gender distribution consistency
        gender_distributions = []
        for run_agents in agent_data:
            genders = [a["gender"] for a in run_agents if a["gender"]]
            if genders:
                dist = Counter(genders)
                total = len(genders)
                gender_distributions.append({g: c/total for g, c in dist.items()})
        
        gender_consistency = self._distribution_similarity(gender_distributions) if gender_distributions else 0
        
        return {
            "age_consistency": round(age_consistency, 3),
            "gender_distribution_consistency": round(gender_consistency, 3),
            "average_agents_per_run": sum(len(ra) for ra in agent_data) / len(agent_data) if agent_data else 0
        }
    
    def _analyze_need_categories(self, runs: List[Dict]) -> Dict[str, Any]:
        """Analyze consistency of need categories across runs."""
        category_distributions = []
        all_categories = set()
        
        for run in runs:
            result = run["result"]
            aggregated = result.get("aggregated_needs", {})
            
            if "summary" in aggregated and "by_category" in aggregated["summary"]:
                dist = aggregated["summary"]["by_category"]
                total = sum(dist.values())
                if total > 0:
                    normalized = {k: v/total for k, v in dist.items()}
                    category_distributions.append(normalized)
                    all_categories.update(dist.keys())
        
        if not category_distributions:
            return {"consistency": 0, "categories_found": []}
        
        # Calculate Jaccard similarity for category presence
        category_sets = [set(d.keys()) for d in category_distributions]
        jaccard_scores = []
        for i in range(len(category_sets)):
            for j in range(i + 1, len(category_sets)):
                intersection = len(category_sets[i] & category_sets[j])
                union = len(category_sets[i] | category_sets[j])
                if union > 0:
                    jaccard_scores.append(intersection / union)
        
        jaccard_avg = sum(jaccard_scores) / len(jaccard_scores) if jaccard_scores else 0
        
        # Calculate distribution similarity
        dist_similarity = self._distribution_similarity(category_distributions)
        
        # Category frequency across runs
        category_frequency = {}
        for cat in all_categories:
            count = sum(1 for d in category_distributions if cat in d)
            category_frequency[cat] = count / len(category_distributions)
        
        return {
            "jaccard_similarity": round(jaccard_avg, 3),
            "distribution_similarity": round(dist_similarity, 3),
            "consistency": round((jaccard_avg + dist_similarity) / 2, 3),
            "categories_found": list(all_categories),
            "category_frequency": category_frequency
        }
    
    def _analyze_need_priorities(self, runs: List[Dict]) -> Dict[str, Any]:
        """Analyze consistency of need priority distributions."""
        priority_distributions = []
        
        for run in runs:
            result = run["result"]
            aggregated = result.get("aggregated_needs", {})
            
            if "summary" in aggregated and "by_priority" in aggregated["summary"]:
                dist = aggregated["summary"]["by_priority"]
                total = sum(dist.values())
                if total > 0:
                    normalized = {k: v/total for k, v in dist.items()}
                    priority_distributions.append(normalized)
        
        if not priority_distributions:
            return {"consistency": 0}
        
        consistency = self._distribution_similarity(priority_distributions)
        
        # Calculate average priority distribution
        avg_distribution = {}
        for priority in ["High", "Medium", "Low"]:
            values = [d.get(priority, 0) for d in priority_distributions]
            avg_distribution[priority] = sum(values) / len(values) if values else 0
        
        return {
            "consistency": round(consistency, 3),
            "average_distribution": {k: round(v, 3) for k, v in avg_distribution.items()},
            "high_priority_std": round(self._std([d.get("High", 0) for d in priority_distributions]), 3)
        }
    
    def _analyze_need_statements(self, runs: List[Dict]) -> Dict[str, Any]:
        """Analyze semantic similarity of need statements."""
        all_needs_per_run = []
        
        for run in runs:
            result = run["result"]
            aggregated = result.get("aggregated_needs", {})
            categories = aggregated.get("categories", {})
            
            run_needs = []
            for category, needs in categories.items():
                for need in needs:
                    if isinstance(need, dict) and "need_statement" in need:
                        run_needs.append(need["need_statement"])
            
            all_needs_per_run.append(run_needs)
        
        if not all_needs_per_run:
            return {"similarity": 0}
        
        # Calculate keyword overlap as a proxy for semantic similarity
        keyword_sets = []
        for needs in all_needs_per_run:
            keywords = set()
            for need in needs:
                # Extract meaningful words (simple tokenization)
                words = re.findall(r'\b[a-zA-Z]{4,}\b', need.lower())
                keywords.update(words)
            keyword_sets.append(keywords)
        
        # Pairwise Jaccard similarity of keywords
        jaccard_scores = []
        for i in range(len(keyword_sets)):
            for j in range(i + 1, len(keyword_sets)):
                if keyword_sets[i] and keyword_sets[j]:
                    intersection = len(keyword_sets[i] & keyword_sets[j])
                    union = len(keyword_sets[i] | keyword_sets[j])
                    jaccard_scores.append(intersection / union if union > 0 else 0)
        
        avg_similarity = sum(jaccard_scores) / len(jaccard_scores) if jaccard_scores else 0
        
        # Count needs per run
        needs_counts = [len(needs) for needs in all_needs_per_run]
        
        return {
            "keyword_similarity": round(avg_similarity, 3),
            "average_needs_count": round(sum(needs_counts) / len(needs_counts), 1) if needs_counts else 0,
            "needs_count_std": round(self._std(needs_counts), 2) if needs_counts else 0
        }
    
    def _analyze_interviews(self, runs: List[Dict]) -> Dict[str, Any]:
        """Analyze consistency of interview content."""
        interview_lengths = []
        all_answers = []
        
        for run in runs:
            result = run["result"]
            interviews = result.get("interviews", [])
            
            run_answer_lengths = []
            run_answers = []
            
            for interview in interviews:
                qa_pairs = interview.get("interview", [])
                for qa in qa_pairs:
                    if isinstance(qa, dict) and "answer" in qa:
                        run_answer_lengths.append(len(qa["answer"]))
                        run_answers.append(qa["answer"])
            
            if run_answer_lengths:
                interview_lengths.append(sum(run_answer_lengths) / len(run_answer_lengths))
            all_answers.append(run_answers)
        
        # Answer length consistency
        length_consistency = 1 - (self._std(interview_lengths) / 500) if interview_lengths else 0
        length_consistency = max(0, min(1, length_consistency))
        
        return {
            "answer_length_consistency": round(length_consistency, 3),
            "average_answer_length": round(sum(interview_lengths) / len(interview_lengths), 1) if interview_lengths else 0
        }
    
    def _calculate_overall_score(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall reproducibility score."""
        scores = []
        weights = []
        
        # Agent consistency (weight: 0.15)
        agent_score = metrics.get("agent_consistency", {})
        if agent_score:
            avg_agent = (agent_score.get("age_consistency", 0) + 
                        agent_score.get("gender_distribution_consistency", 0)) / 2
            scores.append(avg_agent)
            weights.append(0.15)
        
        # Need category consistency (weight: 0.25)
        category_score = metrics.get("need_category_consistency", {}).get("consistency", 0)
        scores.append(category_score)
        weights.append(0.25)
        
        # Need priority consistency (weight: 0.20)
        priority_score = metrics.get("need_priority_consistency", {}).get("consistency", 0)
        scores.append(priority_score)
        weights.append(0.20)
        
        # Need statement similarity (weight: 0.25)
        statement_score = metrics.get("need_statement_similarity", {}).get("keyword_similarity", 0)
        scores.append(statement_score)
        weights.append(0.25)
        
        # Interview consistency (weight: 0.15)
        interview_score = metrics.get("interview_consistency", {}).get("answer_length_consistency", 0)
        scores.append(interview_score)
        weights.append(0.15)
        
        # Weighted average
        if sum(weights) > 0:
            overall = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        else:
            overall = 0
        
        # Determine rating
        if overall >= 0.85:
            rating = "Excellent"
        elif overall >= 0.70:
            rating = "Good"
        elif overall >= 0.50:
            rating = "Moderate"
        else:
            rating = "Low"
        
        return {
            "score": round(overall, 3),
            "rating": rating,
            "component_scores": {
                "agent_consistency": round(scores[0] if len(scores) > 0 else 0, 3),
                "category_consistency": round(scores[1] if len(scores) > 1 else 0, 3),
                "priority_consistency": round(scores[2] if len(scores) > 2 else 0, 3),
                "statement_similarity": round(scores[3] if len(scores) > 3 else 0, 3),
                "interview_consistency": round(scores[4] if len(scores) > 4 else 0, 3)
            }
        }
    
    def _std(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def _distribution_similarity(self, distributions: List[Dict[str, float]]) -> float:
        """
        Calculate average similarity between probability distributions.
        Uses simplified cosine-like similarity.
        """
        if len(distributions) < 2:
            return 1.0
        
        # Get all keys
        all_keys = set()
        for d in distributions:
            all_keys.update(d.keys())
        
        # Convert to vectors
        vectors = []
        for d in distributions:
            vector = [d.get(k, 0) for k in sorted(all_keys)]
            vectors.append(vector)
        
        # Pairwise cosine similarity
        similarities = []
        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                sim = self._cosine_similarity(vectors[i], vectors[j])
                similarities.append(sim)
        
        return sum(similarities) / len(similarities) if similarities else 1.0
    
    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = sum(a * a for a in v1) ** 0.5
        norm2 = sum(b * b for b in v2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot / (norm1 * norm2)
