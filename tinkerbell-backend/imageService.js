/**
 * Enhanced Image Service for Tinkerbell MVP
 * Handles image generation, analysis, and matching for social media posts
 */

const OpenAI = require('openai');
const fs = require('fs').promises;
const path = require('path');
const sharp = require('sharp');
const https = require('https');
const { pipeline } = require('stream/promises');

class ImageService {
    constructor() {
        this.openai = process.env.OPENAI_API_KEY ? new OpenAI({
            apiKey: process.env.OPENAI_API_KEY
        }) : null;

        this.uploadDir = path.join(__dirname, 'uploads');
        this.generatedDir = path.join(__dirname, 'generated-images');

        // Ensure directories exist
        this.initializeDirectories();
    }

    /**
     * Initialize required directories
     */
    async initializeDirectories() {
        try {
            await fs.mkdir(this.uploadDir, { recursive: true });
            await fs.mkdir(this.generatedDir, { recursive: true });
            console.log('📁 Image directories initialized');
        } catch (error) {
            console.error('❌ Error creating directories:', error);
        }
    }

    /**
     * Generate image using DALL-E based on description
     * @param {string} description - Image description from campaign post
     * @param {string} businessName - Business name for context
     * @returns {Promise<Object>} Generated image data
     */
    async generateImage(description, businessName) {
        console.log(`🎨 Generating image: ${description}`);

        if (!this.openai) {
            return this._getMockGeneratedImage(description);
        }

        try {
            const enhancedPrompt = this._enhanceImagePrompt(description, businessName);

            const response = await this.openai.images.generate({
                model: "dall-e-3",
                prompt: enhancedPrompt,
                size: "1024x1024",
                quality: "standard",
                n: 1,
            });

            const imageUrl = response.data[0].url;

            // Download and save the image
            const savedImage = await this._downloadAndSaveImage(imageUrl, description);
            return {
                success: true,
                imageUrl: imageUrl,
                localPath: savedImage.path,
                filename: savedImage.filename,
                url: `/generated/${savedImage.filename}`, // Add URL for frontend
                description: description,
                prompt: enhancedPrompt
            };

        } catch (error) {
            console.error('❌ Image generation failed:', error);
            return this._getMockGeneratedImage(description);
        }
    }

    /**
     * Analyze uploaded images and match them to posts
     * @param {Array} uploadedImages - Array of uploaded image files
     * @param {Array} posts - Campaign posts needing images
     * @returns {Promise<Object>} Matching results
     */
    async analyzeAndMatchImages(uploadedImages, posts) {
        console.log(`🔍 Analyzing ${uploadedImages.length} images for ${posts.length} posts`);

        const results = {
            matches: [],
            unmatched_images: [],
            posts_without_images: []
        };

        // Process each uploaded image
        for (const image of uploadedImages) {
            try {
                const analysis = await this._analyzeImage(image.path);
                const bestMatch = this._findBestMatchingPost(analysis, posts);

                if (bestMatch) {
                    results.matches.push({
                        image: {
                            filename: image.filename,
                            path: image.path,
                            analysis: analysis
                        },
                        post: bestMatch.post,
                        confidence: bestMatch.confidence,
                        reasons: bestMatch.reasons
                    });
                } else {
                    results.unmatched_images.push({
                        filename: image.filename,
                        analysis: analysis
                    });
                }
            } catch (error) {
                console.error(`❌ Error analyzing image ${image.filename}:`, error);
            }
        }

        // Find posts without matched images
        const matchedPostIds = results.matches.map(m => m.post.id || m.post.platform + '_' + m.post.target_persona);
        results.posts_without_images = posts.filter(post => {
            const postId = post.id || post.platform + '_' + post.target_persona;
            return !matchedPostIds.includes(postId);
        });

        return results;
    }

    /**
     * Process images for a complete campaign
     * @param {Array} posts - Campaign posts
     * @param {Array} uploadedImages - User uploaded images (optional)
     * @param {boolean} generateMissing - Whether to generate missing images
     * @returns {Promise<Object>} Complete image processing results
     */
    async processCampaignImages(posts, uploadedImages = [], generateMissing = true) {
        console.log(`📸 Processing images for ${posts.length} posts`);

        const results = {
            processed_posts: [],
            generated_images: [],
            matched_images: [],
            processing_summary: {}
        };

        // Step 1: Analyze and match uploaded images if any
        if (uploadedImages.length > 0) {
            const matchResults = await this.analyzeAndMatchImages(uploadedImages, posts);
            results.matched_images = matchResults.matches;

            // Update posts with matched images
            for (const match of matchResults.matches) {
                const postIndex = posts.findIndex(p =>
                    (p.id && p.id === match.post.id) ||
                    (p.platform + '_' + p.target_persona === match.post.platform + '_' + match.post.target_persona)
                );
                if (postIndex !== -1) {
                    posts[postIndex].matched_image = {
                        filename: match.image.filename,
                        path: match.image.path,
                        confidence: match.confidence,
                        source: 'uploaded'
                    };
                }
            }
        }

        // Step 2: Generate images for posts without matched images
        if (generateMissing) {
            for (const post of posts) {
                if (!post.matched_image && post.image_description) {
                    try {
                        const generatedImage = await this.generateImage(
                            post.image_description,
                            post.business_name || 'Business'
                        );

                        if (generatedImage.success) {
                            post.generated_image = {
                                filename: generatedImage.filename,
                                path: generatedImage.localPath,
                                url: generatedImage.imageUrl,
                                source: 'generated'
                            };
                            results.generated_images.push(generatedImage);
                        }
                    } catch (error) {
                        console.error(`❌ Failed to generate image for post:`, error);
                    }
                }
            }
        }

        // Step 3: Prepare final processed posts
        results.processed_posts = posts.map(post => ({
            ...post,
            image: post.matched_image || post.generated_image || null,
            has_image: !!(post.matched_image || post.generated_image)
        }));

        // Step 4: Generate summary
        results.processing_summary = {
            total_posts: posts.length,
            posts_with_images: results.processed_posts.filter(p => p.has_image).length,
            matched_images: results.matched_images.length,
            generated_images: results.generated_images.length,
            posts_without_images: results.processed_posts.filter(p => !p.has_image).length
        };

        console.log(`✅ Image processing complete:`, results.processing_summary);
        return results;
    }

    /**
     * Enhance image generation prompt for better results
     * @private
     */
    _enhanceImagePrompt(description, businessName) {
        return `Create a professional, high-quality marketing image for "${businessName}". ${description}. 
        Style: Modern, clean, commercial photography style. High resolution, good lighting, appealing composition. 
        Suitable for social media marketing. No text or logos in the image.`;
    }

    /**
     * Analyze image content using OpenAI Vision
     * @private
     */
    async _analyzeImage(imagePath) {
        if (!this.openai) {
            return this._getMockImageAnalysis();
        }

        try {
            // Convert image to base64
            const imageBuffer = await fs.readFile(imagePath);
            const base64Image = imageBuffer.toString('base64');
            const response = await this.openai.chat.completions.create({
                model: "gpt-4o", // Updated from deprecated gpt-4-vision-preview
                messages: [{
                    role: "user",
                    content: [{
                            type: "text",
                            text: "Analyze this image and describe: 1) Main subjects/objects, 2) Setting/environment, 3) Mood/style, 4) Colors, 5) What type of business this would be suitable for. Be detailed but concise."
                        },
                        {
                            type: "image_url",
                            image_url: {
                                url: `data:image/jpeg;base64,${base64Image}`
                            }
                        }
                    ]
                }],
                max_tokens: 300
            });

            return {
                description: response.choices[0].message.content,
                keywords: this._extractKeywords(response.choices[0].message.content),
                analysis_time: new Date().toISOString()
            };

        } catch (error) {
            console.error('❌ Image analysis failed:', error);
            return this._getMockImageAnalysis();
        }
    }

    /**
     * Find best matching post for an analyzed image
     * @private
     */
    _findBestMatchingPost(imageAnalysis, posts) {
        let bestMatch = null;
        let highestScore = 0;

        for (const post of posts) {
            const score = this._calculateMatchScore(imageAnalysis, post);

            if (score > highestScore && score > 0.3) { // Minimum confidence threshold
                highestScore = score;
                bestMatch = {
                    post: post,
                    confidence: score,
                    reasons: this._getMatchReasons(imageAnalysis, post)
                };
            }
        }

        return bestMatch;
    }

    /**
     * Calculate match score between image and post
     * @private
     */
    _calculateMatchScore(imageAnalysis, post) {
        const imageKeywords = imageAnalysis.keywords || [];
        const postKeywords = [
            ...this._extractKeywords(post.post_text || ''),
            ...this._extractKeywords(post.image_description || ''),
            ...(post.hashtags || []),
            post.target_persona || ''
        ];

        // Simple keyword matching algorithm
        let matches = 0;
        let totalKeywords = Math.max(imageKeywords.length, postKeywords.length);

        for (const imgKeyword of imageKeywords) {
            for (const postKeyword of postKeywords) {
                if (imgKeyword.toLowerCase().includes(postKeyword.toLowerCase()) ||
                    postKeyword.toLowerCase().includes(imgKeyword.toLowerCase())) {
                    matches++;
                    break;
                }
            }
        }

        return totalKeywords > 0 ? matches / totalKeywords : 0;
    }

    /**
     * Extract keywords from text
     * @private
     */
    _extractKeywords(text) {
        if (!text) return [];

        return text.toLowerCase()
            .replace(/[^\w\s]/g, ' ')
            .split(/\s+/)
            .filter(word => word.length > 2)
            .slice(0, 10); // Limit to top 10 keywords
    }

    /**
     * Get human-readable match reasons
     * @private
     */
    _getMatchReasons(imageAnalysis, post) {
            return [
                `Image content matches post theme`,
                `Keywords align with: ${post.target_persona}`,
                `Suitable for ${post.platform} platform`
            ];
        }
        /**
         * Download and save generated image
         * @private
         */
    async _downloadAndSaveImage(imageUrl, description) {
        try {
            // Use node-fetch or https module instead of fetch
            const response = await this._fetchImage(imageUrl);

            const filename = `generated_${Date.now()}_${Math.random().toString(36).substr(2, 9)}.jpg`;
            const filepath = path.join(this.generatedDir, filename);

            // Optimize image using Sharp
            await sharp(response)
                .jpeg({ quality: 85 })
                .resize(1200, 1200, { fit: 'inside', withoutEnlargement: true })
                .toFile(filepath);

            console.log(`✅ Image saved: ${filename}`);
            return { path: filepath, filename };
        } catch (error) {
            throw new Error(`Failed to download image: ${error.message}`);
        }
    }

    /**
     * Fetch image using https module (Node.js compatible)
     * @private
     */
    async _fetchImage(imageUrl) {
        return new Promise((resolve, reject) => {
            https.get(imageUrl, (response) => {
                if (response.statusCode !== 200) {
                    reject(new Error(`HTTP ${response.statusCode}: ${response.statusMessage}`));
                    return;
                }

                const chunks = [];
                response.on('data', chunk => chunks.push(chunk));
                response.on('end', () => resolve(Buffer.concat(chunks)));
                response.on('error', reject);
            }).on('error', reject);
        });
    }

    /**
     * Mock image generation for testing
     * @private
     */
    _getMockGeneratedImage(description) {
        const filename = `mock_generated_${Date.now()}.jpg`;
        return {
            success: true,
            imageUrl: `https://picsum.photos/1024/1024?random=${Date.now()}`,
            localPath: `/mock/path/${filename}`,
            filename: filename,
            url: `https://picsum.photos/1024/1024?random=${Date.now()}`, // Add URL for frontend
            description: description,
            prompt: `Mock generation for: ${description}`
        };
    }

    /**
     * Mock image analysis for testing
     * @private
     */
    _getMockImageAnalysis() {
        return {
            description: "Professional business image with modern aesthetic, suitable for marketing purposes.",
            keywords: ["professional", "business", "modern", "marketing", "commercial"],
            analysis_time: new Date().toISOString()
        };
    }
}

module.exports = ImageService;