"""
VBVA Agent Orchestrator
Main orchestrator for multi-agent system using LangGraph
"""

import asyncio
import uuid
from typing import Dict, List, Optional, AsyncGenerator, TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from pydantic import BaseModel

from config.settings import get_settings
from services.stt import STTService
from services.tts import TTSService
from services.lip_sync import LipSyncService
from services.answer_validator import AnswerValidator
from agents.base import BaseAgent
from agents.hotel_agent import HotelAgent
from agents.airport_agent import AirportAgent
from agents.sales_agent import SalesAgent
from services.logging import log_user_question, log_agent_response, log_processing_step, log_error

class AgentState(TypedDict):
    """State class for agent workflow"""
    session_id: str
    input_text: str
    agent_type: str
    response: Optional[str]
    audio_url: Optional[str]
    video_url: Optional[str]
    need_audio: bool
    need_video: bool
    validation_result: Optional[Dict]

class AgentOrchestrator:
    """Main orchestrator for the multi-agent system"""
    
    def __init__(self):
        self.settings = get_settings()
        self.llm = ChatOpenAI(
            api_key=self.settings.openai_api_key,
            model=self.settings.openai_model,
            temperature=0.7
        )
        
        # Initialize services
        self.stt_service = STTService()
        self.tts_service = TTSService()
        self.lip_sync_service = LipSyncService()
        self.answer_validator = AnswerValidator()
        
        # Initialize agents
        self.agents: Dict[str, BaseAgent] = {
            "general": BaseAgent(self.llm),
            "hotel": HotelAgent(self.llm),
            "airport": AirportAgent(self.llm),
            "sales": SalesAgent(self.llm)
        }
        
        # Session management
        self.sessions: Dict[str, Dict] = {}
        
        # Build the agent graph
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("route", self._route_request)
        workflow.add_node("process", self._process_with_agent)
        workflow.add_node("validate_answer", self._validate_answer)
        workflow.add_node("generate_audio", self._generate_audio)
        workflow.add_node("generate_video", self._generate_video)
        
        # Add edges
        workflow.add_edge("route", "process")
        workflow.add_edge("process", "validate_answer")
        workflow.add_edge("validate_answer", "generate_audio")
        workflow.add_edge("generate_audio", "generate_video")
        workflow.add_edge("generate_video", END)
        
        # Set entry point
        workflow.set_entry_point("route")
        
        return workflow.compile()
    
    async def process_text_request(
        self, 
        text: str, 
        session_id: Optional[str] = None,
        agent_type: str = "general"
    ) -> Dict:
        """Process text-based request with answer validation"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Clear logging of user question
        log_user_question(
            question=text,
            session_id=session_id,
            agent_type=agent_type,
            request_type="chat"
        )
        
        # Initialize session if needed
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "agent_type": agent_type,
                "messages": [],
                "context": {}
            }
        
        # Add user message to session
        self.sessions[session_id]["messages"].append(HumanMessage(content=text))
        
        # Prepare state for graph
        state = {
            "session_id": session_id,
            "input_text": text,
            "agent_type": agent_type,
            "need_audio": False,
            "need_video": False
        }
        
        log_processing_step("Preparing graph state")
        
        try:
            # Process through graph
            result = await self.graph.ainvoke(state)
            print(f"✅ Graph result: {result}")
            return result
        except Exception as e:
            log_error(f"Graph error: {e}", "process_text_request")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise
    
    async def process_voice_request(
        self,
        audio_file,
        session_id: Optional[str] = None,
        agent_type: str = "general"
    ) -> Dict:
        """Process voice-based request with answer validation"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Transcribe audio
        text = await self.stt_service.transcribe(audio_file)
        
        # Process text request with validation
        result = await self.process_text_request(text, session_id, agent_type)
        
        # Check if validation passed
        if not result.get("validation_result", {}).get("is_complete", True):
            raise Exception("Answer validation failed - incomplete response detected")
        
        # Generate audio response
        audio_url = await self.tts_service.generate_speech(result["response"])
        
        # Generate video with lip sync
        video_url = await self.lip_sync_service.generate_video(
            audio_url=audio_url,
            avatar_type=agent_type
        )
        
        return {
            "text": result["response"],
            "audio_url": audio_url,
            "video_url": video_url,
            "session_id": session_id,
            "validation_result": result.get("validation_result")
        }
    
    async def stream_response(self, session_id: str) -> AsyncGenerator[str, None]:
        """Stream real-time response"""
        if session_id not in self.sessions:
            yield "error: Session not found"
            return
        
        session = self.sessions[session_id]
        agent = self.agents[session["agent_type"]]
        
        async for chunk in agent.stream_response(session["messages"]):
            yield chunk
    
    def get_available_agents(self) -> List[str]:
        """Get list of available agent types"""
        return list(self.agents.keys())
    
    def reset_session(self, session_id: str) -> None:
        """Reset session context"""
        if session_id in self.sessions:
            self.sessions[session_id]["messages"] = []
            self.sessions[session_id]["context"] = {}
    
    async def _route_request(self, state: Dict) -> Dict:
        """Route request to appropriate agent"""
        return state
    
    async def _process_with_agent(self, state: Dict) -> Dict:
        """Process request with selected agent"""
        agent = self.agents[state["agent_type"]]
        response = await agent.process(state["input_text"], state["session_id"])
        
        log_agent_response(response, state["agent_type"])
        
        # Add response to session
        session_id = state["session_id"]
        self.sessions[session_id]["messages"].append(AIMessage(content=response))
        
        return {**state, "response": response}
    
    async def _validate_answer(self, state: Dict) -> Dict:
        """Validate answer completeness before proceeding"""
        response = state.get("response", "")
        if not response:
            return {**state, "validation_result": {"is_complete": False, "error": "No response to validate"}}
        
        # Set validation mode based on agent type
        agent_type = state.get("agent_type", "general")
        if agent_type in ["general", "poetry", "creative"]:
            from config.validation_settings import get_validation_settings, ValidationMode
            get_validation_settings().set_validation_mode(ValidationMode.LENIENT)
            strict_mode = False
        else:
            strict_mode = True
        
        # Validate answer completeness
        validation_result = await self.answer_validator.validate_answer_completeness(
            text=response,
            context={"original_question": state["input_text"]},
            strict_mode=strict_mode
        )
        
        # Log validation results
        print(f"🔍 Answer validation: {validation_result.completeness_level.value}")
        print(f"🔍 Confidence: {validation_result.confidence_score:.2f}")
        print(f"🔍 Issues: {len(validation_result.issues)}")
        
        # Convert validation result to dict for state
        validation_dict = {
            "is_complete": validation_result.is_complete,
            "completeness_level": validation_result.completeness_level.value,
            "confidence_score": validation_result.confidence_score,
            "issues": validation_result.issues,
            "suggestions": validation_result.suggestions,
            "validation_time": validation_result.validation_time,
            "text_length": validation_result.text_length,
            "word_count": validation_result.word_count
        }
        
        return {**state, "validation_result": validation_dict}
    
    async def _generate_audio(self, state: Dict) -> Dict:
        """Generate audio from text response"""
        if state.get("need_audio") and state.get("response"):
            audio_url = await self.tts_service.generate_speech(state["response"])
            return {**state, "audio_url": audio_url}
        return state
    
    async def _generate_video(self, state: Dict) -> Dict:
        """Generate video with lip sync"""
        if state.get("need_video") and state.get("audio_url"):
            video_url = await self.lip_sync_service.generate_video(
                audio_url=state["audio_url"],
                avatar_type=state["agent_type"]
            )
            return {**state, "video_url": video_url}
        return state 