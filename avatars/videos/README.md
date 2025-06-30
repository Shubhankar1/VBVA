# Video Avatars Directory

This directory contains AI-generated video avatars for the VBVA system.

## 📁 Directory Structure

```
avatars/videos/
├── README.md                    # This file
├── ai_generated/                # AI-generated 5-second videos
│   ├── general_ai.mp4          # General assistant AI video
│   ├── hotel_ai.mp4            # Hotel receptionist AI video
│   ├── airport_ai.mp4          # Airport assistant AI video
│   ├── sales_ai.mp4            # Sales agent AI video
│   └── ...                     # Additional AI-generated videos
├── enhanced/                    # Enhanced versions (if needed)
│   ├── general_enhanced.mp4
│   ├── hotel_enhanced.mp4
│   └── ...
└── legacy/                      # Legacy generated videos
    ├── general_talking.mp4
    ├── hotel_receptionist_talking.mp4
    └── ...
```

## 🎬 Video Specifications

### AI-Generated Videos (Recommended)
- **Duration:** 5 seconds (loopable)
- **Format:** MP4 (H.264)
- **Resolution:** 512x512 or 720x720
- **Frame Rate:** 25 FPS
- **File Size:** Target 2-8 MB per video
- **Content:** Natural talking movements, subtle expressions

### Naming Convention
- `{agent_type}_ai.mp4` for AI-generated videos
- `{agent_type}_enhanced.mp4` for enhanced versions
- `{agent_type}_talking.mp4` for legacy generated videos

## 🔧 Integration

The system will automatically use AI-generated videos when available, falling back to enhanced static images if needed.

## 📊 File Size Guidelines

| Agent Type | Target Size | Max Size |
|------------|-------------|----------|
| General    | 3-5 MB      | 8 MB     |
| Hotel      | 3-5 MB      | 8 MB     |
| Airport    | 3-5 MB      | 8 MB     |
| Sales      | 3-5 MB      | 8 MB     |

## 🚀 Usage

1. Place your AI-generated videos in `ai_generated/` directory
2. Follow the naming convention: `{agent_type}_ai.mp4`
3. Ensure videos are 5 seconds and loopable
4. Test with the system to verify quality 