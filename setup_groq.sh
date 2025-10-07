#!/bin/bash

# Magentic-Groq-UI Setup Script
# This script helps you set up Magentic-Groq-UI with Groq API

echo "🚀 Setting up Magentic-Groq-UI..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.10+ first."
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install the package
echo "⬇️  Installing Magentic-Groq-UI..."
pip install -e .

# Check for Groq API key
if [ -z "$GROQ_API_KEY" ]; then
    echo "🔑 GROQ_API_KEY environment variable not found."
    echo "Please set your Groq API key:"
    echo "export GROQ_API_KEY='your-groq-api-key-here'"
    echo ""
    echo "You can get a free API key from: https://console.groq.com/keys"
    echo ""
    read -p "Enter your Groq API key now (or press Enter to skip): " api_key
    if [ ! -z "$api_key" ]; then
        export GROQ_API_KEY="$api_key"
        echo "export GROQ_API_KEY='$api_key'" >> ~/.bashrc
        echo "✅ API key set and saved to ~/.bashrc"
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start Magentic-Groq-UI:"
echo "1. Make sure your virtual environment is activated: source .venv/bin/activate"
echo "2. Set your Groq API key: export GROQ_API_KEY='your-key-here'"
echo "3. Run: magentic-groq-ui --port 8081"
echo "4. Open http://localhost:8081 in your browser"
echo ""
echo "For custom configuration, use: magentic-groq-ui --port 8081 --config config_groq_example.yaml"
echo ""
echo "Available Groq models:"
echo "- llama-3.3-70b-versatile (recommended for most tasks)"
echo "- llama-3.1-70b-versatile (good balance of speed and capability)"
echo "- llama-3.1-8b-instant (fastest for simple tasks)"
echo "- llama-3.2-11b-vision-preview (for vision tasks)"
echo "- mixtral-8x7b-32768 (for text generation)"
