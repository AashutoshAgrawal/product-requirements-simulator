"""
Analytics and metrics collection for pipeline execution.
"""
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class AnalyticsCollector:
    """Collects and aggregates analytics during pipeline execution."""
    
    def __init__(self):
        self.api_calls: List[Dict[str, Any]] = []
        self.stage_metrics: Dict[str, Dict[str, Any]] = {}
        self.activity_log: List[Dict[str, Any]] = []
        self.start_time: Optional[float] = time.time()
        self.agent_metrics: Dict[str, Dict[str, Any]] = {}
        
    def start_tracking(self):
        """Start tracking pipeline execution."""
        self.start_time = time.time()
        self.log_activity("info", "Pipeline initialized", {})
        
    def track_api_call(
        self,
        call_id: str,
        stage: str,
        agent_id: Optional[str] = None,
        start_time: float = None,
        end_time: float = None,
        input_tokens: int = 0,
        output_tokens: int = 0,
        model: str = "",
        status: str = "success",
        error: Optional[str] = None,
        retry_count: int = 0
    ):
        """Track an API call with detailed metrics."""
        duration = end_time - start_time if start_time and end_time else 0
        total_tokens = input_tokens + output_tokens
        
        # Calculate cost (approximate - can be made configurable)
        cost = self._calculate_cost(model, input_tokens, output_tokens)
        
        call_data = {
            "call_id": call_id,
            "stage": stage,
            "agent_id": agent_id,
            "timestamp": datetime.fromtimestamp(end_time).isoformat() if end_time else datetime.now().isoformat(),
            "duration": round(duration, 2),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "model": model,
            "cost": round(cost, 4),
            "status": status,
            "error": error,
            "retry_count": retry_count
        }
        
        self.api_calls.append(call_data)
        
        # Log activity
        if status == "success":
            # Create descriptive message with agent info
            stage_display = stage.replace('_', ' ').title()
            agent_prefix = f"Agent {agent_id} - " if agent_id else ""
            self.log_activity(
                "api_success",
                f"{agent_prefix}{stage_display} completed",
                {
                    "agent_id": agent_id,
                    "duration": duration,
                    "tokens": total_tokens,
                    "cost": cost
                }
            )
        elif status == "error":
            stage_display = stage.replace('_', ' ').title()
            agent_prefix = f"Agent {agent_id} - " if agent_id else ""
            self.log_activity(
                "api_error",
                f"{agent_prefix}{stage_display} failed",
                {"agent_id": agent_id, "error": error, "retry_count": retry_count}
            )
            
        # Update agent metrics
        if agent_id:
            if agent_id not in self.agent_metrics:
                self.agent_metrics[agent_id] = {
                    "stages": {},
                    "total_duration": 0,
                    "total_cost": 0,
                    "total_tokens": 0
                }
            
            if stage not in self.agent_metrics[agent_id]["stages"]:
                self.agent_metrics[agent_id]["stages"][stage] = {
                    "duration": 0,
                    "tokens": 0,
                    "cost": 0,
                    "calls": 0
                }
            
            self.agent_metrics[agent_id]["stages"][stage]["duration"] += duration
            self.agent_metrics[agent_id]["stages"][stage]["tokens"] += total_tokens
            self.agent_metrics[agent_id]["stages"][stage]["cost"] += cost
            self.agent_metrics[agent_id]["stages"][stage]["calls"] += 1
            self.agent_metrics[agent_id]["total_duration"] += duration
            self.agent_metrics[agent_id]["total_cost"] += cost
            self.agent_metrics[agent_id]["total_tokens"] += total_tokens
    
    def track_stage(
        self,
        stage_name: str,
        start_time: float,
        end_time: float,
        items_processed: int = 0,
        status: str = "completed"
    ):
        """Track a pipeline stage."""
        duration = end_time - start_time
        
        self.stage_metrics[stage_name] = {
            "start_time": datetime.fromtimestamp(start_time).isoformat(),
            "end_time": datetime.fromtimestamp(end_time).isoformat(),
            "duration": round(duration, 2),
            "items_processed": items_processed,
            "status": status
        }
        
        self.log_activity(
            "stage_complete",
            f"{stage_name} stage completed",
            {"duration": duration, "items": items_processed}
        )
    
    def log_activity(
        self,
        event_type: str,
        message: str,
        metadata: Dict[str, Any]
    ):
        """Log an activity event."""
        self.activity_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "message": message,
            "metadata": metadata
        })
    
    def log_warning(self, message: str, metadata: Dict[str, Any] = None):
        """Log a warning event."""
        self.log_activity("warning", message, metadata or {})
    
    def log_error(self, message: str, metadata: Dict[str, Any] = None):
        """Log an error event."""
        self.log_activity("error", message, metadata or {})
    
    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate approximate cost based on model and tokens."""
        # Pricing per 1K tokens (approximate as of 2024)
        pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
            "gemini-pro": {"input": 0.00025, "output": 0.0005},
            "gemini-1.5-pro": {"input": 0.00125, "output": 0.00375},
        }
        
        # Default pricing if model not found
        default_pricing = {"input": 0.01, "output": 0.03}
        
        model_lower = model.lower()
        model_pricing = default_pricing
        
        for key in pricing:
            if key in model_lower:
                model_pricing = pricing[key]
                break
        
        input_cost = (input_tokens / 1000) * model_pricing["input"]
        output_cost = (output_tokens / 1000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive analytics summary."""
        total_duration = time.time() - self.start_time if self.start_time else 0
        
        # Calculate totals
        total_calls = len(self.api_calls)
        successful_calls = len([c for c in self.api_calls if c["status"] == "success"])
        failed_calls = len([c for c in self.api_calls if c["status"] == "error"])
        total_tokens = sum(c["total_tokens"] for c in self.api_calls)
        total_cost = sum(c["cost"] for c in self.api_calls)
        total_api_duration = sum(c["duration"] for c in self.api_calls)
        
        # Calculate averages
        avg_latency = total_api_duration / total_calls if total_calls > 0 else 0
        
        # Find extremes
        if self.api_calls:
            slowest_call = max(self.api_calls, key=lambda x: x["duration"])
            fastest_call = min(self.api_calls, key=lambda x: x["duration"])
        else:
            slowest_call = fastest_call = None
        
        # Stage breakdown
        stage_breakdown = {}
        for stage_name, stage_data in self.stage_metrics.items():
            stage_calls = [c for c in self.api_calls if c["stage"] == stage_name]
            stage_breakdown[stage_name] = {
                "duration": stage_data["duration"],
                "items": stage_data["items_processed"],
                "api_calls": len(stage_calls),
                "tokens": sum(c["total_tokens"] for c in stage_calls),
                "cost": sum(c["cost"] for c in stage_calls)
            }
        
        # Agent performance
        agent_performance = []
        for agent_id, metrics in self.agent_metrics.items():
            agent_performance.append({
                "agent_id": agent_id,
                "total_duration": round(metrics["total_duration"], 2),
                "total_cost": round(metrics["total_cost"], 4),
                "total_tokens": metrics["total_tokens"],
                "stages": {
                    stage: {
                        "duration": round(data["duration"], 2),
                        "tokens": data["tokens"],
                        "cost": round(data["cost"], 4)
                    }
                    for stage, data in metrics["stages"].items()
                }
            })
        
        # Sort agents by duration
        agent_performance.sort(key=lambda x: x["total_duration"])
        
        return {
            "overview": {
                "total_duration": round(total_duration, 2),
                "total_api_calls": total_calls,
                "successful_calls": successful_calls,
                "failed_calls": failed_calls,
                "total_tokens": total_tokens,
                "total_cost": round(total_cost, 4),
                "avg_latency": round(avg_latency, 2),
                "tokens_per_second": round(total_tokens / total_duration, 2) if total_duration > 0 else 0
            },
            "stage_breakdown": stage_breakdown,
            "agent_performance": agent_performance,
            "api_calls": self.api_calls,
            "activity_log": self.activity_log,
            "extremes": {
                "slowest_call": slowest_call,
                "fastest_call": fastest_call,
                "most_expensive_agent": agent_performance[-1] if agent_performance else None,
                "fastest_agent": agent_performance[0] if agent_performance else None
            }
        }
    
    def export_to_dict(self) -> Dict[str, Any]:
        """Export all analytics data."""
        return {
            "summary": self.get_summary(),
            "raw_data": {
                "api_calls": self.api_calls,
                "stage_metrics": self.stage_metrics,
                "agent_metrics": self.agent_metrics,
                "activity_log": self.activity_log
            }
        }
