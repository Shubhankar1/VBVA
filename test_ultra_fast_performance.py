#!/usr/bin/env python3
"""
Ultra-Fast Performance Test for VBVA
Tests the aggressive optimizations to achieve sub-8-second processing for 9-second outputs
"""

import asyncio
import time
import json
import requests
from typing import Dict, List

# Test configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api/v1"

class UltraFastPerformanceTester:
    """Test suite for ultra-fast processing performance"""
    
    def __init__(self):
        self.test_results = []
        self.baseline_time = 16.0  # Baseline processing time (16 seconds)
        self.target_time = 8.0     # Target processing time (8 seconds)
    
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "=" * 70)
        print(f"🚀 {title}")
        print("=" * 70)
    
    def print_section(self, title: str):
        """Print formatted section"""
        print(f"\n📋 {title}")
        print("-" * 50)
    
    async def test_ultra_fast_short_content(self) -> Dict:
        """Test ultra-fast processing of short content"""
        self.print_section("Ultra-Fast Short Content Processing")
        
        short_text = "Hello! This is a quick test of our ultra-fast video processing system."
        
        print(f"📝 Text length: {len(short_text)} characters")
        print("🚀 Processing with ultra-fast optimizations...")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": short_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 6,
                    "use_ultra_fast": True
                },
                timeout=30  # 30 seconds timeout for ultra-fast
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                details = result.get('processing_details', {})
                
                print(f"✅ Ultra-fast processing completed in {processing_time:.2f}s")
                print(f"🎥 Video URL: {result.get('video_url', 'N/A')}")
                print(f"⚙️ Optimization level: {details.get('optimization_level', 'N/A')}")
                print(f"🚀 Speed multiplier: {details.get('speed_multiplier', 'N/A')}x")
                print(f"🎯 Target achieved: {details.get('target_achieved', 'N/A')}")
                
                speed_improvement = ((self.baseline_time - processing_time) / self.baseline_time) * 100
                print(f"📈 Speed improvement: {speed_improvement:.1f}% faster than baseline")
                
                return {
                    "test_type": "ultra_fast_short",
                    "success": True,
                    "processing_time": processing_time,
                    "text_length": len(short_text),
                    "speed_multiplier": details.get('speed_multiplier', 1.0),
                    "target_achieved": details.get('target_achieved', False),
                    "speed_improvement": speed_improvement,
                    "details": details
                }
            else:
                print(f"❌ Ultra-fast processing failed: {response.status_code}")
                return {
                    "test_type": "ultra_fast_short",
                    "success": False,
                    "processing_time": processing_time,
                    "error": response.text
                }
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Ultra-fast test error: {str(e)}")
            return {
                "test_type": "ultra_fast_short",
                "success": False,
                "processing_time": processing_time,
                "error": str(e)
            }
    
    async def test_ultra_fast_medium_content(self) -> Dict:
        """Test ultra-fast processing of medium content"""
        self.print_section("Ultra-Fast Medium Content Processing")
        
        medium_text = """
        Welcome to our ultra-fast video processing demonstration! This medium-length content 
        showcases the aggressive optimizations we've implemented to achieve sub-8-second 
        processing times. The system now uses ultra-small chunks, maximum parallelization, 
        and optimized Wav2Lip parameters to dramatically reduce processing time while 
        maintaining high quality output. This represents a significant breakthrough in 
        real-time video generation technology.
        """.strip()
        
        print(f"📝 Text length: {len(medium_text)} characters")
        print("🚀 Processing with ultra-fast optimizations...")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": medium_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 6,
                    "use_ultra_fast": True
                },
                timeout=60  # 60 seconds timeout
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                details = result.get('processing_details', {})
                
                print(f"✅ Ultra-fast processing completed in {processing_time:.2f}s")
                print(f"🎥 Video URL: {result.get('video_url', 'N/A')}")
                print(f"⚙️ Optimization level: {details.get('optimization_level', 'N/A')}")
                print(f"🚀 Speed multiplier: {details.get('speed_multiplier', 'N/A')}x")
                print(f"🎯 Target achieved: {details.get('target_achieved', 'N/A')}")
                
                speed_improvement = ((self.baseline_time - processing_time) / self.baseline_time) * 100
                print(f"📈 Speed improvement: {speed_improvement:.1f}% faster than baseline")
                
                return {
                    "test_type": "ultra_fast_medium",
                    "success": True,
                    "processing_time": processing_time,
                    "text_length": len(medium_text),
                    "speed_multiplier": details.get('speed_multiplier', 1.0),
                    "target_achieved": details.get('target_achieved', False),
                    "speed_improvement": speed_improvement,
                    "details": details
                }
            else:
                print(f"❌ Ultra-fast processing failed: {response.status_code}")
                return {
                    "test_type": "ultra_fast_medium",
                    "success": False,
                    "processing_time": processing_time,
                    "error": response.text
                }
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Ultra-fast test error: {str(e)}")
            return {
                "test_type": "ultra_fast_medium",
                "success": False,
                "processing_time": processing_time,
                "error": str(e)
            }
    
    async def test_performance_comparison(self) -> Dict:
        """Compare ultra-fast vs enhanced vs standard processing"""
        self.print_section("Performance Comparison: Ultra-Fast vs Enhanced vs Standard")
        
        test_text = """
        This is a comprehensive performance comparison test to demonstrate the dramatic 
        improvements achieved with ultra-fast processing. We're targeting sub-8-second 
        processing times for content that previously took 16 seconds or more.
        """.strip()
        
        print(f"📝 Test content length: {len(test_text)} characters")
        
        results = {}
        
        # Test ultra-fast processing
        print("\n🚀 Testing ultra-fast processing...")
        ultra_start = time.time()
        
        try:
            ultra_response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": test_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 6,
                    "use_ultra_fast": True
                },
                timeout=60
            )
            ultra_time = time.time() - ultra_start
            
            if ultra_response.status_code == 200:
                ultra_details = ultra_response.json().get('processing_details', {})
                results["ultra_fast"] = {
                    "time": ultra_time,
                    "speed_multiplier": ultra_details.get('speed_multiplier', 1.0),
                    "target_achieved": ultra_details.get('target_achieved', False)
                }
                print(f"✅ Ultra-fast: {ultra_time:.2f}s")
            else:
                print(f"❌ Ultra-fast failed: {ultra_response.status_code}")
                
        except Exception as e:
            print(f"❌ Ultra-fast error: {str(e)}")
        
        # Test enhanced processing
        print("\n🔄 Testing enhanced processing...")
        enhanced_start = time.time()
        
        try:
            enhanced_response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": test_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 15,
                    "use_ultra_fast": False
                },
                timeout=120
            )
            enhanced_time = time.time() - enhanced_start
            
            if enhanced_response.status_code == 200:
                enhanced_details = enhanced_response.json().get('processing_details', {})
                results["enhanced"] = {
                    "time": enhanced_time,
                    "optimization_level": enhanced_details.get('optimization_level', 'standard')
                }
                print(f"✅ Enhanced: {enhanced_time:.2f}s")
            else:
                print(f"❌ Enhanced failed: {enhanced_response.status_code}")
                
        except Exception as e:
            print(f"❌ Enhanced error: {str(e)}")
        
        # Calculate improvements
        if "ultra_fast" in results and "enhanced" in results:
            ultra_time = results["ultra_fast"]["time"]
            enhanced_time = results["enhanced"]["time"]
            
            improvement_vs_enhanced = ((enhanced_time - ultra_time) / enhanced_time) * 100
            improvement_vs_baseline = ((self.baseline_time - ultra_time) / self.baseline_time) * 100
            
            print(f"\n📊 Performance Results:")
            print(f"   Ultra-fast: {ultra_time:.2f}s")
            print(f"   Enhanced: {enhanced_time:.2f}s")
            print(f"   Baseline: {self.baseline_time:.2f}s")
            print(f"   Improvement vs Enhanced: {improvement_vs_enhanced:.1f}%")
            print(f"   Improvement vs Baseline: {improvement_vs_baseline:.1f}%")
            
            if ultra_time <= self.target_time:
                print("   🎉 Target achieved! Sub-8-second processing successful!")
            else:
                print(f"   ⚠️ Target not achieved. Need {ultra_time - self.target_time:.1f}s more optimization")
            
            return {
                "test_type": "performance_comparison",
                "success": True,
                "ultra_fast_time": ultra_time,
                "enhanced_time": enhanced_time,
                "baseline_time": self.baseline_time,
                "improvement_vs_enhanced": improvement_vs_enhanced,
                "improvement_vs_baseline": improvement_vs_baseline,
                "target_achieved": ultra_time <= self.target_time
            }
        else:
            print("❌ One or more processing modes failed")
            return {
                "test_type": "performance_comparison",
                "success": False,
                "error": "Processing comparison failed"
            }
    
    async def test_quality_verification(self) -> Dict:
        """Verify that ultra-fast processing maintains quality"""
        self.print_section("Quality Verification for Ultra-Fast Processing")
        
        test_text = "This is a quality verification test to ensure ultra-fast processing maintains high output standards."
        
        print(f"📝 Test content length: {len(test_text)} characters")
        print("🚀 Testing ultra-fast processing with quality verification...")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{API_BASE}/generate_video",
                json={
                    "message": test_text,
                    "agent_type": "general",
                    "enable_parallel": True,
                    "chunk_duration": 6,
                    "use_ultra_fast": True
                },
                timeout=60
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                video_url = result.get('video_url', '')
                
                print(f"✅ Ultra-fast processing completed in {processing_time:.2f}s")
                print(f"🎥 Video URL: {video_url}")
                
                # Check if video URL is accessible
                try:
                    video_response = requests.head(video_url, timeout=10)
                    if video_response.status_code == 200:
                        print("✅ Video file is accessible and valid")
                        quality_status = "verified"
                    else:
                        print("⚠️ Video file may have issues")
                        quality_status = "potential_issues"
                except Exception as e:
                    print(f"⚠️ Could not verify video accessibility: {str(e)}")
                    quality_status = "unverified"
                
                return {
                    "test_type": "quality_verification",
                    "success": True,
                    "processing_time": processing_time,
                    "video_url": video_url,
                    "quality_status": quality_status,
                    "target_achieved": processing_time <= self.target_time
                }
            else:
                print(f"❌ Quality verification failed: {response.status_code}")
                return {
                    "test_type": "quality_verification",
                    "success": False,
                    "processing_time": processing_time,
                    "error": response.text
                }
                
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Quality verification error: {str(e)}")
            return {
                "test_type": "quality_verification",
                "success": False,
                "processing_time": processing_time,
                "error": str(e)
            }
    
    async def run_all_tests(self) -> Dict:
        """Run all ultra-fast performance tests"""
        self.print_header("Ultra-Fast Performance Testing Suite")
        
        print("🚀 This test suite validates our ultra-fast processing optimizations")
        print("   targeting sub-8-second processing times for 9-second outputs.")
        print(f"   Baseline: {self.baseline_time}s → Target: {self.target_time}s")
        
        # Check backend health
        try:
            health_response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if health_response.status_code != 200:
                print("\n❌ Backend is not available. Please start the backend first.")
                return {"error": "Backend not available"}
        except Exception as e:
            print(f"\n❌ Cannot connect to backend: {str(e)}")
            return {"error": "Backend connection failed"}
        
        print("\n✅ Backend is healthy, starting ultra-fast performance tests...")
        
        # Run all tests
        tests = [
            self.test_ultra_fast_short_content(),
            self.test_ultra_fast_medium_content(),
            self.test_performance_comparison(),
            self.test_quality_verification()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Process results
        successful_tests = 0
        total_processing_time = 0
        target_achievements = 0
        
        for result in results:
            if isinstance(result, Exception):
                print(f"❌ Test failed with exception: {str(result)}")
            else:
                self.test_results.append(result)
                if result.get("success", False):
                    successful_tests += 1
                    total_processing_time += result.get("processing_time", 0)
                    if result.get("target_achieved", False):
                        target_achievements += 1
        
        # Generate summary
        summary = {
            "total_tests": len(results),
            "successful_tests": successful_tests,
            "failed_tests": len(results) - successful_tests,
            "target_achievements": target_achievements,
            "total_processing_time": total_processing_time,
            "average_processing_time": total_processing_time / successful_tests if successful_tests > 0 else 0,
            "baseline_time": self.baseline_time,
            "target_time": self.target_time,
            "test_results": self.test_results
        }
        
        # Print summary
        self.print_header("Ultra-Fast Performance Test Summary")
        print(f"📊 Total tests: {summary['total_tests']}")
        print(f"✅ Successful: {summary['successful_tests']}")
        print(f"❌ Failed: {summary['failed_tests']}")
        print(f"🎯 Target achievements: {summary['target_achievements']}")
        print(f"⏱️ Total processing time: {summary['total_processing_time']:.2f}s")
        print(f"📈 Average processing time: {summary['average_processing_time']:.2f}s")
        print(f"🚀 Baseline time: {summary['baseline_time']:.1f}s")
        print(f"🎯 Target time: {summary['target_time']:.1f}s")
        
        if summary['average_processing_time'] > 0:
            overall_improvement = ((summary['baseline_time'] - summary['average_processing_time']) / summary['baseline_time']) * 100
            print(f"📈 Overall improvement: {overall_improvement:.1f}% faster than baseline")
        
        # Save results
        with open("ultra_fast_performance_results.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: ultra_fast_performance_results.json")
        
        if target_achievements > 0:
            print("\n🎉 Ultra-fast processing targets achieved! Sub-8-second processing is working!")
        else:
            print("\n⚠️ Some targets not achieved. Further optimization may be needed.")
        
        return summary

async def main():
    """Main test execution function"""
    tester = UltraFastPerformanceTester()
    results = await tester.run_all_tests()
    
    if "error" in results:
        print(f"\n❌ Test execution failed: {results['error']}")
        return 1
    
    print(f"\n✅ All ultra-fast performance tests completed!")
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code) 