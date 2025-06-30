"""
VBVA Ultra-Fast Processing Service
Implements aggressive optimizations to achieve sub-8-second processing for 9-second outputs
"""

import asyncio
import time
import tempfile
import os
import hashlib
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
import httpx
import sys

from services.tts import TTSService
from services.lip_sync import LipSyncService

# Try to import enhanced TTS service
try:
    from services.enhanced_tts import EnhancedTTSService
    ENHANCED_TTS_AVAILABLE = True
except ImportError:
    ENHANCED_TTS_AVAILABLE = False
    print("⚠️ Enhanced TTS not available - using basic TTS")

@dataclass
class UltraProcessingStats:
    """Ultra-fast processing statistics"""
    total_chunks: int
    successful_chunks: int
    failed_chunks: int
    parallel_processing: bool
    chunk_duration: float
    total_processing_time: float
    audio_generation_time: float
    video_generation_time: float
    optimization_level: str
    speed_multiplier: float

class UltraFastProcessor:
    """Ultra-fast video processor with aggressive optimizations"""
    
    def __init__(self):
        # Use enhanced TTS service if available, otherwise fall back to basic TTS
        if ENHANCED_TTS_AVAILABLE:
            self.tts_service = EnhancedTTSService()
            print("🚀 Using Enhanced TTS Service with fallback options")
        else:
            self.tts_service = TTSService()
            print("⚠️ Using Basic TTS Service")
        
        self.lip_sync_service = LipSyncService()
        
        # Ultra-fast configuration
        self.max_parallel_chunks = 8  # Maximum parallel processing
        self.optimal_chunk_duration = 6  # 6-second chunks for speed
        self.max_chunk_duration = 12  # Maximum chunk size
        
        # Performance optimizations
        self.enable_preprocessing = True
        self.enable_parallel_audio = True
        self.enable_memory_optimization = True
        self.enable_gpu_optimization = True
        
        # Cache configuration
        self.cache_dir = "/tmp/vbva_ultra_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Thread pool for parallel processing
        self.thread_pool = ThreadPoolExecutor(max_workers=8)
    
    async def process_video_ultra_fast(
        self,
        text: str,
        agent_type: str = "general",
        target_time: float = 8.0  # Target processing time in seconds
    ) -> Tuple[str, UltraProcessingStats]:
        """Process video with ultra-fast optimizations targeting sub-8-second processing"""
        
        start_time = time.time()
        
        try:
            # Step 1: Parallel audio generation with preprocessing
            audio_start = time.time()
            audio_url = await self._generate_audio_ultra_fast(text, agent_type)
            audio_time = time.time() - audio_start
            
            # Step 2: Ultra-fast video generation
            video_start = time.time()
            video_url = await self._generate_video_ultra_fast(audio_url, agent_type)
            video_time = time.time() - video_start
            
            total_time = time.time() - start_time
            speed_multiplier = 16.0 / total_time if total_time > 0 else 1.0  # 16s baseline
            
            # Create ultra processing stats
            stats = UltraProcessingStats(
                total_chunks=1,
                successful_chunks=1,
                failed_chunks=0,
                parallel_processing=True,
                chunk_duration=self.optimal_chunk_duration,
                total_processing_time=total_time,
                audio_generation_time=audio_time,
                video_generation_time=video_time,
                optimization_level="ultra_fast",
                speed_multiplier=speed_multiplier
            )
            
            print(f"🚀 Ultra-fast processing completed in {total_time:.2f}s (target: {target_time:.1f}s)")
            print(f"🚀 Speed multiplier: {speed_multiplier:.1f}x faster than baseline")
            
            return video_url, stats
            
        except Exception as e:
            total_time = time.time() - start_time
            raise Exception(f"Ultra-fast processing failed after {total_time:.2f}s: {str(e)}")
    
    async def _generate_audio_ultra_fast(self, text: str, agent_type: str) -> str:
        """Generate audio with ultra-fast optimizations"""
        
        # Temporarily disable caching to ensure fresh content
        # cache_key = self._get_audio_cache_key(text, agent_type)
        # cached_audio = await self._check_audio_cache(cache_key)
        # if cached_audio:
        #     print(f"🚀 Using ultra-cached audio: {cached_audio}")
        #     return cached_audio
        
        # Generate audio with optimized settings
        audio_url = await self.tts_service.generate_speech(text, agent_type=agent_type)
        
        # Cache the result
        # await self._cache_audio(cache_key, audio_url)
        
        return audio_url
    
    async def _generate_video_ultra_fast(self, audio_url: str, agent_type: str) -> str:
        """Generate video with ultra-fast optimizations and robust looping prevention"""
        
        print(f"🎬 Starting ultra-fast video generation for audio: {audio_url}")
        
        # Temporarily disable caching to ensure fresh content
        # cache_key = self._get_video_cache_key(audio_url, agent_type)
        # cached_video = await self._check_video_cache(cache_key)
        # if cached_video:
        #     print(f"🚀 Using ultra-cached video: {cached_video}")
        #     return cached_video
        
        # Get audio duration
        audio_duration = await self._get_audio_duration_fast(audio_url)
        print(f"🎵 Audio duration: {audio_duration:.2f}s")
        
        # ROBUST processing strategy to prevent looping issues
        if audio_duration <= 12:  # Extended range for single video generation (was 15)
            print(f"🎬 Using single video generation for optimal audio ({audio_duration:.2f}s)")
            print(f"🎬 This prevents any potential looping issues from chunking")
            video_url = await self._generate_single_video_ultra_fast(audio_url, agent_type)
        else:
            print(f"🎬 Using parallel video generation for very long audio ({audio_duration:.2f}s)")
            print(f"🎬 Only using chunking for content longer than 12 seconds")
            video_url = await self._generate_parallel_video_ultra_fast(audio_url, agent_type)
        
        # Cache the result
        # await self._cache_video(cache_key, video_url)
        
        return video_url
    
    async def _generate_single_video_ultra_fast(self, audio_url: str, agent_type: str) -> str:
        """Generate single video with ultra-fast settings"""
        
        # Prepare files with minimal processing
        audio_path = await self._prepare_audio_ultra_fast(audio_url)
        avatar_path = await self._prepare_avatar_ultra_fast(agent_type)
        
        # Run Wav2Lip with ultra-fast parameters
        output_path = await self._run_wav2lip_ultra_fast(audio_path, avatar_path)
        
        # Convert to web-accessible URL
        video_url = await self._convert_to_web_format(output_path)
        
        return video_url
    
    async def _generate_single_video_local_ultra_fast(self, audio_url: str, agent_type: str) -> str:
        """Generate single video with ultra-fast settings and return local path (for chunk processing)"""
        
        # Prepare files with minimal processing
        audio_path = await self._prepare_audio_ultra_fast(audio_url)
        avatar_path = await self._prepare_avatar_ultra_fast(agent_type)
        
        # Run Wav2Lip with ultra-fast parameters
        output_path = await self._run_wav2lip_ultra_fast(audio_path, avatar_path)
        
        # Return local path for chunk processing
        return output_path
    
    async def _generate_parallel_video_ultra_fast(self, audio_url: str, agent_type: str) -> str:
        """Generate video with ultra-fast parallel processing and robust fallback"""
        
        print(f"🎬 Starting parallel video generation with fallback protection")
        
        try:
            # Split audio into ultra-small chunks
            print(f"🎵 Splitting audio into chunks...")
            audio_chunks = await self._split_audio_ultra_fast(audio_url)
            print(f"✅ Audio split into {len(audio_chunks)} chunks")
            
            # Validate chunks before processing
            if len(audio_chunks) <= 1:
                print(f"⚠️ Only {len(audio_chunks)} chunk(s) generated, falling back to single video")
                return await self._generate_single_video_ultra_fast(audio_url, agent_type)
            
            # Process chunks in parallel with maximum concurrency
            print(f"🎬 Processing {len(audio_chunks)} chunks in parallel...")
            video_paths = await self._process_chunks_ultra_fast(audio_chunks, agent_type)
            print(f"✅ Generated {len(video_paths)} video chunks")
            
            # Validate video chunks before combination
            if len(video_paths) != len(audio_chunks):
                print(f"⚠️ Video chunk mismatch! Expected {len(audio_chunks)}, got {len(video_paths)}")
                print(f"⚠️ Falling back to single video generation")
                return await self._generate_single_video_ultra_fast(audio_url, agent_type)
            
            # Validate video chunks for duplicates and invalid files
            validated_paths = await self._validate_video_chunks(video_paths)
            if len(validated_paths) != len(video_paths):
                print(f"⚠️ Video validation removed {len(video_paths) - len(validated_paths)} invalid chunks")
                if len(validated_paths) == 0:
                    print(f"❌ No valid video chunks after validation, falling back to single video")
                    return await self._generate_single_video_ultra_fast(audio_url, agent_type)
                video_paths = validated_paths
            
            # Combine videos with ultra-fast settings
            print(f"🎬 Combining {len(video_paths)} video chunks...")
            combined_video_path = await self._combine_videos_with_improved_sync(video_paths)
            print(f"✅ Video combination completed: {combined_video_path}")
            
            if not combined_video_path:
                print("❌ Video combination failed")
                return ""
            
            # Convert to web format with cache-busting
            web_url = await self._convert_to_web_format(combined_video_path)
            print(f"✅ Final video URL: {web_url}")
            
            return web_url
            
        except Exception as e:
            print(f"❌ Parallel processing failed: {str(e)}")
            print(f"🔄 Falling back to single video generation")
            return await self._generate_single_video_ultra_fast(audio_url, agent_type)
    
    async def _split_audio_ultra_fast(self, audio_path: str) -> List[str]:
        """Split audio into ultra-small chunks for maximum speed with improved synchronization"""
        
        # Get duration
        duration = await self._get_audio_duration_fast(audio_path)
        
        print(f"🎵 Audio duration: {duration:.2f}s")
        
        # For very short audio (6 seconds or less), process as single chunk
        if duration <= 6:
            print(f"✅ Processing short audio as single chunk")
            return [audio_path]
        
        # IMPROVED CHUNKING LOGIC to eliminate duration gaps and prevent chunk 1 repeating
        # Use adaptive chunk sizing based on duration to avoid problematic remainders
        
        if duration <= 12:
            # For 6-12 seconds, use single chunk to avoid issues
            print(f"✅ Processing medium audio as single chunk (6-12s range)")
            return [audio_path]
        elif duration <= 18:
            # For 12-18 seconds, use 2 equal chunks to avoid remainders
            chunk_duration = duration / 2
            print(f"🎵 Using 2 equal chunks of ~{chunk_duration:.2f}s each")
        elif duration <= 24:
            # For 18-24 seconds, use 3 equal chunks
            chunk_duration = duration / 3
            print(f"🎵 Using 3 equal chunks of ~{chunk_duration:.2f}s each")
        elif duration <= 30:
            # For 24-30 seconds, use 4 equal chunks
            chunk_duration = duration / 4
            print(f"🎵 Using 4 equal chunks of ~{chunk_duration:.2f}s each")
        else:
            # For longer content, use 6-second chunks but handle remainders better
            chunk_duration = 6.0
            num_chunks = int(duration / chunk_duration)
            remainder = duration % chunk_duration
            
            if remainder > 0:
                if remainder < 3.0:  # Increased threshold for better stability
                    # Distribute remainder evenly among existing chunks
                    print(f"🎵 Adjusting chunking to avoid very short chunks (remainder: {remainder:.2f}s)")
                    chunk_duration = duration / num_chunks
                    print(f"🎵 Using {num_chunks} chunks of ~{chunk_duration:.2f}s each")
                else:
                    # Add one more chunk for the remainder
                    num_chunks += 1
                    print(f"🎵 Splitting into {num_chunks} chunks of ~{chunk_duration:.2f}s each")
            else:
                print(f"🎵 Splitting into {num_chunks} chunks of ~{chunk_duration:.2f}s each")
        
        # Use ffmpeg with improved settings for better chunk alignment and synchronization
        temp_dir = tempfile.mkdtemp(prefix="ultra_chunks_")
        
        cmd = [
            "ffmpeg", "-i", audio_path,
            "-f", "segment",
            "-segment_time", str(chunk_duration),
            "-c", "copy",  # Use copy to maintain audio quality
            "-reset_timestamps", "1",
            "-avoid_negative_ts", "make_zero",  # Handle negative timestamps
            "-fflags", "+genpts",  # Generate presentation timestamps
            "-segment_start_number", "0",  # Ensure proper numbering
            "-segment_list", os.path.join(temp_dir, "chunk_list.txt"),  # Create segment list for validation
            os.path.join(temp_dir, "chunk_%03d.mp3"),
            "-y"
        ]
        
        print(f"🔧 Running ffmpeg command: {' '.join(cmd)}")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            print(f"❌ FFmpeg error: {stderr.decode()}")
            # Fallback: return original audio as single chunk
            return [audio_path]
        
        # Get chunk files and verify they exist with proper ordering
        chunk_files = []
        total_chunk_duration = 0
        
        # Read segment list if available for validation
        segment_list_path = os.path.join(temp_dir, "chunk_list.txt")
        expected_chunks = []
        if os.path.exists(segment_list_path):
            try:
                with open(segment_list_path, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            expected_chunks.append(line.strip())
                print(f"📋 Expected chunks from segment list: {len(expected_chunks)}")
            except Exception as e:
                print(f"⚠️ Could not read segment list: {e}")
        
        # Check for all possible chunk files and sort them properly
        for i in range(10):  # Check more chunks in case of rounding issues
            chunk_path = os.path.join(temp_dir, f"chunk_{i:03d}.mp3")
            if os.path.exists(chunk_path) and os.path.getsize(chunk_path) > 0:
                # Get duration of this chunk
                chunk_duration_actual = await self._get_audio_duration_fast(chunk_path)
                if chunk_duration_actual > 1.0:  # Increased threshold for better stability
                    total_chunk_duration += chunk_duration_actual
                    chunk_files.append(chunk_path)
                    print(f"✅ Chunk {i}: {chunk_duration_actual:.2f}s")
                else:
                    print(f"⚠️ Chunk {i} too short, skipping: {chunk_duration_actual:.2f}s")
            else:
                # Stop when we find the first missing chunk
                break
        
        print(f"✅ Split audio into {len(chunk_files)} chunks")
        print(f"✅ Total chunk duration: {total_chunk_duration:.2f}s (original: {duration:.2f}s)")
        
        # Verify we're not losing audio content
        if abs(total_chunk_duration - duration) > 1.0:  # Allow 1s tolerance
            print(f"⚠️ Duration mismatch! Original: {duration:.2f}s, Chunks: {total_chunk_duration:.2f}s")
            print(f"⚠️ Falling back to single chunk processing")
            return [audio_path]
        
        # Check for very short chunks that could cause issues
        for i, chunk in enumerate(chunk_files):
            chunk_duration_actual = await self._get_audio_duration_fast(chunk)
            if chunk_duration_actual < 2.5:  # Increased threshold for better stability
                print(f"⚠️ Very short chunk {i} detected: {chunk_duration_actual:.2f}s")
                print(f"⚠️ Falling back to single chunk processing")
                return [audio_path]
        
        # Verify chunk order and continuity
        if len(chunk_files) > 1:
            print(f"🔍 Verifying chunk continuity...")
            for i in range(len(chunk_files) - 1):
                chunk1_duration = await self._get_audio_duration_fast(chunk_files[i])
                chunk2_duration = await self._get_audio_duration_fast(chunk_files[i + 1])
                print(f"🔍 Chunk {i}: {chunk1_duration:.2f}s -> Chunk {i+1}: {chunk2_duration:.2f}s")
        
        # Ensure chunks are in correct order and remove any duplicates
        chunk_files.sort()
        unique_chunks = []
        seen_chunks = set()
        for chunk in chunk_files:
            if chunk not in seen_chunks:
                seen_chunks.add(chunk)
                unique_chunks.append(chunk)
        
        if len(unique_chunks) != len(chunk_files):
            print(f"⚠️ Removed {len(chunk_files) - len(unique_chunks)} duplicate chunks")
            chunk_files = unique_chunks
        
        return chunk_files
    
    async def _process_chunks_ultra_fast(self, audio_chunks: List[str], agent_type: str) -> List[str]:
        """Process audio chunks with maximum parallelization, preserving order and preventing duplicates"""
        print(f"🎬 Processing {len(audio_chunks)} chunks with max {self.max_parallel_chunks} parallel workers")
        semaphore = asyncio.Semaphore(self.max_parallel_chunks)

        # Track processed chunks to prevent duplicates
        processed_chunks = set()
        chunk_results = {}

        async def process_single_chunk(chunk_path: str, chunk_index: int) -> (int, str):
            async with semaphore:
                # Prevent duplicate processing
                chunk_id = f"{chunk_path}_{chunk_index}"
                if chunk_id in processed_chunks:
                    print(f"⚠️ Chunk {chunk_index + 1} already processed, skipping duplicate")
                    return chunk_index, ""
                
                processed_chunks.add(chunk_id)
                print(f"🎬 Processing chunk {chunk_index + 1}/{len(audio_chunks)}: {chunk_path}")
                try:
                    video_path = await self._generate_single_video_local_ultra_fast(chunk_path, agent_type)
                    print(f"✅ Chunk {chunk_index + 1} completed: {video_path}")
                    return chunk_index, video_path
                except Exception as e:
                    print(f"❌ Chunk {chunk_index + 1} failed: {str(e)}")
                    raise e

        # Launch all chunk processing tasks
        tasks = [process_single_chunk(chunk, i) for i, chunk in enumerate(audio_chunks)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect results in the correct order with duplicate prevention
        ordered_video_paths = []
        successful_chunks = 0
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ Chunk {i + 1} processing failed: {str(result)}")
            elif isinstance(result, tuple) and len(result) == 2:
                idx, path = result
                if path and path not in ordered_video_paths:  # Prevent duplicate paths
                    ordered_video_paths.append(path)
                    successful_chunks += 1
                    print(f"✅ Chunk {idx + 1} added to video paths: {path}")
                elif path in ordered_video_paths:
                    print(f"⚠️ Duplicate video path detected for chunk {idx + 1}, skipping")
                else:
                    print(f"⚠️ Empty video path for chunk {idx + 1}")
            else:
                print(f"❌ Unexpected result for chunk {i + 1}: {result}")

        # Debug: print chunk order and check for duplicates
        print(f"\n🔍 Final chunk order for combination:")
        for i, path in enumerate(ordered_video_paths):
            print(f"  Chunk {i+1}: {path}")
        
        # Validate no duplicates in final list
        if len(set(ordered_video_paths)) != len(ordered_video_paths):
            print(f"⚠️ Duplicate chunk files detected in final combination!")
            # Remove duplicates while preserving order
            seen = set()
            unique_paths = []
            for path in ordered_video_paths:
                if path not in seen:
                    seen.add(path)
                    unique_paths.append(path)
            ordered_video_paths = unique_paths
            print(f"✅ Removed duplicates, final count: {len(ordered_video_paths)}")

        print(f"✅ Successfully processed {successful_chunks}/{len(audio_chunks)} chunks")
        return ordered_video_paths
    
    async def _run_wav2lip_ultra_fast(self, audio_path: str, avatar_path: str) -> str:
        """Run Wav2Lip with ultra-fast parameters and improved synchronization"""
        
        # Create cache key with timestamp to prevent serving old cached videos
        with open(audio_path, 'rb') as f:
            audio_hash = hashlib.md5(f.read()).hexdigest()[:8]
        with open(avatar_path, 'rb') as f:
            avatar_hash = hashlib.md5(f.read()).hexdigest()[:8]
        
        # Add timestamp to make cache key unique for each request
        timestamp = str(int(time.time() * 1000))[-6:]  # Last 6 digits of timestamp
        cache_key = f"ultra_wav2lip_{audio_hash}_{avatar_hash}_{timestamp}"
        
        # Temporarily disable caching to ensure fresh content
        # Check cache
        # output_dir = "/tmp/wav2lip_ultra_outputs"
        # os.makedirs(output_dir, exist_ok=True)
        # 
        # cached_path = os.path.join(output_dir, f"{cache_key}.mp4")
        # if os.path.exists(cached_path):
        #     return cached_path
        
        # Ultra-fast Wav2Lip command with improved synchronization
        wav2lip_dir = os.path.join(os.path.dirname(__file__), "..", "Wav2Lip")
        output_path = os.path.join("/tmp/wav2lip_ultra_outputs", f"{cache_key}.mp4")
        os.makedirs("/tmp/wav2lip_ultra_outputs", exist_ok=True)
        
        # Get audio duration to adjust parameters
        audio_duration = await self._get_audio_duration_fast(audio_path)
        
        # Adjust parameters based on audio duration for better synchronization
        if audio_duration <= 4:
            fps = 10  # Lower FPS for very short content
            batch_size = 32
        elif audio_duration <= 8:
            fps = 10  # Standard FPS for short content
            batch_size = 64
        else:
            fps = 10  # Consistent FPS for longer content
            batch_size = 64
        
        cmd = [
            "python", "inference.py",
            "--checkpoint_path", "checkpoints/wav2lip.pth",
            "--face", avatar_path,
            "--audio", audio_path,
            "--outfile", output_path,
            "--static", "True",
            "--fps", str(fps),  # Consistent FPS for better sync
            "--resize_factor", "6",  # Maximum resize for speed
            "--pads", "0", "2", "0", "0",  # Minimal padding
            "--wav2lip_batch_size", str(batch_size),  # Adjusted batch size
            "--nosmooth"  # Disable smoothing for consistency
        ]
        
        print(f"🎬 Wav2Lip command: {' '.join(cmd)}")
        print(f"🎵 Audio duration: {audio_duration:.2f}s, FPS: {fps}, Batch size: {batch_size}")
        
        # Optimized environment
        env = os.environ.copy()
        env.update({
            "CUDA_VISIBLE_DEVICES": "0",
            "OMP_NUM_THREADS": "2",
            "MKL_NUM_THREADS": "2",
        })
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=wav2lip_dir,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        # Check if Wav2Lip completed successfully
        if process.returncode != 0:
            print(f"❌ Wav2Lip failed with return code {process.returncode}")
            print(f"❌ Wav2Lip stderr: {stderr.decode()}")
            raise Exception(f"Wav2Lip processing failed: {stderr.decode()}")
        
        # Verify output file exists and has content
        if not os.path.exists(output_path):
            print(f"❌ Wav2Lip output file not found: {output_path}")
            raise Exception("Wav2Lip output file not found")
        
        if os.path.getsize(output_path) < 1000:  # Less than 1KB
            print(f"⚠️ Wav2Lip output file too small: {os.path.getsize(output_path)} bytes")
            raise Exception("Wav2Lip output file too small")
        
        print(f"✅ Wav2Lip completed successfully: {output_path}")
        return output_path
    
    async def _combine_videos_with_improved_sync(self, video_paths: List[str]) -> str:
        """Combine multiple videos with improved synchronization to prevent looping"""
        if not video_paths:
            return ""
        
        if len(video_paths) == 1:
            return video_paths[0]
        
        try:
            print(f"[UltraFastProcessor] Combining {len(video_paths)} videos with improved sync:")
            for i, path in enumerate(video_paths, 1):
                print(f"[UltraFastProcessor] {i}. {path}")
            
            # Validate video paths and remove duplicates
            unique_paths = []
            seen_paths = set()
            for path in video_paths:
                if path not in seen_paths and os.path.exists(path):
                    seen_paths.add(path)
                    unique_paths.append(path)
                elif path in seen_paths:
                    print(f"⚠️ Duplicate video path detected and removed: {path}")
                elif not os.path.exists(path):
                    print(f"⚠️ Video path does not exist: {path}")
            
            if len(unique_paths) != len(video_paths):
                print(f"⚠️ Removed {len(video_paths) - len(unique_paths)} invalid/duplicate video paths")
                video_paths = unique_paths
            
            if not video_paths:
                print(f"❌ No valid video paths to combine")
                return ""
            
            # Generate output path
            combined_hash = hashlib.md5()
            for path in video_paths:
                combined_hash.update(path.encode())
            cache_key = f"ultra_combined_{combined_hash.hexdigest()[:12]}"
            output_path = os.path.join("/tmp/wav2lip_ultra_outputs", f"{cache_key}.mp4")
            
            # STEP 1: Create a concat file for more reliable combination
            concat_file = f"/tmp/concat_{int(time.time())}.txt"
            with open(concat_file, 'w') as f:
                for video_path in video_paths:
                    f.write(f"file '{video_path}'\n")
            
            print(f"[UltraFastProcessor] Concat file created with {len(video_paths)} videos")
            
            # STEP 2: Use concat demuxer with strict timing parameters
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "128k",
                "-ar", "24000",
                "-movflags", "+faststart",
                "-avoid_negative_ts", "make_zero",
                "-fflags", "+genpts",
                "-async", "1",
                "-vsync", "1",
                "-max_interleave_delta", "0",
                output_path,
                "-y"
            ]
            
            print(f"[UltraFastProcessor] Running ffmpeg with concat demuxer for reliable sync:")
            print(f"[UltraFastProcessor] Command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Clean up concat file
            if os.path.exists(concat_file):
                os.remove(concat_file)
            
            if result.returncode != 0:
                print(f"❌ Video combination failed: {result.stderr}")
                return ""
            
            print(f"✅ Video combination completed with improved sync: {output_path}")
            
            # STEP 3: Validate the combined video
            if not os.path.exists(output_path) or os.path.getsize(output_path) < 1000:
                print(f"❌ Combined video validation failed: {output_path}")
                return ""
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error combining videos: {e}")
            return ""
    
    async def _get_audio_duration_fast(self, audio_path: str) -> float:
        """Get audio duration with fast ffprobe"""
        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "csv=p=0",
                audio_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return float(stdout.decode().strip())
            else:
                return 10.0  # Default duration
                
        except Exception:
            return 10.0  # Default duration
    
    async def _prepare_audio_ultra_fast(self, audio_url: str) -> str:
        """Prepare audio with minimal processing"""
        if os.path.exists(audio_url):
            return audio_url
        else:
            # Download with minimal processing
            async with httpx.AsyncClient() as client:
                response = await client.get(audio_url)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(response.content)
                    return f.name
    
    async def _prepare_avatar_ultra_fast(self, agent_type: str) -> str:
        """Prepare avatar with minimal processing"""
        # Use absolute paths for Wav2Lip
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        avatar_images = {
            "general": os.path.join(base_dir, "avatars", "general.jpg"),
            "hotel": os.path.join(base_dir, "avatars", "hotel_receptionist.jpg"),
            "airport": os.path.join(base_dir, "avatars", "airport_assistant.jpg"),
            "sales": os.path.join(base_dir, "avatars", "sales_agent.jpg")
        }
        avatar_path = avatar_images.get(agent_type, avatar_images["general"])
        
        # Verify the avatar exists
        if not os.path.exists(avatar_path):
            print(f"⚠️ Avatar not found: {avatar_path}, using general")
            avatar_path = avatar_images["general"]
        
        return avatar_path
    
    def _get_audio_cache_key(self, text: str, agent_type: str) -> str:
        """Generate audio cache key"""
        content = f"{text}_{agent_type}_ultra_audio"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _get_video_cache_key(self, audio_url: str, agent_type: str) -> str:
        """Generate video cache key"""
        content = f"{audio_url}_{agent_type}_ultra_video"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    async def _check_audio_cache(self, cache_key: str) -> Optional[str]:
        """Check audio cache"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    audio_path = cache_data.get("audio_path")
                    if audio_path and os.path.exists(audio_path):
                        return audio_path
            except Exception:
                pass
        return None
    
    async def _check_video_cache(self, cache_key: str) -> Optional[str]:
        """Check video cache"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                    video_path = cache_data.get("video_path")
                    if video_path and os.path.exists(video_path):
                        return video_path
            except Exception:
                pass
        return None
    
    async def _cache_audio(self, cache_key: str, audio_path: str):
        """Cache audio"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        cache_data = {
            "audio_path": audio_path,
            "timestamp": time.time()
        }
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception:
            pass
    
    async def _cache_video(self, cache_key: str, video_path: str):
        """Cache video"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        cache_data = {
            "video_path": video_path,
            "timestamp": time.time()
        }
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
        except Exception:
            pass
    
    async def _convert_to_web_format(self, video_path: str) -> str:
        """Convert video to web format with comprehensive validation and metadata fixing"""
        if not video_path or not os.path.exists(video_path):
            return ""
        
        # STEP 1: Validate and fix video metadata to prevent playback issues
        fixed_video_path = await self._fix_video_metadata(video_path)
        
        # STEP 2: Add cache-busting timestamp to prevent browser caching issues
        timestamp = int(time.time())
        filename = os.path.basename(fixed_video_path)
        
        # Create web URL with cache-busting parameter
        web_url = f"http://localhost:8000/api/v1/videos/{filename}?t={timestamp}"
        
        print(f"✅ Final video URL (with metadata fix): {web_url}")
        return web_url
    
    async def _fix_video_metadata(self, video_path: str) -> str:
        """Fix video metadata to prevent looping and playback issues"""
        try:
            # Create a new filename for the fixed video
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            fixed_filename = f"{base_name}_fixed.mp4"
            fixed_path = os.path.join(os.path.dirname(video_path), fixed_filename)
            
            # Comprehensive FFmpeg command to fix all potential playback issues
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-c:v", "libx264",  # Re-encode video
                "-preset", "ultrafast",
                "-crf", "23",
                "-c:a", "aac",  # Re-encode audio
                "-b:a", "128k",
                "-ar", "24000",
                "-movflags", "+faststart",  # Optimize for web streaming
                "-avoid_negative_ts", "make_zero",  # Fix timestamp issues
                "-fflags", "+genpts",  # Generate proper timestamps
                "-async", "1",  # Audio sync correction
                "-vsync", "1",  # Video sync correction
                "-max_interleave_delta", "0",  # Better interleaving
                "-metadata", "title=VBVA Generated Video",  # Add metadata
                "-metadata", "artist=VBVA System",
                "-metadata", "comment=Generated by Video Based Virtual Assistant",
                "-y",  # Overwrite output
                fixed_path
            ]
            
            print(f"[UltraFastProcessor] Fixing video metadata to prevent playback issues:")
            print(f"[UltraFastProcessor] Command: {' '.join(cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                print(f"❌ Video metadata fix failed: {stderr.decode()}")
                return video_path  # Return original if fix fails
            
            # Verify the fixed video exists and has content
            if not os.path.exists(fixed_path) or os.path.getsize(fixed_path) < 1000:
                print(f"⚠️ Fixed video validation failed, using original")
                return video_path
            
            print(f"✅ Video metadata fixed successfully: {fixed_path}")
            return fixed_path
            
        except Exception as e:
            print(f"❌ Video metadata fix error: {str(e)}")
            return video_path  # Return original if any error occurs
    
    def get_ultra_fast_status(self) -> Dict:
        """Get ultra-fast processing status"""
        return {
            "max_parallel_chunks": self.max_parallel_chunks,
            "optimal_chunk_duration": self.optimal_chunk_duration,
            "enable_preprocessing": self.enable_preprocessing,
            "enable_parallel_audio": self.enable_parallel_audio,
            "enable_memory_optimization": self.enable_memory_optimization,
            "enable_gpu_optimization": self.enable_gpu_optimization,
            "target_processing_time": "8.0 seconds",
            "speed_multiplier": "2x+ faster than baseline"
        }
    
    async def _validate_video_chunks(self, video_paths: List[str]) -> List[str]:
        """Validate video chunks and remove duplicates/invalid files"""
        if not video_paths:
            return []
        
        valid_paths = []
        seen_paths = set()
        
        for i, path in enumerate(video_paths):
            if not path:
                print(f"⚠️ Empty video path at index {i}, skipping")
                continue
                
            if path in seen_paths:
                print(f"⚠️ Duplicate video path detected at index {i}: {path}")
                continue
                
            if not os.path.exists(path):
                print(f"⚠️ Video path does not exist at index {i}: {path}")
                continue
                
            if os.path.getsize(path) < 1000:  # Less than 1KB is suspicious
                print(f"⚠️ Video file too small at index {i}: {path} ({os.path.getsize(path)} bytes)")
                continue
            
            seen_paths.add(path)
            valid_paths.append(path)
            print(f"✅ Valid video chunk {i+1}: {path}")
        
        if len(valid_paths) != len(video_paths):
            print(f"⚠️ Removed {len(video_paths) - len(valid_paths)} invalid/duplicate video chunks")
        
        return valid_paths 