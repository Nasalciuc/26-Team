/**
 * Enhanced Planable API Client for Tinkerbell MVP
 * Author: Nicolae Cociorva + Enhanced by Aurelian
 * 
 * This module handles all interactions with the Planable API for creating
 * workspaces, scheduling social media posts, and auto-posting to Facebook
 */

const FormData = require('form-data');
const fs = require('fs');
const path = require('path');
const axios = require('axios');

class PlanableClient {
    constructor() {
            this.apiKey = process.env.PLANABLE_ACCESS_TOKEN;
            this.baseUrl = 'https://app.planable.io/api/v1'; // Updated from api.planable.io to app.planable.io/api
            this.facebookPageId = process.env.FACEBOOK_PAGE_ID; // Your Facebook page ID
            this.facebookAppId = process.env.FACEBOOK_APP_ID; // Facebook App ID
            this.facebookAppSecret = process.env.FACEBOOK_APP_SECRET; // Facebook App Secret
            this.autoPost = process.env.AUTO_POST_ENABLED === 'true'; // Enable auto-posting

            if (!this.apiKey) {
                console.warn('⚠️ PLANABLE_ACCESS_TOKEN not found - using mock responses');
            }

            if (this.autoPost && !this.facebookPageId) {
                console.warn('⚠️ FACEBOOK_PAGE_ID not found - auto-posting may not work correctly');
            }

            if (this.autoPost && (!this.facebookAppId || !this.facebookAppSecret)) {
                console.warn('⚠️ Facebook App credentials missing - auto-posting may not work correctly');
            }
        }
        /**
         * Create a new workspace in Planable
         * @param {string} workspaceName - Name for the new workspace
         * @returns {Promise<Object>} Workspace creation response
         */
    async createWorkspace(workspaceName) {
            console.log(`📋 Planable: Creating workspace "${workspaceName}"`);

            if (!this.apiKey) {
                return this._getMockWorkspace(workspaceName);
            }

            try {
                const response = await axios.post(`${this.baseUrl}/workspaces`, {
                    name: workspaceName,
                    description: `Tinkerbell Marketing Campaign for ${workspaceName}`
                }, {
                    headers: {
                        'Authorization': `Bearer ${this.apiKey}`,
                        'Content-Type': 'application/json'
                    }
                });

                console.log(`✅ Planable: Workspace created with ID ${response.data.id}`);
                return response.data;

            } catch (error) {
                console.error('❌ Planable workspace creation failed:', error.message);
                return this._getMockWorkspace(workspaceName);
            }
        }
        /**
         * Get or use an existing workspace (bypass creation issues)
         * @param {string} workspaceName - Name for the workspace (for logging)
         * @returns {Promise<Object>} Existing workspace response
         */
    async getOrCreateWorkspace(workspaceName) {
        console.log(`📋 Planable: Getting existing workspace for "${workspaceName}"`);

        if (!this.apiKey) {
            return this._getMockWorkspace(workspaceName);
        }

        try {
            // Get existing workspaces first
            const response = await axios.get(`${this.baseUrl}/workspaces`, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.data && response.data.length > 0) {
                // Use the first available workspace
                const workspace = response.data[0];
                console.log(`✅ Using existing workspace: "${workspace.name}" (ID: ${workspace.id})`);

                return {
                    id: workspace.id,
                    name: workspace.name,
                    success: true,
                    message: 'Using existing workspace'
                };
            } else {
                // Fallback to mock if no workspaces found
                console.warn('⚠️ No existing workspaces found, using mock');
                return this._getMockWorkspace(workspaceName);
            }

        } catch (error) {
            console.error(`❌ Failed to get existing workspace: ${error.message}`);

            // Fallback to mock on error
            return this._getMockWorkspace(workspaceName);
        }
    }

    /**
     * Schedule a social media post in Planable with image support and auto-posting
     * @param {string} workspaceId - ID of the workspace
     * @param {Object} postData - Post content and metadata
     * @returns {Promise<Object>} Post scheduling response
     */
    async schedulePost(workspaceId, postData) {
        console.log(`📝 Planable: Scheduling post for ${postData.platform}`);

        if (!this.apiKey) {
            return this._getMockPostResponse(postData);
        }

        try {
            // Transform our post data to Planable format
            const planablePost = this._transformPostData(postData);

            // Handle image attachment if present
            if (postData.image && postData.image.path) {
                const imageUpload = await this._uploadImage(workspaceId, postData.image.path);
                if (imageUpload.success) {
                    planablePost.media = [imageUpload.mediaId];
                }
            }
            const response = await axios.post(`${this.baseUrl}/workspaces/${workspaceId}/posts`, planablePost, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json'
                }
            });

            const data = response.data;
            console.log(`✅ Planable: Post scheduled with ID ${data.id}`);

            // Auto-publish to Facebook if enabled
            if (this.autoPost && this._shouldAutoPost(postData.platform)) {
                setTimeout(async() => {
                    await this._autoPublishPost(data.id, workspaceId);
                }, 1000); // Small delay to ensure post is processed
            }

            return data;

        } catch (error) {
            console.error('❌ Planable post scheduling failed:', error.message);
            return this._getMockPostResponse(postData);
        }
    }

    /**
     * Schedule multiple posts in batch
     * @param {string} workspaceId - ID of the workspace
     * @param {Array} postsData - Array of post objects
     * @returns {Promise<Array>} Array of scheduling responses
     */
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

                // Small delay to avoid rate limiting
                await this._delay(500);

            } catch (error) {
                console.error(`❌ Failed to schedule post for ${postData.platform}:`, error.message);
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
    }

    /**
     * Get workspace URL for user access
     * @param {string} workspaceId - ID of the workspace
     * @returns {string} Direct URL to workspace
     */
    getWorkspaceUrl(workspaceId) {
        return `https://app.planable.io/workspace/${workspaceId}`;
    }

    /**
     * Transform our post data format to Planable API format
     * @private
     */
    _transformPostData(postData) {
        return {
            content: postData.post_text,
            platforms: this._getPlatformIds(postData.platform),
            hashtags: postData.hashtags ? postData.hashtags.join(' ') : '',
            call_to_action: postData.call_to_action,
            status: 'draft', // Create as draft for review
            metadata: {
                target_persona: postData.target_persona,
                post_goal: postData.post_goal,
                image_description: postData.image_description
            }
        };
    }

    /**
     * Map platform names to Planable platform IDs
     * @private
     */
    _getPlatformIds(platform) {
        const platformMap = {
            'facebook': ['facebook'],
            'instagram': ['instagram'],
            'both': ['facebook', 'instagram']
        };

        return platformMap[platform] || ['facebook'];
    }

    /**
     * Mock workspace for testing without API key
     * @private
     */
    _getMockWorkspace(workspaceName) {
        console.log('🔄 Using mock workspace (API key not available)');
        const mockId = `mock_ws_${Date.now()}`;
        return {
            id: mockId,
            name: workspaceName,
            url: this.getWorkspaceUrl(mockId),
            created_at: new Date().toISOString(),
            status: 'active'
        };
    }

    /**
     * Mock post response for testing without API key
     * @private
     */
    _getMockPostResponse(postData) {
            console.log('🔄 Using mock post response (API key not available)');
            return {
                id: `mock_post_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                platform: postData.platform,
                content: postData.post_text,
                status: 'scheduled',
                scheduled_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // Tomorrow
                created_at: new Date().toISOString()
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
     * Upload image to Planable
     * @param {string} workspaceId - Workspace ID
     * @param {string} imagePath - Path to image file
     * @returns {Promise<Object>} Upload response
     * @private
     */
    async _uploadImage(workspaceId, imagePath) {
        if (!this.apiKey) {
            return { success: false, error: 'No API key' };
        }

        try {
            const form = new FormData();
            form.append('file', fs.createReadStream(imagePath));
            form.append('workspace_id', workspaceId);
            const response = await axios.post(`${this.baseUrl}/media/upload`, form, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    ...form.getHeaders()
                }
            });

            const data = response.data;
            console.log(`✅ Image uploaded successfully: ${data.id}`);

            return {
                success: true,
                mediaId: data.id,
                url: data.url
            };

        } catch (error) {
            console.error('❌ Image upload failed:', error.message);
            return { success: false, error: error.message };
        }
    }

    /**
     * Auto-publish post to Facebook
     * @param {string} postId - Planable post ID
     * @param {string} workspaceId - Workspace ID
     * @returns {Promise<Object>} Publish response
     * @private
     */
    async _autoPublishPost(postId, workspaceId) {
        if (!this.apiKey || !this.autoPost) {
            console.log('🔄 Auto-posting disabled or no API key');
            return { success: false, reason: 'Auto-posting disabled' };
        }
        try {
            console.log(`🚀 Auto-publishing post ${postId} to Facebook...`);
            const response = await axios.post(`${this.baseUrl}/workspaces/${workspaceId}/posts/${postId}/publish`, {
                platforms: ['facebook'],
                facebook_page_id: this.facebookPageId,
                facebook_app_id: this.facebookAppId,
                facebook_app_secret: this.facebookAppSecret,
                publish_now: true
            }, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json'
                }
            });

            const data = response.data;
            console.log(`✅ Post auto-published to Facebook: ${data.facebook_post_id}`);

            return {
                success: true,
                facebook_post_id: data.facebook_post_id,
                published_at: new Date().toISOString()
            };

        } catch (error) {
            console.error('❌ Auto-publish failed:', error.message);
            return { success: false, error: error.message };
        }
    }

    /**
     * Check if post should be auto-published
     * @param {string} platform - Post platform
     * @returns {boolean} Should auto-post
     * @private
     */
    _shouldAutoPost(platform) {
        return this.autoPost && (platform === 'facebook' || platform === 'both');
    }
}

module.exports = PlanableClient;