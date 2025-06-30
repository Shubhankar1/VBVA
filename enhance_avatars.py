#!/usr/bin/env python3
"""
Script to enhance avatar images for better Wav2Lip quality
"""

import cv2
import numpy as np
import os
from pathlib import Path

def enhance_avatar_image(input_path: str, output_path: str = None):
    """Enhance avatar image for better lip-sync results"""
    try:
        # Read the image
        img = cv2.imread(input_path)
        if img is None:
            print(f"❌ Could not read image: {input_path}")
            return False
        
        # Get original dimensions
        height, width = img.shape[:2]
        print(f"📏 Original size: {width}x{height}")
        
        # Ensure minimum size for good quality
        min_size = 512  # Increased for better quality
        if width < min_size or height < min_size:
            # Upscale if too small
            scale_factor = max(min_size / width, min_size / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
            print(f"📈 Upscaled to: {new_width}x{new_height}")
        
        # Ensure square aspect ratio (Wav2Lip works better with square images)
        if width != height:
            # Make it square by padding
            max_dim = max(img.shape[0], img.shape[1])
            square_img = np.zeros((max_dim, max_dim, 3), dtype=np.uint8)
            
            # Center the image
            y_offset = (max_dim - img.shape[0]) // 2
            x_offset = (max_dim - img.shape[1]) // 2
            square_img[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
            img = square_img
            print(f"⬜ Made square: {max_dim}x{max_dim}")
        
        # Apply slight sharpening for better lip detection
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        img = cv2.filter2D(img, -1, kernel)
        
        # Apply contrast enhancement
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        lab = cv2.merge([l, a, b])
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Apply slight noise reduction
        img = cv2.bilateralFilter(img, 9, 75, 75)
        
        # Save enhanced image
        if output_path is None:
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}_enhanced.jpg"
        
        cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        # Get file sizes
        original_size = os.path.getsize(input_path) / (1024 * 1024)
        enhanced_size = os.path.getsize(output_path) / (1024 * 1024)
        
        print(f"✅ Enhanced image saved: {output_path}")
        print(f"📊 Original: {original_size:.2f} MB → Enhanced: {enhanced_size:.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Error enhancing image: {str(e)}")
        return False

def main():
    """Enhance all avatar images"""
    print("🎨 Enhancing Avatar Images for Better Lip-Sync Quality")
    print("=" * 60)
    
    # Get avatar directory
    avatar_dir = Path("./avatars")
    if not avatar_dir.exists():
        print("❌ Avatars directory not found")
        return
    
    # Find all image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    avatar_files = []
    
    for ext in image_extensions:
        avatar_files.extend(avatar_dir.glob(f"*{ext}"))
        avatar_files.extend(avatar_dir.glob(f"*{ext.upper()}"))
    
    if not avatar_files:
        print("❌ No avatar images found")
        return
    
    print(f"📁 Found {len(avatar_files)} avatar images")
    
    # Create enhanced directory
    enhanced_dir = avatar_dir / "enhanced"
    enhanced_dir.mkdir(exist_ok=True)
    
    # Enhance each avatar
    success_count = 0
    for avatar_file in avatar_files:
        print(f"\n🖼️  Processing: {avatar_file.name}")
        
        output_path = enhanced_dir / f"{avatar_file.stem}_enhanced.jpg"
        
        if enhance_avatar_image(str(avatar_file), str(output_path)):
            success_count += 1
        else:
            print(f"❌ Failed to enhance {avatar_file.name}")
    
    print(f"\n🎉 Enhancement complete!")
    print(f"✅ Successfully enhanced: {success_count}/{len(avatar_files)} images")
    print(f"📁 Enhanced images saved in: {enhanced_dir}")
    
    # Update the lip-sync service to use enhanced avatars
    print(f"\n💡 To use enhanced avatars, update the avatar paths in services/lip_sync.py:")
    for avatar_file in avatar_files:
        enhanced_path = enhanced_dir / f"{avatar_file.stem}_enhanced.jpg"
        if enhanced_path.exists():
            print(f"   {avatar_file.name} → {enhanced_path}")

if __name__ == "__main__":
    main() 