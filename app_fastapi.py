"""
FastAPI Application for Elicitron Requirements Elicitation Pipeline

Modern, production-grade API with:
- Auto-generated OpenAPI docs
- Type safety with Pydantic
- Async background processing
- High performance (2-3x faster than Flask)
"""

import os
import json
import uuid
import asyncio
from datetime import datetime
from typing import Dict, Optional, List
from pathlib import Path

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import yaml

from src.llm.gemini_client import GeminiClient
from src.pipeline.pipeline import RequirementsPipeline
from src.utils.logger import configure_logging, get_logger

# Initialize FastAPI app
app = FastAPI(
    title="Elicitron API",
    description="AI-powered requirements elicitation using the Elicitron methodology",
    version="2.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# CORS configuration - allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job storage (use Redis in production)
jobs: Dict[str, dict] = {}
logger = get_logger(__name__)


# Pydantic models for request/response validation
class AnalyzeRequest(BaseModel):
    product: str = Field(..., min_length=1, description="Product name or idea")
    design_context: str = Field(..., min_length=1, description="Design context or usage scenario")
    n_agents: int = Field(default=1, ge=1, le=5, description="Number of agent personas to generate")

    class Config:
        json_schema_extra = {
            "example": {
                "product": "camping tent",
                "design_context": "ultralight backpacking in alpine conditions",
                "n_agents": 1
            }
        }


class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: Optional[dict] = None
    error: Optional[str] = None


class ResultsResponse(BaseModel):
    job_id: str
    status: str
    results: Optional[dict] = None


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


async def run_pipeline_async(job_id: str, product_idea: str, design_context: str, n_agents: int):
    """
    Run the requirements elicitation pipeline asynchronously.
    """
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = {
            "stage": "initializing",
            "message": "Starting pipeline..."
        }
        
        # Load configuration
        config = load_config()
        interview_questions = load_interview_questions()
        
        # Initialize LLM client
        llm_config = config.get('llm', {})
        llm_client = GeminiClient(
            model_name=llm_config.get('model_name', 'gemini-1.5-flash'),
            temperature=llm_config.get('temperature', 0.7)
        )
        
        # Create pipeline
        pipeline = RequirementsPipeline(
            llm_client=llm_client,
            config=config,
            interview_questions=interview_questions
        )
        
        # Update progress
        jobs[job_id]["progress"] = {
            "stage": "generating_agents",
            "message": f"Generating {n_agents} agent persona(s)..."
        }
        
        # Run pipeline stages
        logger.info(f"Job {job_id}: Running pipeline for '{product_idea}'")
        
        # Stage 1: Generate agents
        agents = await asyncio.to_thread(
            pipeline.generate_agents,
            product_idea,
            design_context,
            n_agents
        )
        
        jobs[job_id]["progress"] = {
            "stage": "simulating_experiences",
            "message": "Simulating user experiences..."
        }
        
        # Stage 2: Simulate experiences
        experiences = await asyncio.to_thread(
            pipeline.simulate_experiences,
            agents,
            product_idea
        )
        
        jobs[job_id]["progress"] = {
            "stage": "conducting_interviews",
            "message": "Conducting follow-up interviews..."
        }
        
        # Stage 3: Conduct interviews
        interviews = await asyncio.to_thread(
            pipeline.conduct_interviews,
            agents,
            experiences,
            product_idea
        )
        
        jobs[job_id]["progress"] = {
            "stage": "extracting_needs",
            "message": "Extracting latent needs..."
        }
        
        # Stage 4: Extract needs
        need_extractions = await asyncio.to_thread(
            pipeline.extract_latent_needs,
            agents,
            interviews,
            product_idea
        )
        
        # Aggregate results
        aggregated_needs = await asyncio.to_thread(
            pipeline.aggregate_needs,
            need_extractions
        )
        
        # Prepare results
        results = {
            "metadata": {
                "start_time": jobs[job_id]["start_time"],
                "end_time": datetime.now().isoformat(),
                "n_agents": n_agents,
                "design_context": design_context,
                "product": product_idea,
                "pipeline_version": "2.0.0",
                "status": "completed"
            },
            "agents": agents,
            "experiences": experiences,
            "interviews": interviews,
            "need_extractions": need_extractions,
            "aggregated_needs": aggregated_needs
        }
        
        # Save results
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pipeline_results_{timestamp}.json"
        results_path = results_dir / filename
        
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Update job
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["results"] = results
        jobs[job_id]["results_file"] = str(results_path)
        
        logger.info(f"Job {job_id}: Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Job {job_id}: Pipeline failed: {str(e)}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


# API Routes

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Elicitron API",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    Used by Render.com for uptime monitoring and auto-restart.
    """
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "elicitron-backend"
    }


@app.post("/api/analyze", response_model=JobResponse)
async def analyze(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    """
    Start a new requirements elicitation analysis.
    
    Returns a job_id for tracking progress.
    """
    job_id = str(uuid.uuid4())
    
    # Initialize job
    jobs[job_id] = {
        "status": "queued",
        "start_time": datetime.now().isoformat(),
        "product": request.product,
        "design_context": request.design_context,
        "n_agents": request.n_agents
    }
    
    # Add background task
    background_tasks.add_task(
        run_pipeline_async,
        job_id,
        request.product,
        request.design_context,
        request.n_agents
    )
    
    logger.info(f"Created job {job_id} for product: {request.product}")
    
    return JobResponse(
        job_id=job_id,
        status="queued",
        message="Analysis started. Use the job_id to check status."
    )


@app.get("/api/status/{job_id}", response_model=JobStatusResponse)
async def get_status(job_id: str):
    """
    Get the status of an analysis job.
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    return JobStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job.get("progress"),
        error=job.get("error")
    )


@app.get("/api/results/{job_id}", response_model=ResultsResponse)
async def get_results(job_id: str):
    """
    Get the results of a completed analysis job.
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job not completed. Current status: {job['status']}"
        )
    
    return ResultsResponse(
        job_id=job_id,
        status=job["status"],
        results=job.get("results")
    )


@app.get("/api/jobs")
async def list_jobs():
    """
    List all jobs (for debugging/admin).
    """
    return {
        "total": len(jobs),
        "jobs": [
            {
                "job_id": job_id,
                "status": job["status"],
                "product": job.get("product"),
                "start_time": job.get("start_time")
            }
            for job_id, job in jobs.items()
        ]
    }


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    """
    Delete a job from memory.
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    del jobs[job_id]
    return {"message": f"Job {job_id} deleted"}


if __name__ == "__main__":
    import uvicorn
    
    # Configure logging
    configure_logging()
    
    # Run server
    uvicorn.run(
        "app_fastapi:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (dev only)
        log_level="info"
    )
