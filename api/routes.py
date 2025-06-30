"""
VBVA API Routes
Main API endpoints for the virtual assistant system
"""

import time
import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from models.requests import ChatRequest, VoiceRequest, VideoGenerationRequest
from models.responses import ChatResponse, VideoResponse
from services.monitoring import record_request, record_agent_execution
from services.logging import log_user_question, log_video_generation_request, log_agent_response, log_error
from agents.orchestrator import AgentOrchestrator
from config.validation_settings import get_validation_settings, ValidationMode

import traceback

router = APIRouter()

# Initialize agent orchestrator
orchestrator = AgentOrchestrator()

# Global variable to track recent requests
recent_requests = []

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Process text input and return text response with validation"""
    start_time = time.time()
    
    try:
        # Set lenient mode for general/creative agent types
        if request.agent_type in ["general", "poetry", "creative"]:
            get_validation_settings().set_validation_mode(ValidationMode.LENIENT)
        else:
            get_validation_settings().set_validation_mode(ValidationMode.STRICT)
        
        # Clear logging of user question
        log_user_question(
            question=request.message,
            session_id=request.session_id,
            agent_type=request.agent_type,
            request_type="chat"
        )
        
        # Track this request
        recent_requests.append({
            "timestamp": time.time(),
            "endpoint": "/chat",
            "message": request.message,
            "session_id": request.session_id,
            "agent_type": request.agent_type
        })
        
        # Keep only last 50 requests
        if len(recent_requests) > 50:
            recent_requests.pop(0)
        
        # Process through agent orchestrator
        result = await orchestrator.process_text_request(
            text=request.message,
            session_id=request.session_id,
            agent_type=request.agent_type
        )
        
        print("Orchestrator result:", result)
        
        duration = time.time() - start_time
        record_request("/chat", "POST", duration)
        record_agent_execution("text_processing", duration)
        
        # Extract the response text and validation result
        response_text = result.get("response", "No response generated")
        validation_result = result.get("validation_result", {})
        
        # Check if answer is complete enough for video generation
        is_complete = validation_result.get("is_complete", True)
        completeness_level = validation_result.get("completeness_level", "complete")
        confidence_score = validation_result.get("confidence_score", 1.0)
        issues = validation_result.get("issues", [])
        
        # If answer is incomplete, add a note to the response
        if not is_complete:
            warning_note = f"\n\n⚠️ **Note**: This answer may be incomplete for video generation. Issues detected: {', '.join(issues[:2])} (confidence: {confidence_score:.2f})"
            response_text += warning_note
        
        return ChatResponse(
            message=response_text,
            session_id=request.session_id,
            agent_type=request.agent_type,
            processing_time=duration,
            validation_info={
                "is_complete": is_complete,
                "completeness_level": completeness_level,
                "confidence_score": confidence_score,
                "issues": issues,
                "can_generate_video": is_complete
            }
        )
        
    except Exception as e:
        print("Error in chat endpoint:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice", response_model=VideoResponse)
async def voice_endpoint(
    audio_file: UploadFile = File(...),
    session_id: Optional[str] = None,
    agent_type: Optional[str] = "general"
):
    """Process voice input and return video response"""
    start_time = time.time()
    
    try:
        # Process voice through orchestrator
        result = await orchestrator.process_voice_request(
            audio_file=audio_file,
            session_id=session_id,
            agent_type=agent_type or "general"
        )
        
        duration = time.time() - start_time
        record_request("/voice", "POST", duration)
        record_agent_execution("voice_processing", duration)
        
        return VideoResponse(
            video_url=result.get("video_url", ""),
            audio_url=result.get("audio_url", ""),
            session_id=session_id,
            agent_type=agent_type or "general",
            processing_time=duration
        )
        
    except Exception as e:
        print("Error in voice endpoint:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream/{session_id}")
async def stream_response(session_id: str):
    """Stream real-time response for a session"""
    async def generate():
        try:
            async for chunk in orchestrator.stream_response(session_id):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: error: {str(e)}\n\n"
    
    return StreamingResponse(generate(), media_type="text/plain")

@router.get("/agents")
async def list_agents():
    """List available agent types"""
    return {
        "agents": orchestrator.get_available_agents(),
        "default": "general"
    }

@router.post("/sessions/{session_id}/reset")
async def reset_session(session_id: str):
    """Reset session context"""
    try:
        orchestrator.reset_session(session_id)
        return {"message": "Session reset successfully", "session_id": session_id}
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
async def test():
    return {"message": "Backend is working"}

@router.post("/generate_video", response_model=VideoResponse)
async def generate_video_endpoint(request: ChatRequest):
    """Generate video from text input with ultra-fast processing"""
    start_time = time.time()
    
    try:
        from services.answer_validator import AnswerValidator
        validator = AnswerValidator()
        message_text = request.message
        if len(message_text) > 2000:
            message_text = message_text[:2000] + "..."
            print(f"Truncated message from {len(request.message)} to {len(message_text)} characters")
        # Set lenient mode for general/creative agent types
        if request.agent_type in ["general", "poetry", "creative"]:
            get_validation_settings().set_validation_mode(ValidationMode.LENIENT)
            strict_mode = False
        else:
            get_validation_settings().set_validation_mode(ValidationMode.STRICT)
            strict_mode = True
        print("🔍 Validating answer completeness...")
        validation_result = await validator.validate_answer_completeness(
            text=message_text,
            context={"original_question": request.message},
            strict_mode=strict_mode
        )
        
        # Log validation results
        print(f"🔍 Validation result: {validation_result.completeness_level.value}")
        print(f"🔍 Confidence score: {validation_result.confidence_score:.2f}")
        print(f"🔍 Issues found: {len(validation_result.issues)}")
        
        # Check if answer is complete enough for video generation
        if not validation_result.is_complete:
            print(f"❌ Answer validation failed: {validation_result.completeness_level.value}")
            print(f"❌ Issues: {validation_result.issues}")
            print(f"❌ Suggestions: {validation_result.suggestions}")
            
            # Create detailed error response with guidance
            error_detail = {
                "error": "Incomplete answer detected - video generation blocked",
                "message": "The provided answer is not complete enough for video generation. Please use the /regenerate_complete endpoint to get a more comprehensive answer.",
                "completeness_level": validation_result.completeness_level.value,
                "confidence_score": validation_result.confidence_score,
                "issues": validation_result.issues,
                "suggestions": validation_result.suggestions,
                "text_length": validation_result.text_length,
                "word_count": validation_result.word_count,
                "remediation": {
                    "endpoint": "/regenerate_complete",
                    "method": "POST",
                    "description": "Use this endpoint to regenerate a complete answer",
                    "example_request": {
                        "message": request.message,
                        "session_id": request.session_id,
                        "agent_type": request.agent_type
                    }
                }
            }
            
            # Return error response with validation details
            raise HTTPException(status_code=400, detail=error_detail)
        
        print(f"✅ Answer validation passed: {validation_result.completeness_level.value}")
        
        # Clear logging of user question for video generation
        log_video_generation_request(
            text=message_text,
            session_id=request.session_id,
            agent_type=request.agent_type
        )
        
        # Track this request
        recent_requests.append({
            "timestamp": time.time(),
            "endpoint": "/generate_video",
            "message": message_text,
            "session_id": request.session_id,
            "agent_type": request.agent_type,
            "validation_result": {
                "completeness_level": validation_result.completeness_level.value,
                "confidence_score": validation_result.confidence_score,
                "issue_count": len(validation_result.issues)
            }
        })
        
        # Keep only last 50 requests
        if len(recent_requests) > 50:
            recent_requests.pop(0)
        
        # Check for enhanced processing parameters
        enable_parallel = getattr(request, 'enable_parallel', True)  # Default to True
        chunk_duration = getattr(request, 'chunk_duration', 8)  # Default to 8 seconds for ultra-fast
        use_ultra_fast = getattr(request, 'use_ultra_fast', True)  # Default to ultra-fast mode
        
        if use_ultra_fast:
            # Use ultra-fast processor for maximum speed
            from services.ultra_fast_processor import UltraFastProcessor
            ultra_processor = UltraFastProcessor()
            
            # Step 1: Ultra-fast processing
            video_url, stats = await ultra_processor.process_video_ultra_fast(
                text=message_text,
                agent_type=request.agent_type,
                target_time=8.0  # Target 8 seconds or less
            )
            
            total_time = time.time() - start_time
            
            # Prepare response with ultra-fast processing details
            response_data = {
                "video_url": video_url,
                "audio_url": None,  # Not returned in ultra-fast mode
                "session_id": request.session_id,
                "agent_type": request.agent_type,
                "processing_time": total_time,
                "processing_details": {
                    "parallel_processing": enable_parallel,
                    "chunk_duration": chunk_duration,
                    "audio_generation_time": stats.audio_generation_time,
                    "video_generation_time": stats.video_generation_time,
                    "optimization_level": "ultra_fast",
                    "speed_multiplier": stats.speed_multiplier,
                    "target_achieved": total_time <= 8.0,
                    "validation": {
                        "completeness_level": validation_result.completeness_level.value,
                        "confidence_score": validation_result.confidence_score,
                        "validation_time": validation_result.validation_time
                    }
                }
            }
            
            print(f"🚀 Ultra-fast generation completed in {total_time:.2f}s (target: 8.0s)")
            print(f"🚀 Speed multiplier: {stats.speed_multiplier:.1f}x faster than baseline")
            
        else:
            # Fallback to enhanced processing
            # Step 1: Generate audio from text
            audio_start = time.time()
            audio_url = await orchestrator.tts_service.generate_speech(message_text)
            audio_time = time.time() - audio_start
            print(f"Audio generated: {audio_url} (took {audio_time:.2f}s)")
            
            # Step 2: Generate video with lip sync (enhanced with parallel processing)
            video_start = time.time()
            video_url = await orchestrator.lip_sync_service.generate_video(
                audio_url=audio_url,
                avatar_type=request.agent_type
            )
            video_time = time.time() - video_start
            print(f"Video generated: {video_url} (took {video_time:.2f}s)")
            
            total_time = time.time() - start_time
            
            # Prepare response with processing details
            response_data = {
                "video_url": video_url,
                "audio_url": audio_url,
                "session_id": request.session_id,
                "agent_type": request.agent_type,
                "processing_time": total_time,
                "processing_details": {
                    "parallel_processing": enable_parallel,
                    "chunk_duration": chunk_duration,
                    "audio_generation_time": audio_time,
                    "video_generation_time": video_time,
                    "optimization_level": "enhanced" if enable_parallel else "standard",
                    "validation": {
                        "completeness_level": validation_result.completeness_level.value,
                        "confidence_score": validation_result.confidence_score,
                        "validation_time": validation_result.validation_time
                    }
                }
            }
        
        record_request("/generate_video", "POST", total_time)
        record_agent_execution("video_generation", total_time)
        
        return VideoResponse(**response_data)
        
    except HTTPException as http_exc:
        # Re-raise HTTP exceptions (like validation errors)
        raise http_exc
    except Exception as e:
        total_time = time.time() - start_time
        print(f"🚀 Video generation failed after {total_time:.2f}s: {str(e)}")
        record_request("/generate_video", "POST", total_time)
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

@router.get("/videos/{filename}")
@router.head("/videos/{filename}")
async def serve_video(filename: str):
    """Serve video files with comprehensive headers to prevent playback issues"""
    try:
        # Check multiple possible video directories
        video_paths = [
            f"/tmp/wav2lip_outputs/{filename}",
            f"/tmp/wav2lip_ultra_outputs/{filename}"
        ]
        
        video_path = None
        for path in video_paths:
            if os.path.exists(path):
                video_path = path
                break
        
        # Check if file exists
        if not video_path:
            print(f"Video file not found in any directory: {filename}")
            print(f"Checked paths: {video_paths}")
            raise HTTPException(status_code=404, detail="Video file not found")
        
        print(f"Serving video: {video_path}")
        
        # Get file size for Content-Length header
        file_size = os.path.getsize(video_path)
        
        # Comprehensive headers to prevent playback issues
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "Content-Type": "video/mp4",
            "Content-Length": str(file_size),
            "Accept-Ranges": "bytes",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "SAMEORIGIN"
        }
        
        # Return the video file with comprehensive headers
        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename=filename,
            headers=headers
        )
        
    except Exception as e:
        print(f"Error serving video {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.options("/videos/{filename}")
async def video_options(filename: str):
    """Handle CORS preflight requests for video serving"""
    return {
        "message": "OK",
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    }

@router.get("/debug/videos")
async def debug_videos():
    """Debug endpoint to list all available videos"""
    try:
        video_dirs = [
            "/tmp/wav2lip_outputs",
            "/tmp/wav2lip_ultra_outputs"
        ]
        
        all_videos = []
        
        for video_dir in video_dirs:
            if not os.path.exists(video_dir):
                print(f"Video directory not found: {video_dir}")
                continue
            
            videos = []
            for filename in os.listdir(video_dir):
                if filename.endswith('.mp4'):
                    file_path = os.path.join(video_dir, filename)
                    stat = os.stat(file_path)
                    videos.append({
                        "filename": filename,
                        "directory": video_dir,
                        "size_bytes": stat.st_size,
                        "size_mb": round(stat.st_size / (1024 * 1024), 2),
                        "created": stat.st_ctime,
                        "modified": stat.st_mtime,
                        "url": f"http://localhost:8000/api/v1/videos/{filename}"
                    })
            
            all_videos.extend(videos)
        
        return {
            "video_count": len(all_videos),
            "directories_checked": video_dirs,
            "videos": all_videos
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/debug/recent-requests")
async def debug_recent_requests():
    """Debug endpoint to show recent user requests"""
    try:
        # Get recent sessions and their messages
        recent_data = []
        for session_id, session_data in list(orchestrator.sessions.items())[-5:]:  # Last 5 sessions
            messages = session_data.get("messages", [])
            if messages:
                recent_data.append({
                    "session_id": session_id,
                    "agent_type": session_data.get("agent_type", "unknown"),
                    "message_count": len(messages),
                    "last_message": str(messages[-1].content) if messages else "No messages",
                    "all_messages": [str(msg.content) for msg in messages]
                })
        
        return {
            "recent_sessions": recent_data,
            "total_sessions": len(orchestrator.sessions),
            "recent_api_calls": recent_requests[-10:],  # Last 10 API calls
            "note": "This shows the last 5 sessions and last 10 API calls"
        }
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/regenerate_complete", response_model=ChatResponse)
async def regenerate_complete_answer(request: ChatRequest):
    """Regenerate a complete answer when the original was incomplete"""
    start_time = time.time()
    
    try:
        # Clear logging of regeneration request
        log_user_question(
            question=f"REGENERATE COMPLETE: {request.message}",
            session_id=request.session_id,
            agent_type=request.agent_type,
            request_type="regenerate"
        )
        
        # Track this request
        recent_requests.append({
            "timestamp": time.time(),
            "endpoint": "/regenerate_complete",
            "message": request.message,
            "session_id": request.session_id,
            "agent_type": request.agent_type
        })
        
        # Keep only last 50 requests
        if len(recent_requests) > 50:
            recent_requests.pop(0)
        
        # Process through agent orchestrator with enhanced prompt for completeness
        enhanced_message = f"Please provide a complete, detailed answer to: {request.message}. Ensure the response is comprehensive, well-structured, and addresses all aspects of the question."
        
        result = await orchestrator.process_text_request(
            text=enhanced_message,
            session_id=request.session_id,
            agent_type=request.agent_type
        )
        
        print("Regeneration result:", result)
        
        duration = time.time() - start_time
        record_request("/regenerate_complete", "POST", duration)
        record_agent_execution("text_processing", duration)
        
        # Extract the response text and validation result
        response_text = result.get("response", "No response generated")
        validation_result = result.get("validation_result", {})
        
        # Check if answer is complete enough for video generation
        is_complete = validation_result.get("is_complete", True)
        completeness_level = validation_result.get("completeness_level", "complete")
        confidence_score = validation_result.get("confidence_score", 1.0)
        issues = validation_result.get("issues", [])
        
        # If still incomplete, add a stronger warning
        if not is_complete:
            warning_note = f"\n\n⚠️ **Warning**: Regeneration still produced an incomplete answer. Issues: {', '.join(issues[:2])} (confidence: {confidence_score:.2f})"
            response_text += warning_note
        
        return ChatResponse(
            message=response_text,
            session_id=request.session_id,
            agent_type=request.agent_type,
            processing_time=duration,
            validation_info={
                "is_complete": is_complete,
                "completeness_level": completeness_level,
                "confidence_score": confidence_score,
                "issues": issues,
                "can_generate_video": is_complete,
                "is_regenerated": True
            }
        )
        
    except Exception as e:
        print("Error in regenerate_complete endpoint:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))