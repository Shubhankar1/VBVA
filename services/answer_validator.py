"""
VBVA Answer Validation Service
Validates answer completeness before video generation to prevent partial responses
"""

import re
import time
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import os

from config.validation_settings import get_validation_settings, ValidationMode

class CompletenessLevel(Enum):
    """Answer completeness levels"""
    INCOMPLETE = "incomplete"
    PARTIAL = "partial"
    COMPLETE = "complete"
    VERIFIED = "verified"

@dataclass
class ValidationResult:
    """Result of answer validation"""
    is_complete: bool
    completeness_level: CompletenessLevel
    confidence_score: float
    issues: List[str]
    suggestions: List[str]
    validation_time: float
    text_length: int
    word_count: int
    sentence_count: int

class AnswerValidator:
    """Validates answer completeness before video generation"""
    
    def __init__(self):
        # Get validation settings
        self.settings = get_validation_settings()
        
        # Cache for validation results
        self.cache_dir = "/tmp/vbva_validation_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    async def validate_answer_completeness(
        self, 
        text: str, 
        context: Optional[Dict] = None,
        strict_mode: bool = True
    ) -> ValidationResult:
        """Validate if an answer is complete before video generation"""
        
        start_time = time.time()
        
        # Check if validation is disabled
        if not self.settings.is_validation_enabled():
            return ValidationResult(
                is_complete=True,
                completeness_level=CompletenessLevel.VERIFIED,
                confidence_score=1.0,
                issues=[],
                suggestions=[],
                validation_time=0.0,
                text_length=len(text),
                word_count=len(text.split()),
                sentence_count=len(re.split(r'[.!?]+', text.strip()))
            )
        
        # Check cache first
        cache_key = self._generate_cache_key(text, strict_mode)
        cached_result = await self._check_cache(cache_key)
        if cached_result:
            return cached_result
        
        # Get current configuration
        config = self.settings.get_config()
        mode_settings = self.settings.get_mode_settings()
        
        # Basic text analysis
        text_length = len(text)
        word_count = len(text.split())
        sentence_count = len(re.split(r'[.!?]+', text.strip()))
        
        # Initialize issues and suggestions
        issues = []
        suggestions = []
        
        # Check minimum requirements
        if word_count < mode_settings["min_words"]:
            issues.append(f"Answer too short: {word_count} words (minimum: {mode_settings['min_words']})")
            suggestions.append("Provide more detailed information")
        
        if sentence_count < mode_settings["min_sentences"]:
            issues.append(f"Answer lacks proper sentences: {sentence_count} sentences")
            suggestions.append("Structure the response with complete sentences")
        
        if text_length < mode_settings["min_length"]:
            issues.append(f"Answer too brief: {text_length} characters (minimum: {mode_settings['min_length']})")
            suggestions.append("Expand the response with more details")
        
        # Check for incomplete indicators (truncation, cutoffs, etc.)
        incomplete_count = 0
        incomplete_indicators = self.settings.get_incomplete_indicators()
        for category, patterns in incomplete_indicators.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    incomplete_count += 1
                    issues.append(f"Detected {category} indicator: '{pattern}'")
                    break
        
        if incomplete_count > mode_settings["max_incomplete_indicators"]:
            issues.append(f"Too many incomplete indicators: {incomplete_count}")
            suggestions.append("Complete the response before generating video")
        
        # Check for complete indicators
        complete_count = 0
        complete_indicators = self.settings.get_complete_indicators()
        for category, patterns in complete_indicators.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    complete_count += 1
                    break
        
        # Determine completeness level
        completeness_level = self._determine_completeness_level(
            issues, incomplete_count, complete_count, strict_mode, mode_settings
        )
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            issues, incomplete_count, complete_count, word_count, text_length, mode_settings
        )
        
        # Check against confidence threshold
        if confidence_score < mode_settings["min_confidence_score"]:
            issues.append(f"Confidence score too low: {confidence_score:.2f} (minimum: {mode_settings['min_confidence_score']})")
            suggestions.append("Improve answer completeness and clarity")
        
        # Determine if answer is complete
        is_complete = completeness_level in [CompletenessLevel.COMPLETE, CompletenessLevel.VERIFIED]
        
        # Create validation result
        validation_time = time.time() - start_time
        result = ValidationResult(
            is_complete=is_complete,
            completeness_level=completeness_level,
            confidence_score=confidence_score,
            issues=issues,
            suggestions=suggestions,
            validation_time=validation_time,
            text_length=text_length,
            word_count=word_count,
            sentence_count=sentence_count
        )
        
        # Cache the result if caching is enabled
        if config.enable_caching:
            await self._cache_result(cache_key, result)
        
        return result
    
    async def validate_session_completeness(
        self, 
        session_id: str, 
        session_data: Dict
    ) -> ValidationResult:
        """Validate if a session has a complete answer ready for video generation"""
        
        # Get the latest response from session
        messages = session_data.get("messages", [])
        if not messages:
            return ValidationResult(
                is_complete=False,
                completeness_level=CompletenessLevel.INCOMPLETE,
                confidence_score=0.0,
                issues=["No messages in session"],
                suggestions=["Start a conversation first"],
                validation_time=0.0,
                text_length=0,
                word_count=0,
                sentence_count=0
            )
        
        # Find the latest AI response
        latest_response = None
        for message in reversed(messages):
            if hasattr(message, 'content') and message.content:
                latest_response = message.content
                break
        
        if not latest_response:
            return ValidationResult(
                is_complete=False,
                completeness_level=CompletenessLevel.INCOMPLETE,
                confidence_score=0.0,
                issues=["No AI response found in session"],
                suggestions=["Wait for the AI to respond"],
                validation_time=0.0,
                text_length=0,
                word_count=0,
                sentence_count=0
            )
        
        # Validate the latest response
        return await self.validate_answer_completeness(latest_response, session_data)
    
    def _determine_completeness_level(
        self, 
        issues: List[str], 
        incomplete_count: int, 
        complete_count: int,
        strict_mode: bool,
        mode_settings: Dict
    ) -> CompletenessLevel:
        """Determine the completeness level based on validation results"""

        # If there are any issues, the answer is INCOMPLETE
        if issues:
            return CompletenessLevel.INCOMPLETE

        # No issues and sufficient complete indicators
        if complete_count >= mode_settings["min_complete_indicators"]:
            return CompletenessLevel.VERIFIED

        # No issues but insufficient complete indicators
        if incomplete_count == 0:
            return CompletenessLevel.COMPLETE

        # Some incomplete indicators but not too many
        if incomplete_count <= 1 and len(issues) <= 2:
            return CompletenessLevel.PARTIAL if strict_mode else CompletenessLevel.COMPLETE

        return CompletenessLevel.INCOMPLETE
    
    def _calculate_confidence_score(
        self, 
        issues: List[str], 
        incomplete_count: int, 
        complete_count: int,
        word_count: int,
        text_length: int,
        mode_settings: Dict
    ) -> float:
        """Calculate confidence score for answer completeness"""
        
        base_score = 1.0
        
        # Penalize for issues (more severe penalty)
        issue_penalty = len(issues) * 0.3  # Increased from 0.1
        base_score -= issue_penalty
        
        # Penalize for incomplete indicators
        incomplete_penalty = incomplete_count * 0.2
        base_score -= incomplete_penalty
        
        # Reward for complete indicators
        complete_bonus = complete_count * 0.1
        base_score += complete_bonus
        
        # Reward for sufficient length
        if word_count >= mode_settings["min_words"] * 1.5:
            base_score += 0.1
        if text_length >= mode_settings["min_length"] * 1.5:
            base_score += 0.1
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, base_score))
    
    def _generate_cache_key(self, text: str, strict_mode: bool) -> str:
        """Generate cache key for validation result"""
        content = f"{text}_{strict_mode}_validation"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    async def _check_cache(self, cache_key: str) -> Optional[ValidationResult]:
        """Check if validation result exists in cache"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    # Reconstruct ValidationResult from cache
                    return ValidationResult(
                        is_complete=cache_data["is_complete"],
                        completeness_level=CompletenessLevel(cache_data["completeness_level"]),
                        confidence_score=cache_data["confidence_score"],
                        issues=cache_data["issues"],
                        suggestions=cache_data["suggestions"],
                        validation_time=cache_data["validation_time"],
                        text_length=cache_data["text_length"],
                        word_count=cache_data["word_count"],
                        sentence_count=cache_data["sentence_count"]
                    )
            except Exception as e:
                print(f"Cache read error: {e}")
        return None
    
    async def _cache_result(self, cache_key: str, result: ValidationResult) -> None:
        """Cache validation result"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        try:
            cache_data = {
                "is_complete": result.is_complete,
                "completeness_level": result.completeness_level.value,
                "confidence_score": result.confidence_score,
                "issues": result.issues,
                "suggestions": result.suggestions,
                "validation_time": result.validation_time,
                "text_length": result.text_length,
                "word_count": result.word_count,
                "sentence_count": result.sentence_count
            }
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception as e:
            print(f"Cache write error: {e}")
    
    async def get_validation_summary(self, text: str) -> Dict:
        """Get a summary of validation results for logging"""
        result = await self.validate_answer_completeness(text)
        return {
            "is_complete": result.is_complete,
            "completeness_level": result.completeness_level.value,
            "confidence_score": result.confidence_score,
            "issue_count": len(result.issues),
            "text_length": result.text_length,
            "word_count": result.word_count,
            "validation_time": result.validation_time
        } 