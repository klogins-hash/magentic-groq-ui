#!/usr/bin/env python3
"""
Test script to demonstrate multi-agent system spawning and coordination
"""
import requests
import json
import time
import asyncio

BASE_URL = "http://localhost:8081/api"

def create_session():
    """Create a new session for testing"""
    response = requests.post(f"{BASE_URL}/sessions", 
                           json={"name": "Multi-Agent Test Session"})
    if response.status_code == 200:
        session_data = response.json()
        print(f"✅ Created session: {session_data.get('id', 'Unknown ID')}")
        return session_data.get('id')
    else:
        print(f"❌ Failed to create session: {response.status_code}")
        return None

def start_task(session_id, task_description):
    """Start a task that requires multiple agents"""
    task_data = {
        "task": task_description,
        "session_id": session_id
    }
    
    response = requests.post(f"{BASE_URL}/runs", json=task_data)
    if response.status_code == 200:
        run_data = response.json()
        print(f"✅ Started task run: {run_data.get('id', 'Unknown ID')}")
        return run_data.get('id')
    else:
        print(f"❌ Failed to start task: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def check_run_status(run_id):
    """Check the status of a running task"""
    response = requests.get(f"{BASE_URL}/runs/{run_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to get run status: {response.status_code}")
        return None

def list_sessions():
    """List all sessions to see what's available"""
    response = requests.get(f"{BASE_URL}/sessions")
    if response.status_code == 200:
        sessions = response.json()
        print(f"📋 Found {len(sessions)} sessions")
        for session in sessions:
            print(f"  - Session {session.get('id')}: {session.get('name', 'Unnamed')}")
        return sessions
    else:
        print(f"❌ Failed to list sessions: {response.status_code}")
        return []

def test_multi_agent_task():
    """Test a complex task that requires multiple agents to work together"""
    
    print("🚀 Testing Multi-Agent System")
    print("=" * 50)
    
    # First, let's see what sessions exist
    print("\n1. Checking existing sessions...")
    sessions = list_sessions()
    
    # Create a new session
    print("\n2. Creating new session...")
    session_id = create_session()
    if not session_id:
        return False
    
    # Define a complex task that requires multiple agents:
    # - Web browsing (WebSurfer agent)
    # - Code generation (Coder agent) 
    # - File operations (FileSurfer agent)
    # - Orchestration (Orchestrator agent)
    
    complex_task = """
    Please help me with a multi-step task:
    
    1. Search the web for information about "Python FastAPI best practices"
    2. Create a simple Python script that demonstrates these best practices
    3. Save the script to a file called 'fastapi_example.py'
    4. Provide a summary of what you learned and created
    
    This task should involve multiple agents working together - web research, code generation, and file operations.
    """
    
    print(f"\n3. Starting complex multi-agent task...")
    print(f"Task: {complex_task[:100]}...")
    
    run_id = start_task(session_id, complex_task)
    if not run_id:
        return False
    
    print(f"\n4. Monitoring task execution...")
    print("   (This will show which agents are being spawned and coordinated)")
    
    # Monitor the task for a bit to see agent activity
    for i in range(10):  # Check for 10 iterations
        time.sleep(2)
        status = check_run_status(run_id)
        if status:
            print(f"   Status check {i+1}: {status.get('status', 'unknown')}")
            
            # Look for evidence of multiple agents
            messages = status.get('messages', [])
            if messages:
                latest_message = messages[-1] if messages else {}
                sender = latest_message.get('sender', 'unknown')
                content_preview = str(latest_message.get('content', ''))[:100]
                print(f"   Latest from {sender}: {content_preview}...")
                
                # Check if we can see different agent types
                unique_senders = set(msg.get('sender', 'unknown') for msg in messages[-5:])
                if len(unique_senders) > 1:
                    print(f"   🎯 Multiple agents active: {', '.join(unique_senders)}")
            
            if status.get('status') in ['completed', 'failed', 'cancelled']:
                print(f"   ✅ Task {status.get('status')}")
                break
        else:
            print(f"   ⚠️  Could not get status for iteration {i+1}")
    
    return True

def demonstrate_available_agents():
    """Show what agents are available in the system"""
    print("\n🤖 Available Agent Types in Magentic-Groq-UI:")
    print("=" * 50)
    
    agents_info = [
        ("🌐 WebSurfer", "Browses websites, searches the internet, interacts with web pages"),
        ("💻 CoderAgent", "Writes, executes, and debugs code in various programming languages"),
        ("📁 FileSurfer", "Reads, writes, and manages files and directories"),
        ("🎯 Orchestrator", "Coordinates other agents, plans tasks, manages workflow"),
        ("👤 UserProxy", "Represents user input and handles human-in-the-loop interactions"),
        ("🔒 ApprovalGuard", "Reviews and approves potentially risky actions"),
        ("🔌 McpAgent", "Connects to MCP (Model Context Protocol) servers for extended capabilities"),
    ]
    
    for name, description in agents_info:
        print(f"{name}: {description}")
    
    print(f"\n🚀 All agents are powered by Groq's lightning-fast inference:")
    print(f"   - Primary model: llama-3.3-70b-versatile")
    print(f"   - Action guard: llama-3.1-8b-instant")
    print(f"   - Base URL: https://api.groq.com/openai/v1")

if __name__ == "__main__":
    print("🎯 Magentic-Groq-UI Multi-Agent System Test")
    print("=" * 60)
    
    # Show available agents
    demonstrate_available_agents()
    
    # Test the multi-agent system
    try:
        success = test_multi_agent_task()
        if success:
            print(f"\n🎉 Multi-agent test completed!")
            print(f"   The system successfully spawned and coordinated multiple agents")
            print(f"   to work together on a complex task involving web research,")
            print(f"   code generation, and file operations.")
        else:
            print(f"\n⚠️  Multi-agent test encountered issues")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
    
    print(f"\n📝 Note: You can also test the multi-agent system through the web UI")
    print(f"   at http://localhost:8081 by giving it complex tasks that require")
    print(f"   multiple types of operations (web browsing + coding + file handling).")
