#!/usr/bin/env python3
"""
VBVA Command Line Interface
CLI tool for interacting with the Video-Based Virtual Assistant
"""

import argparse
import asyncio
import json
import sys
from typing import Optional
import httpx
from pathlib import Path

# Backend configuration
BACKEND_URL = "http://localhost:8000"

class VBVACLI:
    """Command-line interface for VBVA"""
    
    def __init__(self):
        self.client = httpx.AsyncClient()
    
    async def health_check(self) -> bool:
        """Check if backend is running"""
        try:
            response = await self.client.get(f"{BACKEND_URL}/health")
            return response.status_code == 200
        except:
            return False
    
    async def list_agents(self):
        """List available agents"""
        try:
            response = await self.client.get(f"{BACKEND_URL}/api/v1/agents")
            if response.status_code == 200:
                agents = response.json()["agents"]
                print("Available agents:")
                for agent in agents:
                    print(f"  - {agent}")
            else:
                print("Error: Could not fetch agents")
        except Exception as e:
            print(f"Error: {e}")
    
    async def chat(self, message: str, agent_type: str = "general", session_id: Optional[str] = None):
        """Send chat message"""
        try:
            payload = {
                "message": message,
                "agent_type": agent_type
            }
            if session_id:
                payload["session_id"] = session_id
            
            response = await self.client.post(f"{BACKEND_URL}/api/v1/chat", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n🤖 {result['agent_type'].title()} Assistant:")
                print(f"   {result['message']}")
                print(f"\n⏱️  Processing time: {result['processing_time']:.2f}s")
                if result.get('session_id'):
                    print(f"🆔 Session ID: {result['session_id']}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    
    async def voice_chat(self, audio_file: str, agent_type: str = "general", session_id: Optional[str] = None):
        """Send voice message"""
        try:
            if not Path(audio_file).exists():
                print(f"Error: Audio file {audio_file} not found")
                return
            
            with open(audio_file, "rb") as f:
                files = {"audio_file": f}
                data = {
                    "agent_type": agent_type
                }
                if session_id:
                    data["session_id"] = session_id
                
                response = await self.client.post(f"{BACKEND_URL}/api/v1/voice", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n🎥 Video Response:")
                print(f"   Video URL: {result['video_url']}")
                if result.get('audio_url'):
                    print(f"   Audio URL: {result['audio_url']}")
                print(f"\n⏱️  Processing time: {result['processing_time']:.2f}s")
                if result.get('session_id'):
                    print(f"🆔 Session ID: {result['session_id']}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    
    async def stream_chat(self, session_id: str):
        """Stream chat response"""
        try:
            async with self.client.stream("GET", f"{BACKEND_URL}/api/v1/stream/{session_id}") as response:
                print("🔄 Streaming response:")
                async for chunk in response.aiter_text():
                    if chunk.startswith("data: "):
                        data = chunk[6:].strip()
                        if data and not data.startswith("error"):
                            print(data, end="", flush=True)
        except Exception as e:
            print(f"Error: {e}")
    
    async def reset_session(self, session_id: str):
        """Reset session"""
        try:
            response = await self.client.post(f"{BACKEND_URL}/api/v1/sessions/{session_id}/reset")
            if response.status_code == 200:
                print(f"✅ Session {session_id} reset successfully")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    
    async def interactive_mode(self, agent_type: str = "general"):
        """Interactive chat mode"""
        session_id = None
        print(f"\n🎥 VBVA Interactive Mode - {agent_type.title()} Agent")
        print("Type 'quit' to exit, 'reset' to reset session")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'reset':
                    if session_id:
                        await self.reset_session(session_id)
                        session_id = None
                    print("✅ Session reset")
                    continue
                elif not user_input:
                    continue
                
                # Send message
                payload = {
                    "message": user_input,
                    "agent_type": agent_type
                }
                if session_id:
                    payload["session_id"] = session_id
                
                response = await self.client.post(f"{BACKEND_URL}/api/v1/chat", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    session_id = result.get('session_id', session_id)
                    
                    print(f"\n🤖 {result['agent_type'].title()} Assistant:")
                    print(f"   {result['message']}")
                else:
                    print(f"❌ Error: {response.text}")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

async def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="VBVA Command Line Interface")
    parser.add_argument("--backend", default=BACKEND_URL, help="Backend URL")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Health check command
    subparsers.add_parser("health", help="Check backend health")
    
    # List agents command
    subparsers.add_parser("agents", help="List available agents")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Send chat message")
    chat_parser.add_argument("message", help="Message to send")
    chat_parser.add_argument("--agent", default="general", help="Agent type")
    chat_parser.add_argument("--session", help="Session ID")
    
    # Voice chat command
    voice_parser = subparsers.add_parser("voice", help="Send voice message")
    voice_parser.add_argument("audio_file", help="Audio file path")
    voice_parser.add_argument("--agent", default="general", help="Agent type")
    voice_parser.add_argument("--session", help="Session ID")
    
    # Stream command
    stream_parser = subparsers.add_parser("stream", help="Stream chat response")
    stream_parser.add_argument("session_id", help="Session ID")
    
    # Reset session command
    reset_parser = subparsers.add_parser("reset", help="Reset session")
    reset_parser.add_argument("session_id", help="Session ID")
    
    # Interactive mode command
    interactive_parser = subparsers.add_parser("interactive", help="Interactive chat mode")
    interactive_parser.add_argument("--agent", default="general", help="Agent type")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize CLI
    cli = VBVACLI()
    
    # Check backend health first
    if not await cli.health_check():
        print("❌ Backend is not running. Please start the backend first.")
        print("   Run: uvicorn backend.main:app --reload")
        sys.exit(1)
    
    # Execute command
    if args.command == "health":
        print("✅ Backend is running")
    
    elif args.command == "agents":
        await cli.list_agents()
    
    elif args.command == "chat":
        await cli.chat(args.message, args.agent, args.session)
    
    elif args.command == "voice":
        await cli.voice_chat(args.audio_file, args.agent, args.session)
    
    elif args.command == "stream":
        await cli.stream_chat(args.session_id)
    
    elif args.command == "reset":
        await cli.reset_session(args.session_id)
    
    elif args.command == "interactive":
        await cli.interactive_mode(args.agent)

if __name__ == "__main__":
    asyncio.run(main()) 