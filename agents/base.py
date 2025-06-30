"""
VBVA Base Agent
Base class for all virtual assistant agents
"""

import asyncio
from typing import List, Dict, Optional, AsyncGenerator
from langchain.schema import HumanMessage, AIMessage, BaseMessage
from langchain_openai import ChatOpenAI

class BaseAgent:
    """Base agent class for all virtual assistants"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.name = "General Assistant"
        self.description = "A helpful virtual assistant"
        self.capabilities = ["text_processing", "conversation"]
        
        # Default system prompt
        self.system_prompt = """You are a helpful virtual assistant. 
        Respond in a natural, conversational manner.
        Keep responses concise and informative."""
    
    async def process(self, text: str, session_id: str) -> str:
        """Process user input and return response"""
        messages = [HumanMessage(content=text)]
        
        try:
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
    
    async def stream_response(self, messages: List[BaseMessage]) -> AsyncGenerator[str, None]:
        """Stream response tokens"""
        try:
            async for chunk in self.llm.astream(messages):
                if chunk.content:
                    yield chunk.content
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def get_prompt_template(self) -> str:
        """Get agent-specific prompt template"""
        return self.system_prompt
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return self.capabilities
    
    def get_info(self) -> Dict:
        """Get agent information"""
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "prompt_template": self.get_prompt_template()
        } 