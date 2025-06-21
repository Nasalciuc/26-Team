# Tinkerbell Backend (Node.js/Express)

## Quick Setup (Aurelian's Tasks - Hour 1)

### API Endpoints Created:
- `POST /api/create-personas` - Creates customer personas from business data
- `POST /api/schedule-campaign` - Schedules marketing campaign with generated content
- `GET /health` - Health check endpoint

### Installation:
```bash
cd tinkerbell-backend
npm install
npm start
```

### Environment Variables:
Copy `.env` file and update with your API keys:
- `OPENAI_API_KEY` - For AI content generation
- `PLANABLE_ACCESS_TOKEN` - For social media posting

### Testing the endpoints:

1. **Create Personas:**
```bash
curl -X POST http://localhost:3000/api/create-personas \
  -H "Content-Type: application/json" \
  -d '{"businessName": "Test Florist", "description": "Local flower shop"}'
```

2. **Schedule Campaign:**
```bash
curl -X POST http://localhost:3000/api/schedule-campaign \
  -H "Content-Type: application/json" \
  -d '{"personas": [], "campaigns": []}'
```

### Status: ✅ Hour 1 Complete
- [x] Express server setup
- [x] Two API endpoints created
- [x] Basic logging and success responses
- [x] Ready for integration with AI and Planable APIs

### Next Steps (Hour 2):
- Integrate with Vladimir's AI service
- Integrate with Nicolae's Planable client
