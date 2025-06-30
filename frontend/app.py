"""
VBVA Frontend - Streamlit Application
Interactive interface for Video-Based Virtual Assistant
"""

import streamlit as st
import requests
import json
import time
import os
from typing import Optional
import tempfile
from pathlib import Path

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_BASE = f"{BACKEND_URL}/api/v1"

def main():
    st.set_page_config(
        page_title="VBVA - Video-Based Virtual Assistant",
        page_icon="🎥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .video-container {
        text-align: center;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🎥 VBVA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Video-Based Virtual Assistant</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Agent selection
        agent_type = st.selectbox(
            "Select Agent Type",
            ["general", "hotel", "airport", "sales"],
            format_func=lambda x: x.title()
        )
        
        # Session management
        if "session_id" not in st.session_state:
            st.session_state.session_id = None
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 New Session"):
                st.session_state.session_id = None
                st.session_state.messages = []
                clear_cached_video_urls()
                st.rerun()
        
        with col2:
            if st.button("🧹 Clear Cache"):
                clear_cached_video_urls()
                st.rerun()
        
        if st.session_state.session_id:
            st.info(f"Session ID: {st.session_state.session_id[:8]}...")
        
        # Backend status
        st.header("📊 System Status")
        if check_backend_health():
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Unavailable")
    
    # Main content area
    st.header("💬 Chat Interface")
    
    # Initialize messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "video_url" in message and message["video_url"]:
                robust_video_display(message["video_url"])
    
    # Chat input - moved outside of tabs
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            try:
                # Step 1: Get text response
                with st.spinner("🤖 Processing text response..."):
                    response = send_text_message(prompt, agent_type)
                
                if response:
                    # Display text response
                    message_text = response.get("message", "No response received")
                    st.write(message_text)
                    
                    # Debug: Log the text being sent to video generation
                    st.info(f"🔍 Debug: Sending text to video generation (length: {len(message_text)} chars)")
                    st.code(message_text[:200] + "..." if len(message_text) > 200 else message_text)
                    
                    # Step 2: Automatically generate video
                    video_response = generate_video_with_progress(message_text, agent_type)
                    
                    if video_response and video_response.get("video_url"):
                        video_url = video_response["video_url"]
                        
                        # Accept both combined videos (ultra_combined_*) and single videos (ultra_wav2lip_*) as valid
                        if "ultra_combined_" in video_url or "ultra_wav2lip_" in video_url:
                            st.success("✅ Video generated successfully!")
                            st.info(f"Video URL: {video_url}")
                            
                            # Clear any old video URLs from session state to prevent caching issues
                            for msg in st.session_state.messages:
                                if "video_url" in msg:
                                    del msg["video_url"]
                            
                            # Enhanced video display with multiple fallback methods
                            robust_video_display(video_url)
                            
                            # Add video URL to last assistant message with cache-busting
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": response.get("message", ""),
                                "video_url": video_response["video_url"]
                            })
                        else:
                            st.warning("⚠️ Unknown video URL pattern")
                            st.info(f"Video URL: {video_url}")
                            
                            # Enhanced video display with multiple fallback methods
                            robust_video_display(video_url)
                            
                            # Add video URL to last assistant message
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": response.get("message", ""),
                                "video_url": video_response["video_url"]
                            })
                    else:
                        st.error("❌ Video generation failed")
                        # Add message without video URL
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response.get("message", "")
                        })
                else:
                    st.error("Failed to get response from backend")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Additional tabs for other features
    tab1, tab2 = st.tabs(["🎤 Voice Chat", "📊 System Info"])
    
    with tab1:
        voice_chat_interface(agent_type)
    
    with tab2:
        system_info_interface()

def generate_video_with_progress(text: str, agent_type: str) -> Optional[dict]:
    """Generate video with enhanced progress tracking for parallel processing"""
    import time
    
    try:
        start_time = time.time()
        
        # Create progress bar with multiple stages
        progress_bar = st.progress(0)
        status_text = st.empty()
        timing_text = st.empty()
        details_text = st.empty()
        
        # Step 1: Initial setup (10%)
        step_start = time.time()
        status_text.text("🚀 Initializing video generation...")
        progress_bar.progress(10)
        
        # Step 2: Audio generation (20%)
        status_text.text("🎵 Generating audio from text...")
        progress_bar.progress(20)
        
        # Step 3: Video processing with enhanced tracking (60%)
        status_text.text("🎬 Processing video with parallel optimization...")
        progress_bar.progress(40)
        
        # Call backend to generate video with enhanced processing
        # Debug: Log the exact text being sent
        st.info(f"🎬 Debug: Sending to backend (length: {len(text)} chars)")
        st.code(text[:200] + "..." if len(text) > 200 else text)
        
        response = requests.post(
            f"{API_BASE}/generate_video",
            json={
                "message": text,
                "agent_type": agent_type,
                "session_id": st.session_state.session_id,
                "enable_parallel": True,  # Enable parallel processing
                "chunk_duration": 15  # Optimal chunk duration
            },
            timeout=300  # 5 minutes timeout for enhanced processing
        )
        
        if response.status_code == 200:
            # Step 4: Video ready (100%)
            total_time = time.time() - start_time
            status_text.text("✅ Video ready with seamless processing!")
            progress_bar.progress(100)
            timing_text.text(f"⏱️ Total time: {total_time:.1f} seconds")
            
            result = response.json()
            
            # Add cache-busting to video URL to prevent frontend caching issues
            if "video_url" in result and result["video_url"]:
                # Add a fresh timestamp to prevent browser caching
                cache_buster = int(time.time())
                if "?" in result["video_url"]:
                    result["video_url"] = f"{result['video_url']}&cb={cache_buster}"
                else:
                    result["video_url"] = f"{result['video_url']}?cb={cache_buster}"
                st.info(f"🔄 Added cache-busting to video URL")
            
            # Display processing details if available
            if "processing_details" in result:
                details = result["processing_details"]
                details_text.text(
                    f"📊 Processing: {details.get('chunks', 0)} chunks, "
                    f"Parallel: {details.get('parallel_processing', False)}, "
                    f"Optimization: {details.get('optimization_level', 'standard')}"
                )
            
            return result
        else:
            total_time = time.time() - start_time
            status_text.text("❌ Video generation failed")
            progress_bar.empty()
            timing_text.text(f"⏱️ Failed after: {total_time:.1f} seconds")
            st.error(f"Backend error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        total_time = time.time() - start_time
        status_text.text("⏰ Video generation timed out")
        progress_bar.empty()
        timing_text.text(f"⏱️ Timed out after: {total_time:.1f} seconds")
        st.error("Video generation took too long. Please try again.")
        return None
    except Exception as e:
        total_time = time.time() - start_time
        status_text.text("❌ Error occurred")
        progress_bar.empty()
        timing_text.text(f"⏱️ Error after: {total_time:.1f} seconds")
        st.error(f"Error generating video: {str(e)}")
        return None

def voice_chat_interface(agent_type: str):
    """Voice-based chat interface"""
    st.header("🎤 Voice Chat")
    
    st.info("Voice chat feature requires audio file upload.")
    
    uploaded_file = st.file_uploader(
        "Upload Audio File", 
        type=['wav', 'mp3', 'm4a', 'ogg'],
        help="Upload an audio file to get a video response"
    )
    
    if uploaded_file is not None:
        st.audio(uploaded_file)
        with st.spinner("🎤 Processing voice input and generating video response..."):
            try:
                response = send_voice_message(uploaded_file, agent_type)
                
                if response:
                    # Display text response
                    st.write("**Response:**", response.get("message", "No response received"))
                    
                    # Automatically display video if available
                    if "video_url" in response and response["video_url"]:
                        st.success("✅ Video generated successfully!")
                        video_url = response["video_url"]
                        st.info(f"Video URL: {video_url}")
                        
                        # Enhanced video display with multiple fallback methods
                        robust_video_display(video_url)
                        
                        # Update session ID
                        if "session_id" in response:
                            st.session_state.session_id = response["session_id"]
                    else:
                        st.error("❌ Video generation failed")
                else:
                    st.error("Failed to get response from backend")
            except Exception as e:
                st.error(f"Error: {str(e)}")

def system_info_interface():
    """System information interface"""
    st.header("📊 System Information")
    
    # Backend health
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Backend Status")
        if check_backend_health():
            st.success("✅ Backend is running")
            
            # Get available agents
            try:
                agents_response = requests.get(f"{API_BASE}/agents")
                if agents_response.status_code == 200:
                    agents = agents_response.json()
                    st.write("**Available Agents:**")
                    for agent in agents.get("agents", []):
                        st.write(f"- {agent.title()}")
                else:
                    st.error("Failed to get agents list")
            except Exception as e:
                st.error(f"Error getting agents: {str(e)}")
        else:
            st.error("❌ Backend is not responding")
    
    with col2:
        st.subheader("📈 Usage Statistics")
        if "messages" in st.session_state:
            st.metric("Messages in Session", len(st.session_state.messages))
        else:
            st.metric("Messages in Session", 0)
        
        if st.session_state.session_id:
            st.metric("Session Active", "Yes")
        else:
            st.metric("Session Active", "No")
    
    # API Documentation
    st.subheader("📚 API Documentation")
    st.markdown(f"Visit [API Docs]({BACKEND_URL}/docs) for detailed endpoint information.")

def send_text_message(text: str, agent_type: str) -> Optional[dict]:
    """Send text message to backend"""
    try:
        response = requests.post(
            f"{API_BASE}/chat",
            json={
                "message": text,
                "agent_type": agent_type,
                "session_id": st.session_state.session_id
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Backend error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {str(e)}")
        return None

def send_voice_message(audio_file, agent_type: str) -> Optional[dict]:
    """Send voice message to backend"""
    try:
        files = {"audio_file": audio_file}
        data = {
            "agent_type": agent_type,
            "session_id": st.session_state.session_id
        }
        
        response = requests.post(
            f"{API_BASE}/voice",
            files=files,
            data=data,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Backend error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {str(e)}")
        return None

def check_backend_health() -> bool:
    """Check if backend is healthy"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def validate_video_url(video_url: str) -> bool:
    """Validate if a video URL is accessible and valid"""
    try:
        response = requests.head(video_url, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            content_length = response.headers.get('content-length', '0')
            
            # Check if it's a video file
            if 'video' in content_type or video_url.endswith('.mp4'):
                # Check if file has reasonable size (at least 1KB)
                if int(content_length) > 1024:
                    return True
                else:
                    print(f"⚠️ Video file too small: {content_length} bytes")
                    return False
            else:
                print(f"⚠️ Not a video file: {content_type}")
                return False
        else:
            print(f"⚠️ Video URL not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error validating video URL: {str(e)}")
        return False

def robust_video_display(video_url: str):
    """Display video robustly with multiple fallback methods and better error handling."""
    video_displayed = False
    errors = []
    
    # Pre-validate the video URL
    if not validate_video_url(video_url):
        st.error(f"❌ Invalid video URL: {video_url}")
        st.info("💡 This might be a cached URL from a previous request")
        st.info("🔄 Try refreshing the page or starting a new session")
        return
    
    # Method 1: Direct st.video() with error handling
    try:
        st.video(video_url)
        video_displayed = True
        # Don't show success message here to avoid clutter - video is already visible
    except Exception as e:
        errors.append(f"Direct video display: {str(e)}")
    
    # Method 2: Test URL accessibility and try again with different approach
    if not video_displayed:
        try:
            st.info("🔍 Testing video URL accessibility...")
            test_response = requests.get(video_url, timeout=10, stream=True)
            if test_response.status_code == 200:
                st.success(f"✅ Video URL accessible (Status: {test_response.status_code})")
                
                # Try HTML video player with better configuration
                try:
                    html_video = f"""
                    <video width='100%' height='400px' controls preload='metadata'>
                        <source src='{video_url}' type='video/mp4'>
                        Your browser does not support the video tag.
                    </video>
                    """
                    st.markdown(html_video, unsafe_allow_html=True)
                    video_displayed = True
                    st.success("✅ Video displayed with HTML player!")
                except Exception as e2:
                    errors.append(f"HTML video player: {str(e2)}")
            else:
                errors.append(f"Video URL not accessible: {test_response.status_code}")
        except Exception as e:
            errors.append(f"Error testing video URL: {str(e)}")
    
    # Method 3: Alternative HTML video player with different configuration
    if not video_displayed:
        st.info("🔄 Trying alternative HTML video player...")
        try:
            # Use a more compatible HTML video configuration
            html_video_alt = f"""
            <div style="text-align: center; margin: 20px 0;">
                <video 
                    controls 
                    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px;"
                    preload="none"
                    poster="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjRjVGNUY1Ii8+CjxwYXRoIGQ9Ik0yNCAxNkw0MCAzMkwyNCA0OFYxNloiIGZpbGw9IiM5Q0E2RjUiLz4KPC9zdmc+"
                >
                    <source src="{video_url}" type="video/mp4">
                    <p>Your browser does not support the video tag. <a href="{video_url}" target="_blank">Click here to download the video</a></p>
                </video>
            </div>
            """
            st.markdown(html_video_alt, unsafe_allow_html=True)
            video_displayed = True
            st.success("✅ Video displayed with alternative HTML player!")
        except Exception as e:
            errors.append(f"Alternative HTML video player: {str(e)}")
    
    # Method 4: Iframe embed as fallback
    if not video_displayed:
        st.info("🔄 Trying iframe embed...")
        try:
            # Create a simple iframe that might work better in some browsers
            iframe_html = f"""
            <div style="text-align: center; margin: 20px 0;">
                <iframe 
                    src="{video_url}" 
                    width="100%" 
                    height="400" 
                    frameborder="0" 
                    allowfullscreen
                    style="border: 1px solid #ddd; border-radius: 8px;"
                >
                    <p>Your browser does not support iframes. <a href="{video_url}" target="_blank">Click here to view the video</a></p>
                </iframe>
            </div>
            """
            st.markdown(iframe_html, unsafe_allow_html=True)
            video_displayed = True
            st.success("✅ Video displayed with iframe embed!")
        except Exception as e:
            errors.append(f"Iframe embed: {str(e)}")
    
    # Only show errors if ALL methods failed
    if not video_displayed:
        st.error("❌ All video display methods failed")
        st.info("📥 Alternative viewing options:")
        
        # Create a download button
        st.markdown(f"""
        <a href="{video_url}" target="_blank" style="
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px 0;
        ">
            📥 Download Video
        </a>
        """, unsafe_allow_html=True)
        
        # Provide manual instructions
        st.info("💡 Manual viewing instructions:")
        st.markdown("""
        1. **Right-click the download link above** and select "Open in new tab"
        2. **Or copy this URL** and paste it in a new browser tab:
        """)
        st.code(video_url)
        st.markdown("""
        3. **Or try refreshing the page** and generating the video again
        4. **Check your browser's video codec support** - try Chrome or Firefox
        """)
        
        # Show video info
        try:
            response = requests.head(video_url, timeout=5)
            if response.status_code == 200:
                st.info(f"📊 Video info: {response.headers.get('content-length', 'Unknown')} bytes, {response.headers.get('content-type', 'Unknown type')}")
        except:
            pass
        
        # Show detailed errors for debugging
        if errors:
            st.error("🔍 Detailed errors for debugging:")
            for error in errors:
                st.text(f"• {error}")
    else:
        # Video was displayed successfully - show a subtle success indicator
        st.success("✅ Video ready for playback")

def clear_cached_video_urls():
    """Clear all cached video URLs from session state to prevent caching issues"""
    if "messages" in st.session_state:
        for msg in st.session_state.messages:
            if "video_url" in msg:
                del msg["video_url"]
        st.success("🧹 Cleared cached video URLs")

if __name__ == "__main__":
    main() 