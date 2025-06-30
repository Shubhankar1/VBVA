"""
VBVA Answer Validation Configuration
Configurable settings for answer completeness validation
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class ValidationMode(Enum):
    """Validation modes"""
    STRICT = "strict"
    MODERATE = "moderate"
    LENIENT = "lenient"
    DISABLED = "disabled"

@dataclass
class ValidationConfig:
    """Configuration for answer validation"""
    
    # Validation mode
    mode: ValidationMode = ValidationMode.STRICT
    
    # Minimum requirements
    min_words: int = 10
    min_sentences: int = 1
    min_length: int = 50
    
    # Maximum allowed incomplete indicators
    max_incomplete_indicators: int = 2
    
    # Minimum required complete indicators
    min_complete_indicators: int = 1
    
    # Confidence thresholds
    min_confidence_score: float = 0.6
    
    # Context validation (disabled - we don't judge answer correctness)
    enable_context_validation: bool = False
    context_similarity_threshold: float = 0.5
    
    # Caching
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600  # 1 hour
    
    # Logging
    enable_validation_logging: bool = True
    log_validation_details: bool = True

class ValidationSettings:
    """Global validation settings manager"""
    
    def __init__(self):
        self.config = ValidationConfig()
        self._load_default_settings()
    
    def _load_default_settings(self):
        """Load default validation settings"""
        # Default incomplete indicators
        self.incomplete_indicators = {
            "truncated": [
                r"\.\.\.$",  # Ends with ellipsis
                r"…$",       # Unicode ellipsis
                r"etc\.$",   # Ends with etc.
                r"and so on$",  # Ends with and so on
                r"and more$",   # Ends with and more
                r"\.\.\.$",     # Multiple dots
            ],
            "unfinished": [
                r"but\s+[^.]*$",  # Ends with "but" without completion
                r"however\s+[^.]*$",  # Ends with "however" without completion
                r"although\s+[^.]*$",  # Ends with "although" without completion
                r"while\s+[^.]*$",     # Ends with "while" without completion
                r"if\s+[^.]*$",        # Ends with "if" without completion
                r"when\s+[^.]*$",      # Ends with "when" without completion
            ],
        }
        
        # Default complete indicators
        self.complete_indicators = {
            "proper_ending": [
                r"[.!?]\s*$",  # Ends with proper punctuation
                r"thank you[.!?]?\s*$",  # Ends with thank you
                r"hope this helps[.!?]?\s*$",  # Ends with helpful conclusion
                r"let me know[.!?]?\s*$",  # Ends with invitation for follow-up
            ],
            "comprehensive": [
                r"in summary",  # Contains summary
                r"to conclude",  # Contains conclusion
                r"in conclusion",  # Contains conclusion
                r"therefore",  # Contains logical conclusion
                r"thus",  # Contains logical conclusion
            ]
        }
    
    def get_config(self) -> ValidationConfig:
        """Get current validation configuration"""
        return self.config
    
    def update_config(self, new_config: ValidationConfig):
        """Update validation configuration"""
        self.config = new_config
    
    def get_validation_mode(self) -> ValidationMode:
        """Get current validation mode"""
        return self.config.mode
    
    def set_validation_mode(self, mode: ValidationMode):
        """Set validation mode"""
        self.config.mode = mode
    
    def is_validation_enabled(self) -> bool:
        """Check if validation is enabled"""
        return self.config.mode != ValidationMode.DISABLED
    
    def get_minimum_requirements(self) -> Dict:
        """Get minimum requirements for validation"""
        return {
            "min_words": self.config.min_words,
            "min_sentences": self.config.min_sentences,
            "min_length": self.config.min_length,
            "max_incomplete_indicators": self.config.max_incomplete_indicators,
            "min_complete_indicators": self.config.min_complete_indicators
        }
    
    def get_confidence_threshold(self) -> float:
        """Get confidence threshold for validation"""
        return self.config.min_confidence_score
    
    def get_incomplete_indicators(self) -> Dict[str, List[str]]:
        """Get incomplete answer indicators"""
        return self.incomplete_indicators
    
    def get_complete_indicators(self) -> Dict[str, List[str]]:
        """Get complete answer indicators"""
        return self.complete_indicators
    
    def add_incomplete_indicator(self, category: str, pattern: str):
        """Add a custom incomplete indicator"""
        if category not in self.incomplete_indicators:
            self.incomplete_indicators[category] = []
        self.incomplete_indicators[category].append(pattern)
    
    def add_complete_indicator(self, category: str, pattern: str):
        """Add a custom complete indicator"""
        if category not in self.complete_indicators:
            self.complete_indicators[category] = []
        self.complete_indicators[category].append(pattern)
    
    def get_mode_settings(self) -> Dict:
        """Get settings based on current mode"""
        if self.config.mode == ValidationMode.STRICT:
            return {
                "min_words": 15,
                "min_sentences": 2,
                "min_length": 100,
                "max_incomplete_indicators": 1,
                "min_complete_indicators": 1,
                "min_confidence_score": 0.7
            }
        elif self.config.mode == ValidationMode.MODERATE:
            return {
                "min_words": 10,
                "min_sentences": 1,
                "min_length": 50,
                "max_incomplete_indicators": 2,
                "min_complete_indicators": 1,
                "min_confidence_score": 0.6
            }
        elif self.config.mode == ValidationMode.LENIENT:
            return {
                "min_words": 5,
                "min_sentences": 1,
                "min_length": 25,
                "max_incomplete_indicators": 3,
                "min_complete_indicators": 0,
                "min_confidence_score": 0.4
            }
        else:  # DISABLED
            return {
                "min_words": 0,
                "min_sentences": 0,
                "min_length": 0,
                "max_incomplete_indicators": 999,
                "min_complete_indicators": 0,
                "min_confidence_score": 0.0
            }

# Global validation settings instance
validation_settings = ValidationSettings()

def get_validation_settings() -> ValidationSettings:
    """Get global validation settings"""
    return validation_settings

def configure_validation(
    mode: ValidationMode = ValidationMode.STRICT,
    min_words: Optional[int] = None,
    min_sentences: Optional[int] = None,
    min_length: Optional[int] = None,
    max_incomplete_indicators: Optional[int] = None,
    min_complete_indicators: Optional[int] = None,
    min_confidence_score: Optional[float] = None
):
    """Configure validation settings"""
    settings = get_validation_settings()
    
    # Update mode
    settings.set_validation_mode(mode)
    
    # Get mode-based settings
    mode_settings = settings.get_mode_settings()
    
    # Create new config with provided overrides
    new_config = ValidationConfig(
        mode=mode,
        min_words=min_words if min_words is not None else mode_settings["min_words"],
        min_sentences=min_sentences if min_sentences is not None else mode_settings["min_sentences"],
        min_length=min_length if min_length is not None else mode_settings["min_length"],
        max_incomplete_indicators=max_incomplete_indicators if max_incomplete_indicators is not None else mode_settings["max_incomplete_indicators"],
        min_complete_indicators=min_complete_indicators if min_complete_indicators is not None else mode_settings["min_complete_indicators"],
        min_confidence_score=min_confidence_score if min_confidence_score is not None else mode_settings["min_confidence_score"]
    )
    
    settings.update_config(new_config)
    return settings 