"""
VBVA Airport Assistant Agent
Specialized agent for airport information and travel assistance
"""

from typing import List, Dict
from langchain.schema import HumanMessage, SystemMessage
from agents.base import BaseAgent

class AirportAgent(BaseAgent):
    """Airport assistant agent for travel information"""
    
    def __init__(self, llm):
        super().__init__(llm)
        self.name = "Airport Assistant"
        self.description = "Helpful airport assistant for travel information and guidance"
        self.capabilities = [
            "text_processing", 
            "conversation", 
            "flight_information",
            "travel_assistance",
            "airport_guidance"
        ]
        
        # Airport-specific system prompt
        self.system_prompt = """You are a helpful airport assistant named Alex. 
        You work at the International Airport and provide travel assistance to passengers.
        
        Your responsibilities include:
        - Providing flight information and status updates
        - Assisting with check-in and boarding procedures
        - Guiding passengers to gates and facilities
        - Providing information about airport services and amenities
        - Helping with travel documentation and requirements
        - Assisting with baggage and security procedures
        - Providing local transportation information
        
        Airport Information:
        - Location: Major international airport
        - Terminals: 3 terminals (A, B, C)
        - Services: Free WiFi, restaurants, shops, lounges, medical center
        - Transportation: Taxi, rideshare, public transit, rental cars
        - Security: TSA PreCheck available, standard security procedures
        
        Always be helpful, patient, and clear in your instructions.
        If you don't have specific information, direct passengers to the information desk."""
    
    async def process(self, text: str, session_id: str) -> str:
        """Process airport-specific requests"""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=text)
        ]
        
        try:
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            return f"I apologize, but I'm having trouble accessing that information. Please visit the information desk for assistance."
    
    def get_airport_services(self) -> List[str]:
        """Get available airport services"""
        return [
            "Flight information and status",
            "Check-in assistance",
            "Gate directions and navigation",
            "Security procedure guidance",
            "Baggage assistance",
            "Restaurant and dining options",
            "Shopping and retail",
            "Airport lounges",
            "Medical and first aid",
            "Transportation services",
            "Currency exchange",
            "Lost and found"
        ]
    
    def get_terminal_info(self) -> Dict[str, Dict]:
        """Get terminal information"""
        return {
            "terminal_a": {
                "description": "Domestic flights",
                "airlines": ["Delta", "American", "Southwest"],
                "gates": "A1-A30",
                "services": ["Restaurants", "Shops", "Lounges", "Medical Center"]
            },
            "terminal_b": {
                "description": "International flights",
                "airlines": ["United", "British Airways", "Lufthansa"],
                "gates": "B1-B25",
                "services": ["Duty-free shops", "International lounges", "Currency exchange"]
            },
            "terminal_c": {
                "description": "Regional and charter flights",
                "airlines": ["JetBlue", "Spirit", "Frontier"],
                "gates": "C1-C20",
                "services": ["Quick-service restaurants", "Convenience stores"]
            }
        }
    
    def get_security_info(self) -> Dict[str, str]:
        """Get security procedure information"""
        return {
            "standard_security": "Standard TSA security screening required for all passengers",
            "tsa_precheck": "Available for enrolled passengers - expedited screening",
            "prohibited_items": "Liquids over 3.4oz, weapons, explosives prohibited",
            "electronics": "Laptops and large electronics must be removed from bags",
            "shoes": "Shoes must be removed for screening",
            "wait_times": "Typical wait times: 15-30 minutes (varies by time of day)"
        } 