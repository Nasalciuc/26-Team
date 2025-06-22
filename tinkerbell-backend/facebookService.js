/**
 * Direct Facebook Graph API Service for Tinkerbell
 * Posts directly to Facebook without Planable
 */

const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

class FacebookService {
    constructor() {
        // Updated Facebook credentials - working as of June 22, 2025
        this.pageAccessToken = process.env.FACEBOOK_PAGE_ACCESS_TOKEN ||
            process.env.META_ACCESS_TOKEN ||
            'EAAY2VBFOoHwBOwrpZCXSRjDZAXSNZC8rZBnRM49dmreEE9UsCfIMHBqx2ZAoRPwgZAoncIRzDugchj1NaQJ0cCkcx2iqHXTBHScZBLpRZCkaP01adZBIpRO0x2iq410dRDrrZAFIQspkH57pYL3Qj9XVbIw7r7QvDR16QmM9WMfSxGE03mahti9dYHLOyL56SV6kG7A0gooD4vS0Lu9vudQeK8dZCqLOmmtUiEdlle9DmIZD';
        this.pageId = process.env.FACEBOOK_PAGE_ID || '532394313287326';
        this.baseUrl = 'https://graph.facebook.com';

        if (!this.pageAccessToken) {
            console.warn('⚠️ FACEBOOK_PAGE_ACCESS_TOKEN not found - using mock responses');
        }

        if (!this.pageId) {
            console.warn('⚠️ FACEBOOK_PAGE_ID not found - using mock responses');
        }
    }

    /**
     * Post directly to Facebook Page
     * @param {Object} postData - Post content and metadata
     * @returns {Promise<Object>} Facebook posting response
     */
    async postToFacebook(postData) {
        console.log(`📘 Facebook: Posting to page ${this.pageId}`);

        if (!this.pageAccessToken || !this.pageId) {
            return this._getMockPostResponse(postData);
        }

        try {
            let result;

            if (postData.image && postData.image.path) {
                // Post with image
                result = await this._postWithImage(postData);
            } else {
                // Text-only post
                result = await this._postTextOnly(postData);
            }

            console.log(`✅ Facebook: Post created with ID ${result.id}`);
            return {
                success: true,
                facebook_post_id: result.id,
                platform: 'facebook',
                post_data: postData,
                published_at: new Date().toISOString()
            };

        } catch (error) {
            console.error('❌ Facebook posting failed:', error.message);
            if (error.response) {
                console.error('Facebook API Error:', error.response.data);
            }
            return {
                success: false,
                platform: 'facebook',
                post_data: postData,
                error: error.message,
                error_details: error.response && error.response.data
            };
        }
    }

    /**
     * Post text-only content to Facebook
     * @private
     */
    async _postTextOnly(postData) {
        const message = this._buildPostMessage(postData);

        const response = await axios.post(`${this.baseUrl}/${this.pageId}/feed`, {
            message: message,
            access_token: this.pageAccessToken
        });

        return response.data;
    }

    /**
     * Post content with image to Facebook
     * @private
     */
    async _postWithImage(postData) {
        const message = this._buildPostMessage(postData);

        if (!fs.existsSync(postData.image.path)) {
            throw new Error(`Image file not found: ${postData.image.path}`);
        }

        const formData = new FormData();
        formData.append('source', fs.createReadStream(postData.image.path));
        formData.append('caption', message);
        formData.append('access_token', this.pageAccessToken);

        const response = await axios.post(`${this.baseUrl}/${this.pageId}/photos`, formData, {
            headers: {
                ...formData.getHeaders(),
            }
        });

        return response.data;
    }

    /**
     * Build complete Facebook post message
     * @private
     */
    _buildPostMessage(postData) {
        let message = postData.post_text || '';

        // Add hashtags if present
        if (postData.hashtags && postData.hashtags.length > 0) {
            const hashtagString = postData.hashtags.map(tag =>
                tag.startsWith('#') ? tag : `#${tag}`
            ).join(' ');
            message += '\n\n' + hashtagString;
        }

        // Add call to action if present
        if (postData.call_to_action) {
            message += '\n\n' + postData.call_to_action;
        }

        return message.trim();
    }

    /**
     * Post multiple posts to Facebook in batch
     * @param {Array} postsData - Array of post objects
     * @returns {Promise<Array>} Array of posting responses
     */
    async postMultiplePosts(postsData) {
        console.log(`📘 Facebook: Posting ${postsData.length} posts in batch`);

        const results = [];

        for (const postData of postsData) {
            try {
                // Skip non-Facebook posts
                if (postData.platform !== 'facebook' && postData.platform !== 'both') {
                    console.log(`⏭️ Skipping ${postData.platform} post`);
                    continue;
                }

                const result = await this.postToFacebook(postData);
                results.push(result);

                // Add delay to avoid rate limiting
                await this._delay(2000);

            } catch (error) {
                console.error(`❌ Failed to post:`, error.message);
                results.push({
                    success: false,
                    platform: 'facebook',
                    post_data: postData,
                    error: error.message
                });
            }
        }

        const successfulPosts = results.filter(r => r.success).length;
        console.log(`✅ Facebook: ${successfulPosts}/${results.length} posts completed`);

        return results;
    }

    /**
     * Mock post response for testing without API credentials
     * @private
     */
    _getMockPostResponse(postData) {
        const mockId = `mock_fb_${Date.now()}_${Math.random().toString(36).substring(7)}`;

        console.log('🔄 Facebook: Using mock response (no credentials)');

        return {
            success: true,
            facebook_post_id: mockId,
            platform: 'facebook',
            post_data: postData,
            published_at: new Date().toISOString(),
            mock: true
        };
    }

    /**
     * Utility delay function
     * @private
     */
    _delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Test Facebook API connection
     * @returns {Promise<Object>} Connection test result
     */
    async testConnection() {
        console.log('🔍 Facebook: Testing API connection...');

        if (!this.pageAccessToken || !this.pageId) {
            return {
                success: false,
                error: 'Missing Facebook credentials',
                configured: false
            };
        }

        try {
            const response = await axios.get(`${this.baseUrl}/${this.pageId}`, {
                params: {
                    fields: 'id,name,access_token',
                    access_token: this.pageAccessToken
                }
            });

            console.log(`✅ Facebook: Connected to page "${response.data.name}"`);

            return {
                success: true,
                page_name: response.data.name,
                page_id: response.data.id,
                configured: true
            };

        } catch (error) {
            console.error('❌ Facebook: Connection test failed:', error.message);
            return {
                success: false,
                error: error.message,
                configured: true,
                error_details: error.response ? error.response.data : null
            };
        }
    }
}

module.exports = FacebookService;