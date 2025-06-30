"""
VBVA Logging Service
Structured logging configuration
"""

import logging
import sys
from typing import Any, Dict, Optional
import structlog

def setup_logging() -> None:
    """Setup structured logging for the application"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)

def log_user_question(question: str, session_id: Optional[str] = None, agent_type: str = "general", request_type: str = "chat") -> None:
    """Log user questions clearly and prominently"""
    print(f"\n{'='*80}")
    print(f"💬 USER QUESTION ({request_type.upper()}): {question}")
    print(f"📋 Details: session_id={session_id}, agent_type={agent_type}")
    print(f"{'='*80}")

def log_video_generation_request(text: str, session_id: Optional[str] = None, agent_type: str = "general") -> None:
    """Log video generation requests clearly and prominently"""
    print(f"\n{'='*80}")
    print(f"🎬 VIDEO GENERATION REQUEST: {text}")
    print(f"📋 Details: session_id={session_id}, agent_type={agent_type}")
    print(f"{'='*80}")

def log_agent_response(response: str, agent_type: str = "general") -> None:
    """Log agent responses clearly"""
    print(f"\n🤖 {agent_type.upper()} AGENT RESPONSE:")
    print(f"   {response}")
    print(f"{'-'*80}")

def log_processing_step(step: str, duration: Optional[float] = None) -> None:
    """Log processing steps with timing"""
    if duration:
        print(f"⏱️  {step}: {duration:.2f}s")
    else:
        print(f"🔄 {step}")

def log_error(error: str, context: str = "") -> None:
    """Log errors clearly"""
    print(f"\n❌ ERROR in {context}: {error}")
    print(f"{'='*80}") 