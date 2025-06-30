#!/usr/bin/env python3
"""
Test Wav2Lip Directly
"""

import asyncio
import os
import subprocess
import tempfile

async def test_wav2lip_direct():
    """Test Wav2Lip directly"""
    
    print("🔍 Testing Wav2Lip directly...")
    
    # Check if we have the required files
    wav2lip_dir = "./Wav2Lip"
    checkpoint_path = os.path.join(wav2lip_dir, "checkpoints/wav2lip.pth")
    inference_script = os.path.join(wav2lip_dir, "inference.py")
    
    print(f"📁 Wav2Lip directory: {wav2lip_dir}")
    print(f"📁 Checkpoint exists: {os.path.exists(checkpoint_path)}")
    print(f"📁 Inference script exists: {os.path.exists(inference_script)}")
    
    # Create a simple test audio file
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        # Create a simple beep sound
        import wave
        import struct
        
        sample_rate = 44100
        duration = 2.0  # 2 seconds
        frequency = 440  # A4 note
        
        # Generate beep samples
        samples = []
        for i in range(int(sample_rate * duration)):
            sample = int(32767 * 0.3 * (i % 2))  # Simple square wave
            samples.append(struct.pack('<h', sample))
        
        # Write WAV file
        with wave.open(f.name, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b''.join(samples))
        
        test_audio = f.name
    
    print(f"🎵 Created test audio: {test_audio}")
    
    # Test avatar
    avatar_path = os.path.abspath("./avatars/general.jpg")
    print(f"🖼️  Avatar exists: {os.path.exists(avatar_path)}")
    print(f"🖼️  Avatar path: {avatar_path}")
    
    # Create output directory
    output_dir = "/tmp/wav2lip_ultra_outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "test_direct.mp4")
    
    print(f"📁 Output path: {output_path}")
    
    # Run Wav2Lip
    cmd = [
        "python", "inference.py",
        "--checkpoint_path", "checkpoints/wav2lip.pth",
        "--face", avatar_path,
        "--audio", test_audio,
        "--outfile", output_path,
        "--static", "True",
        "--fps", "10",
        "--resize_factor", "6",
        "--pads", "0", "2", "0", "0",
        "--wav2lip_batch_size", "64",
        "--nosmooth"
    ]
    
    print(f"🚀 Running command: {' '.join(cmd)}")
    
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=wav2lip_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        print(f"📊 Process completed with return code: {process.returncode}")
        print(f"📤 Stdout: {stdout.decode()[:500]}...")
        print(f"📥 Stderr: {stderr.decode()[:500]}...")
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Video created successfully! Size: {file_size} bytes")
        else:
            print(f"❌ Video file not created")
            
    except Exception as e:
        print(f"❌ Error running Wav2Lip: {e}")
    
    # Cleanup
    os.unlink(test_audio)
    print("🧹 Cleaned up test audio")

if __name__ == "__main__":
    asyncio.run(test_wav2lip_direct()) 