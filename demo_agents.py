#!/usr/bin/env python3
"""
Demonstration of the Multi-Agent System Configuration in Magentic-Groq-UI
"""
import sys
import os
import yaml

# Add the src directory to the path
sys.path.insert(0, 'src')

def show_agent_configuration():
    """Show how the multi-agent system is configured"""
    print("🎯 Magentic-Groq-UI Multi-Agent System Configuration")
    print("=" * 60)
    
    # Load and display the Groq configuration
    print("\n📋 Current Groq Configuration:")
    try:
        with open('groq_config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"   🤖 Primary Model: {config['groq_client']['config']['model']}")
        print(f"   ⚡ Action Guard: {config['groq_action_guard']['config']['model']}")
        print(f"   🌐 API Endpoint: {config['groq_client']['config']['base_url']}")
        
        print(f"\n🔧 Agent Assignments:")
        agent_assignments = [
            ("Orchestrator", config.get('orchestrator_client', 'Not configured')),
            ("Coder", config.get('coder_client', 'Not configured')),
            ("Web Surfer", config.get('web_surfer_client', 'Not configured')),
            ("File Surfer", config.get('file_surfer_client', 'Not configured')),
            ("Action Guard", config.get('action_guard_client', 'Not configured')),
            ("Plan Learning", config.get('plan_learning_client', 'Not configured')),
        ]
        
        for agent_name, agent_config in agent_assignments:
            if isinstance(agent_config, str):
                status = agent_config
            else:
                status = "✅ Configured with Groq"
            print(f"   {agent_name}: {status}")
            
    except Exception as e:
        print(f"   ❌ Could not load config: {e}")

def show_agent_capabilities():
    """Show what each agent can do"""
    print(f"\n🤖 Agent Capabilities & Responsibilities:")
    print("=" * 50)
    
    agents = [
        {
            "name": "🎯 Orchestrator Agent",
            "model": "llama-3.3-70b-versatile",
            "capabilities": [
                "Plans and coordinates multi-step tasks",
                "Decides which agents to use for each step",
                "Manages conversation flow and context",
                "Handles cooperative planning with users",
                "Learns from previous task executions"
            ]
        },
        {
            "name": "🌐 WebSurfer Agent", 
            "model": "llama-3.3-70b-versatile",
            "capabilities": [
                "Browses websites using Playwright browser",
                "Performs web searches and research",
                "Interacts with web forms and buttons",
                "Takes screenshots and analyzes web content",
                "Downloads files from websites"
            ]
        },
        {
            "name": "💻 Coder Agent",
            "model": "llama-3.3-70b-versatile", 
            "capabilities": [
                "Writes code in multiple programming languages",
                "Executes code in isolated Docker containers",
                "Debugs and fixes code errors",
                "Installs packages and dependencies",
                "Creates and manages project structures"
            ]
        },
        {
            "name": "📁 FileSurfer Agent",
            "model": "llama-3.3-70b-versatile",
            "capabilities": [
                "Reads and analyzes files of various formats",
                "Creates, modifies, and organizes files",
                "Searches through file contents",
                "Handles document processing and conversion",
                "Manages file system operations"
            ]
        },
        {
            "name": "🔒 Action Guard",
            "model": "llama-3.1-8b-instant (fast decisions)",
            "capabilities": [
                "Reviews potentially risky actions",
                "Provides safety checks for code execution",
                "Validates web interactions for security",
                "Implements approval workflows",
                "Prevents harmful operations"
            ]
        },
        {
            "name": "👤 User Proxy",
            "model": "Human-in-the-loop",
            "capabilities": [
                "Represents user input and preferences",
                "Handles interactive decision making",
                "Provides feedback and guidance",
                "Manages approval requests",
                "Maintains conversation context"
            ]
        }
    ]
    
    for agent in agents:
        print(f"\n{agent['name']}")
        print(f"   Model: {agent['model']}")
        print(f"   Capabilities:")
        for capability in agent['capabilities']:
            print(f"     • {capability}")

def show_multi_agent_workflow():
    """Show how agents work together"""
    print(f"\n🔄 Multi-Agent Workflow Example:")
    print("=" * 40)
    
    workflow_example = """
    User Request: "Research Python web frameworks and create a comparison chart"
    
    🎯 Orchestrator: 
       • Analyzes the request
       • Creates a plan with multiple steps
       • Decides which agents to involve
    
    🌐 WebSurfer:
       • Searches for "Python web frameworks comparison"
       • Visits framework documentation sites
       • Gathers information about Flask, Django, FastAPI, etc.
    
    💻 Coder:
       • Processes the research data
       • Creates a Python script to generate comparison chart
       • Uses libraries like matplotlib or pandas
    
    📁 FileSurfer:
       • Saves the research data to files
       • Creates the comparison chart image
       • Organizes output files
    
    🔒 Action Guard:
       • Reviews code execution for safety
       • Approves file operations
       • Validates web scraping activities
    
    🎯 Orchestrator:
       • Coordinates all agent activities
       • Ensures task completion
       • Provides final summary to user
    """
    
    print(workflow_example)

def show_groq_advantages():
    """Show why Groq is perfect for multi-agent systems"""
    print(f"\n⚡ Why Groq is Perfect for Multi-Agent Systems:")
    print("=" * 50)
    
    advantages = [
        "🚀 Ultra-fast inference (10x faster than traditional GPUs)",
        "🔄 Low latency enables real-time agent coordination", 
        "💰 Cost-effective for high-volume agent interactions",
        "🎯 Consistent performance across all agent types",
        "🔧 Easy integration with existing AutoGen framework",
        "📈 Scalable for complex multi-step workflows",
        "🌐 Reliable API with high availability"
    ]
    
    for advantage in advantages:
        print(f"   {advantage}")

def create_test_task_suggestions():
    """Suggest tasks that demonstrate multi-agent capabilities"""
    print(f"\n🧪 Test Tasks to Try in the Web UI:")
    print("=" * 40)
    
    tasks = [
        {
            "title": "Web Research + Code Generation",
            "task": "Research the latest Python testing frameworks and create a sample test suite using pytest",
            "agents": ["WebSurfer", "Coder", "FileSurfer"]
        },
        {
            "title": "Data Analysis Pipeline", 
            "task": "Find a public dataset online, download it, and create a data visualization dashboard",
            "agents": ["WebSurfer", "Coder", "FileSurfer"]
        },
        {
            "title": "Documentation Generator",
            "task": "Analyze my Python project files and generate comprehensive documentation with examples",
            "agents": ["FileSurfer", "Coder", "WebSurfer"]
        },
        {
            "title": "Competitive Analysis",
            "task": "Research competitor websites for a SaaS product and create a feature comparison matrix",
            "agents": ["WebSurfer", "FileSurfer", "Coder"]
        }
    ]
    
    for i, task in enumerate(tasks, 1):
        print(f"\n{i}. {task['title']}")
        print(f"   Task: {task['task']}")
        print(f"   Agents involved: {', '.join(task['agents'])}")

if __name__ == "__main__":
    show_agent_configuration()
    show_agent_capabilities() 
    show_multi_agent_workflow()
    show_groq_advantages()
    create_test_task_suggestions()
    
    print(f"\n🎉 Ready to Test!")
    print("=" * 20)
    print(f"1. Open http://localhost:8081 in your browser")
    print(f"2. Create a new session")
    print(f"3. Try one of the test tasks above")
    print(f"4. Watch as multiple agents work together powered by Groq!")
    print(f"\nThe system will automatically spawn and coordinate the appropriate")
    print(f"agents based on the complexity and requirements of your task.")
