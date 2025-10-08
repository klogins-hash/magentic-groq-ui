# 🚀 Deployment Guide

## Quick Deploy to Northflank

This project is set up for **automatic deployment** from GitHub to Northflank. Here's how to get it running:

### Prerequisites

1. **GitHub Repository**: ✅ Already set up at `https://github.com/klogins-hash/magentic-groq-ui`
2. **Northflank Account**: Sign up at [northflank.com](https://northflank.com)
3. **Groq API Key**: Get one from [console.groq.com](https://console.groq.com)

### One-Command Deployment

```bash
./deploy.sh
```

This script will:
- Install Northflank CLI (if needed)
- Authenticate with Northflank
- Create the "show-monies" project
- Set up your Groq API key as a secret
- Deploy the service with GitHub auto-deploy enabled

### What Happens Next

1. **Automatic Builds**: Every push to `main` branch triggers a new deployment
2. **Docker Build**: Northflank builds your app using the included `Dockerfile`
3. **Live URL**: Your app will be available at `https://magentic-groq-ui--show-monies.code.run`

### Manual Setup (Alternative)

If you prefer to set up manually via Northflank dashboard:

1. **Create Project**: 
   - Go to [app.northflank.com](https://app.northflank.com)
   - Create project named "show-monies"

2. **Add Secret**:
   - Go to Project Settings → Secrets
   - Create secret named `groq-api-key`
   - Set value to your Groq API key

3. **Create Service**:
   - Click "Create Service"
   - Choose "Git Repository"
   - Repository: `https://github.com/klogins-hash/magentic-groq-ui`
   - Branch: `main`
   - Build Type: `Dockerfile`
   - Dockerfile Path: `/Dockerfile`

4. **Configure Service**:
   - Port: `8081`
   - Environment Variables:
     - `PORT=8081`
     - `HOST=0.0.0.0`
   - Secrets:
     - `GROQ_API_KEY` → `groq-api-key`
   - Resources:
     - CPU: `1000m`
     - Memory: `2Gi`
   - Health Check: `/api/health`

5. **Enable Auto-Deploy**:
   - Go to Service Settings → Git
   - Enable "Auto Deploy"
   - Branch: `main`

### Environment Variables

The application uses these environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes |
| `PORT` | Application port | No (defaults to 8081) |
| `HOST` | Bind address | No (defaults to 127.0.0.1) |

### Monitoring

- **Service Status**: `northflank get service --project show-monies --service magentic-groq-ui`
- **Logs**: View in Northflank dashboard
- **Metrics**: Built-in monitoring available

### Updating the Application

Simply push changes to the `main` branch:

```bash
git add .
git commit -m "Update application"
git push origin main
```

Northflank will automatically:
1. Detect the changes
2. Build a new Docker image
3. Deploy the updated application
4. Health check the new deployment
5. Switch traffic to the new version

### Troubleshooting

**Build Failures**:
- Check Dockerfile syntax
- Ensure all dependencies are in requirements
- View build logs in Northflank dashboard

**Runtime Errors**:
- Verify GROQ_API_KEY is set correctly
- Check application logs
- Ensure health check endpoint `/api/health` is responding

**Auto-Deploy Not Working**:
- Verify GitHub integration is connected
- Check that auto-deploy is enabled for `main` branch
- Ensure commits are pushed to the correct repository

### Architecture

```
GitHub (main branch)
    ↓ (webhook)
Northflank Build System
    ↓ (Docker build)
Container Registry
    ↓ (deploy)
Running Service
    ↓ (expose)
Public URL: https://magentic-groq-ui--show-monies.code.run
```

### Resources

- **Northflank Docs**: [docs.northflank.com](https://docs.northflank.com)
- **Groq API Docs**: [console.groq.com/docs](https://console.groq.com/docs)
- **Project Repository**: [github.com/klogins-hash/magentic-groq-ui](https://github.com/klogins-hash/magentic-groq-ui)
