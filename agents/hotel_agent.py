"""
VBVA Hotel Receptionist Agent
Specialized agent for hotel reception and guest services
"""

from typing import List, Dict
from langchain.schema import HumanMessage, SystemMessage
from agents.base import BaseAgent

class HotelAgent(BaseAgent):
    """Hotel receptionist agent for guest services"""
    
    def __init__(self, llm):
        super().__init__(llm)
        self.name = "Hotel Receptionist"
        self.description = "Professional hotel receptionist for guest services"
        self.capabilities = [
            "text_processing", 
            "conversation", 
            "hotel_services",
            "booking_assistance",
            "guest_support"
        ]
        
        # Hotel-specific system prompt
        self.system_prompt = """You are a professional hotel receptionist named Sarah. 
        You work at the Grand Plaza Hotel and provide excellent guest services.
        
        Your responsibilities include:
        - Greeting guests warmly and professionally
        - Assisting with check-in and check-out procedures
        - Providing information about hotel amenities and services
        - Helping with room bookings and modifications
        - Addressing guest concerns and requests
        - Providing local area recommendations
        
        Hotel Information:
        - Location: Downtown business district
        - Amenities: Free WiFi, 24/7 room service, fitness center, spa, restaurant
        - Room types: Standard, Deluxe, Suite, Presidential Suite
        - Check-in: 3:00 PM, Check-out: 11:00 AM
        
        Always be polite, professional, and helpful. Use a warm, welcoming tone.
        If you don't know specific details, offer to connect the guest with the appropriate department."""
    
    async def process(self, text: str, session_id: str) -> str:
        """Process hotel-specific requests"""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=text)
        ]
        
        try:
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Please let me connect you with our front desk team."
    
    def get_hotel_services(self) -> List[str]:
        """Get available hotel services"""
        return [
            "Room booking and reservations",
            "Check-in and check-out assistance",
            "Concierge services",
            "Room service",
            "Spa and wellness",
            "Restaurant reservations",
            "Local area information",
            "Transportation assistance",
            "Business center services",
            "Housekeeping requests"
        ]
    
    def get_room_types(self) -> Dict[str, Dict]:
        """Get available room types and pricing"""
        return {
            "standard": {
                "description": "Comfortable room with city view",
                "price": "$150/night",
                "amenities": ["King bed", "Free WiFi", "TV", "Mini fridge"]
            },
            "deluxe": {
                "description": "Spacious room with premium amenities",
                "price": "$250/night", 
                "amenities": ["King bed", "Free WiFi", "TV", "Mini fridge", "Balcony", "Premium toiletries"]
            },
            "suite": {
                "description": "Luxury suite with separate living area",
                "price": "$400/night",
                "amenities": ["King bed", "Living room", "Free WiFi", "TV", "Mini fridge", "Balcony", "Premium toiletries", "Kitchenette"]
            },
            "presidential": {
                "description": "Ultimate luxury with panoramic views",
                "price": "$800/night",
                "amenities": ["King bed", "Living room", "Dining area", "Free WiFi", "TV", "Mini fridge", "Balcony", "Premium toiletries", "Full kitchen", "Butler service"]
            }
        } 