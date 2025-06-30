# VBVA Setup Guide

## Prerequisites

### System Requirements
- Python 3.9 or higher
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Internet connection for API access

### Required API Keys
1. **OpenAI API Key** - For GPT-4o access
2. **ElevenLabs API Key** - For text-to-speech
3. **D-ID API Key** (optional) - For lip-sync
4. **Replicate API Token** (optional) - For alternative lip-sync

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd VBVA-1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp env.example .env
```

Edit `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
D_ID_API_KEY=your_d_id_api_key
SECRET_KEY=your_secret_key_here_32_chars_minimum
```

### 4. Run the Application

#### Option A: Development Mode
```bash
# Terminal 1: Start backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
streamlit run frontend/app.py
```

#### Option B: Docker
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Detailed Setup

### Backend Configuration

#### 1. FastAPI Backend
The backend runs on FastAPI with the following features:
- Multi-agent orchestration with LangGraph
- RESTful API endpoints
- WebSocket support for real-time streaming
- Automatic API documentation at `/docs`

#### 2. Agent Configuration
Agents are configured in `agents/` directory:
- `base.py` - Base agent class
- `hotel_agent.py` - Hotel receptionist
- `airport_agent.py` - Airport assistant
- `sales_agent.py` - Sales agent

#### 3. Service Configuration
Services are in `services/` directory:
- `stt.py` - Speech-to-text (Whisper/Deepgram)
- `tts.py` - Text-to-speech (ElevenLabs)
- `lip_sync.py` - Lip-sync (D-ID/Replicate)

### Frontend Configuration

#### 1. Streamlit Interface
The frontend provides:
- Text and voice input options
- Real-time chat interface
- Video output display
- Agent selection
- Session management

#### 2. WebRTC Integration
For voice input, the system uses:
- `streamlit-webrtc` for audio capture
- Real-time audio processing
- Automatic audio format conversion

### Lip-Sync Configuration

#### Option 1: D-ID API (Recommended)
```env
LIP_SYNC_PROVIDER=d_id
D_ID_API_KEY=your_d_id_api_key
```

#### Option 2: Replicate (Cost-effective)
```env
LIP_SYNC_PROVIDER=replicate
REPLICATE_API_TOKEN=your_replicate_token
```

#### Option 3: Google Colab (Free)
```env
LIP_SYNC_PROVIDER=colab
```
Note: Requires manual Colab setup

## Deployment Options

### 1. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn backend.main:app --reload

# Run frontend
streamlit run frontend/app.py
```

### 2. Docker Deployment
```bash
# Build and run
docker-compose up --build

# Access at:
# Backend: http://localhost:8000
# Frontend: http://localhost:8501
```

### 3. Cloud Deployment

#### Render
1. Connect your GitHub repository
2. Set environment variables
3. Deploy automatically

#### Railway
1. Import from GitHub
2. Configure environment variables
3. Deploy with one click

#### HuggingFace Spaces
1. Create new Space
2. Upload code
3. Configure environment variables

## Testing

### 1. Unit Tests
```bash
pytest tests/
```

### 2. API Tests
```bash
# Test backend health
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "agent_type": "general"}'
```

### 3. Frontend Tests
```bash
# Run Streamlit tests
streamlit run frontend/app.py --server.headless true
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.9+
```

#### 2. API Key Issues
```bash
# Verify environment variables
echo $OPENAI_API_KEY
echo $ELEVENLABS_API_KEY

# Check .env file
cat .env
```

#### 3. Port Conflicts
```bash
# Check if ports are in use
lsof -i :8000
lsof -i :8501

# Use different ports
uvicorn backend.main:app --port 8001
streamlit run frontend/app.py --server.port 8502
```

#### 4. Docker Issues
```bash
# Clean Docker cache
docker system prune -a

# Rebuild containers
docker-compose down
docker-compose up --build
```

### Performance Optimization

#### 1. Caching
```python
# Enable Redis caching
REDIS_URL=redis://localhost:6379
```

#### 2. Async Processing
```python
# Use async endpoints for better performance
async def process_request():
    # Async processing
    pass
```

#### 3. Resource Limits
```python
# Set API rate limits
RATE_LIMIT_PER_MINUTE=60
```

## Security Considerations

### 1. API Key Protection
- Never commit API keys to version control
- Use environment variables
- Rotate keys regularly

### 2. Input Validation
- Sanitize all user inputs
- Validate file uploads
- Implement rate limiting

### 3. Session Management
- Use secure session tokens
- Implement session timeouts
- Isolate user contexts

## Monitoring and Logging

### 1. Application Logs
```python
# Configure logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

### 2. Performance Monitoring
```python
# Enable metrics
from services.monitoring import setup_monitoring
setup_monitoring()
```

### 3. Health Checks
```bash
# Check system health
curl http://localhost:8000/health
```

## Support and Resources

### Documentation
- API Documentation: `http://localhost:8000/docs`
- Code Documentation: See docstrings in code

### Community
- GitHub Issues: Report bugs and feature requests
- Discussions: General questions and support

### Updates
- Regular dependency updates
- Security patches
- Feature enhancements 