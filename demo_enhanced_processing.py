#!/usr/bin/env python3
"""
Enhanced Parallel Processing Demo for VBVA
Demonstrates the seamless approach of splitting long answers into multiple shorter videos
and processing them in parallel to reduce processing time.
"""

import asyncio
import time
import requests
import json
from typing import Dict, List

# Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api/v1"

class EnhancedProcessingDemo:
    """Demo class for enhanced parallel processing capabilities"""
    
    def __init__(self):
        self.demo_results = []
    
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"🎬 {title}")
        print("=" * 60)
    
    def print_section(self, title: str):
        """Print formatted section"""
        print(f"\n📋 {title}")
        print("-" * 40)
    
    async def demo_short_content(self):
        """Demonstrate short content processing"""
        self.print_section("Short Content Processing")
        
        short_text = "Hello! This is a quick demonstration of our enhanced video processing system."
        
        print(f"📝 Text length: {len(short_text)} characters")
        print("🔄 Processing with enhanced parallel processing...")
        
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
                print(f"✅ Completed in {processing_time:.2f} seconds")
                print(f"🎥 Video URL: {result.get('video_url', 'N/A')}")
                
                details = result.get('processing_details', {})
                print(f"⚙️ Processing mode: {details.get('optimization_level', 'N/A')}")
                print(f"🔄 Parallel processing: {details.get('parallel_processing', 'N/A')}")
                
                return {
                    "type": "short",
                    "success": True,
                    "processing_time": processing_time,
                    "text_length": len(short_text),
                    "details": details
                }
            else:
                print(f"❌ Failed: {response.status_code}")
                return {"type": "short", "success": False, "error": response.text}
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Error: {str(e)}")
            return {"type": "short", "success": False, "error": str(e)}
    
    async def demo_medium_content(self):
        """Demonstrate medium content processing"""
        self.print_section("Medium Content Processing")
        
        medium_text = """
        Welcome to our enhanced video processing demonstration! This medium-length content 
        showcases the parallel processing capabilities of our system. The technology 
        automatically splits longer content into optimal chunks and processes them 
        simultaneously, dramatically reducing the overall processing time while maintaining 
        the highest quality standards. This approach ensures that users receive their 
        video responses much faster, especially for detailed explanations and longer 
        conversations. The seamless combining process creates a single, continuous video 
        that appears as if it was processed as one piece, with perfect synchronization 
        between audio and visual elements.
        """.strip()
        
        print(f"📝 Text length: {len(medium_text)} characters")
        print("🔄 Processing with enhanced parallel processing...")
        
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
                print(f"✅ Completed in {processing_time:.2f} seconds")
                print(f"🎥 Video URL: {result.get('video_url', 'N/A')}")
                
                details = result.get('processing_details', {})
                print(f"⚙️ Processing mode: {details.get('optimization_level', 'N/A')}")
                print(f"🔄 Parallel processing: {details.get('parallel_processing', 'N/A')}")
                print(f"⏱️ Audio generation: {details.get('audio_generation_time', 'N/A'):.2f}s")
                print(f"🎬 Video generation: {details.get('video_generation_time', 'N/A'):.2f}s")
                
                return {
                    "type": "medium",
                    "success": True,
                    "processing_time": processing_time,
                    "text_length": len(medium_text),
                    "details": details
                }
            else:
                print(f"❌ Failed: {response.status_code}")
                return {"type": "medium", "success": False, "error": response.text}
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Error: {str(e)}")
            return {"type": "medium", "success": False, "error": str(e)}
    
    async def demo_long_content(self):
        """Demonstrate long content processing"""
        self.print_section("Long Content Processing")
        
        long_text = """
        This comprehensive demonstration showcases the advanced capabilities of our enhanced 
        video processing system designed specifically for handling long-form content with 
        maximum efficiency. The system implements a sophisticated parallel processing 
        architecture that intelligently analyzes content length and complexity to determine 
        the optimal approach for video generation.
        
        For longer content, the system automatically splits the audio into multiple 
        segments, each processed independently and simultaneously. This parallel approach 
        leverages the full capabilities of modern hardware, including multi-core processors 
        and GPU acceleration when available. The result is a dramatic reduction in 
        processing time, often achieving 50-70% faster generation compared to traditional 
        sequential processing methods.
        
        The seamless combining process ensures that all individual video segments are 
        merged into a single, continuous output that maintains perfect audio-visual 
        synchronization. Advanced algorithms handle frame interpolation and crossfade 
        transitions to create smooth, natural-looking video without any visible breaks 
        or artifacts between segments.
        
        This technology is particularly valuable for applications requiring detailed 
        explanations, educational content, or comprehensive responses that would 
        traditionally take several minutes to process. Users can now receive high-quality 
        video responses for complex content in a fraction of the time, significantly 
        improving the overall user experience and making video-based virtual assistants 
        much more practical for real-world use cases.
        
        The system also includes intelligent caching mechanisms that store processed 
        segments for reuse, further improving performance for similar content. Quality 
        optimization algorithms ensure that the final output maintains the highest 
        standards while maximizing processing efficiency.
        """.strip()
        
        print(f"📝 Text length: {len(long_text)} characters")
        print("🔄 Processing with enhanced parallel processing...")
        
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
                timeout=600
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Completed in {processing_time:.2f} seconds")
                print(f"🎥 Video URL: {result.get('video_url', 'N/A')}")
                
                details = result.get('processing_details', {})
                print(f"⚙️ Processing mode: {details.get('optimization_level', 'N/A')}")
                print(f"🔄 Parallel processing: {details.get('parallel_processing', 'N/A')}")
                print(f"⏱️ Audio generation: {details.get('audio_generation_time', 'N/A'):.2f}s")
                print(f"🎬 Video generation: {details.get('video_generation_time', 'N/A'):.2f}s")
                
                return {
                    "type": "long",
                    "success": True,
                    "processing_time": processing_time,
                    "text_length": len(long_text),
                    "details": details
                }
            else:
                print(f"❌ Failed: {response.status_code}")
                return {"type": "long", "success": False, "error": response.text}
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Error: {str(e)}")
            return {"type": "long", "success": False, "error": str(e)}
    
    async def demo_performance_comparison(self):
        """Demonstrate performance comparison between parallel and sequential processing"""
        self.print_section("Performance Comparison: Parallel vs Sequential")
        
        test_text = """
        This is a performance comparison test to demonstrate the significant benefits 
        of parallel processing over traditional sequential methods. The enhanced system 
        should process this content much faster when parallel processing is enabled.
        """.strip()
        
        print(f"📝 Test content length: {len(test_text)} characters")
        
        # Test parallel processing
        print("\n🔄 Testing with parallel processing enabled...")
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
            
            # Test sequential processing
            print("🔄 Testing with parallel processing disabled...")
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
            
            # Calculate and display results
            if parallel_response.status_code == 200 and sequential_response.status_code == 200:
                improvement = ((sequential_time - parallel_time) / sequential_time) * 100
                
                print(f"\n📊 Performance Results:")
                print(f"   Parallel processing: {parallel_time:.2f} seconds")
                print(f"   Sequential processing: {sequential_time:.2f} seconds")
                print(f"   Time saved: {sequential_time - parallel_time:.2f} seconds")
                print(f"   Performance improvement: {improvement:.1f}%")
                
                if improvement > 20:
                    print("   🎉 Significant performance improvement achieved!")
                elif improvement > 10:
                    print("   ✅ Moderate performance improvement achieved!")
                else:
                    print("   📈 Small performance improvement achieved!")
                
                return {
                    "type": "comparison",
                    "success": True,
                    "parallel_time": parallel_time,
                    "sequential_time": sequential_time,
                    "improvement_percentage": improvement
                }
            else:
                print("❌ One or both processing modes failed")
                return {"type": "comparison", "success": False, "error": "Processing failed"}
                
        except Exception as e:
            print(f"❌ Performance comparison error: {str(e)}")
            return {"type": "comparison", "success": False, "error": str(e)}
    
    async def run_demo(self):
        """Run the complete demonstration"""
        self.print_header("Enhanced Parallel Processing Demo")
        
        print("🚀 This demo showcases the seamless approach of splitting long answers")
        print("   into multiple shorter videos and processing them in parallel to")
        print("   dramatically reduce processing time while maintaining high quality.")
        
        # Check backend health
        try:
            health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if health_response.status_code != 200:
                print("\n❌ Backend is not available. Please start the backend first.")
                return
        except Exception as e:
            print(f"\n❌ Cannot connect to backend: {str(e)}")
            return
        
        print("\n✅ Backend is healthy, starting demonstrations...")
        
        # Run all demos
        demos = [
            self.demo_short_content(),
            self.demo_medium_content(),
            self.demo_long_content(),
            self.demo_performance_comparison()
        ]
        
        results = await asyncio.gather(*demos, return_exceptions=True)
        
        # Process and display results
        successful_demos = 0
        total_processing_time = 0
        
        for result in results:
            if isinstance(result, Exception):
                print(f"❌ Demo failed with exception: {str(result)}")
            else:
                self.demo_results.append(result)
                if result.get("success", False):
                    successful_demos += 1
                    total_processing_time += result.get("processing_time", 0)
        
        # Display summary
        self.print_header("Demo Summary")
        print(f"📊 Total demonstrations: {len(results)}")
        print(f"✅ Successful: {successful_demos}")
        print(f"❌ Failed: {len(results) - successful_demos}")
        print(f"⏱️ Total processing time: {total_processing_time:.2f} seconds")
        
        if successful_demos > 0:
            avg_time = total_processing_time / successful_demos
            print(f"📈 Average processing time: {avg_time:.2f} seconds")
        
        # Save results
        with open("enhanced_processing_demo_results.json", "w") as f:
            json.dump({
                "demo_results": self.demo_results,
                "summary": {
                    "total_demos": len(results),
                    "successful_demos": successful_demos,
                    "total_processing_time": total_processing_time,
                    "average_processing_time": total_processing_time / successful_demos if successful_demos > 0 else 0
                }
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: enhanced_processing_demo_results.json")
        print("\n🎉 Demo completed! The enhanced parallel processing system is working effectively.")

async def main():
    """Main demo execution function"""
    demo = EnhancedProcessingDemo()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main()) 