# 🎥 VBVA - Video-Based Virtual Assistant

A **production-ready, scalable, real-time video-to-video virtual assistant** powered by AI, featuring local Wav2Lip lip-sync technology.

## 🚀 Features

- **🤖 Multi-Agent Orchestration**: OpenAI GPT-4 powered agents for different use cases
- **🎵 High-Quality TTS**: ElevenLabs text-to-speech integration
- **🎬 Local Lip-Sync**: Wav2Lip for unlimited video generation
- **🌐 Real-Time Interface**: Streamlit frontend with live video streaming
- **📱 Scalable Architecture**: Docker-based deployment with health checks
- **🔒 Production Ready**: CORS, security, monitoring, and logging

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Wav2Lip       │
│   (Streamlit)   │◄──►│   (FastAPI)     │◄──►│   (Local)       │
│   Port: 8501    │    │   Port: 8000    │    │   GPU/CPU       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│     Redis       │◄─────────────┘
                        │   (Caching)     │
                        │   Port: 6379    │
                        └─────────────────┘
```

## 🛠️ Quick Start

### Prerequisites

- Docker & Docker Compose
- NVIDIA GPU (optional, for faster Wav2Lip processing)
- API Keys: OpenAI, ElevenLabs

### 1. Clone & Setup

```bash
git clone <repository-url>
cd VBVA-1
```

### 2. Environment Configuration

Create `.env` file:

```env
# Required API Keys
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
SECRET_KEY=your_secret_key_here

# Optional Configuration
DEBUG=false
LOG_LEVEL=INFO
LIP_SYNC_PROVIDER=local_wav2lip
```

### 3. Deploy

```bash
# Production deployment
./deploy.sh

# Or manual deployment
docker-compose up -d
```

### 4. Access

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎯 Usage

### Text-to-Video Chat

1. Open http://localhost:8501
2. Select an agent type (General, Hotel, Airport, Sales)
3. Type your message
4. Watch as the system generates a lip-synced video response

### Voice-to-Video Chat

1. Go to the "🎤 Voice Chat" tab
2. Upload an audio file
3. Get a video response with lip-sync

## 🔧 Development

### Local Development

```bash
# Backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend
streamlit run frontend/app.py --server.port 8501
```

### Docker Development

```bash
# Build and run
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📊 Production Features

### Scalability

- **Horizontal Scaling**: Multiple backend instances
- **Load Balancing**: Nginx reverse proxy (optional)
- **Caching**: Redis for session management
- **Storage**: Shared volumes for video persistence

### Monitoring

- **Health Checks**: Automatic service monitoring
- **Logging**: Structured logging with structlog
- **Metrics**: Prometheus metrics (optional)

### Security

- **CORS**: Proper cross-origin configuration
- **Authentication**: JWT-based auth (optional)
- **Rate Limiting**: Request throttling
- **Input Validation**: Pydantic models

## 🎬 Real-Time Video Features

### Current Implementation

- ✅ Static image lip-sync with Wav2Lip
- ✅ Text-to-speech integration
- ✅ Video serving via HTTP
- ✅ Progress tracking

### Planned Features

- 🔄 Real-time video input processing
- 🔄 WebRTC video streaming
- 🔄 Live video-to-video lip-sync
- 🔄 WebSocket progress updates

## 🏗️ System Components

### Backend Services

- **Agent Orchestrator**: Multi-agent coordination
- **TTS Service**: ElevenLabs integration
- **Lip-Sync Service**: Wav2Lip integration
- **Video Service**: File serving and processing

### Frontend Components

- **Chat Interface**: Text and voice input
- **Video Player**: Real-time video display
- **Progress Tracking**: Generation status
- **Agent Selection**: Multi-agent support

## 📈 Performance

### Benchmarks

- **Video Generation**: 5-15 seconds (CPU), 2-5 seconds (GPU)
- **Text Response**: < 1 second
- **Audio Generation**: 2-3 seconds
- **Concurrent Users**: 10+ (scalable)

### Optimization

- **Caching**: Redis for repeated requests
- **Async Processing**: Background video generation
- **GPU Acceleration**: CUDA support for Wav2Lip
- **CDN**: Optional video distribution

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `ELEVENLABS_API_KEY` | ElevenLabs API key | Required |
| `SECRET_KEY` | Application secret | Required |
| `DEBUG` | Debug mode | false |
| `LOG_LEVEL` | Logging level | INFO |
| `LIP_SYNC_PROVIDER` | Lip-sync provider | local_wav2lip |

### Service Configuration

```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
    volumes:
      - ./Wav2Lip:/app/Wav2Lip
      - wav2lip_outputs:/tmp/wav2lip_outputs
```

## 🚀 Deployment Options

### Local Docker

```bash
./deploy.sh
```

### Cloud Deployment

#### AWS ECS

```bash
# Build and push to ECR
docker build -f Dockerfile.backend -t vbva-backend .
docker build -f Dockerfile.frontend -t vbva-frontend .

# Deploy to ECS
aws ecs create-service --cluster vbva --service-name vbva-backend
```

#### Google Cloud Run

```bash
# Deploy to Cloud Run
gcloud run deploy vbva-backend --source .
gcloud run deploy vbva-frontend --source .
```

#### Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

## 🐛 Troubleshooting

### Common Issues

1. **Video not playing**: Check CORS headers and video serving endpoint
2. **Wav2Lip errors**: Ensure CUDA drivers and PyTorch are installed
3. **API key errors**: Verify environment variables in `.env`
4. **Port conflicts**: Check if ports 8000/8501 are available

### Debug Commands

```bash
# Check service health
curl http://localhost:8000/health
curl http://localhost:8501/_stcore/health

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Test video endpoint
curl -I http://localhost:8000/api/v1/videos/filename.mp4
```

## 📚 API Documentation

### Endpoints

- `POST /api/v1/chat` - Text chat
- `POST /api/v1/voice` - Voice chat
- `POST /api/v1/generate_video` - Video generation
- `GET /api/v1/videos/{filename}` - Video serving
- `GET /api/v1/agents` - List agents
- `GET /health` - Health check

### Example Usage

```bash
# Generate video
curl -X POST http://localhost:8000/api/v1/generate_video \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello world", "agent_type": "general"}'

# Get video
curl http://localhost:8000/api/v1/videos/wav2lip_output_abc123.mp4
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: API docs at `/docs`
- **Community**: Discord/Telegram (TBD)

---

**Built with ❤️ using FastAPI, Streamlit, and Wav2Lip**
