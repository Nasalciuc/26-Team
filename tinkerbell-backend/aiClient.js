const OpenAI = require('openai');

class TinkerbellAI {
    constructor() {
        if (!process.env.OPENAI_API_KEY) {
            console.warn('⚠️ OPENAI_API_KEY not found in environment variables');
            this.openai = null;
        } else {
            this.openai = new OpenAI({
                apiKey: process.env.OPENAI_API_KEY
            });
        }
    }

    /**
     * Generate customer personas based on business data
     * @param {Object} businessData - The business information
     * @returns {Promise<Object>} Generated personas in JSON format
     */
    async generatePersonas(businessData) {
        console.log('🧠 AI: Generating customer personas...');

        if (!this.openai) {
            return this._getMockPersonas(businessData);
        }

        const prompt = this._buildPersonaPrompt(businessData);

        try {
            const response = await this.openai.chat.completions.create({
                model: "gpt-4o",
                messages: [{
                        role: "system",
                        content: "You are an expert marketing strategist and customer research analyst specializing in small businesses. Return ONLY valid JSON responses."
                    },
                    {
                        role: "user",
                        content: prompt
                    }
                ],
                max_tokens: 1500,
                temperature: 0.7
            });
            const content = response.choices[0].message.content.trim();
            console.log('🎯 AI: Personas generated successfully');

            // Clean the response - remove markdown code blocks if present
            let cleanContent = content;
            if (content.includes('```json')) {
                cleanContent = content.replace(/```json\s*/g, '').replace(/```\s*/g, '');
            } else if (content.includes('```')) {
                cleanContent = content.replace(/```\s*/g, '');
            }

            // Parse and validate JSON
            return JSON.parse(cleanContent);

        } catch (error) {
            console.error('❌ AI Error generating personas:', error.message);
            return this._getMockPersonas(businessData);
        }
    }

    /**
     * Generate marketing campaign content based on business data and personas
     * @param {Object} businessData - The business information
     * @param {Array} confirmedPersonas - User-confirmed personas
     * @returns {Promise<Object>} Generated campaign content in JSON format
     */
    async generateCampaignContent(businessData, confirmedPersonas) {
        console.log('🎨 AI: Generating campaign content...');

        if (!this.openai) {
            return this._getMockCampaignContent(businessData);
        }

        const prompt = this._buildCampaignPrompt(businessData, confirmedPersonas);

        try {
            const response = await this.openai.chat.completions.create({
                model: "gpt-4o",
                messages: [{
                        role: "system",
                        content: "You are a creative marketing content specialist who creates engaging social media campaigns for small businesses. Return ONLY valid JSON responses."
                    },
                    {
                        role: "user",
                        content: prompt
                    }
                ],
                max_tokens: 2000,
                temperature: 0.8
            });
            const content = response.choices[0].message.content.trim();
            console.log('🚀 AI: Campaign content generated successfully');

            // Clean the response - remove markdown code blocks if present
            let cleanContent = content;
            if (content.includes('```json')) {
                cleanContent = content.replace(/```json\s*/g, '').replace(/```\s*/g, '');
            } else if (content.includes('```')) {
                cleanContent = content.replace(/```\s*/g, '');
            }

            // Parse and validate JSON
            return JSON.parse(cleanContent);

        } catch (error) {
            console.error('❌ AI Error generating campaign:', error.message);
            return this._getMockCampaignContent(businessData);
        }
    }

    /**
     * Build the persona generation prompt
     * @private
     */
    _buildPersonaPrompt(businessData) {
        return `Based on the following business information, create 2-3 detailed customer personas in JSON format.

Business Information:
- Name: ${businessData.businessName || 'Unknown Business'}
- Description: ${businessData.businessDescription || businessData.description || ''}
- Products/Services: ${businessData.products || businessData.services || ''}
- Target Customers: ${businessData.targetCustomers || businessData.customers || ''}
- Business Goals: ${businessData.goals || ''}
- Website Data: ${businessData.scrapedData || 'No website data available'}

For each persona, provide:
1. name: A realistic Romanian/Moldovan name that fits the demographic
2. age_range: Age range (e.g., "25-35")
3. demographics: Basic demographic info (gender, education, income level)
4. interests: 3-4 specific interests related to the business
5. pain_points: 2-3 specific problems this persona faces that the business can solve
6. buying_behavior: How they typically research and make purchases
7. preferred_platforms: Which social media platforms they use most
8. communication_style: How they prefer to be communicated with

Return ONLY valid JSON in this exact format:
{
  "personas": [
    {
      "name": "string",
      "age_range": "string", 
      "demographics": "string",
      "interests": ["string", "string", "string"],
      "pain_points": ["string", "string"],
      "buying_behavior": "string",
      "preferred_platforms": ["string", "string"],
      "communication_style": "string"
    }
  ]
}`;
    }

    /**
     * Build the campaign content generation prompt
     * @private
     */
    _buildCampaignPrompt(businessData, confirmedPersonas) {
        return `Bazat pe informațiile despre afacere și personele confirmate, creează 3-5 postări captivante pentru rețelele sociale care vor atrage clienți calificați pentru o afacere locală din Moldova/România.

Informații despre afacere:
- Nume: ${businessData.businessName || 'Afacere Locală'}
- Descriere: ${businessData.businessDescription || businessData.description || ''}
- Produse/Servicii: ${businessData.products || businessData.services || ''}

Persoane confirmate:
${JSON.stringify(confirmedPersonas, null, 2)}

Pentru fiecare postare, creează:
1. platform: "facebook" sau "instagram" sau "both"
2. post_text: Text captivant în română (150-250 caractere)
3. hashtags: 5-8 hashtag-uri relevante (mixte română/engleză)
4. call_to_action: CTA clar care generează lead-uri
5. image_description: Descriere detaliată pentru generarea imaginii
6. target_persona: Pe cine vizează această postare
7. post_goal: "awareness", "engagement", or "conversion"

Focusează-te pe postări care vor genera lead-uri calificate (persoane gata să cumpere/să întrebe).

Returnează DOAR JSON valid în acest format exact:
{
  "strategy": "O propoziție care descrie strategia generală de marketing",
  "posts": [
    {
      "platform": "string",
      "post_text": "string",
      "hashtags": ["string"],
      "call_to_action": "string",
      "image_description": "string", 
      "target_persona": "string",
      "post_goal": "string"
    }
  ]
}`;
    }

    /**
     * Mock personas for testing/fallback
     * @private
     */
    _getMockPersonas(businessData) {
        console.log('🔄 Using mock personas (API key not available)');
        return {
            personas: [{
                    name: "Maria Popescu",
                    age_range: "28-35",
                    demographics: "Femeie tânără, educată, venit mediu-mare",
                    interests: ["evenimente speciale", "design interior", "fotografii", "calitate premium"],
                    pain_points: ["lipsa timpului pentru organizare", "dificultatea găsirii furnizorilor de calitate"],
                    buying_behavior: "Cercetează online, citește review-uri, valorifică recomandările",
                    preferred_platforms: ["Instagram", "Facebook"],
                    communication_style: "Profesional dar prietenos, apreciază detaliile"
                },
                {
                    name: "Ana Ciobanu",
                    age_range: "30-45",
                    demographics: "Femeie matură, organizator evenimente, venit stabil",
                    interests: ["planning evenimente", "networking", "tendințe în design", "eficiență"],
                    pain_points: ["respectarea bugetelor", "coordonarea furnizorilor multipli"],
                    buying_behavior: "Ia decizii rapide, valorifică relațiile pe termen lung",
                    preferred_platforms: ["Facebook", "LinkedIn"],
                    communication_style: "Direct, orientat spre rezultate, apreciază promptitudinea"
                }
            ]
        };
    }

    /**
     * Mock campaign content for testing/fallback
     * @private
     */
    _getMockCampaignContent(businessData) {
        console.log('🔄 Using mock campaign content (API key not available)');
        return {
            strategy: "Creăm campaniile care evidențiază calitatea și unicitatea produselor pentru a atrage clienți care valorifică excelența.",
            posts: [{
                    platform: "both",
                    post_text: "🌸 Transformăm visurile tale în realitate cu aranjamente florale unice! Fiecare buchet spune o poveste specială. ✨",
                    hashtags: ["#florarie", "#aranjamenteflorale", "#nunti", "#evenimente", "#chisinau", "#flori", "#buchete", "#decoratiuni"],
                    call_to_action: "Contactează-ne pentru o consultație gratuită!",
                    image_description: "Buchet elegant cu flori proaspete, aranjament profesional în culori pastelate",
                    target_persona: "Maria Popescu",
                    post_goal: "awareness"
                },
                {
                    platform: "facebook",
                    post_text: "💍 Nuntă de vis? Avem soluția perfectă! Decorațiuni florale care vor face ca ziua ta specială să fie de neuitat. Vezi portofoliul nostru! 👰",
                    hashtags: ["#nunta", "#decoratiuni", "#mireasa", "#evenimente", "#chisinau", "#florarie"],
                    call_to_action: "Rezervă o întâlnire pentru planificarea nunții tale!",
                    image_description: "Decorațiuni florale elegante pentru nuntă, aranjamente mari cu flori albe și verzi",
                    target_persona: "Maria Popescu",
                    post_goal: "conversion"
                },
                {
                    platform: "instagram",
                    post_text: "🎯 Organizezi un eveniment special? Noi ne ocupăm de partea florală ca să fie perfect! Experiență + Creativitate = Succes garantat! 📞",
                    hashtags: ["#organizatorevenimente", "#florarie", "#professional", "#chisinau", "#evenimente", "#calitate"],
                    call_to_action: "Trimite un mesaj pentru oferta ta personalizată!",
                    image_description: "Aranjament floral modern pentru evenimente corporate, design contemporary",
                    target_persona: "Ana Ciobanu",
                    post_goal: "conversion"
                }
            ]
        };
    }
}

// Export the class
module.exports = TinkerbellAI;