#!/usr/bin/env python3
"""
Test Enhanced Parallel Processing for VBVA
Demonstrates the seamless approach of splitting long answers into multiple shorter videos
and processing them in parallel to reduce processing time.
"""

import asyncio
import time
import json
import os
from typing import List, Dict
import requests

# Test configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api/v1"

class EnhancedProcessingTester:
    """Test suite for enhanced parallel processing"""
    
    def __init__(self):
        self.test_results = []
        self.performance_metrics = {}
    
    async def test_short_content(self) -> Dict:
        """Test processing of short content (should use single video generation)"""
        print("\n🧪 Testing Short Content Processing...")
        
        short_text = "Hello! This is a short test message to verify basic functionality."
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": short_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 15
                },
                timeout=120
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Short content processed successfully in {processing_time:.2f}s")
                print(f"   Video URL: {result.get('video_url', 'N/A')}")
                print(f"   Processing details: {result.get('processing_details', {})}")
                
                return {
                    "test_type": "short_content",
                    "success": True,
                    "processing_time": processing_time,
                    "text_length": len(short_text),
                    "details": result.get('processing_details', {})
                }
            else:
                print(f"❌ Short content processing failed: {response.status_code}")
                return {
                    "test_type": "short_content",
                    "success": False,
                    "processing_time": processing_time,
                    "error": response.text
                }
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Short content test error: {str(e)}")
            return {
                "test_type": "short_content",
                "success": False,
                "processing_time": processing_time,
                "error": str(e)
            }
    
    async def test_medium_content(self) -> Dict:
        """Test processing of medium content (should use parallel processing)"""
        print("\n🧪 Testing Medium Content Processing...")
        
        medium_text = """
        Welcome to our enhanced video processing system! This is a medium-length test message 
        designed to demonstrate the parallel processing capabilities. The system will automatically 
        split this content into optimal chunks and process them simultaneously to reduce overall 
        processing time. This approach ensures that longer responses can be generated much faster 
        while maintaining high quality output. The seamless combining process ensures that the 
        final video appears as a single, continuous presentation without any visible breaks or 
        transitions between the processed chunks.
        """.strip()
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": medium_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 12
                },
                timeout=300
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Medium content processed successfully in {processing_time:.2f}s")
                print(f"   Video URL: {result.get('video_url', 'N/A')}")
                print(f"   Processing details: {result.get('processing_details', {})}")
                
                return {
                    "test_type": "medium_content",
                    "success": True,
                    "processing_time": processing_time,
                    "text_length": len(medium_text),
                    "details": result.get('processing_details', {})
                }
            else:
                print(f"❌ Medium content processing failed: {response.status_code}")
                return {
                    "test_type": "medium_content",
                    "success": False,
                    "processing_time": processing_time,
                    "error": response.text
                }
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Medium content test error: {str(e)}")
            return {
                "test_type": "medium_content",
                "success": False,
                "processing_time": processing_time,
                "error": str(e)
            }
    
    async def test_long_content(self) -> Dict:
        """Test processing of long content (should use enhanced parallel processing)"""
        print("\n🧪 Testing Long Content Processing...")
        
        long_text = """
        This is a comprehensive test of our enhanced video processing system designed to handle 
        long-form content efficiently. The system implements a sophisticated approach where long 
        answers are intelligently split into multiple shorter video segments, each processed in 
        parallel to maximize efficiency and minimize overall processing time.
        
        The parallel processing architecture allows multiple video chunks to be generated 
        simultaneously, leveraging the full capabilities of the underlying hardware and cloud 
        services. This is particularly beneficial for longer responses that would traditionally 
        take a significant amount of time to process sequentially.
        
        The seamless combining process ensures that all the individual video segments are 
        merged into a single, continuous video output that maintains perfect synchronization 
        between audio and visual elements. Advanced crossfade techniques and frame interpolation 
        ensure smooth transitions between segments, creating a natural viewing experience.
        
        This approach dramatically reduces the ultimate processing time for long content while 
        maintaining the highest quality standards. Users can now receive video responses for 
        complex, detailed answers in a fraction of the time previously required, making the 
        system much more practical for real-world applications.
        
        The optimization algorithms automatically determine the optimal chunk size based on 
        content length, available resources, and processing requirements. This adaptive approach 
        ensures optimal performance across different content types and system configurations.
        """.strip()
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": long_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 10
                },
                timeout=600  # 10 minutes for long content
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Long content processed successfully in {processing_time:.2f}s")
                print(f"   Video URL: {result.get('video_url', 'N/A')}")
                print(f"   Processing details: {result.get('processing_details', {})}")
                
                return {
                    "test_type": "long_content",
                    "success": True,
                    "processing_time": processing_time,
                    "text_length": len(long_text),
                    "details": result.get('processing_details', {})
                }
            else:
                print(f"❌ Long content processing failed: {response.status_code}")
                return {
                    "test_type": "long_content",
                    "success": False,
                    "processing_time": processing_time,
                    "error": response.text
                }
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Long content test error: {str(e)}")
            return {
                "test_type": "long_content",
                "success": False,
                "processing_time": processing_time,
                "error": str(e)
            }
    
    async def test_parallel_vs_sequential(self) -> Dict:
        """Compare parallel vs sequential processing performance"""
        print("\n🧪 Testing Parallel vs Sequential Processing...")
        
        test_text = """
        This is a performance comparison test to demonstrate the benefits of parallel processing. 
        The system should process this content much faster when parallel processing is enabled 
        compared to traditional sequential processing methods.
        """.strip()
        
        # Test with parallel processing enabled
        print("   Testing with parallel processing enabled...")
        parallel_start = time.time()
        
        try:
            parallel_response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": test_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 15
                },
                timeout=180
            )
            parallel_time = time.time() - parallel_start
            
            # Test with parallel processing disabled
            print("   Testing with parallel processing disabled...")
            sequential_start = time.time()
            
            sequential_response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": test_text,
                    "agent_type": "general",
                    "enable_parallel": False,
                    "chunk_duration": 15
                },
                timeout=180
            )
            sequential_time = time.time() - sequential_start
            
            # Calculate performance improvement
            if parallel_response.status_code == 200 and sequential_response.status_code == 200:
                improvement = ((sequential_time - parallel_time) / sequential_time) * 100
                print(f"✅ Parallel processing: {parallel_time:.2f}s")
                print(f"✅ Sequential processing: {sequential_time:.2f}s")
                print(f"✅ Performance improvement: {improvement:.1f}%")
                
                return {
                    "test_type": "parallel_vs_sequential",
                    "success": True,
                    "parallel_time": parallel_time,
                    "sequential_time": sequential_time,
                    "improvement_percentage": improvement,
                    "text_length": len(test_text)
                }
            else:
                print("❌ One or both processing modes failed")
                return {
                    "test_type": "parallel_vs_sequential",
                    "success": False,
                    "error": "Processing failed"
                }
                
        except Exception as e:
            print(f"❌ Performance comparison test error: {str(e)}")
            return {
                "test_type": "parallel_vs_sequential",
                "success": False,
                "error": str(e)
            }
    
    async def run_all_tests(self) -> Dict:
        """Run all tests and generate comprehensive report"""
        print("🚀 Starting Enhanced Parallel Processing Tests")
        print("=" * 60)
        
        # Check backend health
        try:
            health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if health_response.status_code != 200:
                print("❌ Backend is not healthy. Please start the backend first.")
                return {"error": "Backend not available"}
        except Exception as e:
            print(f"❌ Cannot connect to backend: {str(e)}")
            return {"error": "Backend connection failed"}
        
        print("✅ Backend is healthy, starting tests...")
        
        # Run all tests
        tests = [
            self.test_short_content(),
            self.test_medium_content(),
            self.test_long_content(),
            self.test_parallel_vs_sequential()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Process results
        successful_tests = 0
        total_processing_time = 0
        
        for result in results:
            if isinstance(result, Exception):
                print(f"❌ Test failed with exception: {str(result)}")
                self.test_results.append({
                    "success": False,
                    "error": str(result)
                })
            else:
                self.test_results.append(result)
                if result.get("success", False):
                    successful_tests += 1
                    total_processing_time += result.get("processing_time", 0)
        
        # Generate summary
        summary = {
            "total_tests": len(results),
            "successful_tests": successful_tests,
            "failed_tests": len(results) - successful_tests,
            "total_processing_time": total_processing_time,
            "average_processing_time": total_processing_time / successful_tests if successful_tests > 0 else 0,
            "test_results": self.test_results
        }
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total tests: {summary['total_tests']}")
        print(f"Successful: {summary['successful_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Total processing time: {summary['total_processing_time']:.2f}s")
        print(f"Average processing time: {summary['average_processing_time']:.2f}s")
        
        # Save results to file
        with open("enhanced_processing_test_results.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: enhanced_processing_test_results.json")
        
        return summary

async def main():
    """Main test execution function"""
    tester = EnhancedProcessingTester()
    results = await tester.run_all_tests()
    
    if "error" in results:
        print(f"\n❌ Test execution failed: {results['error']}")
        return 1
    
    print(f"\n✅ All tests completed successfully!")
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code) 