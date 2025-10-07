#!/usr/bin/env python3
"""
WebSocket test to monitor real-time agent communication
"""
import asyncio
import websockets
import json

async def monitor_agents():
    """Monitor agent communication via WebSocket"""
    uri = "ws://localhost:8081/api/ws"
    
    try:
        print("🔌 Connecting to WebSocket...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected! Monitoring agent communications...")
            print("   (Start a task in the web UI to see agents in action)")
            print("   Press Ctrl+C to stop monitoring")
            print("-" * 60)
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    
                    # Look for agent-related messages
                    if isinstance(data, dict):
                        msg_type = data.get('type', 'unknown')
                        sender = data.get('sender', 'unknown')
                        content = data.get('content', '')
                        
                        print(f"📨 {msg_type.upper()}")
                        print(f"   From: {sender}")
                        if content:
                            preview = str(content)[:100] + "..." if len(str(content)) > 100 else str(content)
                            print(f"   Content: {preview}")
                        print("-" * 40)
                        
                except json.JSONDecodeError:
                    print(f"📝 Raw message: {message[:100]}...")
                    
    except websockets.exceptions.ConnectionRefused:
        print("❌ Could not connect to WebSocket")
        print("   Make sure the application is running on http://localhost:8081")
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped by user")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")

if __name__ == "__main__":
    print("🎯 Magentic-Groq-UI Agent Communication Monitor")
    print("=" * 50)
    print("This tool monitors real-time communication between agents")
    print("via WebSocket connection.")
    print()
    
    asyncio.run(monitor_agents())
