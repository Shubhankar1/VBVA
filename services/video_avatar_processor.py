"""
Video Avatar Processor for VBVA
Handles AI-generated video avatars with intelligent fallbacks
"""

import os
import asyncio
import tempfile
import subprocess
from typing import Optional, Dict, List
from pathlib import Path
import hashlib
import json

class VideoAvatarProcessor:
    """Video-only avatar processor with AI-generated video support"""
    
    def __init__(self):
        # Use absolute paths to avoid working directory issues
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.avatar_dir = Path(project_root) / "avatars"
        self.video_dir = self.avatar_dir / "videos"
        self.ai_generated_dir = self.video_dir / "ai_generated"
        self.enhanced_dir = self.video_dir / "enhanced"
        self.legacy_dir = self.video_dir / "legacy"
        self.static_dir = self.avatar_dir
        self.enhanced_static_dir = self.avatar_dir / "enhanced"
        
        # Create directories if they don't exist
        self.ai_generated_dir.mkdir(parents=True, exist_ok=True)
        self.enhanced_dir.mkdir(parents=True, exist_ok=True)
        self.legacy_dir.mkdir(parents=True, exist_ok=True)
        
        # Video avatar configurations
        self.video_configs = {
            "general": {
                "ai_video": "general_ai.mp4",
                "enhanced_video": "general_enhanced.mp4",
                "legacy_video": "general_talking.mp4",
                "static_image": "general.jpg",
                "enhanced_image": "general_enhanced.jpg"
            },
            "hotel": {
                "ai_video": "hotel_ai.mp4",
                "enhanced_video": "hotel_enhanced.mp4",
                "legacy_video": "hotel_receptionist_talking.mp4",
                "static_image": "hotel_receptionist.jpg",
                "enhanced_image": "hotel_receptionist_enhanced.jpg"
            },
            "airport": {
                "ai_video": "airport_ai.mp4",
                "enhanced_video": "airport_enhanced.mp4",
                "legacy_video": "airport_assistant_talking.mp4",
                "static_image": "airport_assistant.jpg",
                "enhanced_image": "airport_assistant_enhanced.jpg"
            },
            "sales": {
                "ai_video": "sales_ai.mp4",
                "enhanced_video": "sales_enhanced.mp4",
                "legacy_video": "sales_agent_talking.mp4",
                "static_image": "sales_agent.jpg",
                "enhanced_image": "sales_agent_enhanced.jpg"
            }
        }
        
        # Cache for video metadata
        self.video_cache = {}
    
    async def get_video_avatar(self, agent_type: str) -> str:
        """Get the best available video avatar with intelligent fallback"""
        
        config = self.video_configs.get(agent_type, self.video_configs["general"])
        
        # Priority order: AI-generated > Enhanced > Legacy > Static (converted to video)
        
        # 1. Try AI-generated video first
        ai_video_path = self.ai_generated_dir / config["ai_video"]
        if ai_video_path.exists():
            print(f"🎬 Using AI-generated video for {agent_type}")
            return str(ai_video_path)
        
        # 2. Try enhanced video
        enhanced_video_path = self.enhanced_dir / config["enhanced_video"]
        if enhanced_video_path.exists():
            print(f"🎬 Using enhanced video for {agent_type}")
            return str(enhanced_video_path)
        
        # 3. Try legacy video
        legacy_video_path = self.legacy_dir / config["legacy_video"]
        if legacy_video_path.exists():
            print(f"🎬 Using legacy video for {agent_type}")
            return str(legacy_video_path)
        
        # 4. Fallback to static image (will be converted to video during processing)
        enhanced_image_path = self.enhanced_static_dir / config["enhanced_image"]
        if enhanced_image_path.exists():
            print(f"🖼️ Using enhanced static image for {agent_type} (will be converted to video)")
            return str(enhanced_image_path)
        
        # 5. Final fallback to original static image
        static_image_path = self.static_dir / config["static_image"]
        if static_image_path.exists():
            print(f"🖼️ Using original static image for {agent_type} (will be converted to video)")
            return str(static_image_path)
        
        # 6. Ultimate fallback to general avatar, but prevent infinite recursion
        if agent_type == "general":
            print("❌ No avatar found for 'general'. Returning static image as last resort.")
            return str(self.static_dir / self.video_configs["general"]["static_image"])
        print(f"⚠️ No avatar found for {agent_type}, using general avatar")
        return await self.get_video_avatar("general")
    
    async def add_ai_generated_video(self, agent_type: str, video_path: str) -> bool:
        """Add an AI-generated video to the system"""
        
        try:
            config = self.video_configs.get(agent_type, self.video_configs["general"])
            target_path = self.ai_generated_dir / config["ai_video"]
            
            # Validate video
            if not await self._validate_video(video_path):
                print(f"❌ Invalid video file: {video_path}")
                return False
            
            # Copy video to target location
            import shutil
            shutil.copy2(video_path, target_path)
            
            # Clear cache for this agent type
            if agent_type in self.video_cache:
                del self.video_cache[agent_type]
            
            print(f"✅ Added AI-generated video for {agent_type}: {target_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding AI-generated video: {str(e)}")
            return False
    
    async def _validate_video(self, video_path: str) -> bool:
        """Validate video file format and properties"""
        
        try:
            # Check if file exists
            if not os.path.exists(video_path):
                return False
            
            # Get video information using ffprobe
            cmd = [
                "ffprobe", "-v", "quiet",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height,duration,codec_name",
                "-of", "json",
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return False
            
            # Parse video info
            video_info = json.loads(result.stdout)
            if "streams" not in video_info or len(video_info["streams"]) == 0:
                return False
            
            stream = video_info["streams"][0]
            
            # Check basic requirements
            width = int(stream.get("width", 0))
            height = int(stream.get("height", 0))
            codec = stream.get("codec_name", "")
            duration = float(stream.get("duration", 0))
            
            # Validate requirements
            if width < 256 or height < 256:
                print(f"⚠️ Video resolution too low: {width}x{height}")
                return False
            
            if codec not in ["h264", "hevc"]:
                print(f"⚠️ Unsupported codec: {codec}")
                return False
            
            if duration < 1.0 or duration > 30.0:
                print(f"⚠️ Video duration out of range: {duration}s")
                return False
            
            # Check file size
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
            if file_size > 50:  # 50MB limit
                print(f"⚠️ Video file too large: {file_size:.1f}MB")
                return False
            
            print(f"✅ Video validation passed: {width}x{height}, {duration:.1f}s, {file_size:.1f}MB")
            return True
            
        except Exception as e:
            print(f"❌ Video validation error: {str(e)}")
            return False
    
    async def optimize_video_for_wav2lip(self, video_path: str, output_path: Optional[str] = None) -> Optional[str]:
        """Optimize video for Wav2Lip processing"""
        
        try:
            if output_path is None:
                # Create optimized version in enhanced directory
                filename = os.path.basename(video_path)
                name, ext = os.path.splitext(filename)
                output_path = str(self.enhanced_dir / f"{name}_optimized{ext}")
            
            # Optimize video for Wav2Lip
            cmd = [
                "ffmpeg", "-i", video_path,
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                "-pix_fmt", "yuv420p",
                "-vf", "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2",
                "-r", "25",  # 25 FPS
                "-t", "5",   # 5 seconds
                "-loop", "1",  # Make it loopable
                output_path,
                "-y"
            ]
            
            print(f"🎬 Optimizing video for Wav2Lip: {os.path.basename(video_path)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Video optimized: {output_path}")
                return output_path
            else:
                print(f"❌ Video optimization failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error optimizing video: {str(e)}")
            return None
    
    async def get_video_metadata(self, video_path: str) -> Dict:
        """Get metadata for a video file"""
        
        try:
            cmd = [
                "ffprobe", "-v", "quiet",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height,duration,codec_name,bit_rate",
                "-show_entries", "format=duration,size",
                "-of", "json",
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return {}
            
            return json.loads(result.stdout)
            
        except Exception as e:
            print(f"❌ Error getting video metadata: {str(e)}")
            return {}
    
    def get_available_videos(self) -> Dict[str, Dict]:
        """Get information about all available video avatars"""
        
        available = {}
        
        for agent_type, config in self.video_configs.items():
            agent_info = {
                "ai_generated": False,
                "enhanced": False,
                "legacy": False,
                "static_fallback": False,
                "file_sizes": {},
                "total_size": 0
            }
            
            # Check AI-generated video
            ai_path = self.ai_generated_dir / config["ai_video"]
            if ai_path.exists():
                agent_info["ai_generated"] = True
                size = ai_path.stat().st_size / (1024 * 1024)
                agent_info["file_sizes"]["ai_generated"] = size
                agent_info["total_size"] += size
            
            # Check enhanced video
            enhanced_path = self.enhanced_dir / config["enhanced_video"]
            if enhanced_path.exists():
                agent_info["enhanced"] = True
                size = enhanced_path.stat().st_size / (1024 * 1024)
                agent_info["file_sizes"]["enhanced"] = size
                agent_info["total_size"] += size
            
            # Check legacy video
            legacy_path = self.legacy_dir / config["legacy_video"]
            if legacy_path.exists():
                agent_info["legacy"] = True
                size = legacy_path.stat().st_size / (1024 * 1024)
                agent_info["file_sizes"]["legacy"] = size
                agent_info["total_size"] += size
            
            # Check static fallback
            static_path = self.static_dir / config["static_image"]
            if static_path.exists():
                agent_info["static_fallback"] = True
                size = static_path.stat().st_size / (1024 * 1024)
                agent_info["file_sizes"]["static"] = size
                agent_info["total_size"] += size
            
            available[agent_type] = agent_info
        
        return available
    
    async def create_video_placeholder(self, agent_type: str, duration: float = 5.0) -> Optional[str]:
        """Create a placeholder video for testing"""
        
        try:
            config = self.video_configs.get(agent_type, self.video_configs["general"])
            placeholder_path = self.ai_generated_dir / config["ai_video"]
            
            # Get static image for placeholder
            static_path = self.static_dir / config["static_image"]
            if not static_path.exists():
                print(f"❌ Static image not found for placeholder: {static_path}")
                return None
            
            # Create simple placeholder video
            cmd = [
                "ffmpeg",
                "-loop", "1",
                "-i", str(static_path),
                "-c:v", "libx264",
                "-t", str(duration),
                "-pix_fmt", "yuv420p",
                "-vf", "scale=512:512",
                "-r", "25",
                str(placeholder_path),
                "-y"
            ]
            
            print(f"🎬 Creating placeholder video for {agent_type}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Placeholder video created: {placeholder_path}")
                return str(placeholder_path)
            else:
                print(f"❌ Placeholder creation failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating placeholder: {str(e)}")
            return None
    
    async def cleanup_old_videos(self, max_age_days: int = 30) -> int:
        """Clean up old video files"""
        
        import time
        from datetime import datetime, timedelta
        
        cutoff_time = time.time() - (max_age_days * 24 * 60 * 60)
        cleaned_count = 0
        
        for video_dir in [self.ai_generated_dir, self.enhanced_dir, self.legacy_dir]:
            for video_file in video_dir.glob("*.mp4"):
                if video_file.stat().st_mtime < cutoff_time:
                    try:
                        video_file.unlink()
                        cleaned_count += 1
                        print(f"🗑️ Cleaned up old video: {video_file.name}")
                    except Exception as e:
                        print(f"❌ Error cleaning up {video_file.name}: {str(e)}")
        
        return cleaned_count 