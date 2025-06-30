"""
Test Answer Validation Service
Demonstrates the answer validation functionality to ensure complete answers
"""

import asyncio
import time
import requests
from typing import Dict, List

# API base URL
API_BASE = "http://localhost:8000"

class AnswerValidationTester:
    """Test answer validation functionality"""
    
    def __init__(self):
        self.test_results = []
    
    def print_section(self, title: str):
        """Print a formatted section header"""
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    async def test_complete_answer(self) -> Dict:
        """Test with a complete, well-formed answer"""
        self.print_section("Testing Complete Answer")
        
        complete_text = """
        The enhanced video processing system is designed to handle long-form content efficiently 
        by implementing parallel processing capabilities. This approach allows multiple video 
        segments to be generated simultaneously, significantly reducing overall processing time 
        while maintaining high quality standards. The system automatically determines optimal 
        chunk sizes based on content length and available resources, ensuring optimal performance 
        across different scenarios. Thank you for your interest in our advanced video processing technology.
        """.strip()
        
        print(f"📝 Text length: {len(complete_text)} characters")
        print(f"📝 Word count: {len(complete_text.split())} words")
        print("🔄 Testing video generation with complete answer...")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": complete_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 8
                },
                timeout=120
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Completed in {processing_time:.2f} seconds")
                print(f"🎥 Video URL: {result.get('video_url', 'N/A')}")
                
                details = result.get('processing_details', {})
                validation = details.get('validation', {})
                
                print(f"🔍 Validation Level: {validation.get('completeness_level', 'N/A')}")
                print(f"🔍 Confidence Score: {validation.get('confidence_score', 'N/A'):.2f}")
                print(f"⚙️ Processing Mode: {details.get('optimization_level', 'N/A')}")
                
                return {
                    "type": "complete",
                    "success": True,
                    "processing_time": processing_time,
                    "validation_level": validation.get('completeness_level'),
                    "confidence_score": validation.get('confidence_score')
                }
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"❌ Error: {response.text}")
                return {"type": "complete", "success": False, "error": response.text}
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Error: {str(e)}")
            return {"type": "complete", "success": False, "error": str(e)}
    
    async def test_incomplete_answer(self) -> Dict:
        """Test with an incomplete answer that should be rejected"""
        self.print_section("Testing Incomplete Answer")
        
        incomplete_text = "The enhanced video processing system is designed to handle long-form content efficiently by implementing parallel processing capabilities. However, there are some considerations that need to be addressed..."
        
        print(f"📝 Text length: {len(incomplete_text)} characters")
        print(f"📝 Word count: {len(incomplete_text.split())} words")
        print("🔄 Testing video generation with incomplete answer...")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": incomplete_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 8
                },
                timeout=120
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 400:
                error_detail = response.json()
                print(f"✅ Correctly rejected incomplete answer!")
                print(f"🔍 Validation Level: {error_detail.get('completeness_level', 'N/A')}")
                print(f"🔍 Confidence Score: {error_detail.get('confidence_score', 'N/A'):.2f}")
                print(f"❌ Issues: {error_detail.get('issues', [])}")
                print(f"💡 Suggestions: {error_detail.get('suggestions', [])}")
                
                return {
                    "type": "incomplete",
                    "success": True,  # Successfully rejected
                    "processing_time": processing_time,
                    "validation_level": error_detail.get('completeness_level'),
                    "confidence_score": error_detail.get('confidence_score'),
                    "issues": error_detail.get('issues')
                }
            else:
                print(f"❌ Unexpected response: {response.status_code}")
                print(f"❌ Response: {response.text}")
                return {"type": "incomplete", "success": False, "error": "Should have been rejected"}
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Error: {str(e)}")
            return {"type": "incomplete", "success": False, "error": str(e)}
    
    async def test_truncated_answer(self) -> Dict:
        """Test with a truncated answer that should be rejected"""
        self.print_section("Testing Truncated Answer")
        
        truncated_text = "The enhanced video processing system is designed to handle long-form content efficiently by implementing parallel processing capabilities. This approach allows multiple video segments to be generated simultaneously, significantly reducing overall processing time while maintaining high quality standards. The system automatically determines optimal chunk sizes based on content length and available resources, ensuring optimal performance across different scenarios. In summary, the key benefits include..."
        
        print(f"📝 Text length: {len(truncated_text)} characters")
        print(f"📝 Word count: {len(truncated_text.split())} words")
        print("🔄 Testing video generation with truncated answer...")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": truncated_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 8
                },
                timeout=120
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 400:
                error_detail = response.json()
                print(f"✅ Correctly rejected truncated answer!")
                print(f"🔍 Validation Level: {error_detail.get('completeness_level', 'N/A')}")
                print(f"🔍 Confidence Score: {error_detail.get('confidence_score', 'N/A'):.2f}")
                print(f"❌ Issues: {error_detail.get('issues', [])}")
                
                return {
                    "type": "truncated",
                    "success": True,  # Successfully rejected
                    "processing_time": processing_time,
                    "validation_level": error_detail.get('completeness_level'),
                    "confidence_score": error_detail.get('confidence_score'),
                    "issues": error_detail.get('issues')
                }
            else:
                print(f"❌ Unexpected response: {response.status_code}")
                return {"type": "truncated", "success": False, "error": "Should have been rejected"}
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Error: {str(e)}")
            return {"type": "truncated", "success": False, "error": str(e)}
    
    async def test_short_answer(self) -> Dict:
        """Test with a very short answer that should be rejected"""
        self.print_section("Testing Short Answer")
        
        short_text = "Yes, it works."
        
        print(f"📝 Text length: {len(short_text)} characters")
        print(f"📝 Word count: {len(short_text.split())} words")
        print("🔄 Testing video generation with short answer...")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": short_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 8
                },
                timeout=120
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 400:
                error_detail = response.json()
                print(f"✅ Correctly rejected short answer!")
                print(f"🔍 Validation Level: {error_detail.get('completeness_level', 'N/A')}")
                print(f"🔍 Confidence Score: {error_detail.get('confidence_score', 'N/A'):.2f}")
                print(f"❌ Issues: {error_detail.get('issues', [])}")
                
                return {
                    "type": "short",
                    "success": True,  # Successfully rejected
                    "processing_time": processing_time,
                    "validation_level": error_detail.get('completeness_level'),
                    "confidence_score": error_detail.get('confidence_score'),
                    "issues": error_detail.get('issues')
                }
            else:
                print(f"❌ Unexpected response: {response.status_code}")
                return {"type": "short", "success": False, "error": "Should have been rejected"}
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Error: {str(e)}")
            return {"type": "short", "success": False, "error": str(e)}
    
    async def run_all_tests(self):
        """Run all validation tests"""
        print("🚀 Starting Answer Validation Tests")
        print("This will test the system's ability to validate answer completeness")
        print("before allowing video generation.")
        
        # Run all tests
        tests = [
            self.test_complete_answer(),
            self.test_incomplete_answer(),
            self.test_truncated_answer(),
            self.test_short_answer()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ Test {i+1} failed with exception: {result}")
                self.test_results.append({"type": f"test_{i+1}", "success": False, "error": str(result)})
            else:
                self.test_results.append(result)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        self.print_section("Test Summary")
        
        successful_tests = [r for r in self.test_results if r.get("success")]
        failed_tests = [r for r in self.test_results if not r.get("success")]
        
        print(f"✅ Successful tests: {len(successful_tests)}")
        print(f"❌ Failed tests: {len(failed_tests)}")
        print(f"📊 Total tests: {len(self.test_results)}")
        
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            test_type = result.get("type", "unknown")
            success = result.get("success", False)
            status = "✅ PASS" if success else "❌ FAIL"
            
            if success:
                validation_level = result.get("validation_level", "N/A")
                confidence = result.get("confidence_score", "N/A")
                if isinstance(confidence, float):
                    confidence = f"{confidence:.2f}"
                print(f"  {status} {test_type}: {validation_level} (confidence: {confidence})")
            else:
                error = result.get("error", "Unknown error")
                print(f"  {status} {test_type}: {error}")
        
        print(f"\n🎯 Answer validation is working correctly if:")
        print(f"   ✅ Complete answers are accepted")
        print(f"   ❌ Incomplete answers are rejected")
        print(f"   ❌ Truncated answers are rejected")
        print(f"   ❌ Short answers are rejected")

async def main():
    """Main test function"""
    tester = AnswerValidationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 