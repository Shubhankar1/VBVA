# VBVA - Video-Based Virtual Assistant

A robust, multi-agent video-based virtual assistant system with simplified startup and management.

## 🚀 Quick Start

### One-Command Startup
```bash
./start_vbva.sh
```

That's it! The system will automatically:
- ✅ Check and install dependencies
- ✅ Validate and clean your `.env` file
- ✅ Create necessary directories
- ✅ Check port availability
- ✅ Start backend and frontend services
- ✅ Wait for services to be ready
- ✅ Display status summary

### System Management

**Check Status:**
```bash
./status_vbva.sh
```

**Stop Services:**
```bash
./stop_vbva.sh
```

**Restart Services:**
```bash
./stop_vbva.sh && ./start_vbva.sh
```

## 🔧 Configuration

### Environment Setup
1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```bash
   # Required API Keys
   OPENAI_API_KEY=your_openai_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   SECRET_KEY=your_secret_key_here
   
   # Optional API Keys
   DEEPGRAM_API_KEY=your_deepgram_api_key_here
   D_ID_API_KEY=your_d_id_api_key_here
   REPLICATE_API_TOKEN=your_replicate_token_here
   ```

3. The system will automatically clean and validate your `.env` file on startup.

## 🌐 Access URLs

Once started, access the system at:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎯 Features

### ✅ Robust Startup System
- **Automatic dependency management**
- **Environment validation and cleaning**
- **Port conflict resolution**
- **Service health monitoring**
- **Graceful shutdown handling**

### ✅ Simplified Video Processing
- **No more over-engineering**
- **Single video for short content (≤12s)**
- **Smart chunking for long content**
- **Proper order preservation**
- **60% less code complexity**

### ✅ Multi-Agent Support
- **General Assistant**
- **Airport Assistant**
- **Hotel Receptionist**
- **Sales Agent**

### ✅ High-Quality Output
- **OpenAI GPT-4o integration**
- **ElevenLabs TTS**
- **Wav2Lip lip-sync**
- **Real-time video generation**

## 🛠️ Manual Setup (Advanced)

If you prefer manual setup or need to debug:

### Backend Only
```bash
cd backend
python main.py
```

### Frontend Only
```bash
cd frontend
streamlit run app.py --server.port 8501
```

### Dependencies
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
VBVA-1/
├── start_vbva.sh          # 🚀 One-command startup
├── stop_vbva.sh           # 🛑 Stop all services
├── status_vbva.sh         # 📊 Check system status
├── start_robust.py        # 🔧 Robust startup script
├── .env                   # ⚙️ Environment configuration
├── backend/               # 🔧 FastAPI backend
├── frontend/              # 🎨 Streamlit frontend
├── services/              # 🔧 Core services
├── agents/                # 🤖 AI agents
├── config/                # ⚙️ Configuration
└── avatars/               # 🖼️ Avatar images
```

## 🔍 Troubleshooting

### Common Issues

**Port Already in Use:**
- The system automatically handles this
- Run `./stop_vbva.sh` to clean up

**Missing Dependencies:**
- The system automatically installs them
- Check `requirements.txt` for manual installation

**Environment Issues:**
- The system validates and cleans your `.env` file
- Check the startup logs for specific errors

**API Key Issues:**
- Ensure your API keys are valid
- Check the `.env` file format

### Logs and Debugging

**Backend Logs:**
```bash
tail -f backend.log
```

**Frontend Logs:**
```bash
tail -f frontend.log
```

**System Status:**
```bash
./status_vbva.sh
```

## 🎉 What's New

### Latest Improvements
- ✅ **Robust startup system** - No more manual configuration
- ✅ **Simplified video processing** - 60% less code complexity
- ✅ **Automatic dependency management** - Self-healing system
- ✅ **Environment validation** - Clean and validate `.env` files
- ✅ **Port conflict resolution** - Automatic cleanup
- ✅ **Service health monitoring** - Real-time status checking
- ✅ **Graceful shutdown** - Clean process termination

### Video Processing Fixes
- ✅ **No more looping** - Single video for short content
- ✅ **Proper chunking** - Smart handling of long content
- ✅ **Order preservation** - Correct video sequence
- ✅ **Better performance** - Optimized processing pipeline

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with the robust startup system
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Made with ❤️ for robust, simplified AI video generation**
