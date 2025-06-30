"""
VBVA Sales Agent
Specialized agent for property and product sales assistance
"""

from typing import List, Dict
from langchain.schema import HumanMessage, SystemMessage
from agents.base import BaseAgent

class SalesAgent(BaseAgent):
    """Sales agent for property and product sales"""
    
    def __init__(self, llm):
        super().__init__(llm)
        self.name = "Sales Agent"
        self.description = "Professional sales agent for property and product assistance"
        self.capabilities = [
            "text_processing", 
            "conversation", 
            "sales_assistance",
            "property_information",
            "product_guidance"
        ]
        
        # Sales-specific system prompt
        self.system_prompt = """You are a professional sales agent named Michael. 
        You specialize in property sales and provide excellent customer service.
        
        Your responsibilities include:
        - Understanding customer needs and preferences
        - Providing detailed property information and specifications
        - Assisting with property viewings and tours
        - Explaining financing options and payment plans
        - Answering questions about neighborhoods and amenities
        - Following up with potential buyers
        - Providing market insights and pricing information
        
        Sales Approach:
        - Be professional, knowledgeable, and trustworthy
        - Listen carefully to customer needs
        - Provide accurate and detailed information
        - Be patient and helpful throughout the process
        - Offer to schedule viewings or consultations when appropriate
        
        Always maintain a professional tone and focus on helping customers find the right property.
        If you don't have specific information, offer to connect them with the appropriate specialist."""
    
    async def process(self, text: str, session_id: str) -> str:
        """Process sales-specific requests"""
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=text)
        ]
        
        try:
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            return f"I apologize, but I'm having trouble accessing that information. Let me connect you with our sales team for personalized assistance."
    
    def get_property_types(self) -> List[str]:
        """Get available property types"""
        return [
            "Single-family homes",
            "Condominiums",
            "Townhouses",
            "Apartments",
            "Luxury estates",
            "Investment properties",
            "Commercial properties",
            "Land and development"
        ]
    
    def get_sample_properties(self) -> Dict[str, Dict]:
        """Get sample property listings"""
        return {
            "property_1": {
                "type": "Single-family home",
                "price": "$450,000",
                "bedrooms": 3,
                "bathrooms": 2,
                "sqft": 1800,
                "location": "Suburban neighborhood",
                "features": ["Updated kitchen", "Large backyard", "Garage", "Good schools"]
            },
            "property_2": {
                "type": "Luxury condo",
                "price": "$750,000",
                "bedrooms": 2,
                "bathrooms": 2,
                "sqft": 1200,
                "location": "Downtown area",
                "features": ["City views", "Concierge", "Fitness center", "Parking included"]
            },
            "property_3": {
                "type": "Investment property",
                "price": "$300,000",
                "bedrooms": 4,
                "bathrooms": 2,
                "sqft": 2000,
                "location": "University area",
                "features": ["Rental income potential", "Large lot", "Renovation opportunity"]
            }
        }
    
    def get_financing_options(self) -> Dict[str, str]:
        """Get financing information"""
        return {
            "conventional_loan": "Traditional mortgage with 20% down payment",
            "fha_loan": "Government-backed loan with lower down payment (3.5%)",
            "va_loan": "Veterans Affairs loan for eligible service members",
            "usda_loan": "Rural development loan for eligible areas",
            "cash_purchase": "Direct cash purchase option",
            "investment_loan": "Specialized financing for investment properties"
        }
    
    def get_neighborhood_info(self) -> Dict[str, Dict]:
        """Get neighborhood information"""
        return {
            "downtown": {
                "description": "Urban center with shopping, dining, and entertainment",
                "schools": "Excellent public and private schools",
                "transportation": "Public transit, walkable, bike-friendly",
                "amenities": "Restaurants, shops, parks, cultural venues"
            },
            "suburban": {
                "description": "Family-friendly residential area",
                "schools": "Top-rated public schools",
                "transportation": "Easy highway access, good for commuting",
                "amenities": "Parks, community centers, shopping centers"
            },
            "university": {
                "description": "College town with academic atmosphere",
                "schools": "University and associated schools",
                "transportation": "Public transit, bike-friendly",
                "amenities": "Cafes, bookstores, cultural events, sports"
            }
        } 