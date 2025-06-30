"""
Enhanced Avatar Processing Service
Handles both static images and videos with intelligent optimization
"""

import os
import cv2
import numpy as np
import tempfile
import asyncio
from typing import Optional, Dict, List, Tuple
from pathlib import Path
import subprocess
import hashlib
import json

class EnhancedAvatarProcessor:
    """Enhanced avatar processor with hybrid image/video support"""
    
    def __init__(self):
        self.avatar_dir = Path("./avatars")
        self.enhanced_dir = self.avatar_dir / "enhanced"
        self.video_dir = self.avatar_dir / "videos"
        
        # Create directories if they don't exist
        self.enhanced_dir.mkdir(exist_ok=True)
        self.video_dir.mkdir(exist_ok=True)
        
        # Avatar configurations
        self.avatar_configs = {
            "general": {
                "image": "general.jpg",
                "enhanced_image": "general_enhanced.jpg",
                "video": "general_talking.mp4",
                "expressions": ["neutral", "happy", "professional"]
            },
            "hotel": {
                "image": "hotel_receptionist.jpg",
                "enhanced_image": "hotel_receptionist_enhanced.jpg",
                "video": "hotel_receptionist_talking.mp4",
                "expressions": ["welcoming", "helpful", "professional"]
            },
            "airport": {
                "image": "airport_assistant.jpg",
                "enhanced_image": "airport_assistant_enhanced.jpg",
                "video": "airport_assistant_talking.mp4",
                "expressions": ["informative", "helpful", "calm"]
            },
            "sales": {
                "image": "sales_agent.jpg",
                "enhanced_image": "sales_agent_enhanced.jpg",
                "video": "sales_agent_talking.mp4",
                "expressions": ["enthusiastic", "professional", "friendly"]
            }
        }
    
    async def get_optimal_avatar(
        self, 
        agent_type: str, 
        content_length: int = 0,
        use_video: bool = False
    ) -> str:
        """Get the optimal avatar (image or video) based on content and preferences"""
        
        config = self.avatar_configs.get(agent_type, self.avatar_configs["general"])
        
        # Determine if we should use video based on content length and preference
        should_use_video = (
            use_video and 
            content_length > 100 and  # Longer content benefits from video
            await self._has_video_avatar(agent_type)
        )
        
        if should_use_video:
            video_path = await self._get_video_avatar(agent_type)
            if video_path:
                print(f"🎬 Using video avatar for {agent_type}")
                return video_path
        
        # Fall back to enhanced static image
        enhanced_path = await self._get_enhanced_image(agent_type)
        if enhanced_path:
            print(f"🖼️ Using enhanced static avatar for {agent_type}")
            return enhanced_path
        
        # Final fallback to original image
        original_path = await self._get_original_image(agent_type)
        print(f"🖼️ Using original static avatar for {agent_type}")
        return original_path
    
    async def _has_video_avatar(self, agent_type: str) -> bool:
        """Check if video avatar exists for the agent type"""
        config = self.avatar_configs.get(agent_type, self.avatar_configs["general"])
        video_path = self.video_dir / config["video"]
        return video_path.exists()
    
    async def _get_video_avatar(self, agent_type: str) -> Optional[str]:
        """Get video avatar path if available"""
        config = self.avatar_configs.get(agent_type, self.avatar_configs["general"])
        video_path = self.video_dir / config["video"]
        
        if video_path.exists():
            return str(video_path)
        return None
    
    async def _get_enhanced_image(self, agent_type: str) -> Optional[str]:
        """Get enhanced image path if available"""
        config = self.avatar_configs.get(agent_type, self.avatar_configs["general"])
        enhanced_path = self.enhanced_dir / config["enhanced_image"]
        
        if enhanced_path.exists():
            return str(enhanced_path)
        return None
    
    async def _get_original_image(self, agent_type: str) -> str:
        """Get original image path"""
        config = self.avatar_configs.get(agent_type, self.avatar_configs["general"])
        original_path = self.avatar_dir / config["image"]
        
        if original_path.exists():
            return str(original_path)
        
        # Fallback to general avatar
        return str(self.avatar_dir / self.avatar_configs["general"]["image"])
    
    async def create_enhanced_avatar_video(
        self, 
        agent_type: str, 
        duration: float = 10.0,
        fps: int = 25
    ) -> Optional[str]:
        """Create an enhanced avatar video from static image with subtle movements"""
        
        try:
            # Get the enhanced image
            image_path = await self._get_enhanced_image(agent_type)
            if not image_path:
                image_path = await self._get_original_image(agent_type)
            
            if not os.path.exists(image_path):
                print(f"❌ Image not found: {image_path}")
                return None
            
            # Create output video path
            config = self.avatar_configs.get(agent_type, self.avatar_configs["general"])
            output_path = self.video_dir / config["video"]
            
            # Create enhanced video with subtle movements
            success = await self._create_enhanced_video(
                image_path, 
                str(output_path), 
                duration, 
                fps
            )
            
            if success:
                print(f"✅ Created enhanced video avatar: {output_path}")
                return str(output_path)
            else:
                print(f"❌ Failed to create enhanced video avatar")
                return None
                
        except Exception as e:
            print(f"❌ Error creating enhanced avatar video: {str(e)}")
            return None
    
    async def _create_enhanced_video(
        self, 
        image_path: str, 
        output_path: str, 
        duration: float, 
        fps: int
    ) -> bool:
        """Create enhanced video with subtle facial movements"""
        
        try:
            # Read the image
            img = cv2.imread(image_path)
            if img is None:
                return False
            
            # Ensure proper dimensions
            height, width = img.shape[:2]
            target_size = 512  # Optimal size for Wav2Lip
            
            if width != target_size or height != target_size:
                img = cv2.resize(img, (target_size, target_size), interpolation=cv2.INTER_LANCZOS4)
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (target_size, target_size))
            
            frame_count = int(duration * fps)
            
            # Create subtle movements
            for i in range(frame_count):
                frame = img.copy()
                
                # Add subtle breathing movement (very slight scaling)
                scale_factor = 1.0 + 0.002 * np.sin(i * 0.1)  # Very subtle scaling
                if scale_factor != 1.0:
                    new_size = int(target_size * scale_factor)
                    frame = cv2.resize(frame, (new_size, new_size), interpolation=cv2.INTER_LANCZOS4)
                    
                    # Center the frame
                    if new_size > target_size:
                        start = (new_size - target_size) // 2
                        frame = frame[start:start+target_size, start:start+target_size]
                    else:
                        # Pad if smaller
                        pad = (target_size - new_size) // 2
                        padded = np.zeros((target_size, target_size, 3), dtype=np.uint8)
                        padded[pad:pad+new_size, pad:pad+new_size] = frame
                        frame = padded
                
                # Add very subtle head movement
                angle = 0.5 * np.sin(i * 0.05)  # Very subtle rotation
                if abs(angle) > 0.1:
                    center = (target_size // 2, target_size // 2)
                    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                    frame = cv2.warpAffine(frame, rotation_matrix, (target_size, target_size))
                
                out.write(frame)
            
            out.release()
            
            # Convert to web-compatible format
            web_path = output_path.replace('.mp4', '_web.mp4')
            cmd = [
                "ffmpeg", "-i", output_path,
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                "-pix_fmt", "yuv420p",
                web_path,
                "-y"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # Replace original with web-compatible version
                os.replace(web_path, output_path)
                return True
            else:
                print(f"❌ Video conversion failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating enhanced video: {str(e)}")
            return False
    
    async def enhance_all_avatars(self) -> Dict[str, bool]:
        """Enhance all avatar images and create video versions"""
        
        results = {}
        
        for agent_type in self.avatar_configs.keys():
            print(f"\n🎨 Enhancing avatar: {agent_type}")
            
            # Enhance static image
            image_enhanced = await self._enhance_static_image(agent_type)
            
            # Create video version
            video_created = await self.create_enhanced_avatar_video(agent_type)
            
            results[agent_type] = {
                "image_enhanced": image_enhanced,
                "video_created": video_created is not None
            }
            
            print(f"✅ {agent_type}: Image enhanced: {image_enhanced}, Video created: {video_created is not None}")
        
        return results
    
    async def _enhance_static_image(self, agent_type: str) -> bool:
        """Enhance static image for better quality"""
        
        try:
            config = self.avatar_configs.get(agent_type, self.avatar_configs["general"])
            input_path = self.avatar_dir / config["image"]
            output_path = self.enhanced_dir / config["enhanced_image"]
            
            if not input_path.exists():
                print(f"❌ Input image not found: {input_path}")
                return False
            
            # Read the image
            img = cv2.imread(str(input_path))
            if img is None:
                return False
            
            # Get original dimensions
            height, width = img.shape[:2]
            
            # Ensure minimum size for good quality
            min_size = 512
            if width < min_size or height < min_size:
                scale_factor = max(min_size / width, min_size / height)
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
            
            # Ensure square aspect ratio
            if img.shape[0] != img.shape[1]:
                max_dim = max(img.shape[0], img.shape[1])
                square_img = np.zeros((max_dim, max_dim, 3), dtype=np.uint8)
                
                y_offset = (max_dim - img.shape[0]) // 2
                x_offset = (max_dim - img.shape[1]) // 2
                square_img[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
                img = square_img
            
            # Apply enhancements
            # Sharpening
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            img = cv2.filter2D(img, -1, kernel)
            
            # Contrast enhancement
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            lab = cv2.merge([l, a, b])
            img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            # Noise reduction
            img = cv2.bilateralFilter(img, 9, 75, 75)
            
            # Save enhanced image
            cv2.imwrite(str(output_path), img, [cv2.IMWRITE_JPEG_QUALITY, 95])
            
            return True
            
        except Exception as e:
            print(f"❌ Error enhancing image: {str(e)}")
            return False
    
    def get_avatar_stats(self) -> Dict[str, Dict]:
        """Get statistics about available avatars"""
        
        stats = {}
        
        for agent_type, config in self.avatar_configs.items():
            agent_stats = {
                "has_original": False,
                "has_enhanced": False,
                "has_video": False,
                "file_sizes": {}
            }
            
            # Check original image
            original_path = self.avatar_dir / config["image"]
            if original_path.exists():
                agent_stats["has_original"] = True
                agent_stats["file_sizes"]["original"] = original_path.stat().st_size / (1024 * 1024)  # MB
            
            # Check enhanced image
            enhanced_path = self.enhanced_dir / config["enhanced_image"]
            if enhanced_path.exists():
                agent_stats["has_enhanced"] = True
                agent_stats["file_sizes"]["enhanced"] = enhanced_path.stat().st_size / (1024 * 1024)  # MB
            
            # Check video
            video_path = self.video_dir / config["video"]
            if video_path.exists():
                agent_stats["has_video"] = True
                agent_stats["file_sizes"]["video"] = video_path.stat().st_size / (1024 * 1024)  # MB
            
            stats[agent_type] = agent_stats
        
        return stats 