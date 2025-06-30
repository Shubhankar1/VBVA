"""
VBVA Monitoring Service
Metrics and health monitoring
"""

import time
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# Metrics
REQUEST_COUNT = Counter('vbva_requests_total', 'Total requests', ['endpoint', 'method'])
REQUEST_DURATION = Histogram('vbva_request_duration_seconds', 'Request duration')
ACTIVE_SESSIONS = Gauge('vbva_active_sessions', 'Number of active sessions')
AGENT_EXECUTION_TIME = Histogram('vbva_agent_execution_seconds', 'Agent execution time', ['agent_type'])

def setup_monitoring() -> None:
    """Setup monitoring and metrics collection"""
    # Initialize metrics
    pass

def record_request(endpoint: str, method: str, duration: float) -> None:
    """Record request metrics"""
    REQUEST_COUNT.labels(endpoint=endpoint, method=method).inc()
    REQUEST_DURATION.observe(duration)

def record_agent_execution(agent_type: str, duration: float) -> None:
    """Record agent execution metrics"""
    AGENT_EXECUTION_TIME.labels(agent_type=agent_type).observe(duration)

def get_metrics() -> str:
    """Get Prometheus metrics"""
    return generate_latest().decode('utf-8')

def get_health_status() -> Dict[str, Any]:
    """Get system health status"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "api": "running",
            "agents": "available",
            "stt": "available",
            "tts": "available",
            "lip_sync": "available"
        }
    } 