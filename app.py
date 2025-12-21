"""
Elicitron Methodology Web Application

This Flask application provides a web interface to demonstrate the Elicitron
requirements elicitation methodology, allowing users to input product ideas
and visualize the 4-stage pipeline in action.
"""

import os
import json
import uuid
import threading
import yaml
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS

from src.llm.gemini_client import GeminiClient
from src.pipeline.pipeline import RequirementsPipeline
from src.utils.logger import configure_logging, get_logger

app = Flask(__name__)
CORS(app)

# In-memory storage for jobs (use Redis in production)
jobs = {}
jobs_lock = threading.Lock()

logger = get_logger(__name__)


def load_config(config_path: str = "config/settings.yaml") -> dict:
    """Load configuration from YAML file."""
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def load_interview_questions(questions_path: str = "config/interview_questions.yaml") -> list:
    """Load interview questions from YAML file."""
    if os.path.exists(questions_path):
        with open(questions_path, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('questions', [])
    return []


def run_pipeline_async(job_id: str, product_idea: str, design_context: str, n_agents: int):
    """
    Run the pipeline in a background thread and update job status.
    
    Args:
        job_id: Unique job identifier
        product_idea: Product description
        design_context: Design context for agent generation
        n_agents: Number of agents to generate
    """
    try:
        with jobs_lock:
            jobs[job_id] = {
                "status": "initializing",
                "stage": 0,
                "message": "Initializing pipeline...",
                "results": None,
                "error": None
            }
        
        # Load configuration
        config = load_config()
        llm_config = config.get('llm', {})
        log_config = config.get('logging', {})
        
        # Configure logging
        configure_logging(
            level=getattr(__import__('logging'), log_config.get('level', 'INFO')),
            log_file=log_config.get('log_file')
        )
        
        # Initialize LLM client
        llm_client = GeminiClient(
            model_name=llm_config.get('model_name', 'gemini-1.5-flash'),
            temperature=llm_config.get('temperature', 0.7),
            max_retries=llm_config.get('max_retries', 3),
            retry_delay=llm_config.get('retry_delay', 2),
            rate_limit_delay=llm_config.get('rate_limit_delay', 12.0)
        )
        
        # Load interview questions
        questions = load_interview_questions()
        if not questions:
            questions = [
                "What was the most challenging part of your experience?",
                "What would you change to improve the product?"
            ]
        
        # Initialize pipeline
        pipeline = RequirementsPipeline(llm_client, questions)
        
        # Update status: Stage 1 - Agent Generation
        with jobs_lock:
            jobs[job_id].update({
                "status": "running",
                "stage": 1,
                "message": "Generating user agents...",
                "agents": []
            })
        
        # Stage 1: Generate Agents
        agents = pipeline.agent_generator.generate_agents(n_agents, design_context)
        with jobs_lock:
            jobs[job_id].update({
                "stage": 1,
                "message": f"Generated {len(agents)} agents",
                "agents": agents,
                "agents_count": len(agents)
            })
        
        # Update status: Stage 2 - Experience Simulation
        with jobs_lock:
            jobs[job_id].update({
                "stage": 2,
                "message": "Simulating user experiences...",
                "experiences": []
            })
        
        # Stage 2: Simulate Experiences
        experiences = pipeline.experience_simulator.simulate_multiple_experiences(agents, product_idea)
        with jobs_lock:
            jobs[job_id].update({
                "stage": 2,
                "message": f"Simulated {len(experiences)} experiences",
                "experiences": experiences,
                "experiences_count": len(experiences)
            })
        
        # Update status: Stage 3 - Interview Simulation
        with jobs_lock:
            jobs[job_id].update({
                "stage": 3,
                "message": "Conducting interviews...",
                "interviews": []
            })
        
        # Stage 3: Conduct Interviews
        interviews = pipeline.interviewer.conduct_multiple_interviews(experiences)
        total_qa = sum(len(i.get("interview", [])) for i in interviews)
        with jobs_lock:
            jobs[job_id].update({
                "stage": 3,
                "message": f"Completed {len(interviews)} interviews ({total_qa} Q&A pairs)",
                "interviews": interviews,
                "interviews_count": len(interviews),
                "qa_pairs_count": total_qa
            })
        
        # Update status: Stage 4 - Latent Need Extraction
        with jobs_lock:
            jobs[job_id].update({
                "stage": 4,
                "message": "Extracting latent needs...",
                "needs": []
            })
        
        # Stage 4: Extract Needs
        need_extractions = pipeline.need_extractor.extract_from_multiple_interviews(interviews)
        aggregated_needs = pipeline.need_extractor.aggregate_needs(need_extractions)
        
        with jobs_lock:
            jobs[job_id].update({
                "stage": 4,
                "message": f"Extracted {aggregated_needs.get('total_needs', 0)} needs",
                "needs": need_extractions,
                "aggregated_needs": aggregated_needs,
                "total_needs": aggregated_needs.get('total_needs', 0)
            })
        
        # Compile final results
        results = {
            "metadata": {
                "job_id": job_id,
                "start_time": jobs[job_id].get("start_time"),
                "end_time": datetime.now().isoformat(),
                "n_agents": n_agents,
                "design_context": design_context,
                "product": product_idea,
                "pipeline_version": "1.0.0"
            },
            "agents": agents,
            "experiences": experiences,
            "interviews": interviews,
            "need_extractions": need_extractions,
            "aggregated_needs": aggregated_needs
        }
        
        # Mark as complete
        with jobs_lock:
            jobs[job_id].update({
                "status": "completed",
                "stage": 4,
                "message": "Pipeline completed successfully",
                "results": results
            })
        
        logger.info(f"Job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}", exc_info=True)
        with jobs_lock:
            jobs[job_id].update({
                "status": "error",
                "error": str(e),
                "message": f"Error: {str(e)}"
            })


@app.route('/')
def index():
    """Main input page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Start a new pipeline analysis."""
    data = request.get_json() or request.form
    
    product_idea = data.get('product_idea', '').strip()
    design_context = data.get('design_context', '').strip() or product_idea
    n_agents = int(data.get('n_agents', 5))
    
    if not product_idea:
        return jsonify({"error": "Product idea is required"}), 400
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Initialize job
    with jobs_lock:
        jobs[job_id] = {
            "status": "queued",
            "stage": 0,
            "message": "Job queued",
            "start_time": datetime.now().isoformat(),
            "product_idea": product_idea,
            "design_context": design_context,
            "n_agents": n_agents
        }
    
    # Start pipeline in background thread
    thread = threading.Thread(
        target=run_pipeline_async,
        args=(job_id, product_idea, design_context, n_agents)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "job_id": job_id,
        "status": "queued",
        "redirect_url": url_for('processing', job_id=job_id)
    })


@app.route('/processing/<job_id>')
def processing(job_id):
    """Processing page with real-time progress."""
    with jobs_lock:
        job = jobs.get(job_id)
    
    if not job:
        return render_template('error.html', message="Job not found"), 404
    
    return render_template('processing.html', job_id=job_id)


@app.route('/api/status/<job_id>')
def status(job_id):
    """Get current status of a job."""
    with jobs_lock:
        job = jobs.get(job_id)
    
    if not job:
        return jsonify({"error": "Job not found"}), 404
    
    return jsonify({
        "status": job.get("status"),
        "stage": job.get("stage"),
        "message": job.get("message"),
        "agents_count": job.get("agents_count", 0),
        "experiences_count": job.get("experiences_count", 0),
        "interviews_count": job.get("interviews_count", 0),
        "qa_pairs_count": job.get("qa_pairs_count", 0),
        "total_needs": job.get("total_needs", 0),
        "error": job.get("error")
    })


@app.route('/results/<job_id>')
def results(job_id):
    """Results page displaying pipeline output."""
    with jobs_lock:
        job = jobs.get(job_id)
    
    if not job:
        return render_template('error.html', message="Job not found"), 404
    
    if job.get("status") != "completed":
        return redirect(url_for('processing', job_id=job_id))
    
    results_data = job.get("results")
    if not results_data:
        return render_template('error.html', message="Results not available"), 404
    
    return render_template('results.html', results=results_data, job_id=job_id)


@app.route('/api/results/<job_id>')
def api_results(job_id):
    """Get results as JSON."""
    with jobs_lock:
        job = jobs.get(job_id)
    
    if not job:
        return jsonify({"error": "Job not found"}), 404
    
    if job.get("status") != "completed":
        return jsonify({"error": "Job not completed"}), 400
    
    return jsonify(job.get("results"))


if __name__ == '__main__':
    config = load_config()
    web_config = config.get('web_app', {})
    
    # Detect if running on Streamlit Cloud or other cloud platforms
    import os
    is_cloud = os.environ.get('STREAMLIT_SHARING_MODE') or os.environ.get('KUBERNETES_SERVICE_HOST')
    
    host = web_config.get('host', '0.0.0.0' if is_cloud else '127.0.0.1')
    port = int(os.environ.get('PORT', web_config.get('port', 5000)))
    debug = False if is_cloud else web_config.get('debug', True)
    
    logger.info(f"Starting Elicitron web application on {host}:{port}")
    app.run(host=host, port=port, debug=debug, use_reloader=False)

