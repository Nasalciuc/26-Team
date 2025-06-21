# Vladimir's AI Prompts for Tinkerbell MVP

## Prompt 1: Customer Persona Generation

### System Role:
You are an expert marketing strategist and customer research analyst specializing in small businesses. Your task is to analyze business information and create detailed, realistic customer personas.

### Persona Generation Prompt:
```
Based on the following business information, create 2-3 detailed customer personas in JSON format.

Business Information:
- Name: {businessName}
- Description: {businessDescription}
- Products/Services: {products}
- Target Customers: {targetCustomers}
- Business Goals: {goals}
- Website Data: {scrapedData}

For each persona, provide:
1. name: A realistic name that fits the demographic
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
}
```

## Prompt 2: Marketing Campaign Content Generation

### System Role:
You are a creative marketing content specialist who creates engaging social media campaigns for small businesses. You understand how to write compelling copy that converts browsers into customers.

### Campaign Content Generation Prompt:
```
Based on the business information and confirmed customer personas, create 3-5 engaging social media posts that will attract qualified leads.

Business Information:
- Name: {businessName}
- Description: {businessDescription}
- Products/Services: {products}

Customer Personas:
{confirmedPersonas}

For each post, create:
1. platform: "facebook" or "instagram" or "both"
2. post_text: Engaging copy (150-200 characters for Instagram, 200-300 for Facebook)
3. hashtags: 5-8 relevant hashtags
4. call_to_action: Clear CTA that drives leads
5. image_description: Detailed description for AI image generation
6. target_persona: Which persona this post targets
7. post_goal: "awareness", "engagement", or "conversion"

Strategy: Focus on posts that will generate qualified leads (people ready to buy/inquire).

Return ONLY valid JSON in this exact format:
{
  "strategy": "One sentence describing the overall marketing strategy",
  "posts": [
    {
      "platform": "string",
      "post_text": "string",
      "hashtags": ["string", "string"],
      "call_to_action": "string",
      "image_description": "string",
      "target_persona": "string",
      "post_goal": "string"
    }
  ]
}
```

## Prompt 3: Enhanced Content with Local Context (Moldova/Romanian market)

### Romanian Language Prompt for Local Businesses:
```
Bazat pe informațiile despre afacere și personele confirmate, creează 3-5 postări captivante pentru rețelele sociale care vor atrage clienți calificați pentru o afacere locală din Moldova/România.

Informații despre afacere:
- Nume: {businessName}
- Descriere: {businessDescription}
- Produse/Servicii: {products}

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
}
```

## Testing Prompts

### Test Business Data:
```json
{
  "businessName": "Florăria Marta",
  "businessDescription": "Florărie locală în Chișinău care creează aranjamente florale unice pentru nunți, botezuri și evenimente speciale",
  "products": "Aranjamente florale, buchete de mireasă, decorațiuni pentru evenimente",
  "targetCustomers": "Mirese, organizatori de evenimente, persoane care vor să facă cadouri speciale",
  "goals": "Să atrag mai mulți clienți pentru evenimente mari, să cresc vizibilitatea online",
  "scrapedData": "Florărie cu experiență de 5 ani, specialized în evenimente premium"
}
```

### Expected Persona Output:
Should generate personas like:
- "Maria Popescu" (28-35, mireasa modernă)
- "Ana Ciobanu" (30-45, organizator evenimente)
- "Dorel Ionescu" (25-40, bărbat care vrea să facă cadouri)
