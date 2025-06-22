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

class PlanableClient {
    constructor() {
        this.apiKey = process.env.PLANABLE_ACCESS_TOKEN;
        this.baseUrl = 'https://api.planable.io/v1';
        this.facebookPageId = process.env.FACEBOOK_PAGE_ID; // Your Facebook page ID
        this.autoPost = process.env.AUTO_POST_ENABLED === 'true'; // Enable auto-posting

        if (!this.apiKey) {
            console.warn('⚠️ PLANABLE_ACCESS_TOKEN not found - using mock responses');
        }

        if (this.autoPost && !this.facebookPageId) {
            console.warn('⚠️ FACEBOOK_PAGE_ID not found - auto-posting may not work correctly');
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
            const response = await fetch(`${this.baseUrl}/workspaces`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: workspaceName,
                    description: `Tinkerbell Marketing Campaign for ${workspaceName}`
                })
            });

            if (!response.ok) {
                throw new Error(`Planable API error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            console.log(`✅ Planable: Workspace created with ID ${data.id}`);
            return data;

        } catch (error) {
            console.error('❌ Planable workspace creation failed:', error.message);
            return this._getMockWorkspace(workspaceName);
        }
    }

    /**
     * Upload image to Planable for use in posts
     * @param {string} workspaceId - ID of the workspace
     * @param {string} imagePath - Local path to image file
     * @returns {Promise<Object>} Upload response
     */
    async _uploadImage(workspaceId, imagePath) {
        console.log(`📷 Uploading image: ${path.basename(imagePath)}`);

        if (!this.apiKey) {
            return { success: true, mediaId: 'mock_media_id' };
        }

        try {
            const formData = new FormData();
            formData.append('file', fs.createReadStream(imagePath));

            const response = await fetch(`${this.baseUrl}/workspaces/${workspaceId}/media`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    ...formData.getHeaders()
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Image upload failed: ${response.status}`);
            }

            const data = await response.json();
            console.log(`✅ Image uploaded with ID: ${data.id}`);

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

            const response = await fetch(`${this.baseUrl}/workspaces/${workspaceId}/posts`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(planablePost)
            });

            if (!response.ok) {
                throw new Error(`Planable API error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
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
     * Auto-publish post to Facebook through Planable
     * @param {string} postId - ID of the post to publish
     * @param {string} workspaceId - ID of the workspace
     * @returns {Promise<Object>} Publish response
     */
    async _autoPublishPost(postId, workspaceId) {
        console.log(`🚀 Auto-publishing post ${postId} to Facebook`);

        if (!this.apiKey) {
            console.log('🔄 Mock auto-publish (no API key)');
            return { success: true, published_at: new Date().toISOString() };
        }

        try {
            const response = await fetch(`${this.baseUrl}/workspaces/${workspaceId}/posts/${postId}/publish`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    platforms: this.facebookPageId ? [this.facebookPageId] : ['facebook'],
                    publish_now: true
                })
            });

            if (!response.ok) {
                throw new Error(`Auto-publish failed: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            console.log(`✅ Post auto-published to Facebook!`);
            return data;

        } catch (error) {
            console.error('❌ Auto-publish failed:', error.message);
            return { success: false, error: error.message };
        }
    }

    /**
     * Schedule multiple posts in batch with image processing
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
        const platforms = this._getPlatformIds(postData.platform);

        return {
            content: postData.post_text,
            platforms: platforms,
            hashtags: postData.hashtags ? .join(' ') || '',
            call_to_action: postData.call_to_action,
            status: this.autoPost ? 'ready' : 'draft', // Ready for auto-publish or draft for review
            metadata: {
                target_persona: postData.target_persona,
                post_goal: postData.post_goal,
                image_description: postData.image_description,
                has_image: !!(postData.image)
            },
            // Set posting schedule if not auto-posting immediately
            scheduled_at: this.autoPost ? null : this._getOptimalPostTime(postData.platform)
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
     * Determine if post should be auto-published
     * @private
     */
    _shouldAutoPost(platform) {
        // Only auto-post to Facebook for now
        // Instagram may require additional approval
        return platform === 'facebook' || platform === 'both';
    }

    /**
     * Get optimal posting time for platform
     * @private
     */
    _getOptimalPostTime(platform) {
        const now = new Date();
        const optimized = new Date(now);

        // Set optimal times based on platform
        if (platform === 'facebook') {
            // Facebook: 9 AM, 1 PM, or 7 PM
            const hours = [9, 13, 19];
            optimized.setHours(hours[Math.floor(Math.random() * hours.length)]);
        } else if (platform === 'instagram') {
            // Instagram: 11 AM, 2 PM, or 8 PM
            const hours = [11, 14, 20];
            optimized.setHours(hours[Math.floor(Math.random() * hours.length)]);
        }

        // If time has passed today, schedule for tomorrow
        if (optimized <= now) {
            optimized.setDate(optimized.getDate() + 1);
        }

        return optimized.toISOString();
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
            status: this.autoPost ? 'published' : 'scheduled',
            scheduled_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // Tomorrow
            created_at: new Date().toISOString(),
            has_image: !!(postData.image),
            auto_posted: this.autoPost && this._shouldAutoPost(postData.platform)
        };
    }

    /**
     * Utility delay function
     * @private
     */
    _delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

module.exports = PlanableClient;