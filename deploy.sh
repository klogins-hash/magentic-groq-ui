#!/bin/bash

# Simple deployment script for Magentic-Groq-UI to Northflank
# This sets up direct GitHub integration with auto-deploy
set -e

echo "🚀 Setting up Magentic-Groq-UI on Northflank with GitHub Auto-Deploy"
echo "=================================================================="

# Check if Northflank CLI is installed
if ! command -v northflank &> /dev/null; then
    echo "❌ Northflank CLI not found. Installing..."
    npm install -g @northflank/cli
fi

# Check if user is logged in
echo "🔐 Checking Northflank authentication..."
if ! northflank auth:whoami &> /dev/null; then
    echo "❌ Not authenticated with Northflank. Please run:"
    echo "   northflank auth:login"
    echo "   Then run this script again."
    exit 1
fi

echo "✅ Authenticated with Northflank"

# Get or create project
echo "🔍 Setting up 'show-monies' project..."
PROJECT_ID=$(northflank list projects --output json 2>/dev/null | jq -r '.data[] | select(.name=="show-monies") | .id' || echo "")

if [ -z "$PROJECT_ID" ]; then
    echo "📁 Creating 'show-monies' project..."
    PROJECT_RESULT=$(northflank create project \
        --name "show-monies" \
        --description "AI-powered applications and demos" \
        --output json)
    PROJECT_ID=$(echo "$PROJECT_RESULT" | jq -r '.data.id')
    echo "✅ Created project with ID: $PROJECT_ID"
else
    echo "✅ Using existing project: $PROJECT_ID"
fi

# Create or check secret
echo "🔑 Setting up GROQ_API_KEY secret..."
SECRET_EXISTS=$(northflank list secrets --project "$PROJECT_ID" --output json 2>/dev/null | jq -r '.data[] | select(.name=="groq-api-key") | .id' || echo "")

if [ -z "$SECRET_EXISTS" ]; then
    echo "🔐 Creating GROQ_API_KEY secret..."
    echo "Please enter your Groq API key:"
    read -s GROQ_API_KEY
    
    northflank create secret \
        --project "$PROJECT_ID" \
        --name "groq-api-key" \
        --value "$GROQ_API_KEY" \
        --description "Groq API key for Magentic-Groq-UI" \
        --output json > /dev/null
    
    echo "✅ Secret created successfully"
else
    echo "✅ GROQ_API_KEY secret already exists"
fi

# Create service with GitHub auto-deploy
echo "🚀 Creating service with GitHub integration..."
SERVICE_EXISTS=$(northflank list services --project "$PROJECT_ID" --output json 2>/dev/null | jq -r '.data[] | select(.name=="magentic-groq-ui") | .id' || echo "")

if [ -z "$SERVICE_EXISTS" ]; then
    echo "📦 Creating new service with auto-deploy..."
    
    # Create the service
    northflank create service \
        --project "$PROJECT_ID" \
        --name "magentic-groq-ui" \
        --description "Multi-agent AI system powered by Groq's lightning-fast inference" \
        --source-type git \
        --source-url "https://github.com/klogins-hash/magentic-groq-ui" \
        --source-branch main \
        --dockerfile-path "/Dockerfile" \
        --port 8081 \
        --env PORT=8081 \
        --env HOST=0.0.0.0 \
        --secret GROQ_API_KEY=groq-api-key \
        --cpu 1000m \
        --memory 2Gi \
        --replicas 1 \
        --health-check-path "/api/health" \
        --auto-deploy true \
        --output json > /dev/null
    
    echo "✅ Service created with auto-deploy enabled"
else
    echo "🔄 Service already exists, updating configuration..."
    northflank update service \
        --project "$PROJECT_ID" \
        --service magentic-groq-ui \
        --auto-deploy true \
        --auto-deploy-branch main \
        --output json > /dev/null
    echo "✅ Auto-deploy configuration updated"
fi

# Get service URL
echo "🌐 Getting service URL..."
SERVICE_INFO=$(northflank get service --project "$PROJECT_ID" --service magentic-groq-ui --output json 2>/dev/null || echo "{}")
SERVICE_URL=$(echo "$SERVICE_INFO" | jq -r '.data.ports[0].domains[0] // "magentic-groq-ui--show-monies.code.run"')

echo ""
echo "🎉 Setup completed successfully!"
echo "==============================="
echo ""
echo "📋 Configuration:"
echo "   • Project: show-monies ($PROJECT_ID)"
echo "   • Service: magentic-groq-ui"
echo "   • Repository: https://github.com/klogins-hash/magentic-groq-ui"
echo "   • Branch: main"
echo "   • Auto-deploy: ✅ ENABLED"
echo ""
echo "🌐 Your application will be available at:"
echo "   https://$SERVICE_URL"
echo ""
echo "🔄 How it works:"
echo "   1. Push changes to GitHub main branch"
echo "   2. Northflank automatically detects changes"
echo "   3. Builds new Docker image from your Dockerfile"
echo "   4. Deploys updated application"
echo ""
echo "📊 Monitor deployment:"
echo "   northflank get service --project show-monies --service magentic-groq-ui"
echo ""
echo "🔧 Manage via Northflank dashboard:"
echo "   https://app.northflank.com/projects/$PROJECT_ID/services/magentic-groq-ui"
