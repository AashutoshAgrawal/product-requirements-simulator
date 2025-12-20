"""
Requirements Elicitation Pipeline - Main Entry Point

This script demonstrates how to use the requirements elicitation pipeline
to generate user agents, simulate experiences, conduct interviews, and extract needs.
"""

import os
import json
import yaml
from datetime import datetime

from src.llm.gemini_client import GeminiClient
from src.pipeline.pipeline import RequirementsPipeline
from src.utils.logger import configure_logging, get_logger


def load_config(config_path: str = "config/settings.yaml") -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def load_interview_questions(questions_path: str = "config/interview_questions.yaml") -> list:
    """
    Load interview questions from YAML file.
    
    Args:
        questions_path: Path to questions file
        
    Returns:
        List of question strings
    """
    if os.path.exists(questions_path):
        with open(questions_path, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('questions', [])
    return []


def save_results(results: dict, output_dir: str = "results") -> str:
    """
    Save pipeline results to JSON file.
    
    Args:
        results: Pipeline results dictionary
        output_dir: Directory to save results
        
    Returns:
        Path to saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_dir, f"pipeline_results_{timestamp}.json")
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    return filename


def print_summary(results: dict) -> None:
    """
    Print a summary of pipeline results.
    
    Args:
        results: Pipeline results dictionary
    """
    print("\n" + "="*60)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*60)
    
    metadata = results.get('metadata', {})
    print(f"\n📋 Configuration:")
    print(f"   Design Context: {metadata.get('design_context')}")
    print(f"   Product: {metadata.get('product')}")
    print(f"   Number of Agents: {metadata.get('n_agents')}")
    print(f"   Duration: {metadata.get('duration_seconds', 0):.2f}s")
    
    print(f"\n👥 Agents Generated: {len(results.get('agents', []))}")
    print(f"📝 Experiences Simulated: {len(results.get('experiences', []))}")
    print(f"💬 Interviews Conducted: {len(results.get('interviews', []))}")
    
    aggregated = results.get('aggregated_needs', {})
    print(f"\n🎯 Total Needs Extracted: {aggregated.get('total_needs', 0)}")
    
    summary = aggregated.get('summary', {})
    if 'by_category' in summary:
        print(f"\n📊 Needs by Category:")
        for category, count in summary['by_category'].items():
            print(f"   {category}: {count}")
    
    if 'by_priority' in summary:
        print(f"\n⚡ Needs by Priority:")
        for priority, count in summary['by_priority'].items():
            print(f"   {priority}: {count}")
    
    print("\n" + "="*60)


def main():
    """Main execution function."""
    print("🚀 Starting Requirements Elicitation Pipeline...")
    print("="*60)
    
    # Load configuration
    config = load_config()
    llm_config = config.get('llm', {})
    agent_config = config.get('agent_generation', {})
    exp_config = config.get('experience_simulation', {})
    log_config = config.get('logging', {})
    output_config = config.get('output', {})
    
    # Configure logging
    configure_logging(
        level=getattr(__import__('logging'), log_config.get('level', 'INFO')),
        log_file=log_config.get('log_file')
    )
    
    logger = get_logger(__name__)
    logger.info("Application started")
    
    # Initialize LLM client
    try:
        llm_client = GeminiClient(
            model_name=llm_config.get('model_name', 'gemini-1.5-flash'),
            temperature=llm_config.get('temperature', 0.7),
            max_retries=llm_config.get('max_retries', 3),
            retry_delay=llm_config.get('retry_delay', 2),
            rate_limit_delay=llm_config.get('rate_limit_delay', 12.0)
        )
        logger.info("LLM client initialized successfully")
    except ValueError as e:
        logger.error(f"Failed to initialize LLM client: {e}")
        print(f"\n❌ Error: {e}")
        print("Please ensure GOOGLE_API_KEY is set in your .env file")
        return
    
    # Load interview questions
    questions = load_interview_questions()
    if not questions:
        logger.warning("No interview questions loaded, using defaults")
        questions = [
            "What was the most challenging part of your experience?",
            "What would you change to improve the product?"
        ]
    
    logger.info(f"Loaded {len(questions)} interview questions")
    
    # Initialize pipeline
    pipeline = RequirementsPipeline(llm_client, questions)
    logger.info("Pipeline initialized")
    
    # Run pipeline
    try:
        results = pipeline.run(
            n_agents=agent_config.get('default_n_agents', 5),
            design_context=agent_config.get('default_design_context', 'camping tent'),
            product=exp_config.get('default_product', 'tent'),
            save_intermediate=output_config.get('save_intermediate_results', False)
        )
        
        logger.info("Pipeline execution completed successfully")
        
        # Save results
        output_dir = output_config.get('results_directory', 'results')
        output_file = save_results(results, output_dir)
        logger.info(f"Results saved to {output_file}")
        
        # Print summary
        print_summary(results)
        print(f"\n💾 Full results saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)
        print(f"\n❌ Pipeline failed: {e}")
        return
    
    logger.info("Application completed successfully")
    print("\n✅ Pipeline completed successfully!")


if __name__ == "__main__":
    main()
