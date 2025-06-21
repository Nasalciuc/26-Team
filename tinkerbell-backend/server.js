const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Embedded Planable functionality (Nicolae's work - integrated directly)
const Planable = {
    async createWorkspace(workspaceName) {
        console.log(`📋 Planable: Creating workspace "${workspaceName}"`);

        // Mock workspace for reliable demo
        const mockId = `mock_ws_${Date.now()}`;
        return {
            id: mockId,
            name: workspaceName,
            url: `https://app.planable.io/workspace/${mockId}`,
            created_at: new Date().toISOString(),
            status: 'active'
        };
    },

    async schedulePost(workspaceId, postData) {
        console.log(`📝 Planable: Scheduling post for ${postData.platform}`);

        // Mock post response
        return {
            id: `mock_post_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            platform: postData.platform,
            content: postData.post_text,
            status: 'scheduled',
            scheduled_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
            created_at: new Date().toISOString()
        };
    },

    async scheduleMultiplePosts(workspaceId, postsData) {
        console.log(`📚 Planable: Scheduling ${postsData.length} posts in batch`);

        const results = [];

        for (const postData of postsData) {
            try {
                const result = await this.schedulePost(workspaceId, postData);
                results.push({
                    success: true,
                    postData,
                    response: result
                });
            } catch (error) {
                results.push({
                    success: false,
                    postData,
                    error: error.message
                });
            }
        }

        const successCount = results.filter(r => r.success).length;
        console.log(`✅ Planable: ${successCount}/${postsData.length} posts scheduled successfully`);

        return results;
    },

    getWorkspaceUrl(workspaceId) {
        return `https://app.planable.io/workspace/${workspaceId}`;
    }
};

// Import real AI client
const TinkerbellAI = require('./aiClient');
const aiClient = new TinkerbellAI();

// Embedded AI functionality (Vladimir's work - integrated directly)
const AI = {
    async generatePersonas(businessData) {
        console.log('🧠 AI: Generating customer personas...');

        // Try real AI first, fallback to mock for demo reliability
        if (process.env.OPENAI_API_KEY && process.env.OPENAI_API_KEY !== 'your_openai_api_key_here') {
            try {
                console.log('🤖 Using real OpenAI...');
                return await aiClient.generatePersonas(businessData);
            } catch (error) {
                console.log('⚠️ AI failed, using mock data:', error.message);
            }
        }

        // Mock personas for reliable demo
        return {
            personas: [{
                    name: "Maria Popescu",
                    age_range: "28-35",
                    demographics: "Femeie tânără, educată, venit mediu-mare",
                    interests: ["evenimente speciale", "design interior", "fotografii"],
                    pain_points: ["lipsa timpului pentru organizare", "găsirea furnizorilor de calitate"],
                    buying_behavior: "Cercetează online, citește review-uri",
                    preferred_platforms: ["Instagram", "Facebook"],
                    communication_style: "Profesional dar prietenos"
                },
                {
                    name: "Ana Ciobanu",
                    age_range: "30-45",
                    demographics: "Femeie matură, organizator evenimente",
                    interests: ["planning evenimente", "networking", "eficiență"],
                    pain_points: ["respectarea bugetelor", "coordonarea furnizorilor"],
                    buying_behavior: "Decizii rapide, relații pe termen lung",
                    preferred_platforms: ["Facebook", "LinkedIn"],
                    communication_style: "Direct, orientat spre rezultate"
                }
            ]
        };
    },
    async generateCampaignContent(businessData, confirmedPersonas) {
        console.log('🎨 AI: Generating campaign content...');

        // Try real AI first, fallback to mock for demo reliability
        if (process.env.OPENAI_API_KEY && process.env.OPENAI_API_KEY !== 'your_openai_api_key_here') {
            try {
                console.log('🤖 Using real OpenAI for campaign...');
                return await aiClient.generateCampaignContent(businessData, confirmedPersonas);
            } catch (error) {
                console.log('⚠️ AI failed, using mock data:', error.message);
            }
        }

        // Mock campaign content for reliable demo
        return {
            strategy: "Creăm campanii care evidențiază calitatea și unicitatea produselor pentru a atrage clienți care valorifică excelența.",
            posts: [{
                    platform: "both",
                    post_text: "🌸 Transformăm visurile tale în realitate cu aranjamente florale unice! Fiecare buchet spune o poveste specială. ✨",
                    hashtags: ["#florarie", "#aranjamenteflorale", "#nunti", "#chisinau", "#flori"],
                    call_to_action: "Contactează-ne pentru o consultație gratuită!",
                    image_description: "Buchet elegant cu flori proaspete, aranjament profesional",
                    target_persona: "Maria Popescu",
                    post_goal: "awareness"
                },
                {
                    platform: "facebook",
                    post_text: "💍 Nuntă de vis? Avem soluția perfectă! Decorațiuni florale care vor face ca ziua ta specială să fie de neuitat. 👰",
                    hashtags: ["#nunta", "#decoratiuni", "#mireasa", "#evenimente"],
                    call_to_action: "Rezervă o întâlnire pentru planificarea nunții tale!",
                    image_description: "Decorațiuni florale elegante pentru nuntă",
                    target_persona: "Maria Popescu",
                    post_goal: "conversion"
                },
                {
                    platform: "instagram",
                    post_text: "🎯 Organizezi un eveniment special? Noi ne ocupăm de partea florală ca să fie perfect! 📞",
                    hashtags: ["#organizatorevenimente", "#florarie", "#professional", "#chisinau"],
                    call_to_action: "Trimite un mesaj pentru oferta ta personalizată!",
                    image_description: "Aranjament floral modern pentru evenimente corporate",
                    target_persona: "Ana Ciobanu",
                    post_goal: "conversion"
                }
            ]
        };
    }
};

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Route for creating personas (Hour 2: AI Integration)
app.post('/api/create-personas', async(req, res) => {
    console.log('=== CREATE PERSONAS ENDPOINT ===');
    console.log('Request body:', req.body);
    try {
        // Use embedded AI functionality to generate personas
        const personas = await AI.generatePersonas(req.body);

        res.json({
            success: true,
            message: 'Personas generated successfully!',
            data: personas
        });

    } catch (error) {
        console.error('❌ Error generating personas:', error);
        res.status(500).json({
            success: false,
            message: 'Failed to generate personas',
            error: error.message
        });
    }
});

// Route for scheduling campaign (Hour 2: AI Integration)
app.post('/api/schedule-campaign', async(req, res) => {
    console.log('=== SCHEDULE CAMPAIGN ENDPOINT ===');
    console.log('Request body:', req.body);

    try {
        const { businessData, confirmedPersonas } = req.body; // Use embedded AI functionality to generate campaign content
        const campaignContent = await AI.generateCampaignContent(businessData, confirmedPersonas);

        // Nicolae's Planable integration (Hour 3)
        const workspaceName = `${businessData.businessName || 'Tinkerbell'} Campaign - ${new Date().toLocaleDateString()}`;
        console.log('📋 Creating Planable workspace...');
        const workspace = await Planable.createWorkspace(workspaceName);

        console.log('📝 Scheduling posts to Planable...');
        const schedulingResults = await Planable.scheduleMultiplePosts(workspace.id, campaignContent.posts);

        const successfulPosts = schedulingResults.filter(r => r.success).length;
        const workspaceUrl = Planable.getWorkspaceUrl(workspace.id);

        res.json({
            success: true,
            message: `Campaign scheduled successfully! ${successfulPosts}/${campaignContent.posts.length} posts created.`,
            data: {
                campaign: campaignContent,
                workspace: {
                    id: workspace.id,
                    name: workspace.name,
                    url: workspaceUrl
                },
                scheduling: {
                    total: campaignContent.posts.length,
                    successful: successfulPosts,
                    results: schedulingResults
                }
            },
            planableWorkspaceUrl: workspaceUrl
        });

    } catch (error) {
        console.error('❌ Error generating campaign:', error);
        res.status(500).json({
            success: false,
            message: 'Failed to generate campaign',
            error: error.message
        });
    }
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        message: 'Tinkerbell Backend is running!'
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🎯 Tinkerbell Backend server running on port ${PORT}`);
    console.log(`📍 API endpoints available:`);
    console.log(`   POST /api/create-personas`);
    console.log(`   POST /api/schedule-campaign`);
    console.log(`   GET  /health`);
});

module.exports = app;