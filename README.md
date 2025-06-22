# 🧚‍♀️ Tinkerbell - AI Marketing Assistant

<div align="center">

![Tinkerbell Logo](https://img.shields.io/badge/🧚‍♀️-Tinkerbell-6366f1?style=for-the-badge&labelColor=1f2937)

**Transform Your Marketing from Hours to Minutes with AI-Powered Automation**

[![Status](https://img.shields.io/badge/Status-Production%20Ready-28a745?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-007acc?style=flat-square)]()
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat-square&logo=node.js)]()
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=flat-square&logo=openai)]()

[🚀 Quick Start](#-quick-start) • [🌟 Features](#-features) • [🛠️ Setup](#️-setup-guide) • [🏗️ Architecture](#️-architecture)

</div>

---

## 🎯 **What is Tinkerbell?**

Tinkerbell is a **complete AI-powered marketing automation platform** that revolutionizes marketing for small businesses. With a modern, professional interface inspired by Planable and Sintra.ai, it transforms complex marketing tasks into a simple 3-step process:

**Step 1:** Tell us about your business  
**Step 2:** AI creates detailed customer personas  
**Step 3:** Get ready-to-launch campaigns with social media posts  

Built as a **fully functional MVP in 4 hours**, demonstrating rapid development capabilities for investors and users alike.

### 🌟 **Key Features**

| Feature | Description | Status |
|---------|-------------|--------|
| 🤖 **AI Persona Generation** | Creates detailed customer profiles using GPT-4 | ✅ Ready |
| 📝 **Content Creation** | Generates posts, captions, hashtags automatically | ✅ Ready |
| 🖼️ **Image Analysis** | AI-powered product image analysis and generation | ✅ Ready |
| 📋 **Planable Integration** | Seamless workflow publishing to marketing teams | ✅ Ready |
| 📱 **Facebook Integration** | Direct social media posting capabilities | ✅ Ready |
| 🎨 **Modern UI/UX** | Professional, clean Planable-inspired interface | ✅ Ready |
| 🌐 **Landing Page** | Beautiful marketing site with animations | ✅ Ready |

---

## 🚀 **Quick Start**

### Prerequisites
- Node.js 18+ installed
- OpenAI API key
- Facebook Page access token (optional)
- Planable account (optional)

### 1. Clone & Install
```bash
git clone https://github.com/Nicu106/26-Team.git
cd 26-Team
cd tinkerbell-backend && npm install
cd ../tinkerbell-frontend
```

### 2. Configure Environment
```bash
# In tinkerbell-backend directory
copy .env.example .env
# Edit .env with your API keys
```

### 3. Start Services
```bash
# Terminal 1: Backend (port 3000)
cd tinkerbell-backend
npm start

# Terminal 2: Frontend (port 8081)
cd tinkerbell-frontend
node server.js
```

### 4. Open Application
- **Landing Page**: http://localhost:8081
- **Main App**: http://localhost:8081/index.html?app=true

---

## 🛠️ **Setup Guide**

### 📋 **Step 1: Clone & Install**

```bash
git clone https://github.com/Nicu106/26-Team.git
cd 26-Team
```

### 📋 **Step 2: Backend Setup**

```bash
cd tinkerbell-backend

# Install dependencies
npm install

# Create environment file
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Edit .env with your API keys
notepad .env  # Windows
# nano .env   # macOS/Linux
```

**Required Environment Variables:**
```env
OPENAI_API_KEY=sk-your-openai-key-here
PORT=3000

# Optional for enhanced features
PLANABLE_API_KEY=your_planable_key
FACEBOOK_ACCESS_TOKEN=your_fb_token
FACEBOOK_PAGE_ID=your_page_id
```

### 📋 **Step 3: Frontend Setup**

```bash
cd ../tinkerbell-frontend

# The frontend uses a custom Node.js server
# No additional installation required
```

### 📋 **Step 4: Start the Servers**

**Backend (Terminal 1):**
```bash
cd tinkerbell-backend
npm start
```

**Frontend (Terminal 2):**
```bash
cd tinkerbell-frontend
node server.js
```

### 📋 **Step 5: Verify Installation**

1. **Backend Health Check**: http://localhost:3000/api/health
2. **Frontend Landing**: http://localhost:8081
3. **Main Application**: http://localhost:8081/index.html?app=true

---

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │  External APIs  │
│   (Port 8081)   │◄──►│   (Port 3000)   │◄──►│                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
│                      │                      │                 │
│ • Landing Page       │ • AI Processing     │ • OpenAI GPT-4   │
│ • 3-Step Onboarding  │ • Image Analysis    │ • Facebook API   │
│ • Modern UI/UX       │ • Campaign Logic    │ • Planable API   │
│ • Session Management │ • API Endpoints     │ • Image Services │
└─────────────────────┘└─────────────────────┘└─────────────────┘
```

### 🔧 **Technology Stack**

**Frontend:**
- **Framework**: Vanilla JavaScript + Modern CSS
- **UI**: Planable-inspired design system
- **Server**: Custom Node.js static file server
- **Fonts**: Inter (Google Fonts)

**Backend:** 
- **Runtime**: Node.js 18+
- **Framework**: Express.js
- **AI**: OpenAI GPT-4
- **Integrations**: Planable API, Facebook Graph API
- **File Handling**: Multer for image uploads

**External Services:**
- **AI Processing**: OpenAI GPT-4 & DALL-E
- **Publishing**: Planable Workspace API
- **Social Media**: Facebook Graph API

---

## 📁 **Project Structure**

```
Tinkerbell/
├── 📂 tinkerbell-frontend/           # Frontend application
│   ├── 🌐 landing.html              # Marketing landing page
│   ├── 🎯 index.html                # Main application
│   ├── 🎨 style.css                 # Application styles  
│   ├── ⚙️ script.js                 # Application logic
│   └── 🚀 server.js                 # Frontend server
├── 📂 tinkerbell-backend/            # Backend API server
│   ├── 🔧 server.js                 # Main server file
│   ├── 🤖 aiClient.js               # OpenAI integration
│   ├── 📋 planableClient.js         # Planable API client
│   ├── 📱 facebookService.js        # Facebook integration
│   ├── 🖼️ imageService.js           # Image processing
│   └── 📦 package.json              # Dependencies
├── 📂 docs/                         # Documentation
├── 📂 testing/                      # Test files
└── 📄 README.md                     # This file
```

---

## 🧪 **Testing**

### 🔍 **Health Checks**

```bash
# Backend health check
curl http://localhost:3000/api/health

# Test AI functionality
curl -X POST http://localhost:3000/api/personas \
  -H "Content-Type: application/json" \
  -d '{"businessName":"Test Business","businessDescription":"Test"}'
```

### 🧪 **Test Files**

The project includes comprehensive test files:
- `test-ai.js` - AI integration testing
- `test-facebook.js` - Facebook API testing  
- `test-planable.js` - Planable integration testing
- `test-endpoints.js` - Full API testing

```bash
cd tinkerbell-backend
node test-ai.js        # Test AI functionality
node test-endpoints.js # Test all endpoints
```

---

## 📊 **API Documentation**

### 🎯 **Core Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/personas` | POST | Generate AI personas |
| `/api/campaigns` | POST | Create marketing campaigns |
| `/api/upload-images` | POST | Upload and analyze images |
| `/api/publish-to-planable` | POST | Publish to Planable |

### 📝 **Example API Usage**

**Generate Customer Personas:**
```bash
curl -X POST http://localhost:3000/api/personas \
  -H "Content-Type: application/json" \
  -d '{
    "businessName": "Martha'\''s Flower Shop",
    "businessDescription": "Local florist specializing in wedding arrangements",
    "targetCustomers": "Brides-to-be, event planners",
    "businessGoals": "Increase wedding bookings"
  }'
```

---

## 🔧 **Configuration**

### ⚙️ **Environment Variables**

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for AI features |
| `PORT` | ❌ No | Backend port (default: 3000) |
| `PLANABLE_API_KEY` | ❌ No | For Planable integration |
| `FACEBOOK_ACCESS_TOKEN` | ❌ No | For Facebook posting |
| `FACEBOOK_PAGE_ID` | ❌ No | Target Facebook page |

### 🚀 **Production Configuration**

For production deployment:

```env
NODE_ENV=production
OPENAI_API_KEY=your_production_key
PORT=3000
```

---

## 🚀 **Deployment**

### 🌐 **Frontend Deployment**

The frontend is a static site that can be deployed to:
- **Netlify** (recommended)
- **Vercel** 
- **GitHub Pages**
- Any static hosting service

### ⚙️ **Backend Deployment**

The backend can be deployed to:
- **Railway** (recommended)
- **Heroku**
- **DigitalOcean**
- **AWS/Azure/GCP**

---

## 🐛 **Troubleshooting**

### ❓ **Common Issues**

**Port already in use:**
```bash
# Kill processes on ports
npx kill-port 3000 8081
```

**Missing API key:**
```bash
# Check environment variables
echo $OPENAI_API_KEY  # macOS/Linux
echo %OPENAI_API_KEY% # Windows
```

**Navigation issues:**
- Clear browser cache and session storage
- Ensure both servers are running
- Check browser console for errors

### 📞 **Need Help?**

1. Check the [Issues](https://github.com/Nicu106/26-Team/issues) page
2. Review the troubleshooting documentation
3. Create a new issue with detailed information

---

## 🤝 **Contributing**

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **OpenAI** for providing GPT-4 API
- **Planable** for inspiration and integration
- **Inter Font** by Rasmus Andersson
- **The amazing open-source community**

---

<div align="center">

**Made with ❤️ by the Tinkerbell Team**

[⭐ Star this repo](https://github.com/Nicu106/26-Team) • [🐛 Report Bug](https://github.com/Nicu106/26-Team/issues) • [💡 Request Feature](https://github.com/Nicu106/26-Team/issues)

**🌟 From concept to investor-ready MVP in 4 hours!**

</div>
