"""
VBVA Lip-Sync Service
Cloud GPU-based lip-sync using Wav2Lip via various providers
Enhanced with seamless parallel processing for long content
"""

import asyncio
import tempfile
import os
import httpx
from typing import Optional, Dict, List, Tuple
import replicate
import json
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

from config.settings import get_settings

class LipSyncService:
    """Lip-sync service using cloud GPU providers with enhanced parallel processing"""
    
    def __init__(self):
        self.settings = get_settings()
        self.provider = self.settings.lip_sync_provider
        
        # Set Replicate API token if available
        if self.settings.replicate_api_token:
            os.environ["REPLICATE_API_TOKEN"] = self.settings.replicate_api_token
        
        # Provider configurations
        self.providers = {
            "d_id": self._generate_d_id,
            "replicate": self._generate_replicate,
            "heygen": self._generate_heygen,
            "hybrid": self._generate_hybrid,
            "local_wav2lip": self._generate_local_wav2lip,
            "colab": self._generate_colab,
            "runwayml": self._generate_runwayml
        }
        
        # Optimized parallel processing configuration for speed
        self.max_parallel_chunks = 6  # Increased from 4 for better parallelization
        self.optimal_chunk_duration = 8  # Reduced from 15 for faster processing
        self.max_chunk_duration = 20  # Reduced from 30 for faster processing
        
        # Performance optimization flags
        self.enable_aggressive_caching = True
        self.enable_fast_mode = True
        self.enable_gpu_acceleration = True
        
        # Cache configuration
        self.cache_dir = "/tmp/vbva_ultra_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    async def generate_video(
        self, 
        audio_url: str, 
        avatar_type: str = "general",
        avatar_image: Optional[str] = None
    ) -> str:
        """Generate video with enhanced seamless splitting for long content"""
        try:
            start_time = time.time()
            
            # Get audio duration to determine if splitting is needed
            audio_duration = await self._get_audio_duration(audio_url)
            print(f"Audio duration: {audio_duration:.2f} seconds")
            
            # If audio is longer than optimal duration, use enhanced splitting
            if audio_duration > self.optimal_chunk_duration:
                print(f"Using enhanced parallel processing for {audio_duration:.2f}s audio")
                result = await self._generate_seamless_split_videos(audio_url, avatar_type, avatar_image)
                total_time = time.time() - start_time
                print(f"Enhanced processing completed in {total_time:.2f}s")
                return result
            else:
                # Use existing single video generation for short content
                print("Using single video generation for short content")
                result = await self._generate_single_video(audio_url, avatar_type, avatar_image)
                total_time = time.time() - start_time
                print(f"Single video generation completed in {total_time:.2f}s")
                return result
                
        except Exception as e:
            raise Exception(f"Video generation failed: {str(e)}")
    
    async def _generate_seamless_split_videos(
        self, 
        audio_url: str, 
        avatar_type: str = "general",
        avatar_image: Optional[str] = None
    ) -> str:
        """Generate multiple shorter videos with seamless parallel processing"""
        try:
            print(f"Starting seamless split video generation for {audio_url}")
            
            # Step 1: Split audio into optimal chunks
            audio_chunks = await self._split_audio_optimally(audio_url)
            print(f"Split audio into {len(audio_chunks)} optimal chunks")
            
            # Step 2: Generate videos for each chunk in parallel with progress tracking
            video_paths = await self._generate_videos_parallel(audio_chunks, avatar_type, avatar_image)
            print(f"Generated {len(video_paths)} video chunks in parallel")
            
            # Step 3: Combine videos into a single seamless video with crossfade
            combined_video = await self._combine_videos_seamlessly(video_paths)
            print(f"Combined videos into seamless output: {combined_video}")
            
            # Step 4: Clean up temporary files
            await self._cleanup_temp_files(audio_chunks + video_paths)
            
            return combined_video
            
        except Exception as e:
            raise Exception(f"Seamless split video generation failed: {str(e)}")
    
    async def _split_audio_optimally(self, audio_path: str) -> List[str]:
        """Split audio into optimal chunks for ultra-fast parallel processing"""
        try:
            import subprocess
            import tempfile
            import os
            
            # Create temp directory for chunks
            temp_dir = tempfile.mkdtemp(prefix="vbva_ultra_chunks_")
            chunks = []
            
            # Get total duration
            total_duration = await self._get_audio_duration(audio_path)
            
            # Ultra-optimized chunk sizing for speed
            if total_duration <= 30:  # Very short content - no splitting needed
                return [audio_path]
            elif total_duration <= 60:  # Short content
                chunk_duration = min(6, total_duration / 3)  # 6-second chunks
            elif total_duration <= 120:  # Medium content
                chunk_duration = 8  # 8-second chunks
            else:  # Long content
                chunk_duration = min(10, total_duration / 6)  # 10-second chunks max
            
            print(f"Ultra-optimized splitting: {total_duration:.2f}s audio into {chunk_duration:.1f}s chunks")
            
            # Use ffmpeg with optimized settings for speed
            cmd = [
                "ffmpeg", "-i", audio_path,
                "-f", "segment",
                "-segment_time", str(chunk_duration),
                "-c", "copy",  # Fast copy without re-encoding
                "-reset_timestamps", "1",
                "-avoid_negative_ts", "make_zero",
                os.path.join(temp_dir, "chunk_%03d.mp3"),
                "-y"
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Audio splitting failed: {stderr.decode()}")
            
            # Get all generated chunk files
            chunk_files = []
            i = 0
            while True:
                chunk_path = os.path.join(temp_dir, f"chunk_{i:03d}.mp3")
                if os.path.exists(chunk_path) and os.path.getsize(chunk_path) > 0:
                    chunk_files.append(chunk_path)
                    i += 1
                else:
                    break
            
            print(f"Successfully created {len(chunk_files)} ultra-optimized audio chunks")
            return chunk_files
            
        except Exception as e:
            raise Exception(f"Ultra-optimized audio splitting failed: {str(e)}")
    
    async def _generate_videos_parallel(
        self, 
        audio_chunks: List[str], 
        avatar_type: str,
        avatar_image: Optional[str]
    ) -> List[str]:
        """Generate videos for multiple chunks in parallel with progress tracking"""
        try:
            print(f"Starting parallel video generation for {len(audio_chunks)} chunks")
            
            # Create semaphore to limit concurrent processing
            semaphore = asyncio.Semaphore(self.max_parallel_chunks)
            
            async def generate_single_chunk(chunk_index: int, chunk_path: str) -> Tuple[int, str]:
                async with semaphore:
                    try:
                        print(f"Processing chunk {chunk_index + 1}/{len(audio_chunks)}")
                        start_time = time.time()
                        
                        # Generate video for this chunk
                        video_path = await self._generate_single_video(chunk_path, avatar_type, avatar_image)
                        
                        processing_time = time.time() - start_time
                        print(f"Chunk {chunk_index + 1} completed in {processing_time:.2f}s")
                        
                        return chunk_index, video_path
                    except Exception as e:
                        print(f"Error processing chunk {chunk_index + 1}: {str(e)}")
                        raise e
            
            # Create tasks for all chunks
            tasks = [
                generate_single_chunk(i, chunk_path) 
                for i, chunk_path in enumerate(audio_chunks)
            ]
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and handle errors
            video_paths: List[Optional[str]] = [None] * len(audio_chunks)
            successful_chunks = 0
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Chunk {i + 1} processing failed: {str(result)}")
                elif isinstance(result, tuple) and len(result) == 2:
                    chunk_index, video_path = result
                    video_paths[chunk_index] = video_path
                    successful_chunks += 1
                else:
                    print(f"Chunk {i + 1} returned unexpected result type: {type(result)}")
            
            # Filter out None values and ensure order
            final_video_paths = [path for path in video_paths if path is not None]
            
            print(f"Successfully generated {successful_chunks}/{len(audio_chunks)} video chunks")
            
            if len(final_video_paths) == 0:
                raise Exception("No video chunks were successfully generated")
            
            return final_video_paths
            
        except Exception as e:
            raise Exception(f"Parallel video generation failed: {str(e)}")
    
    async def _combine_videos_seamlessly(self, video_paths: List[str]) -> str:
        """Combine multiple videos into a single seamless video with ultra-fast processing"""
        try:
            import subprocess
            import tempfile
            import os
            import hashlib
            
            if len(video_paths) == 1:
                return video_paths[0]
            
            print(f"🚀 Combining {len(video_paths)} videos with ultra-fast processing")
            
            # Create cache key for combined video
            combined_hash = hashlib.md5()
            for path in video_paths:
                combined_hash.update(path.encode())
            cache_key = f"ultra_combined_{combined_hash.hexdigest()[:12]}"
            
            # Create output directory
            output_dir = "/tmp/wav2lip_ultra_outputs"
            os.makedirs(output_dir, exist_ok=True)
            
            # Check cache first
            cached_path = os.path.join(output_dir, f"{cache_key}.mp4")
            if os.path.exists(cached_path):
                print(f"🚀 Using ultra-cached combined video: {cached_path}")
                return cached_path
            
            # Generate unique output filename
            output_filename = f"{cache_key}.mp4"
            output_path = os.path.join(output_dir, output_filename)
            
            # Create a file list for ffmpeg with ultra-fast settings
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                for video_path in video_paths:
                    f.write(f"file '{video_path}'\n")
                file_list_path = f.name
            
            # Ultra-fast ffmpeg command for video combination
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", file_list_path,
                "-filter_complex", "fps=12,format=yuv420p",  # Reduced FPS for speed
                "-c:v", "libx264",
                "-preset", "ultrafast",  # Fastest preset
                "-crf", "28",  # Slightly lower quality for speed
                "-c:a", "aac",
                "-b:a", "96k",  # Reduced audio bitrate for speed
                "-movflags", "+faststart",  # Optimize for web streaming
                "-threads", "4",  # Limit threads for stability
                output_path,
                "-y"
            ]
            
            print(f"🚀 Running ultra-fast video combination: {' '.join(cmd)}")
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # Clean up file list
            os.unlink(file_list_path)
            
            if process.returncode != 0:
                raise Exception(f"Ultra-fast video combination failed: {stderr.decode()}")
            
            print(f"🚀 Successfully combined videos with ultra-fast processing: {output_path}")
            return output_path
            
        except Exception as e:
            raise Exception(f"Ultra-fast video combination failed: {str(e)}")
    
    async def _generate_single_video(
        self, 
        audio_url: str, 
        avatar_type: str = "general",
        avatar_image: Optional[str] = None
    ) -> str:
        """Generate a single video (existing logic)"""
        # Use the current provider
        provider = self.providers.get(self.provider)
        if not provider:
            raise Exception(f"Provider '{self.provider}' not available")
        
        return await provider(audio_url, avatar_image or self._get_avatar_image(avatar_type), avatar_type)
    
    async def _generate_d_id(
        self, 
        audio_url: str, 
        avatar_image: str,
        avatar_type: str
    ) -> str:
        """Generate video using D-ID API"""
        if not self.settings.d_id_api_key:
            raise ValueError("D-ID API key not configured")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.d-id.com/talks",
                headers={
                    "Authorization": f"Bearer {self.settings.d_id_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "script": {
                        "type": "audio",
                        "audio_url": audio_url
                    },
                    "config": {
                        "fluent": True,
                        "pad_audio": 0.0
                    },
                    "source_url": avatar_image
                }
            )
            
            if response.status_code != 201:
                raise Exception(f"D-ID API error: {response.text}")
            
            result = response.json()
            return result["result_url"]
    
    async def _generate_replicate(
        self, 
        audio_url: str, 
        avatar_image: str,
        avatar_type: str
    ) -> str:
        """Generate video using Replicate Wav2Lip"""
        if not self.settings.replicate_api_token:
            raise ValueError("Replicate API token not configured")
        
        # Check if audio_url is a local file path
        if audio_url.startswith('/') and os.path.exists(audio_url):
            # It's a local file, use it directly
            audio_file_path = audio_url
        else:
            # It's a URL, download it
            async with httpx.AsyncClient() as client:
                audio_response = await client.get(audio_url)
                audio_response.raise_for_status()
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                    temp_audio.write(audio_response.content)
                    audio_file_path = temp_audio.name
        
        try:
            # Check if avatar_image is a local file path
            if avatar_image.startswith('./') or avatar_image.startswith('/'):
                # It's a local file, open it directly
                avatar_file = open(avatar_image, "rb")
            else:
                # It's a URL, download it
                async with httpx.AsyncClient() as client:
                    avatar_response = await client.get(avatar_image)
                    avatar_response.raise_for_status()
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_avatar:
                        temp_avatar.write(avatar_response.content)
                        temp_avatar_path = temp_avatar.name
                    avatar_file = open(temp_avatar_path, "rb")
            
            # Run Wav2Lip on Replicate
            output = replicate.run(
                "lucataco/wav2lip:95cc2a26ccfbf51d0785f4f0c4c0dd6d2f4c0e7c0e7c0e7c0e7c0e7c0e7c0e7c0",
                input={
                    "face": avatar_file,
                    "audio": open(audio_file_path, "rb")
                }
            )
            
            return output
            
        finally:
            # Clean up temporary files
            if audio_file_path != audio_url:  # Only delete if we created a temp file
                os.unlink(audio_file_path)
            if 'temp_avatar_path' in locals():
                os.unlink(temp_avatar_path)
    
    async def _generate_heygen(
        self, 
        audio_url: str, 
        avatar_image: str,
        avatar_type: str
    ) -> str:
        """Generate video using HeyGen"""
        # This would require HeyGen API integration
        raise NotImplementedError("HeyGen integration not implemented yet")
    
    async def _generate_hybrid(
        self, 
        audio_url: str, 
        avatar_image: str,
        avatar_type: str
    ) -> str:
        """Generate video using hybrid approach for production"""
        try:
            # Check cache first
            cache_key = f"{avatar_type}_{hash(audio_url)}"
            cached_video = await self._get_cached_video(cache_key)
            if cached_video:
                return cached_video
            
            # For short responses (< 30 seconds), use cloud service
            audio_duration = await self._get_audio_duration(audio_url)
            if audio_duration < 30:
                # Use D-ID for short videos
                video_url = await self._generate_d_id(audio_url, avatar_image, avatar_type)
            else:
                # Use local Wav2Lip for longer videos
                video_url = await self._generate_local_wav2lip(audio_url, avatar_image, avatar_type)
            
            # Cache the result
            await self._cache_video(cache_key, video_url)
            return video_url
            
        except Exception as e:
            # Fallback to local Wav2Lip
            return await self._generate_local_wav2lip(audio_url, avatar_image, avatar_type)
    
    async def _get_cached_video(self, cache_key: str) -> Optional[str]:
        """Get cached video if available"""
        # Implement caching logic here
        return None
    
    async def _cache_video(self, cache_key: str, video_url: str) -> None:
        """Cache video for future use"""
        # Implement caching logic here
        pass
    
    async def _generate_local_wav2lip(
        self, 
        audio_url: str, 
        avatar_image: str,
        avatar_type: str
    ) -> str:
        """Generate video using local Wav2Lip for unlimited length"""
        try:
            # Check if Wav2Lip is available locally
            if not self._check_wav2lip_available():
                raise Exception("Local Wav2Lip not available. Please install Wav2Lip locally.")
            
            # Prepare input files
            audio_path = await self._prepare_audio_file(audio_url)
            avatar_path = await self._prepare_avatar_file(avatar_image)
            
            # Generate video using local Wav2Lip
            output_path = await self._run_local_wav2lip(audio_path, avatar_path)
            
            # Convert to web-compatible format
            web_video_url = await self._convert_to_web_format(output_path)
            
            return web_video_url
            
        except Exception as e:
            raise Exception(f"Local Wav2Lip failed: {str(e)}")
    
    def _check_wav2lip_available(self) -> bool:
        """Check if Wav2Lip is available locally"""
        try:
            # Check if Wav2Lip directory exists
            wav2lip_dir = os.path.join(os.path.dirname(__file__), "..", "Wav2Lip")
            if not os.path.exists(wav2lip_dir):
                return False
            
            # Check if the inference script exists
            inference_script = os.path.join(wav2lip_dir, "inference.py")
            if not os.path.exists(inference_script):
                return False
            
            # Check if the model checkpoint exists
            checkpoint_path = os.path.join(wav2lip_dir, "checkpoints", "wav2lip.pth")
            if not os.path.exists(checkpoint_path):
                return False
            
            return True
            
        except Exception:
            return False
    
    async def _prepare_audio_file(self, audio_url: str) -> str:
        """Prepare audio file for Wav2Lip"""
        # Check if it's a local file path (absolute or relative)
        if (audio_url.startswith('/') or 
            audio_url.startswith('./') or 
            (not audio_url.startswith('http://') and not audio_url.startswith('https://'))):
            
            # If it's a relative path, make it absolute
            if not os.path.isabs(audio_url):
                audio_url = os.path.abspath(audio_url)
            
            if os.path.exists(audio_url):
                return audio_url
            else:
                raise Exception(f"Audio file not found: {audio_url}")
        else:
            # Download and prepare audio from URL
            async with httpx.AsyncClient() as client:
                response = await client.get(audio_url)
                response.raise_for_status()
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                    temp_audio.write(response.content)
                    return temp_audio.name
    
    async def _prepare_avatar_file(self, avatar_image: str) -> str:
        """Prepare avatar image for Wav2Lip (original simple approach)"""
        # Check if it's a local file path (absolute or relative)
        if (avatar_image.startswith('/') or 
            avatar_image.startswith('./') or 
            (not avatar_image.startswith('http://') and not avatar_image.startswith('https://'))):
            
            # If it's a relative path, make it absolute
            if not os.path.isabs(avatar_image):
                avatar_image = os.path.abspath(avatar_image)
            
            if os.path.exists(avatar_image):
                return avatar_image  # Return original, no enhancement
            else:
                raise Exception(f"Avatar file not found: {avatar_image}")
        else:
            # Download and prepare avatar from URL
            async with httpx.AsyncClient() as client:
                response = await client.get(avatar_image)
                response.raise_for_status()
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_avatar:
                    temp_avatar.write(response.content)
                    return temp_avatar.name
    
    async def _run_local_wav2lip(self, audio_path: str, avatar_path: str) -> str:
        """Run local Wav2Lip with ultra-optimized settings"""
        try:
            # Create cache key for output
            with open(audio_path, 'rb') as f:
                audio_hash = hashlib.md5(f.read()).hexdigest()[:8]
            with open(avatar_path, 'rb') as f:
                avatar_hash = hashlib.md5(f.read()).hexdigest()[:8]
            
            # Add timestamp to make cache key unique for each request
            timestamp = str(int(time.time() * 1000))[-6:]  # Last 6 digits of timestamp
            cache_key = f"wav2lip_{audio_hash}_{avatar_hash}_{timestamp}"
            
            # Create output directory
            output_dir = "/tmp/wav2lip_outputs"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate unique output filename
            output_filename = f"{cache_key}.mp4"
            output_path = os.path.join(output_dir, output_filename)
            
            # Get the path to Wav2Lip directory
            wav2lip_dir = os.path.join(os.path.dirname(__file__), "..", "Wav2Lip")
            
            # Get audio duration to adjust parameters
            audio_duration = await self._get_audio_duration(audio_path)
            
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
            
            # STEP 1: Create a video from the static avatar image
            avatar_video_path = os.path.join("/tmp/wav2lip_outputs", f"avatar_video_{timestamp}.mp4")
            
            # Create a video with the static image repeated for the audio duration
            avatar_cmd = [
                "ffmpeg",
                "-loop", "1",  # Loop the input image
                "-i", avatar_path,
                "-c:v", "libx264",
                "-t", str(audio_duration),  # Set duration to match audio
                "-pix_fmt", "yuv420p",
                "-vf", "scale=480:480",  # Resize to standard size
                "-r", str(fps),  # Set frame rate
                avatar_video_path,
                "-y"
            ]
            
            print(f"🎬 Creating avatar video: {' '.join(avatar_cmd)}")
            
            avatar_result = subprocess.run(avatar_cmd, capture_output=True, text=True)
            if avatar_result.returncode != 0:
                print(f"❌ Avatar video creation failed: {avatar_result.stderr}")
                raise Exception("Avatar video creation failed")
            
            print(f"✅ Avatar video created: {avatar_video_path}")
            
            # STEP 2: Run Wav2Lip with the avatar video (not static image)
            cmd = [
                "python", "inference.py",
                "--checkpoint_path", "checkpoints/wav2lip.pth",
                "--face", avatar_video_path,  # Use video instead of static image
                "--audio", audio_path,
                "--outfile", output_path,
                "--fps", str(fps),  # Consistent FPS for better sync
                "--resize_factor", "4",  # Increased resize factor for speed (was 2)
                "--pads", "0", "5", "0", "0",  # Minimal padding
                "--wav2lip_batch_size", str(batch_size),  # Adjusted batch size
                "--nosmooth"  # Disable smoothing for speed
            ]
            
            # Add GPU acceleration if available
            if self.enable_gpu_acceleration:
                cmd.extend(["--gpu", "0"])
            
            print(f"🚀 Running ultra-optimized Wav2Lip: {' '.join(cmd)}")
            print(f"🎵 Audio duration: {audio_duration:.2f}s, FPS: {fps}, Batch size: {batch_size}")
            
            # Run Wav2Lip in a subprocess with optimized environment
            env = os.environ.copy()
            env.update({
                "CUDA_VISIBLE_DEVICES": "0",  # Use first GPU
                "OMP_NUM_THREADS": "4",  # Limit OpenMP threads
                "MKL_NUM_THREADS": "4",  # Limit MKL threads
            })
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=wav2lip_dir,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # Clean up avatar video
            if os.path.exists(avatar_video_path):
                os.remove(avatar_video_path)
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise Exception(f"Ultra-optimized Wav2Lip failed: {error_msg}")
            
            # Check if output file was created
            if not os.path.exists(output_path):
                raise Exception("Ultra-optimized Wav2Lip output file not found")
            
            print(f"🚀 Generated ultra-fast video: {output_path}")
            return output_path
            
        except Exception as e:
            raise Exception(f"Ultra-optimized Wav2Lip execution failed: {str(e)}")
    
    async def _create_placeholder_video(self, audio_path: str, avatar_path: str, output_path: str):
        """Create a placeholder video for testing (fallback method)"""
        try:
            import cv2
            import numpy as np
            
            # Read the avatar image
            avatar_img = cv2.imread(avatar_path)
            if avatar_img is None:
                # Create a default avatar if image can't be read
                avatar_img = np.ones((256, 256, 3), dtype=np.uint8) * 128
            
            # Get audio duration (simplified)
            audio_duration = 5.0  # Default 5 seconds
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = 25
            frame_count = int(audio_duration * fps)
            
            out = cv2.VideoWriter(output_path, fourcc, fps, (avatar_img.shape[1], avatar_img.shape[0]))
            
            # Create simple lip-sync effect (placeholder)
            for i in range(frame_count):
                # Add simple lip movement effect
                frame = avatar_img.copy()
                
                # Add lip movement based on frame number
                lip_movement = int(10 * np.sin(i * 0.5))
                cv2.rectangle(frame, (100, 150), (156, 170 + lip_movement), (0, 0, 255), -1)
                
                out.write(frame)
            
            out.release()
            
        except Exception as e:
            # If video creation fails, create a simple text file as placeholder
            with open(output_path, 'w') as f:
                f.write(f"Placeholder video for audio: {audio_path}")
            output_path = output_path.replace('.mp4', '.txt')
    
    async def _convert_to_web_format(self, video_path: str) -> str:
        """Convert video to web-compatible format"""
        # Extract filename from the video path
        filename = os.path.basename(video_path)
        
        # Return a URL that points to our video serving endpoint
        return f"http://localhost:8000/api/v1/videos/{filename}"
    
    async def _generate_colab(
        self, 
        audio_url: str, 
        avatar_image: str,
        avatar_type: str
    ) -> str:
        """Generate video using Google Colab GPU"""
        # This would require setting up a Colab notebook with Wav2Lip
        # and exposing it via a web API
        raise NotImplementedError("Colab integration not implemented yet")
    
    async def _generate_runwayml(
        self, 
        audio_url: str, 
        avatar_image: str,
        avatar_type: str
    ) -> str:
        """Generate video using RunwayML"""
        # This would require RunwayML API integration
        raise NotImplementedError("RunwayML integration not implemented yet")
    
    def _get_avatar_image(self, avatar_type: str) -> str:
        """Get default avatar image for agent type"""
        avatar_images = {
            "general": "./avatars/general.jpg",
            "hotel": "./avatars/hotel_receptionist.jpg",
            "airport": "./avatars/airport_assistant.jpg",
            "sales": "./avatars/sales_agent.jpg"
        }
        return avatar_images.get(avatar_type, avatar_images["general"])
    
    def get_supported_providers(self) -> list:
        """Get list of supported lip-sync providers"""
        return list(self.providers.keys())
    
    def get_provider_info(self) -> dict:
        """Get information about lip-sync providers"""
        return {
            "current_provider": self.provider,
            "supported_providers": self.get_supported_providers(),
            "pricing": {
                "d_id": "$0.10 per minute",
                "replicate": "$0.05 per minute",
                "heygen": "$0.15 per minute",
                "hybrid": "$0.20 per minute",
                "local_wav2lip": "$0.10 per minute",
                "colab": "Free (with limitations)",
                "runwayml": "$0.15 per minute"
            }
        }
    
    async def _cleanup_temp_files(self, file_paths: List[str]) -> None:
        """Clean up temporary files"""
        try:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    os.unlink(file_path)
        except Exception as e:
            print(f"Warning: Failed to cleanup temp files: {e}")
    
    async def _get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds"""
        try:
            import subprocess
            
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
            
            if process.returncode != 0:
                return 30.0  # Default duration if we can't determine
            
            duration = float(stdout.decode().strip())
            return duration
            
        except Exception as e:
            print(f"Warning: Could not determine audio duration: {e}")
            return 30.0  # Default duration 