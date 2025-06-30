"""
Answer Validation Demo
Demonstrates the answer validation functionality
"""

import asyncio
from services.answer_validator import AnswerValidator
from config.validation_settings import configure_validation, ValidationMode

class AnswerValidationDemo:
    """Demonstrate answer validation functionality"""
    
    def __init__(self):
        self.validator = AnswerValidator()
    
    def print_section(self, title: str):
        """Print a formatted section header"""
        print(f"\n{'='*60}")
        print(f"🎯 {title}")
        print(f"{'='*60}")
    
    async def demo_validation_modes(self):
        """Demonstrate different validation modes"""
        self.print_section("Validation Modes Demo")
        
        test_text = "The enhanced video processing system is designed to handle long-form content efficiently by implementing parallel processing capabilities. However, there are some considerations that need to be addressed..."
        
        print(f"📝 Test text: {test_text}")
        print(f"📝 Length: {len(test_text)} characters, {len(test_text.split())} words")
        
        # Test different validation modes
        modes = [
            ("Strict", ValidationMode.STRICT),
            ("Moderate", ValidationMode.MODERATE),
            ("Lenient", ValidationMode.LENIENT),
            ("Disabled", ValidationMode.DISABLED)
        ]
        
        for mode_name, mode in modes:
            print(f"\n🔧 Testing {mode_name} mode:")
            
            # Configure validation mode
            configure_validation(mode=mode)
            
            # Validate text
            result = await self.validator.validate_answer_completeness(test_text)
            
            print(f"  ✅ Complete: {result.is_complete}")
            print(f"  📊 Level: {result.completeness_level.value}")
            print(f"  🎯 Confidence: {result.confidence_score:.2f}")
            print(f"  ❌ Issues: {len(result.issues)}")
            
            if result.issues:
                for issue in result.issues[:2]:  # Show first 2 issues
                    print(f"    - {issue}")
    
    async def demo_complete_vs_incomplete(self):
        """Demonstrate complete vs incomplete answers"""
        self.print_section("Complete vs Incomplete Answers")
        
        # Configure strict mode
        configure_validation(mode=ValidationMode.STRICT)
        
        # Test cases
        test_cases = [
            {
                "name": "Complete Answer",
                "text": "The enhanced video processing system is designed to handle long-form content efficiently by implementing parallel processing capabilities. This approach allows multiple video segments to be generated simultaneously, significantly reducing overall processing time while maintaining high quality standards. The system automatically determines optimal chunk sizes based on content length and available resources, ensuring optimal performance across different scenarios. Thank you for your interest in our advanced video processing technology."
            },
            {
                "name": "Incomplete Answer (truncated)",
                "text": "The enhanced video processing system is designed to handle long-form content efficiently by implementing parallel processing capabilities. However, there are some considerations that need to be addressed..."
            },
            {
                "name": "Incomplete Answer (unfinished)",
                "text": "The enhanced video processing system is designed to handle long-form content efficiently by implementing parallel processing capabilities. While this approach provides significant benefits, there are some considerations that need to be addressed, particularly regarding resource allocation and error handling. Additionally, the system must account for various edge cases and"
            },
            {
                "name": "Short Answer",
                "text": "Yes, it works."
            }
        ]
        
        for case in test_cases:
            print(f"\n📝 Testing: {case['name']}")
            print(f"📝 Text: {case['text'][:100]}{'...' if len(case['text']) > 100 else ''}")
            
            result = await self.validator.validate_answer_completeness(case['text'])
            
            status = "✅ ACCEPTED" if result.is_complete else "❌ REJECTED"
            print(f"  {status}")
            print(f"  📊 Level: {result.completeness_level.value}")
            print(f"  🎯 Confidence: {result.confidence_score:.2f}")
            
            if result.issues:
                print(f"  ❌ Issues:")
                for issue in result.issues:
                    print(f"    - {issue}")
            
            if result.suggestions:
                print(f"  💡 Suggestions:")
                for suggestion in result.suggestions:
                    print(f"    - {suggestion}")
    
    async def demo_custom_validation(self):
        """Demonstrate custom validation configuration"""
        self.print_section("Custom Validation Configuration")
        
        # Configure custom validation settings
        configure_validation(
            mode=ValidationMode.MODERATE,
            min_words=8,
            min_sentences=1,
            min_length=40,
            min_confidence_score=0.5
        )
        
        print("🔧 Custom configuration applied:")
        print("  - Minimum words: 8")
        print("  - Minimum sentences: 1")
        print("  - Minimum length: 40 characters")
        print("  - Minimum confidence: 0.5")
        
        # Test with borderline case
        test_text = "The video processing system works well for most use cases. It handles parallel processing efficiently."
        
        print(f"\n📝 Testing borderline case:")
        print(f"📝 Text: {test_text}")
        print(f"📝 Length: {len(test_text)} characters, {len(test_text.split())} words")
        
        result = await self.validator.validate_answer_completeness(test_text)
        
        status = "✅ ACCEPTED" if result.is_complete else "❌ REJECTED"
        print(f"  {status}")
        print(f"  📊 Level: {result.completeness_level.value}")
        print(f"  🎯 Confidence: {result.confidence_score:.2f}")
    
    async def demo_validation_summary(self):
        """Demonstrate validation summary functionality"""
        self.print_section("Validation Summary Demo")
        
        # Configure moderate mode
        configure_validation(mode=ValidationMode.MODERATE)
        
        test_texts = [
            "The enhanced video processing system is excellent for handling long-form content with parallel processing capabilities.",
            "Yes, it works.",
            "The system is designed to handle content efficiently. However, there are some considerations..."
        ]
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n📝 Test {i}: {text[:50]}{'...' if len(text) > 50 else ''}")
            
            summary = await self.validator.get_validation_summary(text)
            
            print(f"  ✅ Complete: {summary['is_complete']}")
            print(f"  📊 Level: {summary['completeness_level']}")
            print(f"  🎯 Confidence: {summary['confidence_score']:.2f}")
            print(f"  📏 Length: {summary['text_length']} chars, {summary['word_count']} words")
            print(f"  ⏱️ Validation time: {summary['validation_time']:.3f}s")
    
    async def run_all_demos(self):
        """Run all demonstration scenarios"""
        print("🚀 Answer Validation System Demo")
        print("This demonstrates the system's ability to validate answer completeness")
        print("before allowing video generation.")
        
        demos = [
            self.demo_validation_modes(),
            self.demo_complete_vs_incomplete(),
            self.demo_custom_validation(),
            self.demo_validation_summary()
        ]
        
        for demo in demos:
            await demo
            print("\n" + "="*60)
        
        print("\n🎯 Summary:")
        print("✅ The answer validation system provides:")
        print("   - Multiple validation modes (strict, moderate, lenient, disabled)")
        print("   - Configurable thresholds and requirements")
        print("   - Detection of incomplete, truncated, and short answers")
        print("   - Confidence scoring and detailed feedback")
        print("   - Caching for performance optimization")
        print("   - Context-aware validation")
        print("\n🛡️ This ensures videos are only generated with complete, high-quality answers!")

async def main():
    """Main demo function"""
    demo = AnswerValidationDemo()
    await demo.run_all_demos()

if __name__ == "__main__":
    asyncio.run(main()) 