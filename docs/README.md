# 🎯 Tinkerbell - AI-Powered Marketing Automation for Small Businesses

> **Built in 4 hours** - A fully functional MVP that transforms small business marketing through AI-powered persona generation and automated social media campaigns.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- NPM or Yarn
- Modern web browser

### Backend Setup
```bash
cd tinkerbell-backend
npm install
npm start
```
Server runs on `http://localhost:3000`

### Frontend Setup
```bash
cd tinkerbell-frontend
python -m http.server 8080
# OR use any static file server
```
Frontend runs on `http://localhost:8080`

## 📋 What is Tinkerbell?

Tinkerbell is an AI-powered SaaS solution that helps small business owners:

1. **Generate Customer Personas** - AI creates detailed, data-driven customer profiles
2. **Create Content Campaigns** - Automatically generates social media content tailored to personas
3. **Schedule to Planable** - Seamlessly integrates with Planable for content scheduling and collaboration

## 🏗️ Architecture

### Tech Stack
- **Backend**: Node.js + Express
- **Frontend**: Vanilla HTML/CSS/JavaScript  
- **AI**: OpenAI GPT (with mock fallback)
- **Integration**: Planable API
- **Database**: In-memory (MVP)

### API Endpoints

#### `POST /api/create-personas`
Generates customer personas based on business data.

**Request:**
```json
{
  "businessType": "Romanian Restaurant",
  "targetMarket": "Local food enthusiasts", 
  "businessGoals": "Increase customer base"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Personas generated successfully!",
  "data": {
    "personas": [
      {
        "name": "Maria Popescu",
        "age_range": "28-35",
        "demographics": "Femeie tânără, educată, venit mediu-mare",
        "interests": ["evenimente speciale", "design interior"],
        "pain_points": ["lipsa timpului pentru organizare"],
        "buying_behavior": "Cercetează online, citește review-uri",
        "preferred_platforms": ["Instagram", "Facebook"],
        "communication_style": "Profesional dar prietenos"
      }
    ]
  }
}
```

#### `POST /api/schedule-campaign`
Generates campaign content and schedules to Planable.

**Request:**
```json
{
  "businessData": {
    "businessName": "Restaurant Example",
    "businessType": "Romanian Restaurant"
  },
  "confirmedPersonas": [...]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Campaign scheduled successfully!",
  "data": {
    "campaign": {
      "posts": [...]
    },
    "workspace": {
      "id": "workspace_123",
      "name": "Restaurant Campaign",
      "url": "https://app.planable.io/workspace/workspace_123"
    }
  },
  "planableWorkspaceUrl": "https://app.planable.io/workspace/workspace_123"
}
```

## 🎨 User Journey

### Step 1: Business Onboarding
- User enters business information (name, type, target market, goals)
- Clean, modern form with validation

### Step 2: Persona Generation & Editing  
- AI generates 2 detailed customer personas
- Editable cards allow customization
- Real-time preview of persona data

### Step 3: Campaign Creation
- AI generates 3 targeted social media posts per persona
- Content includes Romanian text, hashtags, and CTAs
- Preview campaign before scheduling

### Step 4: Planable Integration
- Creates dedicated workspace in Planable
- Schedules all posts automatically
- Provides workspace URL for team collaboration

## 🧪 Testing

### Manual Testing
1. **Start both servers** (backend on :3000, frontend on :8080)
2. **Navigate through complete flow**:
   - Fill business information form
   - Review and edit generated personas
   - Generate and schedule campaign
   - Verify Planable workspace creation

### API Testing
```bash
cd tinkerbell-backend
node test-endpoints-simple.js
```

### Expected Results
- ✅ Health check responds with OK
- ✅ Personas endpoint returns 2 Romanian personas
- ✅ Campaign endpoint creates 3 posts per persona
- ✅ Planable workspace URL is returned

## 🔧 Configuration

### Environment Variables
Create `.env` file in `tinkerbell-backend/`:

```env
# OpenAI Configuration (Optional - uses mock data if not provided)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Planable Configuration (Optional - uses mock data if not provided)  
PLANABLE_API_KEY=your_planable_api_key_here
PLANABLE_BASE_URL=https://api.planable.io/v1

# Server Configuration
PORT=3000
NODE_ENV=development
```

**Note**: The system works with mock data by default, so no API keys are required for testing.

## 🎯 Team Contributions

### Hour 1 & 2 Implementation

**👨‍💻 Aurelian** - Backend Infrastructure
- Express server setup with CORS and middleware
- API endpoint structure and routing
- Error handling and logging

**🧠 Vladimir** - AI Integration  
- OpenAI integration with detailed prompts
- Persona generation system (Romanian-focused)
- Campaign content creation with mock fallback
- Comprehensive prompt engineering

**📱 Nicolae** - Planable Integration
- Planable API client development
- Workspace creation and post scheduling
- Batch post scheduling functionality
- Mock implementation for reliable demos

**🎨 Lucian & Nicu** - Frontend Development
- Complete 4-page user interface
- Modern CSS with magical theme
- JavaScript application logic and API integration
- Form handling and real-time data updates

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Set up proper API keys for OpenAI and Planable
2. **Database**: Replace in-memory storage with PostgreSQL/MongoDB
3. **Authentication**: Add user accounts and session management
4. **Rate Limiting**: Implement API rate limiting for production use
5. **Error Monitoring**: Add Sentry or similar for error tracking

### Quick Deploy
```bash
# Backend
npm run build
npm run start:prod

# Frontend  
npm run build
# Deploy to Netlify/Vercel
```

## 📈 Future Enhancements

### Phase 2 Features
- **Multi-language Support**: Expand beyond Romanian market
- **Advanced Personas**: Include demographic data sources
- **Campaign Analytics**: Track performance metrics
- **Template Library**: Pre-built campaign templates
- **Team Collaboration**: Multi-user workspace management

### Phase 3 Features
- **A/B Testing**: Automated campaign optimization
- **CRM Integration**: Connect with Salesforce, HubSpot
- **Advanced Scheduling**: Best time optimization
- **Brand Voice**: Consistent messaging across campaigns

## 🐛 Known Issues & Limitations

### Current Limitations
1. **In-Memory Storage**: Data lost on server restart
2. **Romanian Focus**: Personas optimized for Romanian market
3. **Mock Integrations**: Planable integration uses mock responses
4. **No Authentication**: Open API endpoints
5. **Limited Error Handling**: Basic error responses

### Browser Compatibility
- ✅ Chrome 90+
- ✅ Firefox 88+  
- ✅ Safari 14+
- ⚠️ IE not supported

## 📄 License

MIT License - Built during a 4-hour hackathon as an MVP demonstration.

## 🤝 Contributing

This is a hackathon MVP, but contributions are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Built with ❤️ in 4 hours by Team Tinkerbell**

For questions or support, please open an issue in the repository.
